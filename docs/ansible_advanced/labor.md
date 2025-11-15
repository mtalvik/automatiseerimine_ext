# Ansible Edasijõudnud Labor

**Eeldused:** Ansible põhitõed (inventory, playbooks, ad-hoc käsud), YAML süntaks, Linux CLI  
**Platvorm:** Ubuntu 24.04 (töötab ka Ubuntu 20.04/22.04), Proxmox keskkond  
**Kestus:** ~2 tundi

---

## Õpiväljundid

Pärast seda labori oskad:

- Rakendada muutujate hierarhiat (group_vars, host_vars) erinevate keskkondade haldamiseks
- Luua Jinja2 template'eid dünaamiliste konfiguratsioonifailide genereerimiseks
- Kasutada handler'eid teenuste tõhusaks haldamiseks
- Krüpteerida tundlikke andmeid Ansible Vault'iga
- Ehitada struktureeritud Ansible projekti, mis skaleerub

---

## Labori Ülevaade

Selles laboris ehitate sammhaaval nginx veebiserveri seadistuse, mis töötab kahes erinevas keskkonnas (development ja production). Iga samm lisab ühe võtmetehnoloogia - alustades muutujatest, liikudes template'ide ja handler'ite juurde, lõpetades vault'iga. Õpite mõistma, miks need tehnikad on vajalikud ja kuidas nad koos töötavad.

**Development keskkond:** Ubuntu 1 (localhost) - kiire testimine ja arendus  
**Production keskkond:** Ubuntu 2 (remote) - realistlik deployment

---

## 1. Proxmox VM'ide Ettevalmistus

### 1.1. Kontrolli SSH ühendust

Kasutame Ansible aluste labori VM'e ( sul on enda IP):

- **Ubuntu 1** (192.168.82.10) - Controller, siin jookseb Ansible
- **Ubuntu 2** (192.168.82.11) - Target, siia paigaldame nginx

```bash
# WinKlient'ist: logi sisse Ubuntu 1
ssh ansible@192.168.82.10

# Ubuntu 1'st kontrolli ühendust Ubuntu 2'ga:
ssh ansible@192.168.82.11
# Peaks sisse logima ilma parooli küsimata
exit
```

Kui SSH ei tööta ilma paroolita, vaata Ansible aluste labori SSH võtmete setup'i.

### 1.2. Projekti loomine

```bash
# Ubuntu 1's (controller)
mkdir -p ~/ansible-advanced
cd ~/ansible-advanced

# Loo kaustade struktuur
mkdir -p {group_vars/all,group_vars/webservers,host_vars,templates,playbooks}

# Kontrolli struktuuri
tree .
```

Peaks näitama:
```
.
├── group_vars/
│   ├── all/
│   └── webservers/
├── host_vars/
├── playbooks/
└── templates/
```

### 1.3. Inventory seadistamine

```bash
nano inventory.yml
```

Sisesta:
```yaml
all:
  children:
    webservers:
      hosts:
        dev-web:
          ansible_host: localhost
          ansible_connection: local
          environment: development
          
        prod-web:
          ansible_host: 192.168.82.11  # Ubuntu 2
          ansible_user: ansible
          environment: production
```

**Märkus:** 
- **dev-web** on Ubuntu 1 ise (localhost) - kiire testimine ilma SSH overhead'ita
- **prod-web** on Ubuntu 2 (remote) - realistlik deployment üle SSH

### 1.4. Kontrolli ühendust

```bash
ansible -i inventory.yml all -m ping
```

**Oodatav väljund:**
```
dev-web | SUCCESS => { "ping": "pong" }
prod-web | SUCCESS => { "ping": "pong" }
```

### Kontrollnimekiri
- [ ] Ubuntu 1 ja Ubuntu 2 on töös
- [ ] SSH Ubuntu 2'sse töötab ilma paroolita
- [ ] Projekti struktuur on loodud
- [ ] Mõlemad serverid vastavad ping'ile

---

## 2. Muutujate Hierarhia

Nüüd õpime, kuidas erinevatel tasanditel muutujaid defineerida ja kuidas Ansible neid prioritiseerib.

### 2.1. Globaalsed muutujad (group_vars/all/)

Need muutujad kehtivad KÕIGILE serveritele:

```bash
nano group_vars/all/common.yml
```

Sisesta:
```yaml
---
# Rakenduse põhiinfo
app_name: "ansible-demo"
admin_email: "admin@example.com"

# Nginx põhiseaded
nginx_user: "www-data"
nginx_worker_connections: 1024
```

