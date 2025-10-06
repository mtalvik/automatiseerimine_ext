#  Ansible: Edasijõudnud Funktsioonid

**Teemad:** Ansible Vault, Jinja2 templates, optimiseerimine, troubleshooting

---

## Sissejuhatus

Tere, täna räägime Ansible'i edasijõudnutest funktsioonidest. Eelmisel nädalal õppisime Ansible'i põhitõdesid - kuidas kirjutada lihtsaid playbook'e ja hallata servereid. Aga mis juhtub siis, kui teie infrastruktuur kasvab kolmest serverist kolmesajani? Mis juhtub, kui teil on arenduskeskkond, testimiskeskkond ja produktsioon, kõik erinevate konfiguratsioonidega? Täna õpime tööriistu, mis muudavad suure infrastruktuuri haldamise võimalikuks ja turvaliseks.

Kujutage ette, et töötate startup'is. Alguses on teil kolm serverit - kõik Ubuntud, kõik ühtemoodi seadistatud. Lihtne. Aga firma kasvab. Nüüd on teil 50 serverit, osa neist on andmebaasiserverid, osa veebiserverid, osa cache-serverid. Mõned jooksevad Ubuntu peal, mõned CentOS'il. Arendusmeeskond tahab oma serverites debug-mode'i, aga produktsioonis see kindlasti ei tohi olla. Kuidas te seda kõike hallate ilma hulluks minemata?

Vastus on struktureeritud lähenemine muutujatele, dünaamilised konfiguratsioonid template'idega, intelligentne teenuste haldamine handler'itega ja turvaline paroolide hoidmine Vault'iga. Need neli komponenti moodustavad professionaalse Ansible seadistuse aluse.

## Muutujad ja nende prioriteedid

Alustame muutujate hierarhiast. Ansible'is saate defineerida muutujaid kaheksas erinevas kohas, ja igaühel on oma prioriteet. See pole bug, see on feature - see annab teile tohutult paindlikkust. Kõrgem prioriteet võidab alati madalama.

