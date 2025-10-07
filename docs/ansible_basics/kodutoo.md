# Ansible Kodutöö: LAMP Stack Paigaldus

Looge Ansible lahendus, mis paigaldab täieliku LAMP stack'i (Linux, Apache, MySQL, PHP) ühele või mitmele serverile. Lahendus peab olema taaskasutatav ja konfigureeritav. See ülesanne võtab orienteeruvalt 6-8 tundi ja nõuab iseseisvat dokumentatsiooni lugemist ning probleemide lahendamist.

**Eeldused:** Ansible põhitõed, SSH võtmete kasutamine, YAML süntaks, Linux CLI  
**Esitamine:** GitHub avalik repositoorium koos README.md failiga  
**Tähtaeg:** Järgmise nädala alguseks

---

## Ülesande Kirjeldus

Teie ülesanne on luua professionaalselt organiseeritud Ansible projekt, mis automatiseerib LAMP stack'i paigalduse. Erinevalt laborist, kus kõik oli ühes failis õppimise eesmärgil, peate siin järgima tööstuse parimaid praktikaid - muutujad eraldi failides, playbook'id loogiliselt grupeeritud, ja kõik peab olema konfigureeritav.

Lahendus peab töötama nii, et õpetaja saab muuta ainult inventory failis IP aadresse ja group_vars failis muutujaid, seejärel käivitada playbook'i ja kõik peab töötama.

---

## 1. Infrastruktuuri ettevalmistus

Seadistage vähemalt 2 virtuaalmasinat:
- Üks control node (teie arvuti või eraldi VM)
- Vähemalt üks target server LAMP stack'i jaoks

OLULINE: Lahendus PEAB olema konfigureeritav. Õpetaja testib teie lahendust muutes ainult inventory.ini ja group_vars/all/main.yml faile.

Näide kuidas õpetaja testib:
```bash
# Õpetaja muudab ainult:
# 1. inventory.ini - oma IP-d
# 2. group_vars/all/main.yml - oma kasutajanimi

# Ja käivitab:
ansible-playbook playbooks/site.yml
```

Näide inventory.ini failist:
```ini
[lamp_servers]
server1 ansible_host=192.168.1.100 ansible_user=student
```

Näide group_vars/all/main.yml failist:
```yaml
# Muudetavad muutujad
student_username: "jaan.tamm"
server_ip: "192.168.1.100"
domain_name: "lamp.local"
```

VALE lähenemine - hardcoded väärtused:
```yaml
- name: "Create user"
  user:
name:
- "jaan.tamm"  # VALE
- peab olema muutuja
    
- name: "Copy file"  
  copy:
dest:
- "/home/jaan.tamm/file"  # VALE
- hardcoded path
```

ÕIGE lähenemine - muutujatega:
```yaml
- name: "Create user"
  user:
    name: "{{ student_username }}"  # ÕIGE
    
- name: "Copy file"
  copy:
    dest: "/home/{{ student_username }}/file"  # ÕIGE
```

---

## 2. Süsteemi ettevalmistus

Looge playbook mis:
- Uuendab süsteemi pakette
- Paigaldab vajalikud tööriistad
- Seadistab firewall'i (avage pordid 80, 443, 22)
- Seadistab ajavööndi

Uurige järgmisi mooduleid:
- `apt` või `yum` - pakettide haldus
- `ufw` või `firewalld` - firewall
- `timezone` - ajavööndi seadistus

---

## 3. Apache veebiserver

Paigaldage ja seadistage Apache2:
- Installige Apache2 pakett
- Lubage vajalikud moodulid (rewrite, ssl, headers)
- Looge virtual host konfiguratsioon template abil
- Seadistage handler teenuse restardiks

Kasutage Jinja2 template'd Apache virtual host konfiguratsiooni loomiseks. Template peab sisaldama muutujaid nagu domain_name, server_admin, document_root.

Uurige:
- Kuidas luua Apache virtual host?
- Mis on `a2ensite` ja `a2enmod` käsud?
- Millal kasutada `notify` ja `handlers`?

Template näidis (vhost.conf.j2):
```apache
<VirtualHost *:80>
    ServerName {{ domain_name }}
    ServerAdmin {{ server_admin }}
    DocumentRoot {{ document_root }}
    
    <Directory {{ document_root }}>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

---

## 4. MySQL andmebaas

Paigaldage ja seadistage MySQL:
- Installige MySQL server
- Turvake root kasutaja parooliga
- Looge andmebaas rakenduse jaoks
- Looge andmebaasi kasutaja vajalike õigustega
- Paroolid ei tohi olla nähtavad koodis

Nõuded:
- Kasutage `vars_prompt` või Ansible Vault paroolide salvestamiseks
- Python MySQL moodul peab olema installitud (pymysql)
- Andmebaasi nimi ja kasutaja peavad olema muutujad

MySQL paroolide käsitlemine vars_prompt abil:
```yaml
vars_prompt:
  - name: mysql_root_password
    prompt: "Enter MySQL root password"
    private: yes
    
  - name: mysql_app_password
    prompt: "Enter application database password"
    private: yes