### 2.2. Grupi muutujad (group_vars/webservers/)

Need muutujad kehtivad ainult webservers grupile:

```bash
nano group_vars/webservers/nginx.yml
```

Sisesta:
```yaml
---
# Nginx seaded veebiserveri jaoks
nginx_port: 80
nginx_root: "/var/www/html"

# Dünaamiline worker'ite arv CPU järgi
nginx_workers: "{{ ansible_processor_vcpus | default(2) }}"
```

### 2.3. Host-spetsiifilised muutujad

Development server vajab erinevaid seadeid kui production:

```bash
nano host_vars/dev-web.yml
```

Sisesta:
```yaml
---
server_name: "dev.example.local"
debug_mode: true
max_connections: 100
site_color: "#FFA500"  # Orange
```

```bash
nano host_vars/prod-web.yml
```

Sisesta:
```yaml
---
server_name: "prod.example.com"
debug_mode: false
max_connections: 1000
site_color: "#00AA00"  # Green
```

### 2.4. Muutujate testimine

Loome lihtsa playbook'i, et näha kuidas muutujad töötavad:

```bash
nano playbooks/test_variables.yml
```

Sisesta:
```yaml
---
- name: Test variable hierarchy
  hosts: webservers
  gather_facts: yes
  
  tasks:
    - name: Display all variables
      debug:
        msg: |
          App: {{ app_name }}
          Email: {{ admin_email }}
          Server: {{ server_name }}
          Debug: {{ debug_mode }}
          Workers: {{ nginx_workers }}
          Max Conn: {{ max_connections }}
          Color: {{ site_color }}
```

Käivita:
```bash
ansible-playbook -i inventory.yml playbooks/test_variables.yml
```

**Jälgi väljundit:** dev-web ja prod-web näitavad erinevaid väärtusi!

### Mõistmine: Prioriteedid

Ansible rakendab muutujaid järgmises järjekorras (madalam → kõrgem):
1. `group_vars/all/` - kõige üldisem
2. `group_vars/webservers/` - grupi-spetsiifiline
3. `host_vars/dev-web.yml` - serveri-spetsiifiline (kõrgeim)

**Näide:** Kui `group_vars/all/` ütleb `nginx_port: 80` aga `host_vars/dev-web.yml` ütleb `nginx_port: 8080`, siis dev-web kasutab **8080**.

### Kontrollnimekiri
- [ ] Kõik muutujate failid on loodud
- [ ] Test playbook näitab erinevaid väärtusi dev ja prod serveritel
- [ ] Mõistad muutujate prioriteete

---

## 3. Template'id ja Dünaamilised Konfiguratsioonid

Template'id võimaldavad luua konfiguratsioone, mis kohanduvad automaatselt serveri ja keskkonna järgi.

### 3.1. Nginx konfiguratsioon template

Loome nginx.conf template, mis kasutab meie muutujaid:

```bash
nano templates/nginx.conf.j2
```

Sisesta:
```nginx
# {{ ansible_managed }}
# Nginx configuration for {{ server_name }}

user {{ nginx_user }};
worker_processes {{ nginx_workers }};
pid /run/nginx.pid;

events {
    worker_connections {{ nginx_worker_connections }};
}

http {
    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    {% if debug_mode %}
    # Development - verbose logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log debug;
    {% else %}
    # Production - minimal logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log warn;
    {% endif %}

    # Gzip
    gzip on;

    # Server block
    server {
        listen {{ nginx_port }};
        server_name {{ server_name }};
        root {{ nginx_root }};
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }

        # Security headers (production only)
        {% if not debug_mode %}
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        {% endif %}
    }
}
```

### 3.2. HTML template

Loome ka dünaamilise veebilehe:

```bash
nano templates/index.html.j2
```

