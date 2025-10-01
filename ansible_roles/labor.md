# 🧪 Ansible Rollid Labor: Rolli Loomine

**Kestus:** 2 tundi  
**Eesmärk:** Luua professionaalne Nginx roll Ansible Galaxy standardite järgi

---

## 🎯 Õpiväljundid

Pärast laborit oskate:
- Luua Ansible rolli õiges struktuuris
- Kasutada rolli muutujaid ja sõltuvusi
- Testida rolli Vagrant keskkonnas
- Kasutada Ansible Galaxy rollide haldamist
- Rakendada rolli best practices'eid

---

## 📋 Ülevaade

**Loote:**
- Galaxy standard Nginx role
- Multi-OS tugi (Ubuntu/Debian)
- SSL sertifikaadid automaatselt
- Virtual hosts konfiguratsioon

**Role struktuuri põhimõte:** Ansible roles organiseerivad koodi modulaarselt. Iga komponent (tasks, templates, vars) on eraldatud, mis teeb koodi taaskasutatavaks ja hooldatavaks.

---

## Setup (30min)

### Role genereerimine
```bash
mkdir ~/ansible-roles-lab && cd ~/ansible-roles-lab
mkdir roles && cd roles
ansible-galaxy init nginx-webserver
tree nginx-webserver/
```

**Galaxy tool:** Genereerib standardse role struktuuri. Iga kaust omab spetsiifilist eesmärki - tasks (tegevused), templates (konfiguratsioonid), vars (muutujad).

### Metadata
**`meta/main.yml`:**
```yaml
---
galaxy_info:
  author: "ITS-24 Student"
  description: "Professional Nginx with SSL and virtual hosts"
  min_ansible_version: "2.9"
  platforms:
    - name: Ubuntu
      versions: [focal, jammy]
  galaxy_tags: [web, nginx, ssl]
dependencies: []
```

**Metadata tähtsus:** Defineerib role sõltuvused, toetatud platvormid ja versiooniinfo. Galaxy kasutab seda role jagamisel.

---

## Variables (25min)

### Defaults
**`defaults/main.yml`:**
```yaml
---
nginx_user: "www-data"
nginx_worker_processes: "{{ ansible_processor_vcpus | default(2) }}"
nginx_http_port: 80
nginx_https_port: 443
nginx_ssl_enabled: false
nginx_vhosts: []
nginx_remove_default_vhost: true
nginx_server_tokens: "off"
```

**Defaults vs vars:** Defaults on madalaima prioriteediga muutujad. Kasutaja saab neid kergesti üle kirjutada. Vars on kõrgema prioriteediga.

### System vars
**`vars/main.yml`:**
```yaml
---
_nginx_packages:
  Debian: [nginx, ssl-cert, curl]
  Ubuntu: [nginx, ssl-cert, curl]

nginx_packages: "{{ _nginx_packages[ansible_os_family] | default(_nginx_packages['Debian']) }}"
nginx_config_path: "/etc/nginx"
nginx_sites_available: "{{ nginx_config_path }}/sites-available"
nginx_service_name: "nginx"
```

**OS-specific variables:** Erinevad operatsioonisüsteemid vajavad erinevaid pakette. Sõnastikud võimaldavad dynaamiliset valikut.

---

## Tasks struktuuri (20min)

### Main tasks
**`tasks/main.yml`:**
```yaml
---
- name: "Validate configuration"
  include_tasks: validate.yml

- name: "Install Nginx"
  include_tasks: install.yml

- name: "Configure Nginx" 
  include_tasks: configure.yml

- name: "Setup SSL"
  include_tasks: ssl.yml
  when: nginx_ssl_enabled

- name: "Setup virtual hosts"
  include_tasks: vhosts.yml

- name: "Start service"
  include_tasks: service.yml
```

**Modulaarne struktuur:** Igal alamülesandel on oma fail. See teeb koodi loetavaks ja debug'imist lihtsamaks.

### Validation
**`tasks/validate.yml`:**
```yaml
---
- name: "Validate HTTP port"
  assert:
    that:
      - nginx_http_port is number
      - nginx_http_port > 0
      - nginx_http_port < 65536
    fail_msg: "nginx_http_port must be valid port (1-65535)"

- name: "Check minimum RAM"
  assert:
    that:
      - ansible_memtotal_mb >= 256
    fail_msg: "Need at least 256MB RAM for nginx"
```

**Input validation:** Kontrollib kasutaja sisendeid enne rakendamist. Ennetab konfiguratsioonivigu ja süsteemitõrkeid.

---

## SSL ja Virtual Hosts (25min)

### SSL tasks
**`tasks/ssl.yml`:**
```yaml
---
- name: "Create SSL directories"
  file:
    path: "{{ item }}"
    state: directory
    mode: '0755'
  loop:
    - "/etc/ssl/certs"
    - "/etc/ssl/private"

- name: "Generate self-signed SSL certificate"
  command: >
    openssl req -new -x509 -days 365 -nodes
    -out {{ nginx_ssl_cert_path }}
    -keyout {{ nginx_ssl_key_path }}
    -subj "/C=EE/ST=Harju/L=Tallinn/O=ITS-24/CN={{ ansible_fqdn }}"
  args:
    creates: "{{ nginx_ssl_cert_path }}"

- name: "Set SSL private key permissions"
  file:
    path: "{{ nginx_ssl_key_path }}"
    mode: '0600'
```