Hierarhia on järgmine, kõrgeimast madalaimani:
1. Command line extra-vars (need mida annate -e lipuga)
2. Task muutujad (otse task'i sees defineeritud)
3. Block muutujad (terve bloki jaoks)
4. Role muutujad (role/vars/main.yml)
5. Play muutujad (playbook'i alguses)
6. Host muutujad (host_vars/ kataloogis)
7. Group muutujad (group_vars/ kataloogis)
8. Role vaikeväärtused (role/defaults/main.yml)

Vaatame konkreetset näidet. Teil on muutuja `server_port`, mis määrab, millisel pordil teie rakendus kuulab. Vaikimisi tahate, et kõik serverid kuulaksid pordil 80. Seega panete `group_vars/all.yml` faili:
```yaml
server_port: 80
```

See kehtib nüüd kõigile serveritele. Aga ootke - teie staging serverid peavad kuulama pordil 8080, sest port 80 on juba kasutusel. Pole probleemi, teete `group_vars/staging.yml` faili:
```yaml
server_port: 8080
```

Nüüd kõik staging grupi serverid kasutavad porti 8080, aga ülejäänud ikka 80. Veelgi enam - teil on üks spetsiaalne test server, mis peab kuulama pordil 3000. Teete `host_vars/testserver1.yml`:
```yaml
server_port: 3000
```

See override'ib kõik eelnevad väärtused, aga ainult selle ühe serveri jaoks.

Ja kui teil on vaja kiirelt testida midagi teise pordiga? Käivitate playbook'i:
```bash
ansible-playbook site.yml -e server_port=9000
```

See extra-var override'ib kõik teised. See on kasulik testimiseks, aga ärge kasutage seda produktsioonis - muutujad peaksid olema koodis, mitte käsureal.

Miks see hierarhia oluline on? Sest see võimaldab teil kirjutada ühe playbook'i, mis töötab kogu teie infrastruktuuris. Te ei pea tegema eraldi playbook'i iga serveri või grupi jaoks. DRY principle - Don't Repeat Yourself - toimib ka infrastruktuuri koodis.

Ansible kogub ka automaatselt fakte igast serverist. Need on süsteemi muutujad, mida Ansible automaatselt avastab - operatsioonisüsteem, IP-aadress, mälu hulk, protsessorite arv. Näiteks:
```yaml
- debug:
    msg: "Serveril {{ inventory_hostname }} on {{ ansible_memtotal_mb }}MB mälu"
```

Te saate neid fakte kasutada intelligentsete otsuste tegemiseks. Kui serveril on vähem kui 2GB mälu, seadistage Apache'le vähem worker'eid. Kui server jookseb Debian'il, kasutage apt'i, kui RedHat'il, siis yum'i.

Registered variables on veel üks võimas funktsioon. Saate salvestada mis tahes task'i tulemuse ja kasutada seda hiljem:
```yaml
- name: "Kontrolli, kas Apache jookseb"
  command: systemctl is-active apache2
  register: apache_check
  failed_when: false

- name: "Käivita Apache kui vaja"
  service:
    name: apache2
    state: started
  when: apache_check.stdout != "active"
```

## Jinja2 mallid - dünaamilised konfiguratsioonid

Nüüd jõuame kõige võimsama tööriista juurde - template'id. Mäletate, kuidas vanasti kopeerisite Apache konfiguratsioonifaili serverist serverisse ja muutsite käsitsi IP-aadresse ja pordi numbreid? Unustage see. Template'idega genereerite konfiguratsioonifailid automaatselt, kasutades muutujaid ja loogikat.

Template on põhimõtteliselt tekstifail, kus osad kohad on asendatud muutujate ja loogikaga. Ansible kasutab Jinja2 template engine'it, mis on väga võimas aga samas lihtne õppida.

Vaatame reaalset näidet. Teil on vaja Nginx konfiguratsioonifaili, mis on erinev arendus- ja produktsioonikeskkondades. Arenduses tahate debug logisid ja cache välja lülitatud. Produktsioonis vastupidi. Traditsiooniliselt peaksite haldama kahte erinevat faili. Template'iga teete ühe faili, mis genereerib õige konfiguratsioon vastavalt keskkonnale.

Siin on näide template'ist:
```jinja2
# /etc/nginx/sites-available/{{ site_name }}
# {{ ansible_managed }}

server {
    listen {{ server_port }};
    server_name {{ server_name }};
    root {{ document_root }};
    
    {% if environment == 'production' %}
    # Production settings
    access_log /var/log/nginx/{{ site_name }}-access.log combined;
    error_log /var/log/nginx/{{ site_name }}-error.log error;
    
    # Enable caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 365d;
        add_header Cache-Control "public, immutable";
    }
    {% else %}
    # Development settings
    access_log /var/log/nginx/{{ site_name }}-access.log combined;
    error_log /var/log/nginx/{{ site_name }}-error.log debug;
    
    # Disable caching
    add_header Cache-Control "no-cache, no-store, must-revalidate";
    {% endif %}
    
    location / {
        proxy_pass http://127.0.0.1:{{ app_port | default(3000) }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Näete, kuidas `{% if environment == 'production' %}` kontrollib keskkonda ja lisab erinevad seaded? Ja `{{ app_port | default(3000) }}` kasutab vaikeväärtust 3000, kui muutuja pole defineeritud?

Kõige lahedam asi template'ides on loop'id. Kujutage ette, et peate seadistama 20 virtual host'i Apache'sse. Ilma template'ita peaksite copy-paste'ima 20 korda. Template'iga:

```jinja2
{% for vhost in virtual_hosts %}
<VirtualHost *:{{ vhost.port | default(80) }}>
    ServerName {{ vhost.domain }}
    DocumentRoot {{ vhost.path }}
    
    {% if vhost.ssl_enabled | default(false) %}
    SSLEngine on
    SSLCertificateFile {{ vhost.ssl_cert }}
    SSLCertificateKeyFile {{ vhost.ssl_key }}
    {% endif %}
    
    <Directory {{ vhost.path }}>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
{% endfor %}
```

Kui vaja lisada 21. virtual host, lisate lihtsalt ühe rea oma muutujate faili. Template teeb ülejäänu.

Filter'id on template'ide supervõimed. Need on nagu väikesed funktsioonid, mis töötlevad andmeid:
- `{{ server_name | upper }}` - teeb suurtähtedeks
- `{{ server_name | lower }}` - teeb väiketähtedeks
- `{{ my_list | join(', ') }}` - ühendab listi elemendid stringiks
- `{{ ansible_memtotal_mb * 0.8 | int }}` - arvutab ja ümardab
- `{{ my_dict | to_nice_json }}` - teisendab JSON formaati

Üks oluline nipp - kasutage alati `default` filter'it, kui muutuja võib puududa. See väldib vigu ja teeb template'id robustsemaks.

## Käsitlejad ja teavitused

Järgmine teema on handler'id. Need on spetsiaalsed task'id, mis käivituvad ainult siis, kui midagi muutub. Klassikaline näide - Apache konfiguratsioon. Kui konfiguratsioonifail muutub, peate Apache't taaskäivitama. Aga kui fail ei muutu, pole mõtet teenust puutuda.

Vaatame, kuidas see töötab:
```yaml
- name: "Deploy Apache configuration"
  hosts: webservers
  tasks:
    - name: "Copy Apache config"
      template:
        src: apache.conf.j2
        dest: /etc/apache2/apache2.conf
      notify: restart apache
    
    - name: "Copy PHP config"
      template:
        src: php.ini.j2
        dest: /etc/php/7.4/apache2/php.ini
      notify: restart apache
    
  handlers:
    - name: "restart apache"
      service:
        name: apache2
        state: restarted
```

Handler käivitub ainult siis, kui template tegelikult faili muudab. Kui konfiguratsioon on juba õige, jääb Apache rahule töötama.

Handler'id käivituvad playbook'i lõpus, mitte kohe. See on oluline - kui viis task'i muudavad Apache konfiguratsioon, taaskäivitub Apache ainult üks kord lõpus, mitte viis korda. See on efektiivne ja vähendab downtime'i.

Mõnikord on vaja valida restart'i ja reload'i vahel:
- **Restart** - katkestab kõik ühendused ja käivitab teenuse nullist. Kasutage seda, kui muudate põhilisi seadeid.
- **Reload** - laeb uue konfiguratsioon ilma ühendusi katkestamata. Kasutage seda, kui võimalik.

```yaml
handlers:
  - name: "restart apache"
    service:
      name: apache2
      state: restarted
  
  - name: "reload apache"
    service:
      name: apache2
      state: reloaded
```

Võimas funktsioon on listen groups. Mitu handler'it saavad kuulata sama signaali:
```yaml
tasks:
  - name: "Update PHP config"
    template:
      src: php.ini.j2
      dest: /etc/php/7.4/fpm/php.ini
    notify: restart web stack

handlers:
  - name: "restart php-fpm"
    service:
      name: php7.4-fpm
      state: restarted
    listen: restart web stack
  
  - name: "restart nginx"
    service:
      name: nginx
      state: restarted
    listen: restart web stack
```

Üks praktiline nipp - kui teil on kriitiline task, mis sõltub teenuse taaskäivitamisest, kasutage `meta: flush_handlers`:
```yaml
- name: "Install MySQL"
  apt:
    name: mysql-server
    state: present
  notify: start mysql

- name: "Flush handlers now"
  meta: flush_handlers

- name: "Create database"
  mysql_db:
    name: myapp
    state: present
```

See käivitab kõik ootel handler'id kohe, mitte playbook'i lõpus.

## Ansible Vault - turvalisus esimesena

Nüüd jõuame kõige olulisema teemani - turvalisus. Kui teil on paroolid, API võtmed või sertifikaadid, ei tohi need kunagi olla plain text'ina git'is. Kunagi. Isegi mitte private repository's. Ansible Vault krüpteerib need andmed nii, et saate neid turvaliselt git'i panna.

Vault töötab lihtsalt - te krüpteerite faili parooliga ja Ansible dekrüpteerib selle playbook'i käivitamisel. Krüpteeritud fail näeb välja nagu juhuslikud tähed ja numbrid:
```
$ANSIBLE_VAULT;1.1;AES256
66383439383437366337643938376139323...
38336233353664386139383665656439616...
```

Keegi ei saa sealt midagi kätte ilma paroolita.

Vault'i kasutamine on lihtne. Loome krüpteeritud faili:
```bash
ansible-vault create secrets.yml
```

See küsib parooli ja avab tekstiredaktori. Kirjutate oma saladused:
```yaml
mysql_root_password: "SuperSecret123!"
api_key: "abc123def456ghi789"
ssl_private_key: |
  -----BEGIN PRIVATE KEY-----
  MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKg...
  -----END PRIVATE KEY-----
```

Salvestades krüpteerib Ansible faili automaatselt.

Parim praktika on hoida saladused eraldi failis ja viidatakse neile avalikes failides. Näiteks:

`group_vars/production/vault.yml` (krüpteeritud):
```yaml
vault_mysql_password: "ReallySecretProd123!"
vault_api_key: "production-key-xyz789"
```

`group_vars/production/vars.yml` (avalik):
```yaml
mysql_password: "{{ vault_mysql_password }}"
api_key: "{{ vault_api_key }}"
environment: "production"
debug_mode: false
```

Nii on kohe näha, millised muutujad on salajased (algavad vault_) ja kust nad tulevad.

Playbook'i käivitamisel on mitu võimalust parooli andmiseks:
```bash
# Küsi parooli interaktiivselt
ansible-playbook site.yml --ask-vault-pass

# Kasuta parooli failist
echo "mypassword" > .vault_pass
chmod 600 .vault_pass
ansible-playbook site.yml --vault-password-file .vault_pass

# Kasuta environment variable'it
export ANSIBLE_VAULT_PASSWORD="mypassword"
ansible-playbook site.yml
```

Reaalses elus on teil tõenäoliselt erinevad paroolid arenduses ja produktsioonis. Ansible toetab multiple vault'e:
```bash
# Loo eraldi vault'id
ansible-vault create --vault-id dev@prompt dev-secrets.yml
ansible-vault create --vault-id prod@prompt prod-secrets.yml

# Käivita mõlemaga
ansible-playbook site.yml --vault-id dev@prompt --vault-id prod@prompt
```

Vault parooli haldamine meeskonnas on väljakutse. Mõned variandid:
1. **Password manager** - hoida parooli 1Password'is või LastPass'is
2. **HashiCorp Vault** - tsentraliseeritud secrets management
3. **Environment variable CI/CD-s** - Jenkins/GitLab hoiab parooli
4. **Ansible Tower/AWX** - built-in credential management

Oluline on ka regulaarne paroolide roteerumine. Ansible vault rekey käsk laseb teil muuta vault parooli ilma sisu dekrüpteerimata:
```bash
ansible-vault rekey secrets.yml
```

Tehke seda vähemalt kord kvartalis. Dokumenteerige protsess:
1. Genereeri uus parool
2. Rekey kõik vault failid
3. Uuenda CI/CD süsteemid
4. Jaga uus parool meeskonnaga
5. Eemalda vana parool kõigist süsteemidest

## Praktiline näide - kõik koos

Vaatame nüüd, kuidas kõik need komponendid töötavad koos reaalses projektis. Kujutage ette, et peate üles seadma WordPress hosting platvormi. Teil on kolm keskkonda - dev, staging ja production. Igas keskkonnas on veebiserver, andmebaasiserver ja cache server.

Projekti struktuur:
```
wordpress-platform/
├── ansible.cfg
├── inventory/
│   ├── dev
│   ├── staging
│   └── production
├── group_vars/
│   ├── all/
│   │   ├── vars.yml       # Üldised seaded
│   │   └── vault.yml      # Üldised saladused
│   ├── dev/
│   │   ├── vars.yml       # Dev spetsiifilised
│   │   └── vault.yml      # Dev paroolid
│   ├── staging/
│   │   ├── vars.yml
│   │   └── vault.yml
│   └── production/
│       ├── vars.yml
│       └── vault.yml
├── templates/
│   ├── nginx.conf.j2
│   ├── wp-config.php.j2
│   └── my.cnf.j2
├── playbooks/
│   ├── site.yml
│   ├── deploy.yml
│   └── backup.yml
└── handlers/
    └── main.yml
```

`group_vars/all/vars.yml` - seaded mis kehtivad kõigile:
```yaml
timezone: "Europe/Tallinn"
locale: "et_EE.UTF-8"
wordpress_version: "6.3"
php_version: "8.1"
```

`group_vars/production/vars.yml` - produktsiooni spetsiifilised:
```yaml
environment: "production"
debug_mode: false
wp_debug: false
mysql_max_connections: 500
php_memory_limit: "256M"
nginx_worker_processes: "{{ ansible_processor_vcpus }}"
ssl_enabled: true
ssl_certificate: "/etc/ssl/certs/production.crt"
ssl_private_key: "/etc/ssl/private/production.key"
```

`templates/wp-config.php.j2` - WordPress konfiguratsioon:
```php
<?php
/* {{ ansible_managed }} */

// Database settings
define('DB_NAME', '{{ wp_db_name }}');
define('DB_USER', '{{ wp_db_user }}');
define('DB_PASSWORD', '{{ wp_db_password }}');
define('DB_HOST', '{{ mysql_host }}');

// Environment specific
{% if environment == 'production' %}
define('WP_DEBUG', false);
define('WP_DEBUG_LOG', false);
define('WP_DEBUG_DISPLAY', false);
define('DISALLOW_FILE_EDIT', true);
{% else %}
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', true);
{% endif %}

// Security keys from vault
define('AUTH_KEY', '{{ vault_auth_key }}');
define('SECURE_AUTH_KEY', '{{ vault_secure_auth_key }}');
define('LOGGED_IN_KEY', '{{ vault_logged_in_key }}');
define('NONCE_KEY', '{{ vault_nonce_key }}');

// Cache settings
{% if redis_enabled | default(false) %}
define('WP_REDIS_HOST', '{{ redis_host }}');
define('WP_REDIS_PORT', {{ redis_port }});
{% endif %}

$table_prefix = 'wp_';

require_once(ABSPATH . 'wp-settings.php');
```

Playbook, mis kasutab kõike õpitut:
```yaml
---
- name: "Deploy WordPress Platform"
  hosts: all
  become: yes
  
  tasks:
    - name: "Install required packages"
      apt:
        name: "{{ item }}"
        state: present
      loop:
        - nginx
        - "php{{ php_version }}-fpm"
        - "php{{ php_version }}-mysql"
        - mysql-client
      notify: restart services
    
    - name: "Deploy Nginx configuration"
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/wordpress
      notify: reload nginx
    
    - name: "Deploy WordPress config"
      template:
        src: wp-config.php.j2
        dest: /var/www/wordpress/wp-config.php
        owner: www-data
        group: www-data
        mode: '0640'
      notify: restart php-fpm
    
    - name: "Setup MySQL database"
      mysql_db:
        name: "{{ wp_db_name }}"
        state: present
      delegate_to: "{{ mysql_host }}"
      run_once: true
    
    - name: "Create MySQL user"
      mysql_user:
        name: "{{ wp_db_user }}"
        password: "{{ wp_db_password }}"
        priv: "{{ wp_db_name }}.*:ALL"
        host: "%"
        state: present
      delegate_to: "{{ mysql_host }}"
      run_once: true
  
  handlers:
    - name: "restart services"
      service:
        name: "{{ item }}"
        state: restarted
      loop:
        - nginx
        - "php{{ php_version }}-fpm"
      listen: restart services
    
    - name: "reload nginx"
      service:
        name: nginx
        state: reloaded
    
    - name: "restart php-fpm"
      service:
        name: "php{{ php_version }}-fpm"
        state: restarted
```

Käivitamine erinevates keskkondades:
```bash
# Development
ansible-playbook -i inventory/dev playbooks/site.yml --vault-id dev@prompt

# Staging
ansible-playbook -i inventory/staging playbooks/site.yml --vault-id staging@prompt

# Production (with specific checks)
ansible-playbook -i inventory/production playbooks/site.yml \
  --vault-id prod@prompt \
  --check  # Dry run first!
```

## Kokkuvõte ja soovitused

See oli päris palju infot, aga need funktsioonid muudavad Ansible'i tõeliselt võimsaks tööriistaks. Kokkuvõtteks peamised punktid:

**Muutujate hierarhia** annab paindlikkuse. Defineerige üldised asjad üldiselt ja spetsiifilised spetsiifiliselt. Ärge korrake ennast.

**Template'id** väldivad kordusi. Ärge kunagi kopeeri konfiguratsioonifaile, genereerige need. Üks template töötab kõigis keskkondades.

**Handler'id** optimeerivad teenuste haldust. Taaskäivitage ainult siis, kui vaja. Grupeerige seotud handler'id.

**Vault** hoiab asjad turvalisena. Kunagi, mitte kunagi ärge pange paroole plain text'ina git'i. Krüpteerige kõik tundlikud andmed.

Minu soovitused algajatele:

1. **Alustage väikeselt** - võtke üks lihtne konfiguratsioonifail ja tehke sellest template
2. **Testige alati** - kasutage `--check` lippu enne produktsiooni muudatusi
3. **Dokumenteerige** - kirjutage README, selgitage oma valikuid
4. **Versioonihaldus** - kõik peab olema git'is
5. **Code review** - laske kolleegil üle vaadata enne merge'imist

Sagedased vead mida vältida:

1. **Hardcoded väärtused** - kasutage muutujaid
2. **Paroolid plain text'ina** - kasutage vault'i
3. **Restart asemel reload** - kui reload töötab, kasutage seda
4. **Copy-paste** - kui kopeerite, mõelge template'ile
5. **Testimata muudatused** - alati testige staging'us

Järgmisel nädalal räägime Ansible role'idest, mis viivad korduvkasutuse veelgi kõrgemale tasemele. Role'id on nagu Lego klotsid - saate koostada infrastruktuuri väikestest, testitud ja korduvkasutatavatest komponentidest.

Samuti tutvume Puppet'iga, mis on alternatiivne configuration management tööriist. Puppet läheneb samadele probleemidele teise nurga alt - deklaratiivne vs imperatiivne lähenemine. Huvitav on näha, kuidas erinevad tööriistad lahendavad samu väljakutseid.

##  Praktilised näited

Vaatame mõned praktilised näited. Alustame lihtsast ja liigume keerulisema poole.

### Näide 1: Muutujate hierarhia

Näide, kuidas luua projekti struktuur ja testida, milline muutuja võidab:
```bash
mkdir ansible-practice
cd ansible-practice
mkdir -p group_vars/all group_vars/web host_vars

echo "port: 80" > group_vars/all/main.yml
echo "port: 8080" > group_vars/web/main.yml
echo "port: 3000" > host_vars/server1.yml

# Test playbook
cat > test.yml << EOF
- hosts: server1
  tasks:
    - debug:
        msg: "Port is {{ port }}"
EOF
```

### Näide 2: Lihtne template

Näide dünaamilise konfiguratsioonifaili loomisest:
```bash
mkdir templates
cat > templates/app.conf.j2 << EOF
# {{ ansible_managed }}
[server]
host = {{ ansible_hostname }}
port = {{ app_port | default(3000) }}
workers = {{ ansible_processor_vcpus * 2 }}

[database]
{% if environment == 'production' %}
host = {{ db_host }}
pool_size = 20
{% else %}
host = localhost
pool_size = 5
{% endif %}
EOF
```

### Näide 3: Handler'iga playbook

```yaml
- name: "Web server setup"
  hosts: webservers
  tasks:
    - name: "Update config"
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: restart nginx
    
  handlers:
    - name: "restart nginx"
      service:
        name: nginx
        state: restarted
```

## Lõppsõnad

Täna õpitu on aluseks professionaalsele infrastruktuuri automatiseerimisele. Need pole lihtsalt tehnilised trikid - need on best practice'id, mida kasutavad tuhanded ettevõtted üle maailma.

Pidage meeles - automatiseerimine pole eesmärk omaette. Eesmärk on vähendada vigu, säästa aega ja muuta infrastruktuur ennustatavaks. Ansible'i edasijõudnud funktsioonid aitavad teil seda saavutada.

Järgmiseks korraks palun:
1. Tehke läbi lab harjutused
2. Proovige konverteerida mõni olemasolev konfiguratsioonifail template'iks
3. Harjutage vault'i kasutamist - krüpteerige testfail
4. Mõelge, millised osad teie infrastruktuurist saaksid kasu automatiseerimisest

Küsimused on teretulnud! Võite küsida kohe või hiljem kursuse chat'is. Remember - monkey see, monkey do, aga targem ahv mõistab ka miks ta seda teeb! 

Edu automatiseerimisel ja kohtumiseni järgmisel nädalal!
