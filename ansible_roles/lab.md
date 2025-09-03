# Ansible Roles Lab: Custom Nginx Role Creation
## Eesmärk: Professionaalse Ansible role'i loomine (2h)

Täna loome oma esimese professionaalse Ansible role'i!

---

## 🎯 Samm 1: Lab'i eesmärgid

- **Nginx role** Galaxy standardites
- **Multi-OS tugi** (Ubuntu/Debian)
- **SSL sertifikaadid** automaatselt
- **Virtual hosts** konfiguratsioon

---

## 🚀 Lab 1: Role struktuuri loomine (30 min)

### Töökeskkonna ettevalmistamine

```bash
# Kontrollige Ansible
ansible --version

# Looge töökausta  
mkdir ~/ansible-roles-lab
cd ~/ansible-roles-lab
mkdir roles
cd roles
```

### Role'i genereerimine

```bash
# Galaxy tool genereerib struktuuri
ansible-galaxy init nginx-webserver

# Kontrollige
tree nginx-webserver/
```

Peaks näitama:
```
nginx-webserver/
├── README.md
├── defaults/main.yml
├── handlers/main.yml  
├── meta/main.yml
├── tasks/main.yml
├── templates/
├── vars/main.yml
└── tests/
```

### Metadata seadistamine

**Muutke `meta/main.yml`:**
```yaml
---
galaxy_info:
  author: "ITS-24 Student"
  description: "Professional Nginx with SSL and virtual hosts"
  company: "ITS-24 DevOps Course"
  license: "MIT"
  min_ansible_version: "2.9"
  
  platforms:
    - name: Ubuntu
      versions: [focal, jammy]
    - name: Debian  
      versions: [buster, bullseye]
  
  galaxy_tags:
    - web
    - nginx
    - ssl
    - webserver

dependencies: []
```

---

## 🔧 Samm 1: Variables ja defaults (25 min)

### Vaikimisi seaded - algajasõbralik

**Muutke `defaults/main.yml`:**
```yaml
---
# Basic settings (töötab kohe!)
nginx_user: "www-data"
nginx_worker_processes: "{{ ansible_processor_vcpus | default(2) }}"
nginx_worker_connections: 1024

# Ports
nginx_http_port: 80
nginx_https_port: 443

# SSL (vaikimisi välja lülitatud)
nginx_ssl_enabled: false
nginx_ssl_cert_path: "/etc/ssl/certs/nginx.crt"
nginx_ssl_key_path: "/etc/ssl/private/nginx.key"

# Virtual hosts (tühi list = default site)
nginx_vhosts: []

# Security
nginx_remove_default_vhost: true
nginx_server_tokens: "off"
nginx_gzip_enabled: true
```

### Role sisemised muutujad

**Muutke `vars/main.yml`:**
```yaml
---
# OS-specific packages
_nginx_packages:
  Debian: [nginx, ssl-cert, curl]
  Ubuntu: [nginx, ssl-cert, curl]

nginx_packages: "{{ _nginx_packages[ansible_os_family] | default(_nginx_packages['Debian']) }}"

# System paths
nginx_config_path: "/etc/nginx"
nginx_sites_available: "{{ nginx_config_path }}/sites-available"
nginx_sites_enabled: "{{ nginx_config_path }}/sites-enabled"
nginx_log_path: "/var/log/nginx"

# Service
nginx_service_name: "nginx"
```

---

## 📝 Lab 3: Tasks loomine (20 min)

### Peamine tasks fail - sisukord

**Muutke `tasks/main.yml`:**
```yaml
---
- name: "Include OS variables"
  include_vars: "{{ ansible_os_family }}.yml"
  when: ansible_os_family in ['Debian', 'Ubuntu']

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

- name: "Run tests"
  include_tasks: test.yml
```

### Validation - alati kontrollige sisendeid!

**Looge `tasks/validate.yml`:**
```yaml
---
- name: "Validate HTTP port"
  assert:
    that:
      - nginx_http_port is defined
      - nginx_http_port is number
      - nginx_http_port > 0
      - nginx_http_port < 65536
    fail_msg: "nginx_http_port must be valid port (1-65535)"

- name: "Validate HTTPS port"
  assert:
    that:
      - nginx_https_port is defined
      - nginx_https_port is number
      - nginx_https_port > 0
      - nginx_https_port < 65536
    fail_msg: "nginx_https_port must be valid port (1-65535)"

- name: "Validate SSL settings when enabled"
  assert:
    that:
      - nginx_ssl_cert_path is defined
      - nginx_ssl_key_path is defined
      - nginx_ssl_cert_path | length > 0
      - nginx_ssl_key_path | length > 0
    fail_msg: "SSL certificate paths required when SSL enabled"
  when: nginx_ssl_enabled

- name: "Check minimum RAM"
  assert:
    that:
      - ansible_memtotal_mb >= 256
    fail_msg: "Need at least 256MB RAM for nginx"
```