Sisesta:
```html
<!DOCTYPE html>
<html lang="et">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_name }} - {{ environment | upper }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: {{ site_color }};
            color: white;
            padding: 50px;
            text-align: center;
        }
        .container {
            background: rgba(0,0,0,0.3);
            padding: 40px;
            border-radius: 10px;
            max-width: 600px;
            margin: 0 auto;
        }
        .info {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ app_name | upper }}</h1>
        <h2>Environment: {{ environment | upper }}</h2>
        
        <div class="info">
            <h3>Server Information</h3>
            <p><strong>Hostname:</strong> {{ ansible_hostname }}</p>
            <p><strong>Server Name:</strong> {{ server_name }}</p>
            <p><strong>OS:</strong> {{ ansible_distribution }} {{ ansible_distribution_version }}</p>
        </div>

        <div class="info">
            <h3>Nginx Configuration</h3>
            <p><strong>Workers:</strong> {{ nginx_workers }}</p>
            <p><strong>Port:</strong> {{ nginx_port }}</p>
            <p><strong>Max Connections:</strong> {{ max_connections }}</p>
            <p><strong>Debug Mode:</strong> {{ debug_mode }}</p>
        </div>

        {% if debug_mode %}
        <div class="info">
            <h3>Debug Information</h3>
            <p><strong>Admin:</strong> {{ admin_email }}</p>
            <p><strong>Memory:</strong> {{ ansible_memtotal_mb }} MB</p>
            <p><strong>CPU Cores:</strong> {{ ansible_processor_vcpus }}</p>
            <p><strong>Generated:</strong> {{ ansible_date_time.iso8601 }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
```

### 3.3. Deployment playbook

Nüüd loome playbook'i, mis kasutab neid template'eid:

```bash
nano playbooks/deploy_nginx.yml
```

Sisesta:
```yaml
---
- name: Deploy Nginx with templates
  hosts: webservers
  become: yes
  gather_facts: yes
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"
    
    - name: Install nginx
      apt:
        name: nginx
        state: present
      notify: start nginx
    
    - name: Deploy nginx configuration from template
      template:
        src: ../templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        owner: root
        group: root
        mode: '0644'
        backup: yes
      notify: reload nginx
    
    - name: Deploy website from template
      template:
        src: ../templates/index.html.j2
        dest: "{{ nginx_root }}/index.html"
        owner: "{{ nginx_user }}"
        group: "{{ nginx_user }}"
        mode: '0644'
    
    - name: Ensure nginx is started and enabled
      service:
        name: nginx
        state: started
        enabled: yes
  
  handlers:
    - name: start nginx
      service:
        name: nginx
        state: started
    
    - name: reload nginx
      service:
        name: nginx
        state: reloaded
```

### 3.4. Käivitamine

```bash
ansible-playbook -i inventory.yml playbooks/deploy_nginx.yml
```

### 3.5. Kontrollimine

```bash
# Vaata nginx konfiguratsiooni dev serveris (localhost)
sudo head -20 /etc/nginx/nginx.conf

# Vaata nginx konfiguratsiooni prod serveris (remote)
ansible -i inventory.yml prod-web -m shell -a "head -20 /etc/nginx/nginx.conf" --become

# Testi veebilehte
# Dev (localhost):
curl http://localhost

# Prod (Ubuntu 2):
curl http://192.168.82.11
```

**WinKlient'ist brauseris:**
- Development: `http://192.168.82.10` (oranž leht)
- Production: `http://192.168.82.11` (roheline leht)

### Kontrollnimekiri
- [ ] Template'id on loodud
- [ ] Nginx konfiguratsioon genereeritakse õigesti
- [ ] Dev ja prod serveritel on erinevad konfiguratsioonid
- [ ] Veebileht kuvab õigeid muutujaid
- [ ] Mõlemad lehed on brauseris nähtavad

---

## 4. Handler'id: Tõhus Teenuste Haldamine

Handler'id tagavad, et teenuseid taaskäivitatakse ainult siis, kui see on vajalik.

### 4.1. Handler'ite mõistmine

Vaatame, mis juhtus eelmises playbook'is:

```yaml
notify: reload nginx
```

Handler **ei käivitu kohe** - ta käivitub playbook'i lõpus JA ainult siis, kui task tegi muudatuse (`changed: true`).

### 4.2. Test: Idempotentsus

Käivita sama playbook teist korda:

```bash
ansible-playbook -i inventory.yml playbooks/deploy_nginx.yml
```

**Jälgi väljundit:**
- "Deploy nginx configuration" näitab `ok` (mitte `changed`)
- Handler'it **EI käivitata**, sest midagi ei muutunud
- Nginx jääb töötama ilma taaskäivituseta

### 4.3. Test: Muudatus käivitab handler'i

Muudame nginx konfiguratsiooni:

```bash
nano group_vars/webservers/nginx.yml
```

Muuda:
```yaml
nginx_worker_connections: 2048  # Oli 1024
```