```

Uurige järgmisi mooduleid:
- `mysql_db` - andmebaasi haldus
- `mysql_user` - kasutajate haldus
- `apt` - pymysql paketi installimine

---

## 5. PHP seadistamine

Paigaldage PHP ja vajalikud laiendused:
- PHP 8.x või uuem
- PHP laiendused: mysql, curl, gd, mbstring, xml, zip
- Integreerige Apache'ga (libapache2-mod-php)
- Looge PHP test leht

Test leht peab sisaldama:
- Serveri info kuvamist
- MySQL ühenduse testimist
- PHP versiooni kuvamist
- Dünaamilist sisu Ansible muutujatest

Template näidis (index.php.j2):
```php
<?php
// Server info
echo "<h1>LAMP Stack Test</h1>";
echo "<p>Server: {{ ansible_hostname }}</p>";
echo "<p>PHP Version: " . phpversion() . "</p>";

// MySQL connection test
$host = "{{ mysql_host }}";
$user = "{{ mysql_user }}";
$pass = "{{ mysql_password }}";
$db = "{{ mysql_database }}";

try {
    $conn = new PDO("mysql:host=$host;dbname=$db", $user, $pass);
    echo "<p style='color:green'>MySQL connection: OK</p>";
} catch(PDOException $e) {
    echo "<p style='color:red'>MySQL connection: FAILED</p>";
}
?>
```

---

## 6. Projekti organiseerimine

OLULINE: Failid PEAVAD olema õigesti organiseeritud. Labor oli õppimiseks kus kõik oli ühes failis. Kodutöös peab järgima professionaalset struktuuri.

Nõutud failide struktuur:
```
ansible_lamp/
├── inventory.ini
├── ansible.cfg
├── playbooks/
│   ├── system.yml       # Süsteemi ettevalmistus
│   ├── apache.yml       # Apache seadistus
│   ├── mysql.yml        # MySQL seadistus
│   ├── php.yml          # PHP seadistus
│   └── site.yml         # Master playbook (import_playbook)
├── templates/
│   ├── vhost.conf.j2    # Apache virtual host
│   └── index.php.j2     # PHP test leht
├── group_vars/
│   ├── all/
│   │   └── main.yml     # Globaalsed muutujad
│   └── lamp_servers/
│       └── main.yml     # LAMP serverite muutujad
└── README.md
```

MITTE LUBATUD:
- Kõik muutujad playbook'i sees vars: sektsioonis
- Kõik ühes suures playbook failis
- Handlers playbooki sees (väikeste playbook'ide puhul lubatud)

NÕUTUD:
- Muutujad group_vars/ või host_vars/ kaustades
- Iga teenus eraldi playbook'is
- Templates templates/ kaustas
- Master playbook (site.yml) kasutab import_playbook

VALE struktuuri näide:
```yaml
# HALB - kõik ühes failis
- name: "Everything in one file"
  hosts: servers
  vars:
    mysql_pass: xyz  # Muutujad peaks olema group_vars
  tasks:
    - name: "Install Apache"
    - name: "Install MySQL"  # Erinevad teenused segamini
  handlers:
    - name: restart  # Handlers võiks olla eraldi
```

ÕIGE struktuuri näide:
```yaml
# apache.yml
- name: "Apache setup"
  hosts: lamp_servers
  tasks:
    - name: "Install Apache"
      # ...
    
# mysql.yml  
- name: "MySQL setup"
  hosts: lamp_servers
  tasks:
    - name: "Install MySQL"
      # ...

# site.yml - master playbook
- import_playbook: system.yml
- import_playbook: apache.yml
- import_playbook: mysql.yml
- import_playbook: php.yml
```

---

## 7. Idempotentsus ja testimine

Tagage, et playbook on idempotentne - teine käivitamine ei tohi midagi muuta. Lisage kontrollid:

- Apache töötab ja kuulab port 80-l?
- MySQL teenus töötab?
- PHP töötab koos Apache'ga?
- Veebileht on kättesaadav ja näitab õiget sisu?

Kasutage järgmisi mooduleid:
- `uri` - veebilehe kättesaadavuse test
- `wait_for` - pordi kuulamise test
- `service_facts` - teenuste seisundi kontroll
- `stat` - failide olemasolu kontroll

Testimise näide:
```yaml
- name: "Test Apache is responding"
  uri:
    url: "http://{{ inventory_hostname }}"
    status_code: 200
    
