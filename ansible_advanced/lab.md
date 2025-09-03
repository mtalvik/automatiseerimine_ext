# 🧪 Ansible Advanced Lab: Template-based Configuration

**Kestus:** 2 tundi  
**Eesmärk:** Õppida Ansible'i täpsemaid funktsioone ja luua dünaamilisi konfiguratsioone

## 🎯 Samm 1: Õpiväljundid

Pärast laborit oskate:
- Dünaamilised konfiguratsioonid Jinja2 template'itega
- Muutujate hierarhia mõistmine ja kasutamine
- Handler'ite kasutamise oskus
- Ansible Vault krüpteerimise oskus
- Töökorras LAMP stack vault'iga

---

## 📋 Samm 1: Advanced Variables Setup (30 min)

### 1.1: Projekti struktuuri loomine - Organiseeritud struktuur

**Miks struktureeritud projekt:**
- Suuremad projektid vajavad selget organisatsiooni
- Erinevad keskkonnad (dev, staging, prod) vajavad erinevaid seadistusi
- Team collaboration on lihtsam struktuuriga

**Loome professionaalse struktuuri sammhaaval:**

1. **Looge peakaust:**
   ```bash
   mkdir -p ~/ansible-advanced
   cd ~/ansible-advanced
   ```

2. **Looge kõik vajalikud kaustad:**
   ```bash
   # Põhistruktuur
   mkdir -p {inventory,group_vars,host_vars,roles,playbooks,templates,files}
   
   # Group variables struktuuri
   mkdir -p group_vars/{all,webservers,dbservers}
   
   # Host-spetsiifilised muutujad
   mkdir -p host_vars/{web1,web2,db1}
   ```

3. **Kontrollige struktuuri:**
   ```bash
   tree .  # või ls -la kui tree ei ole installitud
   ```

**Peaks näitama:**
```
.
├── files/
├── group_vars/
│   ├── all/
│   ├── dbservers/
│   └── webservers/
├── host_vars/
│   ├── db1/
│   ├── web1/
│   └── web2/
├── inventory/
├── playbooks/
├── roles/
└── templates/
```

### 1.2: Inventory seadistamine - Serverite hierarhia

**Mõistame inventory struktuuri:**
- **Groups** - serverite grupid (webservers, dbservers)
- **Children** - gruppide hierarhia
- **Vars** - grupi-spetsiifilised muutujad

**Loome inventory faili sammhaaval:**

1. **Looge põhi inventory fail:**
   ```bash
   touch inventory/hosts.yml
   nano inventory/hosts.yml
   ```

2. **Lisage server gruppid:**
   ```yaml
   all:
     children:
       webservers:
         hosts:
           web1:
             ansible_host: localhost
             ansible_connection: local
             server_id: 1
             server_role: primary
           web2:
             ansible_host: localhost
             ansible_connection: local
             server_id: 2
             server_role: secondary
   ```

3. **Lisage group variables:**
   ```yaml
         vars:
           http_port: 80
           https_port: 443
           web_root: "/var/www/html"
   ```

4. **Lisage database serverid:**
   ```yaml
       dbservers:
         hosts:
           db1:
             ansible_host: localhost
             ansible_connection: local
             mysql_server_id: 1
             mysql_role: master
         vars:
           mysql_port: 3306
           mysql_data_dir: "/var/lib/mysql"
   ```

5. **Lisage keskkonna grupid:**
   ```yaml
       development:
         children:
           webservers:
           dbservers:
         vars:
           app_env: "development"
           debug_mode: true
           ssl_enabled: false
           
       production:
         children:
           webservers:
           dbservers:
         vars:
           app_env: "production"
           debug_mode: false
           ssl_enabled: true
   ```

**❓ Mõelge:** Miks on kasulik grupeerida servereid nii rolli kui keskkonna järgi?

### Samm 3: Variables hierarchy loomine

**Loome muutujate hierarhia sammhaaval:**