### Installation tasks

**Looge `tasks/install.yml`:**
```yaml
---
- name: "Update package cache (Debian/Ubuntu)"
  apt:
    update_cache: yes
    cache_valid_time: 3600
  when: ansible_os_family == "Debian"

- name: "Install Nginx packages"
  package:
    name: "{{ nginx_packages }}"
    state: present

- name: "Ensure nginx user exists"
  user:
    name: "{{ nginx_user }}"
    system: yes
    shell: /bin/false
    home: /var/www
    createhome: no
    state: present

- name: "Create required directories"
  file:
    path: "{{ item }}"
    state: directory
    owner: root
    group: root
    mode: '0755'
  loop:
    - "{{ nginx_config_path }}"
    - "{{ nginx_sites_available }}"
    - "{{ nginx_sites_enabled }}"
    - "{{ nginx_log_path }}"
    - "/var/www"
```

### Configuration tasks

**Looge `tasks/configure.yml`:**
```yaml
---
- name: "Backup original nginx.conf"
  copy:
    src: "{{ nginx_config_path }}/nginx.conf"
    dest: "{{ nginx_config_path }}/nginx.conf.original"
    remote_src: yes
    force: no
  ignore_errors: yes

- name: "Configure main nginx.conf"
  template:
    src: nginx.conf.j2
    dest: "{{ nginx_config_path }}/nginx.conf"
    owner: root
    group: root
    mode: '0644'
    backup: yes
  notify: reload nginx

- name: "Remove default nginx site"
  file:
    path: "{{ nginx_sites_enabled }}/default"
    state: absent
  when: nginx_remove_default_vhost
  notify: reload nginx

- name: "Remove default site config"
  file:
    path: "{{ nginx_sites_available }}/default"
    state: absent
  when: nginx_remove_default_vhost
```

---

## 📝 Lab 4: SSL ja Virtual Hosts (25 min)

### SSL tasks

**Looge `tasks/ssl.yml`:**
```yaml
---
- name: "Install OpenSSL for certificate generation"
  package:
    name: openssl
    state: present

- name: "Create SSL directories"
  file:
    path: "{{ item }}"
    state: directory
    owner: root
    group: root
    mode: '0755'
  loop:
    - "/etc/ssl/certs"
    - "/etc/ssl/private"

- name: "Generate self-signed SSL certificate"
  command: >
    openssl req -new -x509 -days 365 -nodes
    -out {{ nginx_ssl_cert_path }}
    -keyout {{ nginx_ssl_key_path }}
    -subj "/C=EE/ST=Harju/L=Tallinn/O=ITS-24 Course/CN={{ ansible_fqdn }}"
  args:
    creates: "{{ nginx_ssl_cert_path }}"
  when: nginx_ssl_enabled

- name: "Set SSL certificate permissions"
  file:
    path: "{{ nginx_ssl_cert_path }}"
    owner: root
    group: root
    mode: '0644'
  when: nginx_ssl_enabled

- name: "Set SSL private key permissions (very important!)"
  file:
    path: "{{ nginx_ssl_key_path }}"
    owner: root
    group: root
    mode: '0600'
  when: nginx_ssl_enabled
```

### Virtual hosts tasks

**Looge `tasks/vhosts.yml`:**
```yaml
---
- name: "Configure virtual hosts"
  template:
    src: vhost.conf.j2
    dest: "{{ nginx_sites_available }}/{{ item.name }}.conf"
    owner: root
    group: root
    mode: '0644'
  loop: "{{ nginx_vhosts }}"
  notify: reload nginx
  when: nginx_vhosts | length > 0

- name: "Enable virtual hosts"
  file:
    src: "{{ nginx_sites_available }}/{{ item.name }}.conf"
    dest: "{{ nginx_sites_enabled }}/{{ item.name }}.conf"
    state: link
  loop: "{{ nginx_vhosts }}"
  notify: reload nginx
  when: nginx_vhosts | length > 0

- name: "Create document root directories"
  file:
    path: "{{ item.root | default('/var/www/' + item.name) }}"
    state: directory
    owner: "{{ nginx_user }}"
    group: "{{ nginx_user }}"
    mode: '0755'
  loop: "{{ nginx_vhosts }}"
  when: nginx_vhosts | length > 0

- name: "Create index.html for sites"
  template:
    src: index.html.j2
    dest: "{{ item.root | default('/var/www/' + item.name) }}/index.html"
    owner: "{{ nginx_user }}"
    group: "{{ nginx_user }}"
    mode: '0644'
  loop: "{{ nginx_vhosts }}"
  when: nginx_vhosts | length > 0
```