Käivita uuesti:
```bash
ansible-playbook -i inventory.yml playbooks/deploy_nginx.yml
```

**Jälgi:** 
- "Deploy nginx configuration" näitab `changed`
- Handler **käivitatakse** lõpus
- Nginx reload'itakse automaatselt

### 4.4. Reload vs Restart

Meie playbook kasutab `reload` mitte `restart`:

```yaml
handlers:
  - name: reload nginx
    service:
      name: nginx
      state: reloaded  # Mitte restarted!
```

**Miks?**
- **Reload:** Laeb konfiguratsiooni uuesti, EI katkesta ühendusi
- **Restart:** Peatab teenuse täielikult, katkestab ühendused

Production serverites eelistame reload'i.

### Kontrollnimekiri
- [ ] Mõistad, millal handler käivitub
- [ ] Teine käivitus ei restart'i nginx'i (idempotentne)
- [ ] Konfiguratsiooni muudatus käivitab handler'i
- [ ] Mõistad reload vs restart erinevust

---

## 5. Ansible Vault: Turvaline Paroolide Haldus

Vault krüpteerib tundlikud andmed nii, et neid saab ohutult Git'i panna.

### 5.1. Vault faili loomine

Loome krüpteeritud faili, kus hoiame paroole:

```bash
ansible-vault create group_vars/all/vault.yml
```

Küsib parooli - kasuta näiteks: `ansible123`

Sisesta vault faili:
```yaml
---
# Database credentials
vault_db_password: "SuperSecret123!"
vault_db_user: "webapp"

# Admin credentials  
vault_admin_password: "AdminPass456!"
vault_admin_email: "admin@example.com"

# API keys
vault_api_key: "abc123xyz789secret"
```

Salvesta ja välju (`:wq`).

### 5.2. Vault muutujate kasutamine

Vault muutujaid ei kasutata otse - need "mappitakse" tavalistele muutujatele:

```bash
nano group_vars/all/common.yml
```

Lisa lõppu:
```yaml
# Reference vault variables
db_password: "{{ vault_db_password }}"
db_user: "{{ vault_db_user }}"
admin_password: "{{ vault_admin_password }}"
admin_email: "{{ vault_admin_email }}"
api_key: "{{ vault_api_key }}"
```

### 5.3. Vault playbook

Loome playbook, mis kasutab vault muutujaid:

```bash
nano playbooks/test_vault.yml
```

Sisesta:
```yaml
---
- name: Test Vault variables
  hosts: localhost
  connection: local
  gather_facts: no
  
  tasks:
    - name: Show that we can access vault variables
      debug:
        msg: |
          DB User: {{ db_user }}
          DB Password: {{ db_password }}
          Admin Email: {{ admin_email }}
          API Key: {{ api_key }}
```

### 5.4. Käivitamine vault'iga

```bash
# Ilma vault paroolita - ebaõnnestub!
ansible-playbook -i inventory.yml playbooks/test_vault.yml

# Küsi vault parooli interaktiivselt
ansible-playbook -i inventory.yml playbooks/test_vault.yml --ask-vault-pass
```

Sisesta: `ansible123`

**Väljund näitab:** Kõik paroolid on dekrüpteeritud ja kättesaadavad!

### 5.5. Vault käsud

```bash
# Vaata vault faili (küsib parooli)
ansible-vault view group_vars/all/vault.yml

# Muuda vault faili
ansible-vault edit group_vars/all/vault.yml

# Muuda vault parooli
ansible-vault rekey group_vars/all/vault.yml

# Krüpteeri olemasolev fail
echo "secret: password123" > test.yml
ansible-vault encrypt test.yml

# Dekrüpteeri (ETTEVAATUST!)
ansible-vault decrypt test.yml
```

### 5.6. Vault password fail (mugavamaks)

```bash
# Loo paroolifail
echo "ansible123" > .vault_pass

# Kaitse õigustega
chmod 600 .vault_pass

# Lisa .gitignore'i
echo ".vault_pass" >> .gitignore

# Käivita ilma --ask-vault-pass
ansible-playbook -i inventory.yml playbooks/test_vault.yml --vault-password-file .vault_pass
```

### 5.7. Uuendame nginx playbook'i vault'iga

Lisame HTTP basic auth kasutades vault paroole:

```bash
nano templates/nginx.conf.j2
```

Lisa server blokki (enne `location /` rida):
```nginx
        # Basic auth for production
        {% if not debug_mode %}
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        {% endif %}
```