1. **Globaalsed muutujad (group_vars/all/vars.yml):**
   ```bash
   touch group_vars/all/vars.yml
   nano group_vars/all/vars.yml
   ```
   
   ```yaml
   # Kõikidele serveritele ühised seadistused
   app_name: "advanced-lamp"
   app_version: "1.0.0"
   admin_email: "admin@company.com"
   
   # OS-spetsiifilised paketid (dünaamilised)
   apache_package: "{% if ansible_os_family == 'Debian' %}apache2{% else %}httpd{% endif %}"
   mysql_package: "{% if ansible_os_family == 'Debian' %}mysql-server{% else %}mariadb-server{% endif %}"
   
   # Keskkonna sõltuvad seadistused
   backup_enabled: "{{ app_env == 'production' }}"
   monitoring_enabled: "{{ app_env == 'production' }}"
   log_level: "{% if debug_mode %}DEBUG{% else %}INFO{% endif %}"
   ```

2. **Webserverite muutujad (group_vars/webservers/vars.yml):**
   ```bash
   touch group_vars/webservers/vars.yml
   nano group_vars/webservers/vars.yml
   ```
   
   ```yaml
   # Apache/Nginx seadistused
   max_workers: "{{ ansible_processor_vcpus * 2 }}"
   max_connections: 1000
   keepalive_timeout: 65
   
   # PHP seadistused
   php_version: "7.4"
   php_memory_limit: "{% if ansible_memtotal_mb > 4096 %}512M{% else %}256M{% endif %}"
   php_max_execution_time: 30
   
   # Virtual hosts
   virtual_hosts:
     - name: "{{ app_name }}.local"
       document_root: "{{ web_root }}/{{ app_name }}"
       ssl_enabled: "{{ ssl_enabled }}"
     - name: "api.{{ app_name }}.local"
       document_root: "{{ web_root }}/api"
       ssl_enabled: "{{ ssl_enabled }}"
   ```

3. **Database serverite muutujad (group_vars/dbservers/vars.yml):**
   ```bash
   touch group_vars/dbservers/vars.yml
   nano group_vars/dbservers/vars.yml
   ```
   
   ```yaml
   # MySQL konfigureerimine
   mysql_root_user: "root"
   mysql_bind_address: "127.0.0.1"
   mysql_max_connections: 100
   
   # Dünaamiline buffer pool arvutamine
   mysql_innodb_buffer_pool_size: "{{ (ansible_memtotal_mb * 0.7) | int }}M"
   
   # Andmebaasid
   mysql_databases:
     - name: "{{ app_name }}_{{ app_env }}"
       encoding: "utf8mb4"
       collation: "utf8mb4_unicode_ci"
   
   mysql_users:
     - name: "{{ app_name }}_user"
       host: "localhost"
       priv: "{{ app_name }}_{{ app_env }}.*:ALL"
       # Parool tuleb vault'ist
   ```

**💡 Märkused:**
- Kasutame Jinja2 loogikat dünaamilisteks väärtusteks
- Serverite võimsus mõjutab konfiguratsiooni
- Keskkond määrab turvalisuse taseme

---

## 📋 Samm 2: Jinja2 Template'ite loomine (45 min)

### 2.1: Apache virtual host template - Dünaamiline konfiguratsioon

**Miks template'id on olulised:**
- Üks template, mitu erinevat konfiguratsiooni
- Automaatne kohandamine serverite järgi
- Vähendab konfiguratsioonivigu

**Loome Apache virtual host template'i sammhaaval:**

1. **Looge template fail:**
   ```bash
   touch templates/apache_vhost.conf.j2
   nano templates/apache_vhost.conf.j2
   ```

2. **Alustage põhistruktuuriga:**
   ```apache
   # {{ ansible_managed }}
   # Virtual Host for {{ item.name }}
   # Generated on {{ ansible_date_time.iso8601 }}
   
   <VirtualHost *:{{ http_port }}>
       ServerName {{ item.name }}
       DocumentRoot {{ item.document_root }}
   ```

3. **Lisage conditionals:**
   ```apache
       # Logging configuration
       {% if debug_mode %}
       LogLevel debug
       {% else %}
       LogLevel warn
       {% endif %}
       
       ErrorLog ${APACHE_LOG_DIR}/{{ item.name }}_error.log
       CustomLog ${APACHE_LOG_DIR}/{{ item.name }}_access.log combined
   ```

