#  Ansible Edasijõudnud Labor: Templates ja Vault (3×45 min)

## Lab'i eesmärk
Täna õpid Ansible'i professionaalseid funktsioone - Jinja2 templates, Ansible Vault, advanced variables! Nagu päris DevOps engineer! 

##  Õpiväljundid
Pärast seda lab'i oskad:
- Kasutada Jinja2 templates dünaamiliste konfiguratsioonide jaoks
- Krüpteerida salajasi Ansible Vault'iga
- Hallata keerulisi variable'eid (group_vars, host_vars)
- Luua professionaalset Ansible projekti struktuuri
- Rakendada best practices tootmiskeskkonnas

---

### Blokk 1 (45 min) – Jinja2 templates ja dynamic configs
- **Eesmärk:** Luua dünaamilisi konfiguratsioone template'idega
- **Tegevused:**
  - Jinja2 syntax (variables, loops, conditions)
  - Nginx config template loomine
  - Variables erinevatel tasanditel (all, group, host)
  - Template'i rendering ja vaatamine
  - Conditional logic template'is
- **Kontrollnimekiri:**
  - [ ] Template fail on loodud (`templates/nginx.conf.j2`)
  - [ ] Variables töötavad template'is
  - [ ] Conditional logic toimib (erinevad config'id dev vs prod)
  - [ ] Nginx config on dünaamiliselt genereeritud
- **Kontrollküsimus:** "Miks kasutada template'eid, mitte static faile?"
- **Refleksioon (1 min):** "Jinja2 on nagu... A) Mad Libs mäng  B) form auto-fill C) mõlemad"

---

### Blokk 2 (45 min) – Ansible Vault ja secrets management
- **Eesmärk:** Õppida krüpteerima ja haldama salajasi
- **Tegevused:**
  - Ansible Vault seadistamine
  - Vault faili loomine (`group_vars/all/vault.yml`)
  - Paroolide ja API võtmete krüpteerimine
  - Vault parooliga playbook jooksutamine
  - Variables vault failist kasutamine
- **Kontrollnimekiri:**
  - [ ] Vault fail on loodud ja krüpteeritud
  - [ ] Paroolid on vault'is (mitte plain text!)
  - [ ] Playbook kasutab vault variables
  - [ ] `ansible-playbook --ask-vault-pass` töötab
- **Kontrollküsimus:** "Miks ei tohi paroole Git'i panna ilma vault'ita?"
- **Refleksioon (1 min):** "Ansible Vault on nagu... A) seif  B) invisible ink C) password manager"

---

### Blokk 3 (45 min) – Advanced project structure ja best practices
- **Eesmärk:** Luua professionaalset projekti struktuuri
- **Tegevused:**
  - Full project structure (inventory, group_vars, host_vars, roles, playbooks)
  - Environment-specific configs (dev/staging/prod)
  - Ansible.cfg seadistamine
  - Error handling ja debugging
  - Full deployment test
- **Kontrollnimekiri:**
  - [ ] Project structure on organiseeritud
  - [ ] Group_vars ja host_vars töötavad koos
  - [ ] Ansible.cfg on seadistatud
  - [ ] Full deployment töötab dev ja prod keskkonnas
- **Kontrollküsimus:** "Kuidas struktureerida Ansible projekti, et see oleks maintainable?"
- **Refleksioon (1 min):** "Kõige professionaalsem osa täna oli... A) templates B) vault C) structure D) ma tunnen end nagu päris DevOps engineer! "

---

**Valmis? Alustame detailsete sammudega!** ⬇

---

##  Samm 1: Advanced Variables Setup (30 min)

### 1.1: Projekti struktuuri loomine - Organiseeritud struktuur

**Miks struktureeritud projekt:**

Kui alustate väikese projektiga, võib kõik failid hoida ühes kaustas, kuid reaalses maailmas kasvavad projektid kiiresti sadadeks failideks. Organiseeritud struktuur muudab projekti haldamise lihtsamaks - te teate täpselt, kus mingi konfiguratsioon asub. Lisaks võimaldab see mitmel inimesel samaaegselt töötada ilma üksteist segamata.

**Loome professionaalse struktuuri sammhaaval:**

1. **Looge peakaust:**
   ```bash
   mkdir -p ~/ansible-advanced
   cd ~/ansible-advanced
   ```
   See loob teie projekti juurkausta, kus kogu töö toimub. Kasutame `-p` lippu, et vältida viga kui kaust juba eksisteerib.

2. **Looge kõik vajalikud kaustad:**
   ```bash
   # Põhistruktuur
   mkdir -p {inventory,group_vars,host_vars,roles,playbooks,templates,files}
   
   # Group variables struktuuri
   mkdir -p group_vars/{all,webservers,dbservers}
   
   # Host-spetsiifilised muutujad
   mkdir -p host_vars/{web1,web2,db1}
   ```
   Iga kaust täidab kindlat rolli - `templates` hoiab konfiguratsioonimalle, `group_vars` hoiab servergruppide muutujaid. See struktuur järgib Ansible best practice'eid, mida tunneb ära iga kogenud DevOps insener.

3. **Kontrollige struktuuri:**
   ```bash
   tree .  # või ls -la kui tree ei ole installitud
   ```
   Kontrollimine kinnitab, et kõik kaustad on loodud õigesti. Kui `tree` käsk puudub, saate selle installida `apt install tree` käsuga.

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

Inventory on Ansible'i süda - see määrab, milliste serveritega töötate ja kuidas need on organiseeritud. Gruppide kasutamine võimaldab rakendada sama konfiguratsiooni mitmele serverile korraga, säästes aega ja vähendades vigu. Hierarhiline struktuur peegeldab reaalse infrastruktuuri keerukust.

**Loome inventory faili sammhaaval:**

1. **Looge põhi inventory fail:**
   ```bash
   touch inventory/hosts.yml
   nano inventory/hosts.yml
   ```
   YAML formaat on loetavam kui vana INI formaat ning võimaldab keerukamaid struktuure. See fail saab olema teie infrastruktuuri kaart.

2. **Lisage täielik inventory konfiguratsioon:**
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
         vars:
           http_port: 80
           https_port: 443
           web_root: "/var/www/html"
   ```
   Siin defineerime kaks veebiserveri, kus `web1` on primaarne ja `web2` sekundaarne. Kasutame `localhost` testimiseks, kuid tootmises oleksid siin päris IP-aadressid. Grupimuutujad `vars` all kehtivad kõigile selle grupi serveritele.

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
   Andmebaasiserver on eraldi grupis koos MySQL-spetsiifiliste muutujatega. See võimaldab rakendada andmebaasi-spetsiifilisi seadistusi ainult neile serveritele, mis seda vajavad.

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
   Keskkonna grupid (`development` ja `production`) võimaldavad sama playbook'i kasutada erinevates keskkondades. Arenduskeskkonnas on debug mode sisse lülitatud ja SSL välja, tootmises vastupidi. See lähenemine tagab, et tootmises ei unune kunagi turvaseadistusi sisse lülitada.

** Mõelge:** Miks on kasulik grupeerida servereid nii rolli kui keskkonna järgi?

### 1.3: Variables hierarchy loomine

**Mõistame muutujate prioriteete:**

Ansible'is kehtib muutujate hierarhia - spetsiifilisemad muutujad kirjutavad üle üldisemad. Host_vars kirjutab üle group_vars, mis omakorda kirjutab üle defaults. See võimaldab luua üldised vaikeväärtused, mida saab vajadusel serveripõhiselt muuta.

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
   ```
   Need on põhilised muutujad, mida kasutab kogu infrastruktuur. Kuna need on `all` grupis, pääsevad kõik serverid neile ligi.

   ```yaml
   # OS-spetsiifilised paketid (dünaamilised)
   apache_package: "{% if ansible_os_family == 'Debian' %}apache2{% else %}httpd{% endif %}"
   mysql_package: "{% if ansible_os_family == 'Debian' %}mysql-server{% else %}mariadb-server{% endif %}"
   ```
   See on tark viis toetada erinevaid Linux distributsioone - Debian/Ubuntu kasutab `apache2` nime, RedHat/CentOS kasutab `httpd`. Ansible tuvastab OS-i automaatselt ja valib õige paketi nime.

   ```yaml
   # Keskkonna sõltuvad seadistused
   backup_enabled: "{{ app_env == 'production' }}"
   monitoring_enabled: "{{ app_env == 'production' }}"
   log_level: "{% if debug_mode %}DEBUG{% else %}INFO{% endif %}"
   ```
   Need seadistused kohanduvad automaatselt vastavalt keskkonnale. Tootmises lülitatakse automaatselt sisse backup ja monitooring, arenduses mitte - see säästab ressursse seal, kus neid ei vajata.

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
   ```
   Apache worker'ite arv arvutatakse dünaamiliselt serveri CPU tuumade järgi. Kui serveril on 4 tuuma, saab Apache automaatselt 8 worker'it. See tagab optimaalse jõudluse igal serveril.

   ```yaml
   # PHP seadistused
   php_version: "7.4"
   php_memory_limit: "{% if ansible_memtotal_mb > 4096 %}512M{% else %}256M{% endif %}"
   php_max_execution_time: 30
   ```
   PHP mälupiirang kohandub serveri RAM-i järgi - võimsamad serverid saavad rohkem mälu. See on oluline, sest liiga väike mälulimiit põhjustab vigu, liiga suur raiskab ressursse.

   ```yaml
   # Virtual hosts
   virtual_hosts:
     - name: "{{ app_name }}.local"
       document_root: "{{ web_root }}/{{ app_name }}"
       ssl_enabled: "{{ ssl_enabled }}"
     - name: "api.{{ app_name }}.local"
       document_root: "{{ web_root }}/api"
       ssl_enabled: "{{ ssl_enabled }}"
   ```
   Virtual host'ide nimekiri võimaldab hallata mitut veebisaiti ühel serveril. SSL seadistus tuleb keskkonna muutujast - tootmises on see automaatselt sisse lülitatud.

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
   ```
   Need on MySQL põhiseadistused, mis kehtivad kõigile andmebaasiserveritele. Bind address `127.0.0.1` tähendab, et MySQL kuulab ainult localhost'i - see on turvalisem.

   ```yaml
   # Dünaamiline buffer pool arvutamine
   mysql_innodb_buffer_pool_size: "{{ (ansible_memtotal_mb * 0.7) | int }}M"
   ```
   InnoDB buffer pool on MySQL jõudluse võti - see hoiab andmeid mälus kiireks ligipääsuks. Kasutame 70% serveri mälust, mis on MySQL-i soovituslik praktika. Filter `| int` tagab, et saame täisarvu.

   ```yaml
   # Andmebaasid
   mysql_databases:
     - name: "{{ app_name }}_{{ app_env }}"
       encoding: "utf8mb4"
       collation: "utf8mb4_unicode_ci"
   ```
   Andmebaasi nimi sisaldab keskkonna nime (nt `advanced-lamp_production`), mis hoiab erinevate keskkondade andmed eraldi. UTF8MB4 toetab ka emoji'sid ja teisi 4-baidiseid Unicode märke.

   ```yaml
   mysql_users:
     - name: "{{ app_name }}_user"
       host: "localhost"
       priv: "{{ app_name }}_{{ app_env }}.*:ALL"
       # Parool tuleb vault'ist
   ```
   Andmebaasi kasutaja õigused on piiratud ainult vajaliku andmebaasiga. Parool hoitakse krüpteeritult Vault'is, mitte tavalises tekstifailis.

** Märkused:**
- Kasutame Jinja2 loogikat dünaamilisteks väärtusteks
- Serverite võimsus mõjutab konfiguratsiooni
- Keskkond määrab turvalisuse taseme

---

##  Samm 2: Jinja2 Template'ite loomine (45 min)

### 2.1: Apache virtual host template - Dünaamiline konfiguratsioon

**Miks template'id on olulised:**

Template'id on nagu vormid, kuhu saate sisestada erinevaid andmeid ja saada välja personaliseeritud konfiguratsiooni. Ühe template'iga saate luua kümneid erinevaid Apache konfiguratsioone, säästes aega ja vähendades vigu. Kui vaja teha muudatus, piisab ühe template'i muutmisest, mitte kümnete konfiguratsioonifailide käsitsi redigeerimisest.

**Loome Apache virtual host template'i sammhaaval:**

1. **Looge template fail:**
   ```bash
   touch templates/apache_vhost.conf.j2
   nano templates/apache_vhost.conf.j2
   ```
   Faililaiend `.j2` näitab, et tegemist on Jinja2 template'iga. See aitab kohe aru saada, et fail sisaldab muutujaid ja loogikat.

2. **Alustage põhistruktuuriga:**
   ```apache
   # {{ ansible_managed }}
   # Virtual Host for {{ item.name }}
   # Generated on {{ ansible_date_time.iso8601 }}
   
   <VirtualHost *:{{ http_port }}>
       ServerName {{ item.name }}
       DocumentRoot {{ item.document_root }}
   ```
   Kommentaarid faili alguses näitavad, et fail on automaatselt genereeritud ja millal. `ansible_managed` muutuja lisab hoiatuse, et faili ei tohiks käsitsi muuta. Iga virtual host saab oma serveri nime ja document root'i.

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
   Debug režiimis logitakse kõik detailselt, tootmises ainult hoiatused ja vead. Iga virtual host saab oma logifailid, mis lihtsustab probleemide lahendamist. Logifailide nimed sisaldavad virtual host'i nime, et neid oleks lihtne eristada.

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
   Tootmiskeskkonnas lisatakse automaatselt turvapäised, mis kaitsevad clickjacking'u ja XSS rünnakute eest. Need päised pole arenduskeskkonnas vajalikud ja võivad isegi segada testimist. Directory seadistused määravad, kuidas Apache käsitleb faile selles kaustas.

5. **Lisage SSL support (conditional):**
   ```apache
   {% if item.ssl_enabled and ssl_enabled %}
   <IfModule mod_ssl.c>
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
   </IfModule>
   {% endif %}
   ```
   SSL konfiguratsioon lisatakse ainult siis, kui see on lubatud nii virtual host'i kui keskkonna tasemel. TLS 1.2 ja 1.3 on ainsad turvalised protokollid - vanemad versioonid on haavatavad. Sertifikaadi teed tulevad vault'ist, kuid on ka vaikeväärtused testimiseks.

** Analüüs:** Kuidas template aitab hallata erinevaid keskkondi (dev vs prod)?

### 2.2: MySQL konfiguratsioon template

**Andmebaasi optimeerimine:**

MySQL vajab hoolikat häälestamist optimaalse jõudluse saavutamiseks. Template võimaldab automaatselt kohandada seadistusi serveri ressursside ja keskkonna järgi. Näiteks arenduskeskkonnas eelistame kiirust turvalisusele, tootmises vastupidi.

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
   ```
   Päis näitab, millisele serverile ja keskkonnale konfiguratsioon kuulub. See on eriti kasulik, kui teil on palju servereid ja peate kiiresti aru saama, millist faili vaatate.

   ```ini
   # Performance tuning based on available memory
   innodb_buffer_pool_size = {{ mysql_innodb_buffer_pool_size }}
   max_connections = {{ mysql_max_connections }}
   ```
   Buffer pool suurus arvutatakse dünaamiliselt serveri mälu järgi - see on MySQL jõudluse kõige olulisem parameeter. Liiga väike buffer pool aeglustab päringuid, liiga suur võib põhjustada mälu puudumise.

   ```ini
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
   ```
   Tootmises kirjutatakse iga transaktsioon kohe kettale (aeglasem aga turvalisem), arenduses puhverdatakse kirjutamised (kiirem aga andmed võivad kaduda krahhi korral). See kompromiss on mõistlik, sest arenduses pole andmete kaotus kriitiline.

   ```ini
   # Logging
   {% if debug_mode %}
   general_log = 1
   general_log_file = /var/log/mysql/general.log
   slow_query_log = 1
   slow_query_log_file = /var/log/mysql/slow.log
   long_query_time = 1
   {% endif %}
   ```
   Debug režiimis logitakse kõik päringud ja eraldi aeglased päringud (üle 1 sekundi). See aitab tuvastada jõudlusprobleeme, kuid tootmises lülitame välja, sest logimine aeglustab andmebaasi.

### 2.3: PHP konfiguratsioon template

**PHP-FPM optimeerimine:**

PHP-FPM (FastCGI Process Manager) haldab PHP protsesse efektiivsemalt kui traditsiooniline mod_php. Template võimaldab automaatselt häälestada protsesside arvu vastavalt serveri võimsusele. Liiga vähe protsesse põhjustab ootejärjekordi, liiga palju raiskab mälu.

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
   ```
   Iga rakendus saab oma PHP pool'i, mis võimaldab isolatsiooni ja erinevaid seadistusi. Pool'i nimi on rakenduse nimi, mis lihtsustab identifitseerimist.

   ```ini
   listen = /var/run/php/php{{ php_version }}-fpm-{{ app_name }}.sock
   listen.owner = www-data
   listen.group = www-data
   listen.mode = 0660
   ```
   Unix socket on kiirem kui TCP port localhost'is suhtlemiseks. Socket'i fail sisaldab PHP versiooni ja rakenduse nime, et vältida konflikte mitme rakenduse korral.

   ```ini
   # Process management
   pm = dynamic
   pm.max_children = {{ ansible_processor_vcpus * 4 }}
   pm.start_servers = {{ ansible_processor_vcpus }}
   pm.min_spare_servers = {{ ansible_processor_vcpus }}
   pm.max_spare_servers = {{ ansible_processor_vcpus * 2 }}
   ```
   Protsesside arv skaleerub automaatselt CPU tuumade arvuga - 4-tuumaline server saab kuni 16 PHP protsessi. Dynamic PM tähendab, et PHP käivitab ja peatab protsesse vastavalt koormusele. See tagab ressursside efektiivse kasutuse.

   ```ini
   # PHP settings
   php_admin_value[memory_limit] = {{ php_memory_limit }}
   php_admin_value[max_execution_time] = {{ php_max_execution_time }}
   php_admin_value[upload_max_filesize] = 32M
   php_admin_value[post_max_size] = 32M
   ```
   PHP seadistused tulevad muutujatest, mis omakorda kohanduvad serveri ressursside järgi. Upload ja POST piirangud on seatud 32MB peale, mis on piisav enamiku rakenduste jaoks.

   ```ini
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
   Arenduses näitame kõiki PHP vigu otse brauseris, mis kiirendab silumist. Tootmises peidame vead kasutajate eest (turvakaalutlused) ja logime ainult kriitilised vead. See hoiab ära tundliku info lekke.

---

##  Samm 3: Handlers ja Advanced Playbook (30 min)

### 3.1: Playbook handlers'itega

**Handler'ite tarkus:**

Handler'id on Ansible'i viis teenuste tõhusaks haldamiseks - nad käivituvad ainult siis, kui midagi tegelikult muutus. Kui muudate 10 konfiguratsiooni faili, taaskäivitub Apache ainult üks kord lõpus, mitte 10 korda. See säästab aega ja vähendab teenuse katkestusi.

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
   ```
   Playbook nimi peaks kirjeldama, mida see teeb. `become: yes` tähendab sudo kasutamist, `gather_facts` kogub infot serverite kohta (OS, mälu, CPU jne).

   ```yaml
     tasks:
       - name: "Update package cache"
         package:
           update_cache: yes
         when: ansible_os_family == "Debian"
   ```
   Debian/Ubuntu süsteemides uuendame paketi nimekirju enne installimist. `when` tingimus tagab, et see käivitatakse ainult Debian põhistel süsteemidel.

3. **Lisage Apache seadistamine handlers'itega:**
   ```yaml
       - name: "Install Apache"
         package:
           name: "{{ apache_package }}"
           state: present
         notify:
           - "start apache"
           - "enable apache"
   ```
   Apache installimisel teavitame handler'eid, et teenus tuleb käivitada ja lubada. Handler'id käivituvad playbook'i lõpus, mitte kohe.

   ```yaml
       - name: "Create virtual host directories"
         file:
           path: "{{ item.document_root }}"
           state: directory
           owner: www-data
           group: www-data
           mode: '0755'
         loop: "{{ virtual_hosts }}"
         when: virtual_hosts is defined
   ```
   Loop käib läbi kõik virtual host'id ja loob igaühele oma kausta. `when` tingimus kaitseb vea eest, kui virtual_hosts muutuja pole defineeritud. Õigused 755 tähendavad, et omanik saab kõike teha, teised ainult lugeda ja siseneda.

   ```yaml
       - name: "Generate virtual host configurations"
         template:
           src: apache_vhost.conf.j2
           dest: "/etc/apache2/sites-available/{{ item.name }}.conf"
           backup: yes
         loop: "{{ virtual_hosts }}"
         notify: "reload apache"
         when: virtual_hosts is defined
   ```
   Template task genereerib iga virtual host'i jaoks eraldi konfiguratsioonifaili. `backup: yes` teeb varukoopia enne ülekirjutamist - see on päästerõngas, kui midagi läheb valesti.

   ```yaml
       - name: "Enable virtual hosts"
         command: "a2ensite {{ item.name }}"
         args:
           creates: "/etc/apache2/sites-enabled/{{ item.name }}.conf"
         loop: "{{ virtual_hosts }}"
         notify: "reload apache"
         when: virtual_hosts is defined
   ```
   `a2ensite` on Apache'i käsk virtual host'i lubamiseks. `creates` argument ütleb Ansible'ile, et kui fail juba eksisteerib, pole vaja käsku uuesti käivitada - see teeb playbook'i idempotentseks.

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
   ```
   Need handler'id käivitavad ja lubavad Apache teenuse. `enabled: yes` tähendab, et Apache käivitub automaatselt serveri taaskäivitumisel.

   ```yaml
       - name: "reload apache"
         service:
           name: "{{ apache_package }}"
           state: reloaded
   
       - name: "restart apache"
         service:
           name: "{{ apache_package }}"
           state: restarted
   ```
   Reload laeb konfiguratsiooni uuesti ilma ühendusi katkestamata, restart peatab ja käivitab teenuse täielikult. Eelistame reload'i, kui võimalik, et vältida teenuse katkestusi.

** Mõelge:** Miks kasutame `reload` mitte `restart`? Mis vahe on?

### 3.2: Testimine

**Kontrollige enne käivitamist:**

Testimine on kriitiline osa automatiseerimisest - parem leida vead testimisel kui tootmises. Ansible pakub mitmeid viise playbook'i testimiseks enne päris käivitamist. Alati testige muudatusi arenduskeskkonnas enne tootmisse viimist.

1. **Syntax check:**
   ```bash
   ansible-playbook --syntax-check playbooks/site.yml
   ```
   Kontrollib YAML süntaksit ja Ansible konstruktide õigsust. See leiab kirjavead ja süntaksivead, kuid ei kontrolli loogikat.

2. **Kuiv käivitus:**
   ```bash
   ansible-playbook --check -i inventory/hosts.yml playbooks/site.yml
   ```
   Check mode näitab, mida Ansible teeks, kuid ei tee tegelikke muudatusi. See on nagu eelvaade - näete, mis muutuks ilma midagi lõhkumata.

3. **Template'i testimine:**
   ```bash
   ansible-playbook -i inventory/hosts.yml playbooks/site.yml --tags "config" -v
   ```
   Verbose mode (`-v`) näitab detailset väljundit, mis aitab mõista, mida Ansible teeb. Saate kasutada ka `-vv` või `-vvv` veel detailsema info jaoks.

---

##  Samm 4: Ansible Vault rakendamine (35 min)

### 4.1: Vault failide loomine

**Turvalisus esimesena:**

Vault on Ansible'i vastus turvalisuse probleemile - kuidas hoida paroole ja API võtmeid versioonikontrollis ilma neid paljastamata. Vault krüpteerib failid AES-256 algoritmiga, mis on panga-tasemel krüpteering. Ilma paroolita on võimatu faile dekrüpteerida.

1. **Looge vault fail group_vars jaoks:**
   ```bash
   ansible-vault create group_vars/all/vault.yml
   ```
   Käsk küsib vault parooli - valige tugev parool ja hoidke see turvaliselt. See parool on ainus viis failile ligi pääseda.

2. **Lisage tundlikud andmed:**
   ```yaml
   # Database credentials
   vault_mysql_root_password: "SecureRootPassword123!"
   vault_mysql_app_password: "AppPassword456!"
   ```
   Kõik paroolid peavad olema tugevad - kasutage suuri ja väikesi tähti, numbreid ja erimärke. Reaalses keskkonnas kasutage parooligeneraatorit.

   ```yaml
   # SSL certificates paths
   vault_ssl_cert_path: "/etc/ssl/certs/company.crt"
   vault_ssl_key_path: "/etc/ssl/private/company.key"
   ```
   SSL sertifikaatide teed on tundlikud, sest näitavad teie infrastruktuuri struktuuri. Privaatne võti on eriti kriitiline - selle lekkimine kompromiteerib kogu HTTPS turvalisuse.

   ```yaml
   # API keys
   vault_backup_api_key: "backup_api_key_here"
   vault_monitoring_token: "monitoring_token_here"
   ```
   API võtmed on nagu paroolid väliste teenuste jaoks. Nende lekkimine võib põhjustada teenuse väärkasutust või andmeleket.

   ```yaml
   # Admin passwords
   vault_admin_password: "AdminSecurePass789!"
   ```
   Administraatori parool annab täieliku kontrolli süsteemi üle. See peaks olema kõige tugevam parool ja regulaarselt vahetatud.

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
   ```
   Tootmise sertifikaat on teie ettevõtte identiteet internetis. YAML-i `|` süntaks säilitab mitmerealise teksti formaadi, mis on vajalik sertifikaatide jaoks.

   ```yaml
   vault_ssl_key_content: |
     -----BEGIN PRIVATE KEY-----
     [private key content here]
     -----END PRIVATE KEY-----
   ```
   Privaatvõti on kõige tundlikum osa - see PEAB olema krüpteeritud. Kui keegi saab kätte teie privaatvõtme, saab ta teeskleda olevat teie server.

   ```yaml
   # Production database settings
   vault_production_db_host: "prod-db.company.com"
   vault_production_db_password: "ProdDbPass123!"
   ```
   Tootmise andmebaasi mandaadid on eraldi, et vältida kogemata arenduse paroolide kasutamist tootmises. See on oluline turvalisuse kiht.

### 4.2: Vault muutujate kasutamine

**Vault ja tavaliste muutujate ühendamine:**

Vault muutujad ei ole otse kasutatavad - need tuleb "mappida" tavalistele muutujatele. See eraldus võimaldab vahetada vault faile ilma põhi konfiguratsiooni muutmata. See on kasulik, kui teil on erinevad paroolid erinevates keskkondades.

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
   Need muutujad viitavad vault muutujatele. Kui Ansible laeb muutujaid, asendab ta need väärtustega vault failist.

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
   Tootmises lubame MySQL SSL-i, kasutades vault'ist tulevaid sertifikaate. See krüpteerib andmebaasi ühendused, kaitstes andmeid võrgus.

### 4.3: Vault käsitsikasutatavus

**Igapäevased vault operatsioonid:**

Vault failidega töötamine nõuab teadmisi erinevatest käskudest. Need käsud on teie igapäevased tööriistad tundlike andmete haldamiseks. Harjutage neid arenduskeskkonnas, enne kui kasutate tootmises.

1. **Vaata vault faili:**
   ```bash
   ansible-vault view group_vars/all/vault.yml
   ```
   View käsk näitab faili sisu ilma dekrüpteeritud faili kettale kirjutamata. See on turvalisem kui edit, kui tahate ainult kontrollida väärtusi.

2. **Muuda vault faili:**
   ```bash
   ansible-vault edit group_vars/production/vault.yml
   ```
   Edit käsk dekrüpteerib faili ajutiselt mälus, avab redaktoris ja krüpteerib uuesti peale salvestamist. Faili ei kirjutata kunagi dekrüpteeritult kettale.

3. **Käivita playbook vault'iga:**
   ```bash
   ansible-playbook -i inventory/hosts.yml playbooks/site.yml --ask-vault-pass
   ```
   `--ask-vault-pass` küsib parooli interaktiivselt. See on turvaline viis ühekordseks käivitamiseks, sest parool ei jää käsurea ajalukku.

4. **Või kasuta vault password faili:**
   ```bash
   echo "your_vault_password" > .vault_pass
   chmod 600 .vault_pass
   ansible-playbook -i inventory/hosts.yml playbooks/site.yml --vault-password-file .vault_pass
   ```
   Paroolifail on mugav automatiseeritud käivitusteks (nt CI/CD). Õigused 600 tähendavad, et ainult omanik saab faili lugeda - see on kriitiline turvalisuse jaoks.

** Turvalisus:** Ära iial commiti `.vault_pass` faili Git'i! Lisage see kohe `.gitignore` faili.

---

##  Samm 5: Lõplik kontrollnimekiri

Veenduge, et olete lõpetanud kõik osad ja mõistnud põhimõtteid:

### Struktuur ja organisatsioon
- [ ] **Organiseeritud projektinstruktuur** - kaustad loogiliselt struktureeritud ja arusaadavad
- [ ] **Inventory hierarhia** - serverid grupeeritud rolli ja keskkonna järgi
- [ ] **Muutujate hierarhia** - group_vars ja host_vars õigesti seadistatud ja prioriteedid selged

### Template'id ja konfiguratsioon
- [ ] **Apache virtual host template** - dünaamiline, töötab erinevates keskkondades
- [ ] **MySQL konfiguratsioon template** - optimeeritud serveri ressursside järgi
- [ ] **PHP-FPM template** - protsesside arv skaleerub automaatselt

### Playbook'id ja handlers
- [ ] **Advanced playbook** - kasutab template'e, loops ja conditionals efektiivselt
- [ ] **Proper handlers** - teenused taaskäivituvad ainult vajadusel
- [ ] **Error handling** - backup'id ja validation töötavad

### Vault ja turvalisus
- [ ] **Vault failid loodud** - kõik tundlikud andmed krüpteeritud
- [ ] **Vault integratsioon** - muutujad korrektselt seotud
- [ ] **Turvaline workflow** - .vault_pass pole repositooriumis

### Testing ja validation
- [ ] **Syntax check** - kõik playbook'id läbivad süntaksi kontrolli
- [ ] **Dry run** - --check mode töötab vigadeta
- [ ] **Template testing** - konfiguratsioonid genereeruvad õigesti

##  Järgmised sammud

**Valmis kodutööks:**

Kasutage siin õpitud mustreid oma projektides - need on industry standard praktikad, mida kasutatakse päris ettevõtetes. Alustage väiksest projektist ja lisage keerukust järk-järgult. Harjutage vault'i kasutamist kõigi paroolidega - see harjumus säästab teid tulevikus.

**Järgmine nädal:**
- Ansible Roles ja Galaxy - kuidas jagada ja taaskasutada koodi
- Automated testing strategies - molecule ja ansible-lint
- Enterprise deployment patterns - blue-green deployment, rolling updates

**Hästi tehtud! ** 

Te oskate nüüd luua production-ready Ansible projekte, mis on turvalised, skaleeruvad ja hooldatavad. Need oskused on väärtuslikud igas DevOps meeskonnas ja aitavad teil automatiseerida keerukaid infrastruktuure. Jätkake harjutamist ja eksperimenteerimist!