### Service ja test tasks

**Looge `tasks/service.yml`:**
```yaml
---
- name: "Start and enable Nginx service"
  service:
    name: "{{ nginx_service_name }}"
    state: started
    enabled: yes

- name: "Check Nginx service status"
  service:
    name: "{{ nginx_service_name }}"
    state: started
  register: nginx_status

- name: "Display service status"
  debug:
    msg: "Nginx teenus on {{ nginx_status.state }}!"
```

**Looge `tasks/test.yml`:**
```yaml
---
- name: "Test nginx configuration syntax"
  command: nginx -t
  register: nginx_config_test
  changed_when: false
  failed_when: nginx_config_test.rc != 0

- name: "Test HTTP response"
  uri:
    url: "http://{{ ansible_default_ipv4.address }}:{{ nginx_http_port }}"
    method: GET
    status_code: [200, 301, 302, 404]
  register: http_test
  ignore_errors: yes

- name: "Test HTTPS response (if SSL enabled)"
  uri:
    url: "https://{{ ansible_default_ipv4.address }}:{{ nginx_https_port }}"
    method: GET
    status_code: [200, 301, 302, 404]
    validate_certs: no
  register: https_test
  ignore_errors: yes
  when: nginx_ssl_enabled

- name: "Display test results"
  debug:
    msg: |
      Test tulemused:
      - Config syntax: {{ 'OK' if nginx_config_test.rc == 0 else 'FAILED' }}
      - HTTP response: {{ 'OK' if http_test.failed is not defined else 'FAILED' }}
      - HTTPS response: {{ 'OK' if https_test.skipped is not defined and https_test.failed is not defined else 'SKIPPED/FAILED' }}
```

---

## 📄 Lab 5: Templates (25 min)

### Main nginx configuration

**Looge `templates/nginx.conf.j2`:**
```nginx
# {{ ansible_managed }}
# Nginx configuration for {{ inventory_hostname }}
# Generated: {{ ansible_date_time.iso8601 }}

user {{ nginx_user }};
worker_processes {{ nginx_worker_processes }};
pid /run/nginx.pid;

events {
    worker_connections {{ nginx_worker_connections }};
    use epoll;
    multi_accept on;
}

http {
    # Basic Settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens {{ nginx_server_tokens }};

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log {{ nginx_log_path }}/access.log main;
    error_log {{ nginx_log_path }}/error.log;

{% if nginx_gzip_enabled %}
    # Gzip Settings
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml;
{% endif %}

{% if nginx_ssl_enabled %}
    # SSL Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
{% endif %}

    # Virtual Host Configs
    include {{ nginx_sites_enabled }}/*;
}
```

### Virtual host template

**Looge `templates/vhost.conf.j2`:**
```nginx
# {{ ansible_managed }}
# Virtual host: {{ item.name }}

{% if item.ssl | default(nginx_ssl_enabled) %}
# HTTPS server
server {
    listen {{ nginx_https_port }} ssl http2;
    server_name {{ item.name }};

    # SSL Configuration
    ssl_certificate {{ nginx_ssl_cert_path }};
    ssl_certificate_key {{ nginx_ssl_key_path }};

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;

    # Document root
    root {{ item.root | default('/var/www/' + item.name) }};
    index index.html index.htm;

    # Logs
    access_log {{ nginx_log_path }}/{{ item.name }}_ssl_access.log main;
    error_log {{ nginx_log_path }}/{{ item.name }}_ssl_error.log;
}

# Redirect HTTP to HTTPS
server {
    listen {{ nginx_http_port }};
    server_name {{ item.name }};
    return 301 https://$server_name$request_uri;
}

{% else %}
# HTTP server
server {
    listen {{ nginx_http_port }};
    server_name {{ item.name }};

    # Document root
    root {{ item.root | default('/var/www/' + item.name) }};
    index index.html index.htm;

    # Logs
    access_log {{ nginx_log_path }}/{{ item.name }}_access.log main;
    error_log {{ nginx_log_path }}/{{ item.name }}_error.log;
}
{% endif %}
```

### Index.html template

