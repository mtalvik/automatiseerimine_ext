# Ansible Rollid - Labor

**Eeldused:** Ansible edasijõudnud labor läbitud, YAML süntaks, Linux CLI  
**Platvorm:** Ubuntu 24.04, Proxmox keskkond  
**Kestus:** 2 × 45 minutit

---

## Õpiväljundid

Pärast seda labori oskad:

- Tuvastada korduvat koodi ja DRY printsiibi rikkumist playbook'ides
- Refaktoreerida olemasoleva projekti Ansible rolliks
- Kasutada Galaxy standardi kasutatruktuuri (defaults/, vars/, tasks/, templates/, handlers/)
- Eristada `defaults/` ja `vars/` kaustade kasutust
- Skaleerida infrastruktuuri - lisada uusi keskkondi ilma koodi kopeerimata
- Dokumenteerida ja jagada rolle

---

## Labori Ülevaade

Selles laboris võtame Ansible edasijõudnud laboris loodud nginx projekti ja refaktoreerin selle professionaalseks rolliks. Näeme konkreetselt, kuidas rollid lahendavad korduse probleemi ja võimaldavad infrastruktuuri skaleerida. Lõpuks lisame kolmanda keskkonna (staging), et näidata kuidas rollid muudavad selle triviaalseks.

---

## 1. Olemasoleva Projekti Analüüs

### 1.1. Kontrolli keskkonda

Kasutame edasijõudnud labori projekti ja servereid:

```bash
# Logi Ubuntu 1 (controller)
ssh ansible@192.168.82.10

# Kontrolli et projekt eksisteerib
cd ~/ansible-advanced
ls -la
```

Peaks näitama:
```
group_vars/
host_vars/
playbooks/
templates/
inventory.yml
```

### 1.2. Vaata praegust struktuuri

```bash
# Kui palju koodi on playbook'is?
wc -l playbooks/full_deploy.yml

# Vaata playbook'i sisu
cat playbooks/full_deploy.yml
```

**Mõtle:** Kui tahaksime lisada staging keskkonna, mis peaks muutuma?

### 1.3. Probleem: Lisame kolmanda keskkonna (ilma rollita)

Kujuta ette, et peame lisama **staging** keskkonna.

**Ilma rollita peaks:**
1. Looma `host_vars/staging-web.yml`
2. Kopeerima kõik muutujad
3. Muutma `inventory.yml`
4. ... ja playbook töötab

**Aga kui tahame muuta nginx konfiguratsiooni?**
- Muudame `templates/nginx.conf.j2` ✓
- See mõjutab KÕIKI keskkondi automaatselt ✓

**Aga kui tahame muuta task'ide järjekorda?**
- Peame muutma `playbooks/full_deploy.yml` ✓
- Ainult ÜKS playbook ✓

**Hmm, tegelikult pole nii hull?**

### 1.4. REAALNE probleem: Jagamine

**Stsenaarium:** Kolleeg teisel projektil tahab ka nginx seadistust.

**Ilma rollita:**
```bash
# Kolleeg peab kopeerima:
cp playbooks/full_deploy.yml ../kolleegi-projekt/
cp templates/nginx.conf.j2 ../kolleegi-projekt/templates/
cp templates/index.html.j2 ../kolleegi-projekt/templates/
cp group_vars/webservers/nginx.yml ../kolleegi-projekt/group_vars/webservers/

# 4 faili, 4 kohta kus hoida sünkroonis
# Kui sa parandad vea, kolleeg ei saa automaatselt
```

**Rolliga:**
```yaml
# Kolleegi playbook:
roles:
  - nginx  # Kõik on ühes kohas!
```

**See on rollide TÕELINE väärtus** - korduvkasutatavus ja jagamine.

### Kontrollnimekiri
- [ ] Edasijõudnud labori projekt on olemas
- [ ] Mõistad, miks rollid on jagamiseks paremad
- [ ] Näed, et playbook ise pole probleem - probleem on komponentide taaskasutamine

---

## 2. Rolli Loomine

### 2.1. Galaxy init

Ansible Galaxy standard struktuur:

```bash
cd ~/ansible-advanced
mkdir -p roles
cd roles
ansible-galaxy init nginx
cd ..
```

