# Ansible Rollid - Labor

**Eeldused:** Ansible playbook'ide kogemus, Linux CLI, YAML põhitundmine  
**Platvorm:** Ansible 2.9+, Ubuntu 20.04+, Vagrant/Docker  
**Kestus:** 2 × 45 minutit

## Õpiväljundid

Pärast laborit õppija:

- Mõistab miks rollid on vajalikud läbi praktilise probleemi (korduvkasutus, hooldus)
- Refaktoreerib mitut playbook'i üheks rolliks
- Loob Galaxy standardi järgi struktureeritud rolli
- Eristab defaults/ ja vars/ kaustade kasutust
- Kasutab Jinja2 template'e ja muutujaid erinevate keskkondade jaoks
- Testib rolli idempotentsust
- Avaldab rolli GitHub'is

---

## 1. Enne Alustamist

Kontrolli et sul on:

```bash
vagrant --version  # 2.2+
vboxmanage --version
ansible --version  # 2.9+
git --version
```

---

## 2. Töökeskkonna Ettevalmistus

Loome **kaks** erinevat keskkonda: development ja production.

```bash
mkdir -p ~/ansible-roles-lab
cd ~/ansible-roles-lab
```

### Vagrantfile

Loo fail `Vagrantfile` **kahe** VM'iga:

```ruby
Vagrant.configure("2") do |config|
  
  # Development server
  config.vm.define "dev" do |dev|
    dev.vm.box = "ubuntu/focal64"
    dev.vm.hostname = "dev-web"
    dev.vm.network "forwarded_port", guest: 80, host: 8080
    
    dev.vm.provider "virtualbox" do |vb|
      vb.memory = "512"
      vb.cpus = 1
    end
    
    dev.vm.provision "shell", inline: <<-SHELL
      apt-get update -qq
      apt-get install -y python3
    SHELL
  end
  
  # Production server
  config.vm.define "prod" do |prod|
    prod.vm.box = "ubuntu/focal64"
    prod.vm.hostname = "prod-web"
    prod.vm.network "forwarded_port", guest: 80, host: 8081
    
    prod.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.cpus = 2
    end
    
    prod.vm.provision "shell", inline: <<-SHELL
      apt-get update -qq
      apt-get install -y python3
    SHELL
  end
end
```

!!! info "Miks kaks VM'i"
    Simuleerime reaalset olukorda kus on eraldi development ja production keskkonnad. Nii näeme probleemi mida rollid lahendavad.

### Käivita Mõlemad VM'd

```bash
vagrant up
```

!!! note "Esimene käivitus"
    Võtab 3-7 minutit kuna laeb Ubuntu image ja seadistab kaks VM'i.

### Inventory

Loo fail `inventory`:

```ini
[dev_servers]
dev ansible_host=127.0.0.1 ansible_port=2222 ansible_user=vagrant ansible_ssh_private_key_file=.vagrant/machines/dev/virtualbox/private_key

[prod_servers]
prod ansible_host=127.0.0.1 ansible_port=2200 ansible_user=vagrant ansible_ssh_private_key_file=.vagrant/machines/prod/virtualbox/private_key

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### Test Ühendust

```bash
ansible all -i inventory -m ping
```

**Oodatav tulemus:**

```
dev | SUCCESS => {"ping": "pong"}
prod | SUCCESS => {"ping": "pong"}
```

??? warning "Kui ping ei tööta"
    **VM ei käi:**
    ```bash
    vagrant status  # kontrolli staatust
    vagrant up dev  # käivita dev
    vagrant up prod # käivita prod
    ```
    
    **SSH võti puudub:**
    ```bash
    ls -la .vagrant/machines/*/virtualbox/private_key
    # Peaksid nägema mõlemat võtit
    ```

**Kontrollpunkt:**

- [ ] 2 VM'i käivad (`vagrant status` näitab "running")
- [ ] Mõlemad vastuvad ping'ile

---

## 3. Probleem: Kaks Keskkonda, Kaks Playbook'i

Nüüd paigaldame Nginx mõlemasse keskkonda. Alguses **ilma rollideta** - näeme mis probleem tekib.

### nginx.conf.j2

Loo template fail:

```nginx
user www-data;
worker_processes {{ nginx_workers }};
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    gzip on;
    
    server {
        listen {{ nginx_port }};
        server_name {{ nginx_hostname }};
        root /var/www/html;
        index index.html;
        
        location / {
            try_files $uri $uri/ =404;
        }
    }
}
```

### dev-nginx.yml

Loo playbook development keskkonnale:

```yaml
---
- name: Setup Development Nginx
  hosts: dev_servers
  become: yes
  
  vars:
    nginx_workers: 1
    nginx_port: 80
    nginx_hostname: "dev.local"
    site_title: "Development Environment"
    site_color: "#FFA500"
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install nginx
      apt:
        name: nginx
        state: present
    
    - name: Copy nginx configuration
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        validate: 'nginx -t -c %s'
      notify: reload nginx
    
    - name: Create index.html
      copy:
        content: |
          <!DOCTYPE html>
          <html>
          <head>
            <title>{{ site_title }}</title>
            <style>body { background: {{ site_color }}; font-family: Arial; text-align: center; padding: 50px; }</style>
          </head>
          <body>
            <h1>{{ site_title }}</h1>
            <p>Workers: {{ nginx_workers }}</p>
            <p>Port: {{ nginx_port }}</p>
          </body>
          </html>
        dest: /var/www/html/index.html
    
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
  
  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded
```

### prod-nginx.yml

Loo playbook production keskkonnale:

```yaml
---
- name: Setup Production Nginx
  hosts: prod_servers
  become: yes
  
  vars:
    nginx_workers: 4
    nginx_port: 80
    nginx_hostname: "prod.local"
    site_title: "Production Environment"
    site_color: "#00AA00"
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install nginx
      apt:
        name: nginx
        state: present
    
    - name: Copy nginx configuration
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        validate: 'nginx -t -c %s'
      notify: reload nginx
    
    - name: Create index.html
      copy:
        content: |
          <!DOCTYPE html>
          <html>
          <head>
            <title>{{ site_title }}</title>
            <style>body { background: {{ site_color }}; font-family: Arial; text-align: center; padding: 50px; }</style>
          </head>
          <body>
            <h1>{{ site_title }}</h1>
            <p>Workers: {{ nginx_workers }}</p>
            <p>Port: {{ nginx_port }}</p>
          </body>
          </html>
        dest: /var/www/html/index.html
    
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
  
  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded
```

!!! warning "Pane tähele"
    Mõlemad playbook'id on peaaegu identsed. Ainult `vars` sektsioon erineb. Kõik task'id on kopeeritud.

### Käivita Mõlemad

```bash
# Development
ansible-playbook -i inventory dev-nginx.yml

# Production
ansible-playbook -i inventory prod-nginx.yml
```

### Kontrolli Brauseris

- Development: `http://localhost:8080` (oranž taust)
- Production: `http://localhost:8081` (roheline taust)

**Kontrollpunkt:**

- [ ] Development töötab (oranž leht)
- [ ] Production töötab (roheline leht)
- [ ] Mõlemad näitavad erinevat worker count'i

---

## 4. Mis On Probleem?

Vaata kaht playbook'i kõrvuti ja mõtle:

1. Mitu korda on "Install nginx" task kopeeritud? (**2 korda**)
2. Kui leiad vea nginx install task'is, mitu faili pead muutma? (**2 faili**)
3. Kui tahad lisada SSL'i, mitu faili muuta? (**2 faili**)
4. Kui lisandub staging keskkond? (**Kopeeri kolmandat korda**)
5. Kui kolleeg tahab kasutada sinu nginx setup'i? (**Saada 3 faili: 2 playbook'i + template**)

!!! danger "DRY printsiibi rikkumine"
    Don't Repeat Yourself - iga koodiosa peaks eksisteerima täpselt üks kord. Praegu on duplikatsioon.

### Simuleerime Viga

Oletame et nginx paketi nimi on valesti! Peab olema `nginx-full` mitte `nginx`.

**Ülesanne:** Paranda mõlemad playbook'id.

```yaml
# Muuda MÕLEMAS playbook'is:
- name: Install nginx
  apt:
    name: nginx-full  # Muutsid 2 failis!
    state: present
```

Ebamugav, eks? Kaks faili muuta sama asja jaoks. Nüüd kujuta ette 5 keskkonda või 10 projekti...

---

## 5. Lahendus: Refaktoreerimine Rolliks

Nüüd võtame kogu selle duplikatsiooni ja paneme **ühte** rolli.

### Samm 1: Loo Roll

```bash
mkdir -p roles
cd roles
ansible-galaxy init nginx
cd ..
```

**Tulemus:**

```plaintext
roles/nginx/
├── defaults/main.yml
├── vars/main.yml
├── tasks/main.yml
├── templates/
├── handlers/main.yml
└── meta/main.yml
```

!!! tip "Galaxy init"
    Loob automaatselt standardse kaustade struktuuri. Iga Ansible roll järgib sama struktuuri.

### Samm 2: Liiguta Tasks

Võta **kummastki** playbook'ist tasks sektsioon (need on identsed!).

Ava `roles/nginx/tasks/main.yml`:

```yaml
---
- name: Update apt cache
  apt:
    update_cache: yes
    cache_valid_time: 3600

- name: Install nginx
  apt:
    name: "{{ nginx_package }}"
    state: present

- name: Copy nginx configuration
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    validate: 'nginx -t -c %s'
  notify: reload nginx

- name: Create index.html
  template:
    src: index.html.j2
    dest: /var/www/html/index.html

- name: Start nginx
  service:
    name: nginx
    state: started
    enabled: yes
```

### Samm 3: Liiguta Handlers

Ava `roles/nginx/handlers/main.yml`:

```yaml
---
- name: reload nginx
  service:
    name: nginx
    state: reloaded
```

### Samm 4: Liiguta Template'id

```bash
mv nginx.conf.j2 roles/nginx/templates/
```

Loo `roles/nginx/templates/index.html.j2`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>{{ site_title }}</title>
  <style>body { background: {{ site_color }}; font-family: Arial; text-align: center; padding: 50px; }</style>
</head>
<body>
  <h1>{{ site_title }}</h1>
  <p>Environment: {{ nginx_environment }}</p>
  <p>Workers: {{ nginx_workers }}</p>
  <p>Port: {{ nginx_port }}</p>
</body>
</html>
```

### Samm 5: Defineeri Muutujad

#### defaults/main.yml

Väärtused mida **kasutaja võib muuta**:

```yaml
---
# Nginx seaded
nginx_workers: "{{ ansible_processor_vcpus | default(2) }}"
nginx_port: 80
nginx_hostname: "localhost"

# Site seaded
nginx_environment: "unknown"
site_title: "Web Server"
site_color: "#CCCCCC"
```

!!! info "Miks defaults"
    Need on väärtused mida iga keskkond (dev, prod, staging) määrab ise. Madal prioriteet - playbook vars kirjutab üle.

#### vars/main.yml

Rolli **sisemised** väärtused:

```yaml
---
nginx_package: "nginx"
nginx_service: "nginx"
nginx_config_path: "/etc/nginx"
nginx_user: "www-data"
```

!!! warning "Miks vars"
    Need on süsteemi-spetsiifilised väärtused. Kasutaja ei tohiks neid muuta, muidu roll läheb katki.

### Samm 6: Uuenda Template

Ava `roles/nginx/templates/nginx.conf.j2`:

```nginx
user {{ nginx_user }};
worker_processes {{ nginx_workers }};
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    gzip on;
    
    server {
        listen {{ nginx_port }};
        server_name {{ nginx_hostname }};
        root /var/www/html;
        index index.html;
        
        location / {
            try_files $uri $uri/ =404;
        }
    }
}
```

### Samm 7: Uued Playbook'id

#### dev.yml

```yaml
---
- name: Development Environment
  hosts: dev_servers
  become: yes
  
  roles:
    - role: nginx
      vars:
        nginx_workers: 1
        nginx_hostname: "dev.local"
        nginx_environment: "development"
        site_title: "Development Environment"
        site_color: "#FFA500"
```

#### prod.yml

```yaml
---
- name: Production Environment
  hosts: prod_servers
  become: yes
  
  roles:
    - role: nginx
      vars:
        nginx_workers: 4
        nginx_hostname: "prod.local"
        nginx_environment: "production"
        site_title: "Production Environment"
        site_color: "#00AA00"
```

!!! success "Vaata erinevust"
    **Enne:** 2 × 50 rida = 100 rida duplikatsiooni  
    **Pärast:** 2 × 12 rida = 24 rida, jagavad sama rolli

### Test

```bash
# Esmalt puhasta vanad paigaldused
vagrant destroy -f
vagrant up

# Käivita uued playbook'id
ansible-playbook -i inventory dev.yml
ansible-playbook -i inventory prod.yml
```

### Kontrolli

- Development: `http://localhost:8080`
- Production: `http://localhost:8081`

**Kontrollpunkt:**

- [ ] Mõlemad töötavad
- [ ] Näitavad erinevaid seadeid
- [ ] Playbook'id on lühikesed

---

## 6. Vaata Erinevust

**Nüüd simuleerime sama viga uuesti:**

Oletame jälle: nginx paketi nimi peab olema `nginx-full`

**Ülesanne:** Paranda.

```yaml
# Muuda AINULT roles/nginx/vars/main.yml:
nginx_package: "nginx-full"  # ÜKS muudatus!
```

```bash
# Mõlemad keskkonnad saavad paranduse:
ansible-playbook -i inventory dev.yml
ansible-playbook -i inventory prod.yml
```

Vaata - üks muudatus, mõlemad keskkonnad saavad paranduse automaatselt.

### Lisame Kolmanda Keskkonna

Kui tahad staging keskkonda:

```yaml
# staging.yml
---
- name: Staging Environment
  hosts: staging_servers
  become: yes
  
  roles:
    - role: nginx
      vars:
        nginx_workers: 2
        nginx_environment: "staging"
        site_title: "Staging Environment"
        site_color: "#FFFF00"
```

!!! tip "Skaleeruvus"
    12 rida, sama roll. Ei kopeeri ühtegi task'i.

---

## 7. defaults/ vs vars/ Selgitus

**Küsimus:** Miks mõned muutujad on `defaults/` ja teised `vars/`?

### defaults/main.yml

**Kasutaja TOHIB muuta playbook'is:**

```yaml
nginx_workers: 2        # Dev: 1, Prod: 4
site_title: "My Site"   # Iga keskkond erinev
site_color: "#CCC"      # Iga keskkond erinev
```

**Prioriteet:** Madalaim (playbook vars kirjutab üle)

### vars/main.yml

**Rolli SISEMISED väärtused, kasutaja EI TOHIKS muuta:**

```yaml
nginx_package: "nginx"     # OS-spetsiifiline
nginx_service: "nginx"     # Süsteemi nimi
nginx_user: "www-data"     # Ubuntu standard
```

**Prioriteet:** Kõrgem kui defaults/

!!! info "Otsustamise reegel"
    - Keskkonnas erinev → `defaults/`
    - Süsteemi-spetsiifiline → `vars/`

---

## 8. Meta ja Dokumentatsioon

### meta/main.yml

```yaml
---
galaxy_info:
  role_name: nginx
  author: "Sinu Nimi"
  description: "Nginx web server for multiple environments"
  company: "IT College"
  license: MIT
  min_ansible_version: "2.9"
  
  platforms:
    - name: Ubuntu
      versions:
        - focal
  
  galaxy_tags:
    - web
    - nginx
    - multienv

dependencies: []
```

### README.md

Loo fail `roles/nginx/README.md`:

```markdown
# Ansible Role: Nginx

Paigaldab Nginx web serveri. Toetab mitut keskkonda (dev, staging, prod).

## Muutujad

Kohustuslikud (määra playbook'is):
- nginx_environment: "production"
- site_title: "My Site"
- site_color: "#00AA00"

Valikulised:
- nginx_workers: 2 (default: CPU arv)
- nginx_port: 80
- nginx_hostname: "localhost"

## Näide

Development:
- role: nginx
  vars:
    nginx_environment: "development"
    nginx_workers: 1

Production:
- role: nginx
  vars:
    nginx_environment: "production"
    nginx_workers: 4

## Test

ansible-playbook -i inventory dev.yml
ansible-playbook -i inventory prod.yml

## Author

Pushkin
```

---
## 9. GitHub Avaldamine

```bash
cd roles/nginx

git init
git add .
git commit -m "Multi-environment nginx role"

git remote add origin https://github.com/USERNAME/ansible-role-nginx.git
git branch -M main
git push -u origin main

git tag v1.0.0
git push origin v1.0.0
```

!!! success "Valmis"
    Nüüd saame kasutada:
    
    ```bash
    ansible-galaxy install git+https://github.com/USERNAME/ansible-role-nginx.git
    ```

---

## 10. Lõplik Test

### Test 1: Idempotentsus

```bash
ansible-playbook -i inventory dev.yml
ansible-playbook -i inventory dev.yml
# Teine käivitus: changed=0

ansible-playbook -i inventory prod.yml
ansible-playbook -i inventory prod.yml
# Teine käivitus: changed=0
```

### Test 2: Keskkonnad Erinevad

```bash
# Development
curl http://localhost:8080 | grep "Development"
curl http://localhost:8080 | grep "Workers: 1"

# Production
curl http://localhost:8081 | grep "Production"
curl http://localhost:8081 | grep "Workers: 4"
```

### Test 3: Üks Muudatus, Kõik Keskkonnad

Muuda `roles/nginx/defaults/main.yml`:

```yaml
site_color: "#0000FF"  # Muudame default värvi
```

```bash
ansible-playbook -i inventory dev.yml
ansible-playbook -i inventory prod.yml
```

Mõlemad saavad uue default värvi (kui playbook ei kirjuta üle).

---

## Kokkuvõte

**Mida tegime:**

1. Lõime 2 keskkonda ilma rollideta
2. Nägime probleemi - duplikatsioon, hooldus raske
3. Refaktoreerisime üheks rolliks
4. Võrdlesime - üks muudatus vs mitu faili
5. Mõistsime defaults/ vs vars/ erinevust
6. Dokumenteerisime ja avaldasime

**Miks rollid:**

- **DRY** - Don't Repeat Yourself
- **Hooldatavus** - üks muudatus, kõik keskkonnad
- **Skaleeruvus** - uus keskkond = 12 rida, mitte 50
- **Jagamine** - Galaxy, kolleegid saavad kasutada

**Järgmised sammud:**

- Kodutöö: Võta oma projekt ja refaktoreeri rolliks
- Lisapraktika: Dependencies, molecule testing

Rollid lahendavad reaalse probleemi mida nägime täna - korduvkasutatavus ja hooldatavus.