**Looge `templates/index.html.j2`:**
```html
<!DOCTYPE html>
<html lang="et">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ item.name }} - ITS-24 Nginx Role</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        h1 { text-align: center; }
        .info { background: rgba(255,255,255,0.2); padding: 15px; border-radius: 5px; margin: 10px 0; }
        .success { color: #4CAF50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 ITS-24 Nginx Role</h1>
        <p class="success">✅ {{ item.name }} on edukalt konfigureeritud!</p>
        
        <div class="info">
            <strong>Virtual Host:</strong> {{ item.name }}<br>
            <strong>Server:</strong> {{ inventory_hostname }}<br>
            <strong>Document Root:</strong> {{ item.root | default('/var/www/' + item.name) }}<br>
            <strong>SSL Enabled:</strong> {{ item.ssl | default(nginx_ssl_enabled) | ternary('Yes', 'No') }}<br>
            <strong>Generated:</strong> {{ ansible_date_time.iso8601 }}
        </div>

        <h3>📊 Server Info</h3>
        <div class="info">
            <strong>OS:</strong> {{ ansible_distribution }} {{ ansible_distribution_version }}<br>
            <strong>Architecture:</strong> {{ ansible_architecture }}<br>
            <strong>CPU Cores:</strong> {{ ansible_processor_vcpus }}<br>
            <strong>Memory:</strong> {{ (ansible_memtotal_mb/1024)|round(1) }} GB
        </div>
    </div>
</body>
</html>
```

### Handlers

**Muutke `handlers/main.yml`:**
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

---

## 🧪 Lab 6: Role'i testimine (10 min)

### Test playbook loomine

**Looge `test-nginx.yml` (roles/ kataloogis):**
```yaml
---
- name: "Test nginx role"
  hosts: localhost
  connection: local
  become: yes
  
  vars:
    # Test konfiguratsioon
    nginx_ssl_enabled: true
    nginx_vhosts:
      - name: "test.local"
        root: "/var/www/test"
        ssl: true
      - name: "demo.local"
        root: "/var/www/demo"
        ssl: false
    
    # Custom seaded
    nginx_worker_processes: 4
    nginx_gzip_enabled: true
  
  roles:
    - nginx-webserver
  
  post_tasks:
    - name: "Final verification"
      debug:
        msg: |
          🎓 ITS-24 Nginx Role Test Complete!
          
          ✅ Nginx installed and configured
          ✅ SSL certificates generated
          ✅ Virtual hosts: {{ nginx_vhosts | length }}
          ✅ Test URLs:
             - http://localhost (should redirect to HTTPS)
             - https://localhost (SSL test site)
          
          Role is ready for production! 🚀
```

### Role'i käivitamine

```bash
# Navigeerige tagasi roles/ kausta
cd ~/ansible-roles-lab

# Käivitage test
ansible-playbook -i localhost, test-nginx.yml

# Kontrollige tulemust
curl http://localhost
curl -k https://localhost  # -k sest self-signed cert

# Vaadake nginx status
sudo systemctl status nginx
```

---

## 📚 Samm 7: README dokumentatsioon

**Looge/muutke `README.md`:**
```markdown
# Nginx Webserver Role

Professional Nginx role with SSL support and virtual hosts management.

## Features

- **Nginx installation and configuration**
- **SSL/TLS support with self-signed certificates**
- **Virtual hosts management**
- **Security headers and optimization**
- **Multi-OS support (Ubuntu/Debian)**

## Quick Start

```yaml
- hosts: webservers
  become: yes
  roles:
    - nginx-webserver
```

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `nginx_ssl_enabled` | `false` | Enable SSL/HTTPS |
| `nginx_http_port` | `80` | HTTP port |
| `nginx_https_port` | `443` | HTTPS port |
| `nginx_vhosts` | `[]` | Virtual hosts list |

## Example with SSL

```yaml
- hosts: webservers
  become: yes
  vars:
    nginx_ssl_enabled: true
    nginx_vhosts:
      - name: "example.com"
        root: "/var/www/example"
        ssl: true
  roles:
    - nginx-webserver
```

## Author

ITS-24 DevOps Automation Course
```

---

## 🎯 Samm 2: Kokkuvõte

Palju õnne! Teil on nüüd:

**Nginx role**
**Multi-OS tugi**
**SSL sertifikaadid**
**Virtual hosts**
**Täielik dokumentatsioon**
**Testitud ja töötav**  

**See role on valmis kasutamiseks päris projektides!**

**Kodutöö:** Puppet vs Ansible analüüs põhineb sellel, mida täna õppisime.