4. **Lisage keskkonna-spetsiifilised seadistused:**
   ```apache
       <Directory {{ item.document_root }}>
           Options Indexes FollowSymLinks
           AllowOverride All
           Require all granted
           
           {% if app_env == 'production' %}
           # Production security headers
           Header always set X-Frame-Options DENY
           Header always set X-Content-Type-Options nosniff
           Header always set X-XSS-Protection "1; mode=block"
           {% endif %}
       </Directory>
   </VirtualHost>
   ```

5. **Lisage SSL support (conditional):**
   ```apache
   {% if item.ssl_enabled and ssl_enabled %}
   # SSL Virtual Host
   <VirtualHost *:{{ https_port }}>
       ServerName {{ item.name }}
       DocumentRoot {{ item.document_root }}
       
       # SSL Configuration
       SSLEngine on
       SSLProtocol TLSv1.2 TLSv1.3
       
       # SSL Certificates (will come from vault)
       SSLCertificateFile {{ ssl_cert_path | default('/etc/ssl/certs/server.crt') }}
       SSLCertificateKeyFile {{ ssl_key_path | default('/etc/ssl/private/server.key') }}
   </VirtualHost>
   {% endif %}
   ```

**🤔 Analüüs:** Kuidas template aitab hallata erinevaid keskkondi (dev vs prod)?

### 2.2: MySQL konfiguratsioon template

**Loome MySQL template'i sammhaaval:**

1. **Looge MySQL template:**
   ```bash
   touch templates/mysql.cnf.j2
   nano templates/mysql.cnf.j2
   ```

2. **Lisage dünaamiline konfiguratsioon:**
   ```ini
   # {{ ansible_managed }}
   # MySQL Configuration for {{ inventory_hostname }}
   # Environment: {{ app_env }}
   
   [mysqld]
   # Basic settings
   port = {{ mysql_port }}
   bind-address = {{ mysql_bind_address }}
   
   # Performance tuning based on available memory
   innodb_buffer_pool_size = {{ mysql_innodb_buffer_pool_size }}
   max_connections = {{ mysql_max_connections }}
   
   # Environment-specific settings
   {% if app_env == 'production' %}
   # Production optimizations
   innodb_flush_log_at_trx_commit = 1
   sync_binlog = 1
   {% else %}
   # Development settings (faster but less safe)
   innodb_flush_log_at_trx_commit = 2
   sync_binlog = 0
   {% endif %}
   
   # Logging
   {% if debug_mode %}
   general_log = 1
   general_log_file = /var/log/mysql/general.log
   slow_query_log = 1
   slow_query_log_file = /var/log/mysql/slow.log
   long_query_time = 1
   {% endif %}
   ```

### 2.3: PHP konfiguratsioon template

**Looge PHP-FPM template:**

1. **Looge PHP template:**
   ```bash
   touch templates/php-fpm.conf.j2
   nano templates/php-fpm.conf.j2
   ```

2. **Lisage dünaamilised seadistused:**
   ```ini
   # {{ ansible_managed }}
   # PHP-FPM pool configuration
   
   [{{ app_name }}]
   user = www-data
   group = www-data
   
   listen = /var/run/php/php{{ php_version }}-fpm-{{ app_name }}.sock
   listen.owner = www-data
   listen.group = www-data
   listen.mode = 0660
   
   # Process management
   pm = dynamic
   pm.max_children = {{ ansible_processor_vcpus * 4 }}
   pm.start_servers = {{ ansible_processor_vcpus }}
   pm.min_spare_servers = {{ ansible_processor_vcpus }}
   pm.max_spare_servers = {{ ansible_processor_vcpus * 2 }}
   
   # PHP settings
   php_admin_value[memory_limit] = {{ php_memory_limit }}
   php_admin_value[max_execution_time] = {{ php_max_execution_time }}
   php_admin_value[upload_max_filesize] = 32M
   php_admin_value[post_max_size] = 32M
   
   {% if app_env == 'development' %}
   # Development settings
   php_admin_flag[display_errors] = on
   php_admin_value[error_reporting] = E_ALL
   {% else %}
   # Production settings
   php_admin_flag[display_errors] = off
   php_admin_value[error_reporting] = E_ERROR
   {% endif %}
   ```