**SSL sertifikaadid:** Ise-allkirjastatud sertifikaadid testiks. Produktsioonis kasutaksite CA sertifikaate. `creates` parameter tagab idempotentsuse.

### Virtual hosts
**`tasks/vhosts.yml`:**
```yaml
---
- name: "Configure virtual hosts"
  template:
    src: vhost.conf.j2
    dest: "{{ nginx_sites_available }}/{{ item.name }}.conf"
  loop: "{{ nginx_vhosts }}"
  notify: reload nginx

- name: "Enable virtual hosts"
  file:
    src: "{{ nginx_sites_available }}/{{ item.name }}.conf"
    dest: "{{ nginx_sites_enabled }}/{{ item.name }}.conf"
    state: link
  loop: "{{ nginx_vhosts }}"

- name: "Create document roots"
  file:
    path: "{{ item.root | default('/var/www/' + item.name) }}"
    state: directory
    owner: "{{ nginx_user }}"
  loop: "{{ nginx_vhosts }}"
```

**Sites-available/enabled pattern:** Debian/Ubuntu standard. Konfiguratsioonid salvestatakse sites-available'sse, sites-enabled sisaldab symlinke aktiivsete saitide jaoks.

---

## Templates (25min)

### Nginx main config
**`templates/nginx.conf.j2`:**
```nginx
# {{ ansible_managed }}
user {{ nginx_user }};
worker_processes {{ nginx_worker_processes }};

events {
    worker_connections {{ nginx_worker_connections }};
    use epoll;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    server_tokens {{ nginx_server_tokens }};

    include /etc/nginx/mime.types;
    
{% if nginx_gzip_enabled %}
    gzip on;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json;
{% endif %}

{% if nginx_ssl_enabled %}
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
{% endif %}

    include {{ nginx_sites_enabled }}/*;
}
```

**Jinja2 templating:** Võimaldab dünaamilisi konfiguratsioone. Conditional blocks (`{% if %}`) ja muutujad (`{{ }}`) teevad template'i kohandatavaks.

### Virtual host template
**`templates/vhost.conf.j2`:**
```nginx
{% if item.ssl | default(nginx_ssl_enabled) %}
server {
    listen {{ nginx_https_port }} ssl http2;
    server_name {{ item.name }};
    
    ssl_certificate {{ nginx_ssl_cert_path }};
    ssl_certificate_key {{ nginx_ssl_key_path }};
    
    root {{ item.root | default('/var/www/' + item.name) }};
    index index.html;
}

server {
    listen {{ nginx_http_port }};
    server_name {{ item.name }};
    return 301 https://$server_name$request_uri;
}
{% else %}
server {
    listen {{ nginx_http_port }};
    server_name {{ item.name }};
    root {{ item.root | default('/var/www/' + item.name) }};
    index index.html;
}
{% endif %}
```

**Conditional SSL:** Template kohandub automaatselt SSL seadistuse järgi. HTTP redirect HTTPS'ile kui SSL on lubatud.

---

## Testimine (15min)

### Test playbook
**`test-nginx.yml`:**
```yaml
---
- name: "Test nginx role"
  hosts: localhost
  connection: local
  become: yes
  
  vars:
    nginx_ssl_enabled: true
    nginx_vhosts:
      - name: "test.local"
        ssl: true
      - name: "demo.local" 
        ssl: false
  
  roles:
    - nginx-webserver
```

### Käivitamine ja kontrollimine
```bash
ansible-playbook test-nginx.yml

# Testimine
curl http://localhost          # peaks redirect'ima HTTPS'ile
curl -k https://localhost      # SSL test
sudo systemctl status nginx   # teenuse olek
```

**Testing strategy:** Alati testida nii HTTP kui HTTPS ühendusi. Kontrollida teenuse olekut ja logisid veakindluse tagamiseks.

---

## Handlers ja dokumentatsioon

### Handlers
**`handlers/main.yml`:**
```yaml
---
- name: reload nginx
  service:
    name: "{{ nginx_service_name }}"
    state: reloaded

- name: restart nginx
  service:
    name: "{{ nginx_service_name }}"
    state: restarted
```

**Handlers:** Käivitatakse ainult muudatuste korral. `notify` direktiiv tasks'ides käivitab handler'eid konfiguratsiooni muutmisel.

### README dokumentatsioon
```markdown
# Nginx Webserver Role

Professional Nginx role with SSL and virtual hosts.

## Quick Start
```yaml
- hosts: webservers
  roles:
    - nginx-webserver
```

## Variables
- `nginx_ssl_enabled: false` - Enable SSL
- `nginx_vhosts: []` - Virtual hosts list
```

**Dokumentatsiooni tähtsus:** Selgitab role kasutamist, muutujaid ja näiteid. Hea dokumentatsioon teeb role'i kasutatavaks teiste poolt.

Role on nüüd valmis professionaalseks kasutamiseks!