- name: "Wait for MySQL port"
  wait_for:
    port: 3306
    state: started
    timeout: 30
```

---

## Esitamine

### README.md nõuded

Teie README.md fail peab sisaldama järgmisi sektsioone:
```markdown
# LAMP Stack Ansible

## Autor
[Teie nimi ja õpperühm]

## Kirjeldus
[Lühike kirjeldus, mida see projekt teeb]

## Eeldused
- Ubuntu 20.04 või 22.04
- Ansible 2.9+
- SSH juurdepääs target serveritele
- Sudo õigused target serverites

## Failide struktuur
```
ansible_lamp/
├── playbooks/
│   ├── site.yml
│   └── ...
...
```
[Kirjeldage, mis igas kaustas on]

## Seadistamine

1. Kloonige repositoorium
2. Muutke inventory.ini failis IP aadresse
3. Muutke group_vars/all/main.yml failis muutujaid
4. Käivitage: `ansible-playbook playbooks/site.yml`

## Kasutamine

### Esimene käivitamine
```bash
ansible-playbook playbooks/site.yml --ask-become-pass
```

### Idempotentsuse test
```bash
ansible-playbook playbooks/site.yml
```

### Testimine
Avage brauseris: http://[teie-server-ip]

## Testimine

[Kirjeldage, kuidas kontrollida, et kõik töötab]

## Screenshot

[Lisa screenshot töötavast veebirakendusest]

## Probleemid ja lahendused

[Kirjeldage, millised probleemid teil tekkisid ja kuidas lahendasite]

## Kasutatud allikad