---

## 📋 Samm 3: Handlers ja Advanced Playbook (30 min)

### 3.1: Playbook handlers'itega

**Loome täiustatud playbook'i sammhaaval:**

1. **Looge põhi playbook:**
   ```bash
   touch playbooks/site.yml
   nano playbooks/site.yml
   ```

2. **Lisage playbook struktuur:**
   ```yaml
   ---
   - name: "LAMP Stack Deployment with Advanced Configuration"
     hosts: all
     become: yes
     gather_facts: yes
     
     tasks:
       - name: "Update package cache"
         package:
           update_cache: yes
         when: ansible_os_family == "Debian"
   ```

3. **Lisage Apache seadistamine handlers'itega:**
   ```yaml
       - name: "Install Apache"
         package:
           name: "{{ apache_package }}"
           state: present
         notify:
           - "start apache"
           - "enable apache"
   
       - name: "Create virtual host directories"
         file:
           path: "{{ item.document_root }}"
           state: directory
           owner: www-data
           group: www-data
           mode: '0755'
         loop: "{{ virtual_hosts }}"
         when: virtual_hosts is defined
   
       - name: "Generate virtual host configurations"
         template:
           src: apache_vhost.conf.j2
           dest: "/etc/apache2/sites-available/{{ item.name }}.conf"
           backup: yes
         loop: "{{ virtual_hosts }}"
         notify: "reload apache"
         when: virtual_hosts is defined
   
       - name: "Enable virtual hosts"
         command: "a2ensite {{ item.name }}"
         args:
           creates: "/etc/apache2/sites-enabled/{{ item.name }}.conf"
         loop: "{{ virtual_hosts }}"
         notify: "reload apache"
         when: virtual_hosts is defined
   ```

4. **Lisage handlers sektsioon:**
   ```yaml
     handlers:
       - name: "start apache"
         service:
           name: "{{ apache_package }}"
           state: started
   
       - name: "enable apache"
         service:
           name: "{{ apache_package }}"
           enabled: yes
   
       - name: "reload apache"
         service:
           name: "{{ apache_package }}"
           state: reloaded
   
       - name: "restart apache"
         service:
           name: "{{ apache_package }}"
           state: restarted
   ```

**💭 Mõelge:** Miks kasutame `reload` mitte `restart`? Mis vahe on?

### 3.2: Testimine

**Testida konfiguratsiooni:**

1. **Syntax check:**
   ```bash
   ansible-playbook --syntax-check playbooks/site.yml
   ```

2. **Kuiv käivitus:**
   ```bash
   ansible-playbook --check -i inventory/hosts.yml playbooks/site.yml
   ```

3. **Template'i testimine:**
   ```bash
   ansible-playbook -i inventory/hosts.yml playbooks/site.yml --tags "config" -v
   ```

---

## 📋 Samm 4: Ansible Vault rakendamine (35 min)

### 4.1: Vault failide loomine

**Loome turvalist vault struktuuri:**

1. **Looge vault fail group_vars jaoks:**
   ```bash
   ansible-vault create group_vars/all/vault.yml
   ```

2. **Lisage tundlikud andmed:**
   ```yaml
   # Database credentials
   vault_mysql_root_password: "SecureRootPassword123!"
   vault_mysql_app_password: "AppPassword456!"
   
   # SSL certificates paths
   vault_ssl_cert_path: "/etc/ssl/certs/company.crt"
   vault_ssl_key_path: "/etc/ssl/private/company.key"
   
   # API keys
   vault_backup_api_key: "backup_api_key_here"
   vault_monitoring_token: "monitoring_token_here"
   
   # Admin passwords
   vault_admin_password: "AdminSecurePass789!"
   ```