Uuenda playbook'i:

```bash
nano playbooks/deploy_nginx.yml
```

Lisa task enne "Deploy nginx configuration" task'i:
```yaml
    - name: Install python3-passlib for htpasswd module
      apt:
        name: python3-passlib
        state: present
    
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
```

Lisa vault muutuja:

```bash
ansible-vault edit group_vars/all/vault.yml
```

Lisa:
```yaml
vault_admin_user: "admin"
```

Käivita:
```bash
ansible-playbook -i inventory.yml playbooks/deploy_nginx.yml --vault-password-file .vault_pass
```

### 5.8. Kontrollimine

```bash
# Development - ei küsi parooli
curl http://192.168.82.10

# Production - küsib parooli
curl -u admin:AdminPass456! http://192.168.82.11
```

**WinKlient brauseris:**
- Dev: `http://192.168.82.10` - avub kohe
- Prod: `http://192.168.82.11` - küsib kasutajat/parooli (admin / AdminPass456!)

### Kontrollnimekiri
- [ ] Vault fail on loodud ja krüpteeritud
- [ ] Saad vault muutujaid kasutada playbook'ides
- [ ] .vault_pass fail töötab
- [ ] Mõistad, miks mitte panna paroole otse Git'i
- [ ] Production server küsib autentimist, dev mitte

---

## 6. Lõplik Projekt: Kõik Koos

Nüüd loome ühe playbook'i, mis kasutab KÕIKI õpitud tehnikaid.

### 6.1. Täielik deployment playbook

```bash
nano playbooks/full_deploy.yml
```

Sisesta:
```yaml
---
- name: Full deployment with all advanced features
  hosts: webservers
  become: yes
  gather_facts: yes
  
  pre_tasks:
    - name: Display deployment info
      debug:
        msg: |
          Deploying to: {{ inventory_hostname }}
          Environment: {{ environment }}
          Server: {{ server_name }}
          Debug mode: {{ debug_mode }}
  
  tasks:
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
        src: ../templates/nginx.conf.j2
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
        src: ../templates/index.html.j2
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
  
  handlers:
    - name: start nginx
      service:
        name: nginx
        state: started
    
    - name: reload nginx
      service:
        name: nginx
        state: reloaded
  
  post_tasks:
    - name: Verify nginx is running
      service:
        name: nginx
        state: started
      check_mode: yes
      register: nginx_status
    
    - name: Display deployment result
      debug:
        msg: "Deployment successful! Visit http://{{ ansible_host if ansible_host != 'localhost' else '192.168.82.10' }}"
```

### 6.2. Käivitamine

```bash
# Development
ansible-playbook -i inventory.yml playbooks/full_deploy.yml \
  --limit dev-web \
  --vault-password-file .vault_pass

# Production
ansible-playbook -i inventory.yml playbooks/full_deploy.yml \
  --limit prod-web \
  --vault-password-file .vault_pass

# Või mõlemad korraga
ansible-playbook -i inventory.yml playbooks/full_deploy.yml \
  --vault-password-file .vault_pass
```

### 6.3. Kontrollimine

```bash
# Development - ei küsi parooli
curl http://192.168.82.10

# Production - küsib parooli
curl -u admin:AdminPass456! http://192.168.82.11
```

### Kontrollnimekiri
- [ ] Playbook kasutab muutujaid hierarhiliselt
- [ ] Template'id genereerivad erinevaid konfiguratsioone
- [ ] Handler'id käivituvad ainult muudatuste korral
- [ ] Vault krüpteerib tundlikke andmeid
- [ ] Production on parooliga kaitstud, dev mitte
- [ ] Mõlemad lehed töötavad brauseris

---

## 7. Projekti Struktuur Lõplikult

Sinu lõplik projekt peaks välja nägema nii:

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
├── templates/
│   ├── nginx.conf.j2
│   └── index.html.j2
└── playbooks/
    ├── test_variables.yml
    ├── deploy_nginx.yml
    ├── test_vault.yml
    └── full_deploy.yml