**Tulemus:**
```
roles/nginx/
├── defaults/main.yml     # Kasutaja võib muuta
├── vars/main.yml         # Rolli sisemised väärtused
├── tasks/main.yml        # Põhilised task'id
├── templates/            # Template'id
├── handlers/main.yml     # Handler'id
├── files/                # Staatilised failid
├── meta/main.yml         # Metadata
└── README.md             # Dokumentatsioon
```

### 2.2. Liiguta tasks

Praegu on tasks playbook'is. Liigutame rolli.

Ava `roles/nginx/tasks/main.yml`:

```bash
nano roles/nginx/tasks/main.yml
```

Sisesta (võta playbook'ist):
```yaml
---
# Package management
- name: Update apt cache
  apt:
    update_cache: yes
    cache_valid_time: 3600
  when: ansible_os_family == "Debian"

- name: Install required packages
  apt:
    name:
      - nginx
      - python3-passlib
    state: present
  notify: start nginx

# Nginx configuration
- name: Deploy nginx configuration from template
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
    backup: yes
    validate: 'nginx -t -c %s'
  notify: reload nginx

# Security (production only)
- name: Create htpasswd file for production
  community.general.htpasswd:
    path: /etc/nginx/.htpasswd
    name: "{{ vault_admin_user | default('admin') }}"
    password: "{{ vault_admin_password }}"
    owner: root
    group: www-data
    mode: 0640
  when: not debug_mode
  notify: reload nginx

# Website deployment
- name: Deploy website from template
  template:
    src: index.html.j2
    dest: "{{ nginx_root }}/index.html"
    owner: "{{ nginx_user }}"
    group: "{{ nginx_user }}"
    mode: '0644'

# Service management
- name: Ensure nginx is started and enabled
  service:
    name: nginx
    state: started
    enabled: yes
```

**Märka:** Template'id on nüüd `src: nginx.conf.j2` (mitte `../templates/`)

### 2.3. Liiguta handlers

```bash
nano roles/nginx/handlers/main.yml
```

Sisesta:
```yaml
---
- name: start nginx
  service:
    name: nginx
    state: started

- name: reload nginx
  service:
    name: nginx
    state: reloaded
```

### 2.4. Liiguta template'id

```bash
# Kopeeri (ära kustuta originaale veel)
cp templates/nginx.conf.j2 roles/nginx/templates/
cp templates/index.html.j2 roles/nginx/templates/
```

### 2.5. Defineeri muutujad

#### defaults/main.yml - Kasutaja saab muuta

```bash
nano roles/nginx/defaults/main.yml
```

Sisesta:
```yaml
---
# Nginx seaded (kasutaja võib override'ida)
nginx_workers: "{{ ansible_processor_vcpus | default(2) }}"
nginx_port: 80
nginx_root: "/var/www/html"
nginx_worker_connections: 1024

# Rakenduse seaded
app_name: "web-app"
admin_email: "admin@example.com"

# Keskkonna seaded (playbook peaks määrama)
environment: "unknown"
server_name: "localhost"
debug_mode: false
max_connections: 100
site_color: "#CCCCCC"
```

**Miks defaults/?** Need on väärtused, mida **iga keskkond** (dev, prod, staging) määrab ise.

#### vars/main.yml - Rolli sisemised

```bash
nano roles/nginx/vars/main.yml
```

Sisesta:
```yaml
---
# Süsteemi-spetsiifilised (kasutaja EI TOHIKS muuta)
nginx_user: "www-data"
nginx_service: "nginx"
nginx_config_path: "/etc/nginx"
nginx_package: "nginx"
```

**Miks vars/?** Need on OS-spetsiifilised väärtused. Kui kasutaja muudab, roll läheb katki.

### Kontrollnimekiri
- [ ] Roll on loodud Galaxy struktuuri järgi
- [ ] Tasks on rolli liigutatud
- [ ] Handlers on rolli liigutatud
- [ ] Template'id on kopeeritud rolli
- [ ] defaults/ ja vars/ on defineeritud

---

## 3. Uued Playbook'id (Lühikesed!)

Nüüd loome **lühikesed** playbook'id, mis kasutavad rolli.

### 3.1. Development playbook

```bash
nano playbooks/dev-role.yml
```

Sisesta:
```yaml
---
- name: Deploy Development Environment
  hosts: dev-web
  become: yes
  gather_facts: yes
  
  roles:
    - role: nginx
      vars:
        environment: "development"
        server_name: "dev.example.local"
        debug_mode: true
        max_connections: 100
        site_color: "#FFA500"  # Orange
```

**VAATA:** Playbook on ainult **15 rida**! Võrdle `full_deploy.yml` ~70 reaga.

### 3.2. Production playbook

```bash
nano playbooks/prod-role.yml
```

Sisesta:
```yaml
---
- name: Deploy Production Environment
  hosts: prod-web
  become: yes
  gather_facts: yes
  
  roles:
    - role: nginx
      vars:
        environment: "production"
        server_name: "prod.example.com"
        debug_mode: false
        max_connections: 1000
        site_color: "#00AA00"  # Green
```

### 3.3. VÕRDLUS

**Enne (ilma rollideta):**
```
playbooks/full_deploy.yml        ~70 rida
tasks + handlers + vars - kõik sees
```

**Pärast (rollidega):**
```
playbooks/dev-role.yml           ~15 rida (ainult muutujad!)
playbooks/prod-role.yml          ~15 rida (ainult muutujad!)
roles/nginx/                     ~70 rida (aga KORDUVKASUTATAV!)
```

**Pluss:** Kui kolleeg tahab sinu nginx seadistust, saad jagada ainult `roles/nginx/` kausta!

---

## 4. Testimine

### 4.1. Käivita uued playbook'id

```bash
# Development
ansible-playbook -i inventory.yml playbooks/dev-role.yml --vault-password-file .vault_pass

# Production
ansible-playbook -i inventory.yml playbooks/prod-role.yml --vault-password-file .vault_pass
```

### 4.2. Kontrolli tulemust

```bash
# Dev
curl http://192.168.82.10

# Prod
curl -u admin:AdminPass456! http://192.168.82.11
```

**WinKlient brauseris:**
- Dev: `http://192.168.82.10` - oranž
- Prod: `http://192.168.82.11` - roheline (küsib parooli)

### 4.3. Idempotentsus

```bash
# Käivita uuesti
ansible-playbook -i inventory.yml playbooks/dev-role.yml --vault-password-file .vault_pass

# Peaks näitama: changed=0
```

### Kontrollnimekiri
- [ ] Uued playbook'id on loodud
- [ ] Mõlemad keskkonnad töötavad
- [ ] Playbook'id on lühikesed (ainult vars)
- [ ] Idempotentsus töötab

---

## 5. Skaleeritavus: Lisa Staging

Nüüd näitame rollide PÄRIS võimsust - lisame kolmanda keskkonna.

### 5.1. Staging keskkond (localhost variant)

Kuna meil on ainult 2 VM'i, kasutame staging'uks localhost teist korda:

```bash
nano inventory.yml
```

Lisa `webservers` gruppi:
```yaml
all:
  children:
    webservers:
      hosts:
        dev-web:
          ansible_host: localhost
          ansible_connection: local
          environment: development
          
        staging-web:
          ansible_host: localhost
          ansible_connection: local
          environment: staging
          
        prod-web:
          ansible_host: 192.168.82.11
          ansible_user: ansible
          environment: production
```

**Või kui sul on 3. VM:**
```yaml
        staging-web:
          ansible_host: 192.168.82.12  # Ubuntu 3 või Alma 1
          ansible_user: ansible
          environment: staging
```

### 5.2. Staging playbook

```bash
nano playbooks/staging-role.yml
```

Sisesta:
```yaml
---
- name: Deploy Staging Environment
  hosts: staging-web
  become: yes
  gather_facts: yes
  
  roles:
    - role: nginx
      vars:
        environment: "staging"
        server_name: "staging.example.com"
        debug_mode: true
        max_connections: 500
        site_color: "#FFFF00"  # Yellow
        nginx_port: 8080  # Erinev port, et ei konflikti dev'iga
```

**VAATA:** Uus keskkond = **16 rida**! Ei kopeerinud ühtegi task'i.

### 5.3. Käivita staging

```bash
ansible-playbook -i inventory.yml playbooks/staging-role.yml --vault-password-file .vault_pass
```

### 5.4. Kontrolli

```bash
curl http://localhost:8080
# Või brauseris: http://192.168.82.10:8080
```

**Peaks näitama:** Kollane leht, "STAGING" keskkond.

### Kontrollnimekiri
- [ ] Kolmas keskkond on lisatud
- [ ] Staging playbook on ainult ~16 rida
- [ ] Staging töötab erineval pordil
- [ ] Ei kopeerinud ühtegi task'i ega template'i

---

## 6. Võrdlus: Enne vs Pärast

### ENNE (ilma rollideta)

**Failid:**
```
playbooks/full_deploy.yml      70 rida
templates/nginx.conf.j2         50 rida
templates/index.html.j2         40 rida
group_vars/webservers/          20 rida
---
KOKKU: 180 rida
```

**Uus keskkond:**
- Kopeeri playbook → muuda vars
- Või lisa --limit flag
- Aga jagamine = kopeeri 4+ faili

### PÄRAST (rollidega)

**Failid:**
```
roles/nginx/                   ~120 rida (aga REUSABLE!)
playbooks/dev-role.yml          15 rida
playbooks/prod-role.yml         15 rida
playbooks/staging-role.yml      16 rida
---
Playbook'id KOKKU: 46 rida
```

**Uus keskkond:**
- Loo 15-realine playbook
- Määra ainult vars
- KÕIK task'id tulevad rollist

**Jagamine:**
```bash
# Kolleegile:
cp -r roles/nginx /kolleegi/projekt/roles/

# Tema playbook:
roles:
  - nginx  # Valmis!
```

---

## 7. Meta ja Dokumentatsioon

### 7.1. Meta info

```bash
nano roles/nginx/meta/main.yml
```

Sisesta:
```yaml
---
galaxy_info:
  role_name: nginx
  author: "Sinu Nimi"
  description: "Nginx web server for multiple environments (dev/staging/prod)"
  company: "IT College"
  license: MIT
  min_ansible_version: "2.9"
  
  platforms:
    - name: Ubuntu
      versions:
        - focal
        - jammy
  
  galaxy_tags:
    - web
    - nginx
    - multienv

dependencies: []
```

### 7.2. README

```bash
nano roles/nginx/README.md
```

Sisesta:
```markdown
# Ansible Role: Nginx

Paigaldab ja seadistab Nginx veebiserveri. Toetab mitut keskkonda (dev, staging, prod).

## Nõuded

- Ansible 2.9+
- Ubuntu 20.04/22.04/24.04
- Vault muutujad (kui kasutatakse HTTP auth)

## Rolli Muutujad

### Kohustuslikud (määra playbook'is)

- `environment`: "development" | "staging" | "production"
- `server_name`: "example.com"
- `site_color`: "#RRGGBB" (hex color)

### Valikulised (on defaults)

- `nginx_workers`: 2 (default: CPU arv)
- `nginx_port`: 80
- `nginx_root`: "/var/www/html"
- `debug_mode`: false
- `max_connections`: 100

### Vault muutujad (HTTP auth jaoks)

- `vault_admin_user`: "admin"
- `vault_admin_password`: "secret"

## Näited

### Development

\`\`\`yaml
- hosts: dev_servers
  roles:
    - role: nginx
      vars:
        environment: "development"
        server_name: "dev.example.local"
        debug_mode: true
        site_color: "#FFA500"
\`\`\`

### Production

\`\`\`yaml
- hosts: prod_servers
  roles:
    - role: nginx
      vars:
        environment: "production"
        server_name: "example.com"
        debug_mode: false
        site_color: "#00AA00"
        max_connections: 1000
\`\`\`

## Kasutamine

\`\`\`bash
ansible-playbook -i inventory site.yml --vault-password-file .vault_pass
\`\`\`

## Testimine

\`\`\`bash
# Idempotentsus
ansible-playbook site.yml
ansible-playbook site.yml  # changed=0

# Kontrolli
curl http://server_name
\`\`\`

## Autor

Su nimi
\`\`\`

```

## 8. GitHub Avaldamine (ära unusta)

Kui tahad rolli jagada:

```bash
cd roles/nginx

# Git init
git init
git add .
git commit -m "Initial nginx role for multi-environment deployment"

# GitHub
git remote add origin https://github.com/USERNAME/ansible-role-nginx.git
git branch -M main
git push -u origin main

# Tag
git tag v1.0.0
git push origin v1.0.0
```

**Kasutamine teistes projektides:**

```bash
# Installi Galaxy'st
ansible-galaxy install git+https://github.com/USERNAME/ansible-role-nginx.git

# Või requirements.yml
echo "- src: https://github.com/USERNAME/ansible-role-nginx.git
  name: nginx" > requirements.yml

ansible-galaxy install -r requirements.yml
```

---

## 9. Lõplik Struktuur

```
ansible-advanced/
├── .gitignore
├── .vault_pass
├── inventory.yml
├── group_vars/
│   ├── all/
│   │   ├── common.yml
│   │   └── vault.yml (encrypted)
│   └── webservers/
│       └── nginx.yml
├── host_vars/
│   ├── dev-web.yml
│   └── prod-web.yml
├── playbooks/
│   ├── dev-role.yml         # 15 rida
│   ├── prod-role.yml        # 15 rida
│   ├── staging-role.yml     # 16 rida
│   ├── full_deploy.yml      # 70 rida (vana viis)
│   └── ...
├── roles/
│   └── nginx/
│       ├── defaults/main.yml
│       ├── vars/main.yml
│       ├── tasks/main.yml
│       ├── templates/
│       │   ├── nginx.conf.j2
│       │   └── index.html.j2
│       ├── handlers/main.yml
│       ├── meta/main.yml
│       └── README.md
└── templates/              # Vanad (võid kustutada)
    ├── nginx.conf.j2
    └── index.html.j2
```

---

## 10. Lõplik Kontrollnimekiri

### Rollid põhimõtted
- [ ] Mõistad DRY printsiipi
- [ ] Mõistad miks rollid lahendavad jagamise probleemi
- [ ] Oled võrrelnud "enne" ja "pärast" koodikogust

### Roll ise
- [ ] Roll on loodud Galaxy struktuuri järgi
- [ ] Tasks, handlers, templates on rolli kaustades
- [ ] defaults/ sisaldab kasutaja-muudetavaid väärtusi
- [ ] vars/ sisaldab süsteemi-spetsiifilisi väärtusi

### Playbook'id
- [ ] Dev, prod, staging playbook'id on loodud
- [ ] Playbook'id on lühikesed (~15 rida)
- [ ] Kõik keskkonnad töötavad

### Skaleeritavus
- [ ] Kolmas keskkond (staging) oli lihtne lisada
- [ ] Ei kopeerinud ühtegi task'i
- [ ] Mõistad kuidas rollid skaleeruvad

### Dokumentatsioon
- [ ] meta/main.yml on täidetud
- [ ] README.md kirjeldab kasutamist
- [ ] Näited on selged

---

## Troubleshooting

### Roll ei leia template'i

**Probleem:** "template not found: nginx.conf.j2"

**Lahendus:**
```bash
# Kontrolli template'i asukohta
ls roles/nginx/templates/

# Template'i path rollis peab olema:
src: nginx.conf.j2  # MITTE ../templates/nginx.conf.j2
```

### Muutuja on undefined

**Probleem:** "vault_admin_password is undefined"

**Lahendus:**
```bash
# Kontrolli et vault fail on kaasas
ansible-vault view group_vars/all/vault.yml

# Kontrolli et kasutad --vault-password-file
ansible-playbook ... --vault-password-file .vault_pass
```

### Playbook ei kasuta rolli

**Probleem:** Tasks ei käivitu

**Lahendus:**
```yaml
# Kontrolli YAML indentatsiooni
roles:
  - role: nginx  # PEAB olema list item
    vars:
      ...
```

---

## Kasulikud Käsud

```bash
# Rolli dokumentatsiooni vaatamine
ansible-doc -t role nginx
```

---

Hästi tehtud! Oled nüüd Ansible rollide meister! 🎉

**Peamised õppetunnid:**
- Rollid = korduvkasutatavad komponendid
- DRY printsiip praktikas
- Skaleeritavus (uus keskkond = 15 rida)
- Jagamine = kopeerida üks kaust
- Galaxy standard = kõik mõistavad struktuuri