3. **Looge production-spetsiifiline vault:**
   ```bash
   ansible-vault create group_vars/production/vault.yml
   ```

   ```yaml
   # Production SSL certificates
   vault_ssl_cert_content: |
     -----BEGIN CERTIFICATE-----
     [certificate content here]
     -----END CERTIFICATE-----
   
   vault_ssl_key_content: |
     -----BEGIN PRIVATE KEY-----
     [private key content here]
     -----END PRIVATE KEY-----
   
   # Production database settings
   vault_production_db_host: "prod-db.company.com"
   vault_production_db_password: "ProdDbPass123!"
   ```

### 4.2: Vault muutujate kasutamine

**Ühendame vault muutujad tavaliste muutujatega:**

1. **Uuendage group_vars/all/vars.yml:**
   ```bash
   nano group_vars/all/vars.yml
   ```

   ```yaml
   # Lisage vault viited
   mysql_root_password: "{{ vault_mysql_root_password }}"
   mysql_app_password: "{{ vault_mysql_app_password }}"
   ssl_cert_path: "{{ vault_ssl_cert_path }}"
   ssl_key_path: "{{ vault_ssl_key_path }}"
   admin_password: "{{ vault_admin_password }}"
   ```

2. **Uuendage MySQL template'i:**
   ```bash
   nano templates/mysql.cnf.j2
   ```

   ```ini
   # Lisage vault-põhised seadistused
   {% if app_env == 'production' %}
   # Production SSL settings
   ssl-ca={{ vault_ssl_cert_path }}
   ssl-cert={{ vault_ssl_cert_path }}
   ssl-key={{ vault_ssl_key_path }}
   {% endif %}
   ```

### 4.3: Vault käsitsikasutatavus

**Vault operatsioonid:**

1. **Vaata vault faili:**
   ```bash
   ansible-vault view group_vars/all/vault.yml
   ```

2. **Muuda vault faili:**
   ```bash
   ansible-vault edit group_vars/production/vault.yml
   ```

3. **Käivita playbook vault'iga:**
   ```bash
   ansible-playbook -i inventory/hosts.yml playbooks/site.yml --ask-vault-pass
   ```

4. **Või kasuta vault password faili:**
   ```bash
   echo "your_vault_password" > .vault_pass
   chmod 600 .vault_pass
   ansible-playbook -i inventory/hosts.yml playbooks/site.yml --vault-password-file .vault_pass
   ```

**🔐 Turvalisus:** Ära iial commiti `.vault_pass` faili Git'i!

---

## 🎯 Samm 2: Labi kontrollnimekiri

Veenduge, et olete lõpetanud:

### Struktuur ja organisatsioon
- [ ] **Organiseeritud projektinstruktuur** - kaustad organiseeritud
- [ ] **Inventory hierarhia** - serverid grupeeritud ja konfigureeritud
- [ ] **Muutujate hierarhia** - group_vars ja host_vars seadistatud

### Template'id ja konfiguratsioon
- [ ] **Apache virtual host template** - dünaamiline ja keskkonna-põhine
- [ ] **MySQL konfiguratsioon template** - tulemuste optimeeritud
- [ ] **PHP-FPM template** - performance tuned

### Playbook'id ja handlers
- [ ] **Advanced playbook** - template'id, loops, conditionals
- [ ] **Proper handlers** - efficient service management
- [ ] **Error handling** - backup ja validation

### Vault ja turvalisus
- [ ] **Vault failid loodud** - tundlikud andmed krüpteeritud
- [ ] **Vault integratsioon** - muutujad ühendatud
- [ ] **Turvaline workflow** - .vault_pass ei commititå

### Testing ja validation
- [ ] **Syntax check** - playbook'id valid
- [ ] **Dry run** - --check mode töötab
- [ ] **Template testing** - konfiguratsioonid genereeruvad õigesti

## 🚀 Järgmised sammud

**Valmis kodutööks:**
- Kasutage siin õpitud advanced pattern'e
- Rakendage vault'i kõikides tootmise playbook'ides
- Organiseerige projektide struktuuri professionaalselt

**Järgmine nädal:**
- Ansible Roles ja Galaxy
- Automated testing strategies
- Enterprise deployment patterns

**Hästi tehtud! 🎉** Te oskate nüüd luua production-ready Ansible projekte!