```

### .gitignore

```bash
nano .gitignore
```

Sisesta:
```
.vault_pass
*.retry
```

---

## 8. Lõplik Kontrollnimekiri

Veendu, et oled täitnud kõik punktid:

### Muutujad
- [ ] `group_vars/all/common.yml` sisaldab globaalseid muutujaid
- [ ] `group_vars/webservers/nginx.yml` sisaldab nginx seadeid
- [ ] `host_vars/` sisaldab server-spetsiifilisi muutujaid
- [ ] Mõistad muutujate prioriteete

### Template'id
- [ ] `nginx.conf.j2` kasutab muutujaid ja conditionals
- [ ] `index.html.j2` näitab serveri infot
- [ ] Template'id genereerivad erinevaid faile dev vs prod

### Handler'id
- [ ] Handler'id on defineeritud playbook'is
- [ ] Notify käivitab õigeid handler'eid
- [ ] Idempotentsus töötab (teine käivitus ei muuda midagi)
- [ ] Reload vs restart erinevus on selge

### Vault
- [ ] `vault.yml` on krüpteeritud
- [ ] Vault muutujad on "mapped" common.yml's
- [ ] Playbook töötab `--vault-password-file`'iga
- [ ] `.vault_pass` on .gitignore's

### Projekt
- [ ] Struktuur järgib best practice'eid
- [ ] Kõik playbook'id töötavad
- [ ] Development ja production erinevad
- [ ] Projekt on valmis Git'i

---

## 9. Troubleshooting

### SSH probleemid

**Probleem:** prod-web ei vasta ping'ile
```bash
# Kontrolli SSH ühendust käsitsi
ssh ansible@192.168.82.11

# Kontrolli SSH võtmeid
ls -la ~/.ssh/
ssh-copy-id ansible@192.168.82.11
```

### Vault vead

**Probleem:** "Decryption failed"
```bash
# Kontrolli vault faili
ansible-vault view group_vars/all/vault.yml

# Kui parool vale, muuda
ansible-vault rekey group_vars/all/vault.yml
```

**Probleem:** "vault_variable is undefined"
```bash
# Kontrolli, kas vault fail on õigesti linked
cat group_vars/all/common.yml | grep vault_
```

### Template vead

**Probleem:** "template error while templating string"
```bash
# Kontrolli Jinja2 süntaksit template's
# Leia rida, kus viga on (error näitab rea numbrit)
# Tihti probleem: {{ muutuja }} või {% if %} lõpetamata
```

### Handler ei käivitu

**Probleem:** Konfiguratsioon muutus aga nginx ei reload'i
```bash
# Kontrolli notify nime
# handlers: - name: "reload nginx"
# tasks:    notify: reload nginx
# PEAVAD OLEMA TÄPSELT SAMAD!
```

### Nginx ei käivitu

**Probleem:** "nginx.service failed"
```bash
# Kontrolli nginx konfiguratsiooni
sudo nginx -t

# Vaata error logi
sudo tail -50 /var/log/nginx/error.log

# Kontrolli kas port on juba kasutusel
sudo ss -tulpn | grep :80
```

---

## 10. Järgmised Sammud

Oled nüüd valmis järgmiseks mooduliks: **Ansible Rollid**!

Rollid võtavad kõik siin õpitud tehnikad ja pakendavad need korduvkasutatavasse struktuuri. Sa refaktoreerid selle nginx seadistuse rolliks, mida saab jagada ja kasutada erinevates projektides.

**Mis tuleb rollides:**
- DRY (Don't Repeat Yourself) printsiip
- Galaxy standard struktuur
- Dependencies
- Taaskasutus erinevates projektides
- Selle sama projekti refaktoreerimine rolliks!

---

## Kasulikud Käsud

```bash
# Muutujate debug
ansible -i inventory.yml dev-web -m debug -a "var=hostvars[inventory_hostname]"

# Kontrolli template väljundit
ansible -i inventory.yml dev-web -m template -a "src=templates/nginx.conf.j2 dest=/tmp/test.conf"

# Vault
ansible-vault view group_vars/all/vault.yml
ansible-vault edit group_vars/all/vault.yml
ansible-vault encrypt file.yml
ansible-vault decrypt file.yml

# Playbook testimine
ansible-playbook playbook.yml --syntax-check  # Süntaks
ansible-playbook playbook.yml --check         # Kuiv käivitus
ansible-playbook playbook.yml --diff          # Näita muudatusi
ansible-playbook playbook.yml -vvv            # Verbose

# Käivita ainult ühes serveris
ansible-playbook -i inventory.yml playbook.yml --limit dev-web
ansible-playbook -i inventory.yml playbook.yml --limit prod-web
```

Hästi tehtud! Oled nüüd Ansible edasijõudnud tehnikate kasutaja! 🎉