- [Ansible dokumentatsioon](https://docs.ansible.com/)
- [Link teisele allikale]
```

### Kontroll enne esitamist

- [ ] GitHubis on avalik repositoorium
- [ ] Inventory fail sisaldab õigeid IP aadresse
- [ ] Vähemalt 4 eraldi playbook'i (system, apache, mysql, php)
- [ ] Template'd on templates/ kaustas
- [ ] Muutujad on group_vars/ kaustas
- [ ] Apache virtual host töötab
- [ ] MySQL andmebaas ja kasutaja on loodud
- [ ] PHP test leht on nähtav brauseris
- [ ] Playbook on idempotentne (teine käivitus ei muuda midagi)
- [ ] README.md on täidetud kõigi nõutud sektsioonidega
- [ ] Screenshot on lisatud
- [ ] Kõik muudatused on GitHubi push'itud

---

## Refleksioon

Lisa oma README.md faili lõppu peatükk "Refleksioon" ja vasta järgmistele küsimustele. Iga vastus peab olema 2-3 lausega.

### 1. Mis oli selle kodutöö juures kõige raskem ja kuidas sa selle lahendasid?

Kirjelda konkreetset tehnilist probleemi, millega kokku puutusid. Näiteks: "Kõige raskem oli mõista, kuidas handlers ja notify töötavad koos. Lahendasin selle lugedes Ansible dokumentatsiooni ja tehes teste väikese playbook'iga."

### 2. Milline Ansible kontseptsioon oli sulle kõige suurem "ahaa!" hetk ja miks?

Kirjelda, milline kontseptsioon või feature tegi sulle selgeks midagi olulist. Näiteks: "Idempotentsus oli mulle suur avastus - võin playbook'i käivitada 100 korda ja tulemus on alati sama. See teeb automatiseerimise palju turvalisemaks."

### 3. Kuidas saaksid Ansible'i kasutada oma tulevikus või teistes projektides?

Kirjelda konkreetseid kasutusjuhte. Näiteks: "Võiksin Ansible'iga automatiseerida oma kodulabori serverite seadistamise. Praegu kulub mul sellele tunde, Ansible'iga võiks see olla 5 minutit."

### 4. Kui peaksid oma sõbrale selgitama, mis on Ansible ja miks see on kasulik, siis mida ütleksid?

Anna lihtne, arusaadav selgitus. Näiteks:
- "Ansible on nagu kaugjuhtimispult serveritele
- ühe käsuga saad seadistada 10 või 100 serverit korraga, kõigil täpselt sama konfiguratsiooniga."

### 5. Mis oli selle projekti juures kõige lõbusam või huvitavam osa?

Kirjelda, mis sulle meeldis või mida huvitav oli õppida. Näitex: "Mulle meeldis template'ide kasutamine - nägin, kuidas samast template'ist tekivad erinevad konfiguratsioonifailid sõltuvalt muutujatest. See on nagu programmeerimine, aga konfiguratsioonifailide jaoks."

---

## Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| Infrastruktuur | 15% | SSH võtmed töötavad, inventory õigesti seadistatud, vähemalt 2 VM-i |
| Playbook kvaliteet | 30% | LAMP stack installeerub edukalt, idempotentne, muutujad korrektselt kasutatud |
| Handlers | 15% | Teenused restarditakse ainult muudatuste korral, handlers õigesti konfigureeritud |
| Koodipraktikad | 15% | Failid organiseeritud, selged nimed, group_vars kasutatud, kood loetav |
| README | 10% | Projekti kirjeldus, seadistamis- ja käivitamisjuhend, selge dokumentatsioon |
| Refleksioon | 15% | Kõik 5 küsimust vastatud, sisukas, näitab mõistmist ja isiklikku õppimist |

Kokku: 100%

---

## Abimaterjalid

Enne kodutöö alustamist lugege läbi:

**Ansible dokumentatsioon:**
- [Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)
- [Variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html)
- [Handlers](https://docs.ansible.com/ansible/latest/user_guide/playbooks_handlers.html)
- [Templates](https://docs.ansible.com/ansible/latest/user_guide/playbooks_templating.html)

**Moodulite dokumentatsioon:**
- `ansible-doc apt` - pakettide installimine
- `ansible-doc service` - teenuste haldamine
- `ansible-doc template` - template'ide kasutamine
- `ansible-doc mysql_db` - MySQL andmebaasid
- `ansible-doc mysql_user` - MySQL kasutajad

**Kui abi vaja:**
1. Kasutage `ansible-doc <module>` dokumentatsiooni vaatamiseks
2. Vaadake Ansible dokumentatsiooni veebis
3. Küsige klassikaaslaselt või õpetajalt
4. StackOverflow: otsige "ansible [teie probleem]"

---

## Boonus

Valikulised täiendused, mis annavad lisapunkte (kokku kuni +10%):

### Ansible Vault (+3%)

Krüpteerige MySQL paroolid Ansible Vault'iga:
```bash
# Looge krüpteeritud fail
ansible-vault create group_vars/all/vault.yml

# Lisage sinna paroolid
mysql_root_password: "secret123"
mysql_app_password: "appsecret456"

# Käivitage playbook vault parooliga
ansible-playbook playbooks/site.yml --ask-vault-pass
```

### Mitme keskkonna tugi (+3%)

Looge eraldi inventory ja muutujad dev ja prod keskkondade jaoks:
```
inventory/
  dev/
    hosts
  prod/
    hosts
group_vars/
  dev/
    main.yml
  prod/
    main.yml
```

### Automaatne testimine (+2%)

Lisage playbook'i lõppu testid, mis kontrollivad teenuste tööd:
```yaml
- name: "Verify all services are running"
  service_facts:
  
- name: "Check Apache"
  assert:
    that:
      - ansible_facts.services['apache2.service'].state == 'running'
      
- name: "Test web page"
  uri:
    url: "http://{{ inventory_hostname }}"
    status_code: 200
```

### SSL sertifikaat (+2%)

Seadistage self-signed SSL sertifikaat ja HTTPS:
```yaml
- name: "Generate SSL certificate"
  command: >
    openssl req -x509 -nodes -days 365 -newkey rsa:2048
    -keyout /etc/ssl/private/apache-selfsigned.key
    -out /etc/ssl/certs/apache-selfsigned.crt
    -subj "/C=EE/ST=Harjumaa/L=Tallinn/O=MyOrg/CN={{ domain_name }}"
  args:
    creates: /etc/ssl/certs/apache-selfsigned.crt
```

---

## Nõuanded

### Kust alustada

1. Alustage lihtsast - tehke ping test
2. Installige Apache käsitsi, siis automatiseerige
3. Lisage järk-järgult MySQL, PHP
4. Viimisena organiseerige failid õigesti

### Debugimine

Verbose režiim rohkem infot saamiseks:
```bash
ansible-playbook playbooks/site.yml -vvv
```

Kuiv käivitus (ei tee muudatusi):
```bash
ansible-playbook playbooks/site.yml --check
```

Vaadake muudatuste diff'i:
```bash
ansible-playbook playbooks/site.yml --diff
```

### Mida MITTE teha

- Paroolid otse koodis
- Kõik ühes suures playbook'is
- SSH parooliga autentimine
- Root kasutaja kasutamine
- Muutujad otse playbook'is vars: sektsioonis
- Hardcoded IP aadressid või kasutajanimed

---

## Tähtis meeles pidada

**Labor vs Kodutöö:**
- Laboris oli OK kõik ühes failis (õppimise eesmärgil)
- Kodutöös peab järgima professionaalset struktuuri
- Laboris näitasime põhitõed, kodutöös rakendate neid õigesti

**Edusammud:**
- Tehke GitHubi commit'e regulaarselt
- Testige iga muudatust kohe
- Alustage lihtsast, lisage keerukust järk-järgult
- Küsige abi kui jääte kinni
- Dokumentatsioon on teie sõber

Edu ja head automatiseerimist!