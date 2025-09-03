# 🧪 Ansible Basics Lab: Setup ja Esimene Playbook

**Kestus:** 2 tundi  
**Eesmärk:** Õppida Ansible'i alused ja luua esimesed automatiseerimise skriptid

## 🎯 Samm 1: Õpiväljundid

Pärast laborit oskate:
- Installida ja konfigureerida Ansible'i
- Seadistada SSH võtmeid turvaliseks ühenduseks
- Luua ja hallata inventory faile
- Kasutada ad-hoc käske kiireks automatiseerimiseks
- Kirjutada YAML süntaksit
- Luua ja käivitada playbook'e
- Automatiseeritult seadistada veebiserveri

---

## 📋 Samm 1: Ansible'i installimine ja seadistamine (30 min)

### 1.1: Ansible'i installimine

**Ubuntu/Debian:**
```bash
# Uuenda pakettide nimekirja
sudo apt update

# Installi Ansible
sudo apt install ansible -y

# Kontrolli installatsiooni
ansible --version
```

**macOS (Homebrew):**
```bash
# Installi Homebrew (kui ei ole)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installi Ansible
brew install ansible

# Kontrolli
ansible --version
```

**Windows (WSL):**
```bash
# Windows'is kasutage Windows Subsystem for Linux
# Seejärel järgige Ubuntu juhendeid
```

### 1.2: SSH võtmete seadistamine

**Miks SSH võtmed on vajalikud:**
- Ansible kasutab SSH'd serveritega ühendumiseks
- Võtmed on turvalisemad kui paroolid
- Automatiseerimine toimib ilma parooli küsimata

**SSH võtme loomine:**
```bash
# Looge SSH võti (kui teil ei ole)
ssh-keygen -t rsa -b 4096 -C "teie.email@example.com"

# Vajutage Enter kõikidele küsimustele (kasutab default asukohti)
# Võite lisada parooli või jätta tühjaks
```

**SSH võtme kopeerimine test serverisse:**
```bash
# Kopeerige avalik võti serverisse
ssh-copy-id kasutaja@test-server.local

# Või käsitsi
cat ~/.ssh/id_rsa.pub | ssh kasutaja@test-server.local "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**Testide ühendust:**
```bash
# Peaks ühenduma ilma parooli küsimata
ssh kasutaja@test-server.local
```

### 1.3: Esimene inventory fail - Serverite "telefoniraamat"

**Esmalt mõistame, mis on inventory:**
- Inventory on fail, kus kirjas kõik serverid, mida Ansible haldab
- See on nagu telefoniraamat - Ansible vaatab sealt, milliseid servereid kontakteeruda
- Saame servereid grupeerida (nt webserverid, andmebaasiserveid)

**Looge töökaust:**
```bash
mkdir ~/ansible-praktikum
cd ~/ansible-praktikum
```

**Nüüd loome inventory faili sammhaaval:**

1. **Looge tühi fail:**
   ```bash
   touch inventory.ini
   ```

2. **Avage fail tekstiredaktoris:**
   ```bash
   nano inventory.ini
   # või
   code inventory.ini
   ```

3. **Lisage esimene server (localhost testimiseks):**
   ```ini
   [test]
   localhost ansible_connection=local
   ```
   
   **Selgitus:**
   - `[test]` = grupi nimi (sulgudes)
   - `localhost` = serveri nimi
   - `ansible_connection=local` = ütleb Ansible'ile, et kasuta lokaalseid käske (SSH pole vaja)

4. **Lisage teine grupp (tuleviku serveritele):**
   ```ini
   [practice]
   # Kommentaar: Siia saate hiljem lisada tegelikke servereid
   # Näide: server1.example.com ansible_user=ubuntu
   ```

5. **Salvestage fail** (Ctrl+X, siis Y, siis Enter nano's)

**Nüüd testima inventory:**
```bash
# Vaatame, kas Ansible näeb meie servereid
ansible -i inventory.ini --list-hosts all

# Peaks näitama: localhost
```

**Testide ühendust:**
```bash
ansible -i inventory.ini test -m ping
```

**❓ Mõtelge:** Miks kasutame `test` mitte `localhost`? (Vastus: test on grupi nimi!)

---

## 📋 Samm 2: Esimesed Ad-hoc käsud (20 min)

### Ad-hoc käskude harjutused

**1. Ping test:**
```bash
# Kontrollige kõiki servereid
ansible -i inventory.ini all -m ping
```

**2. Süsteemi info:**
```bash
# Vaata operatsioonisüsteemi
ansible -i inventory.ini all -m setup -a "filter=ansible_distribution*"

# Vaata mälu ja CPU
ansible -i inventory.ini all -m setup -a "filter=ansible_memtotal_mb,ansible_processor_count"
```

**3. Failide haldamine:**
```bash
# Loo test kaust
ansible -i inventory.ini all -m file -a "path=/tmp/ansible-test state=directory"

# Loo test fail
ansible -i inventory.ini all -m copy -a "content='Ansible test' dest=/tmp/ansible-test/hello.txt"

# Kontrolli faili olemasolu
ansible -i inventory.ini all -m command -a "ls -la /tmp/ansible-test/"
```

**4. Pakettide haldamine:**
```bash
# Installi htop (vajalik sudo)
ansible -i inventory.ini all -m package -a "name=htop state=present" --become

# Kontrolli installatsiooni
ansible -i inventory.ini all -m command -a "which htop"
```

---

## 📋 Samm 3: YAML ja esimene playbook (40 min)

### YAML süntaksi harjutus - Õpime "inimese keelt"

**Miks YAML on oluline:**
- Ansible playbook'id on kirjutatud YAML keeles
- YAML on disainitud inimesele loetavaks
- Taandrimine (indentation) on VÄGA oluline!

**Loome YAML faili sammhaaval:**

1. **Looge uus fail:**
   ```bash
   touch test.yml
   nano test.yml  # või code test.yml
   ```

2. **Alustage YAML dokumendiga:**
   ```yaml
   ---
   # YAML alustab alati kolme kriipsuga
   # Hashtag (#) on kommentaar
   ```

3. **Lisage lihtne väärtus:**
   ```yaml
   nimi: "Minu Ansible Test"
   versioon: 1.0
   ```
   **Märkus:** Jutumärgid on vabatahtlikud, aga hea praktika tekstile

4. **Lisage loend (list):**
   ```yaml
   serverid:
     - nimi: "test1"
       ip: "192.168.1.10"
       roll: "veebiserver"
     - nimi: "test2"
       ip: "192.168.1.11"
       roll: "andmebaas"
   ```
   **Tähelepanu:** 
   - Kriips (-) tähistab loendi elementi
   - Taandrimine peab olema täpne (kasutage 2 tühikut)
   - ÄRA kasutage Tab klahvi!

5. **Lisage seadistused:**
   ```yaml
   seadistused:
     http_port: 80
     https_port: 443
     debug: true
   ```

6. **Salvestage fail**

**Kontrollige süntaksi:**
```bash
# Python abil (kui on installitud)
python3 -c "import yaml; print(yaml.safe_load(open('test.yml')))"

# Ansible abil
ansible-playbook --syntax-check test.yml
```

**❓ Harjutus:** Muutke `debug: true` väärtuseks `false` ja kontrollige uuesti!

### Esimene lihtne playbook - Sammhaaval ehitamine

**Mõistame playbook struktuuri:**
- **Play** = üks stsenaarium ühe grupi serveritele
- **Tasks** = konkreetsed sammud, mida teha
- **Modules** = Ansible'i ehitatud funktsioonid (debug, file, copy jne)

**Loome playbook samm-sammult:**

1. **Looge uus fail:**
   ```bash
   touch minu-esimene-playbook.yml
   nano minu-esimene-playbook.yml
   ```

2. **Alustage YAML ja Play definitsiooniga:**
   ```yaml
   ---
   - name: "Minu esimene Ansible playbook"
     hosts: all
     gather_facts: yes
   ```
   **Selgitus:**
   - `name:` = playbook'i kirjeldus
   - `hosts: all` = käivita kõikidele serveritele inventory's
   - `gather_facts: yes` = kogu serveri infot (OS, IP, jne)

3. **Lisage tasks sektsioon:**
   ```yaml
     tasks:
   ```

4. **Esimene task - lihtne tervitus:**
   ```yaml
       - name: "Tervita maailma"
         debug:
           msg: "Tere! Ansible töötab {{ inventory_hostname }} serveris!"
   ```
   **Märkuseid:**
   - `debug` = moodul sõnumite väljastamiseks
   - `{{ inventory_hostname }}` = muutuja (server nimi)

5. **Teine task - näita süsteemi infot:**
   ```yaml
       - name: "Näita süsteemi infot"
         debug:
           msg: "Server töötab {{ ansible_distribution }} {{ ansible_distribution_version }}"
   ```

6. **Kolmas task - loo kaust:**
   ```yaml
       - name: "Loo test kataloog"
         file:
           path: /tmp/ansible-praktikum
           state: directory
           mode: '0755'
   ```
   **Selgitus:**
   - `file` = moodul failide/kaustade haldamiseks
   - `state: directory` = veendu, et see on kaust
   - `mode: '0755'` = määra õigused (rwx r-x r-x)

7. **Neljas task - kirjuta fail:**
   ```yaml
       - name: "Kirjuta info fail"
         copy:
           dest: /tmp/ansible-praktikum/info.txt
           mode: '0644'
           content: |
             Ansible playbook käivitatud: {{ ansible_date_time.iso8601 }}
             Serveri nimi: {{ inventory_hostname }}
             IP aadress: {{ ansible_default_ipv4.address | default('ei tuvastatud') }}
   ```
   **Märkuseid:**
   - `content: |` = mitme-realine tekst
   - `{{ ansible_date_time.iso8601 }}` = praegune kuupäev

8. **Viies task - loe fail:**
   ```yaml
       - name: "Kuva faili sisu"
         command: cat /tmp/ansible-praktikum/info.txt
         register: faili_sisu
   ```
   **Selgitus:**
   - `command` = käivita shell käsk
   - `register` = salvesta väljund muutujasse

9. **Kuues task - näita tulemust:**
   ```yaml
       - name: "Näita, mis failis on"
         debug:
           msg: "{{ faili_sisu.stdout_lines }}"
   ```

10. **Salvestage fail**

**Nüüd testima meie playbook'i:**

1. **Esmalt kuiv käivitus (dry run):**
   ```bash
   ansible-playbook -i inventory.ini --check minu-esimene-playbook.yml
   ```
   **Mis juhtub:** Ansible näitab, mida ta teeks, aga ei muuda midagi

2. **Kui kuiv käivitus õnnestus, siis tegelik käivitus:**
   ```bash
   ansible-playbook -i inventory.ini minu-esimene-playbook.yml
   ```

3. **Vaadake tulemust:**
   - Kas kõik taskid õnnestusid (roheline)?
   - Kontrollige, kas fail tekkis: `ls -la /tmp/ansible-praktikum/`

**❓ Debugimise küsimused:**
- Mida tähendab "changed" vs "ok"?
- Miks mõned taskid on "changed" ja teised "ok"?
- Käivitage playbook uuesti - mis muutub?

### Playbook muutujatega - Õpime dünaamilisust

**Miks muutujad on olulised:**
- Teevad playbook'i korduvkasutatavaks
- Võimaldavad erinevaid konfiguratsioone
- Lihtsustavad muudatuste tegemist

**Loome muutujatega playbook sammhaaval:**

1. **Uus fail:**
   ```bash
   touch playbook-muutujatega.yml
   nano playbook-muutujatega.yml
   ```

2. **Play definitsioon muutujatega:**
   ```yaml
   ---
   - name: "Playbook muutujatega"
     hosts: all
     vars:
       rakenduse_nimi: "Minu Veebirakendus"
       versioon: "1.2.3"
       portnumber: 8080
       
     tasks:
   ```

3. **Task 1 - Dünaamiline kausta nimi:**
   ```yaml
       - name: "Loo rakenduse kaust"
         file:
           path: "/opt/{{ rakenduse_nimi | lower | replace(' ', '-') }}"
           state: directory
           mode: '0755'
         become: yes
   ```
   **Selgitused:**
   - `{{ rakenduse_nimi }}` = kasuta muutujat
   - `| lower` = muuda väikesteks tähtedeks
   - `| replace(' ', '-')` = asenda tühikud kriipsudega

4. **Task 2 - Dünaamiline konfiguratsioon:**
   ```yaml
       - name: "Kirjuta konfiguratsioon"
         copy:
           dest: "/opt/{{ rakenduse_nimi | lower | replace(' ', '-') }}/config.env"
           mode: '0644'
           content: |
             # {{ rakenduse_nimi }} konfiguratsioon
             APP_NAME={{ rakenduse_nimi }}
             VERSION={{ versioon }}
             PORT={{ portnumber }}
             INSTALLED_ON={{ ansible_date_time.iso8601 }}
         become: yes
   ```

5. **Task 3 - Kuva tulemus:**
   ```yaml
       - name: "Kuva konfiguratsioon"
         command: "cat /opt/{{ rakenduse_nimi | lower | replace(' ', '-') }}/config.env"
         register: config_sisu
         become: yes
       
       - name: "Näita konfiguratsiooni"
         debug:
           msg: "{{ config_sisu.stdout_lines }}"
   ```

6. **Käivita ja eksperimenteerige:**
   ```bash
   ansible-playbook playbook-muutujatega.yml
   ```

**❓ Harjutus:**
1. Muutke `rakenduse_nimi` muutujat
2. Käivitage playbook uuesti
3. Vaadake, kuidas tulemus muutub

**💡 Lisaharjutus:** Lisage uus muutuja `kirjeldus` ja kasutage seda config failis!

---

## 📋 Samm 4: Veebiserveri seadistamine (30 min)

### Nginx playbook - Automatiseeritud veebiserver

**Nüüd loome keerulisema playbook'i sammhaaval:**

**Miks Nginx:**
- Populaarne veebiserver
- Lihtne seadistada
- Hea näide produktsiooni-lähedase automatiseerimise kohta

**Loome Nginx playbook etappide kaupa:**

1. **Alustage uue failiga:**
   ```bash
   touch nginx-setup.yml
   nano nginx-setup.yml
   ```

2. **Play definitsioon muutujatega:**
   ```yaml
   ---
   - name: "Nginx veebiserveri seadistamine"
     hosts: all
     become: yes
     vars:
       web_root: "/var/www/html"
       site_name: "Minu Test Sait"
       
     tasks:
   ```
   **Märkuseid:**
   - `become: yes` = kasuta sudo õiguseid kõikides tasks'ides
   - `vars:` = playbook'i muutujad

3. **Task 1 - Süsteemi ettevalmistus:**
   ```yaml
       - name: "Uuenda pakettide nimekirja"
         package:
           update_cache: yes
         when: ansible_os_family == "Debian"
   ```
   **Selgitus:** `when:` = conditional - käivita ainult Debian/Ubuntu's

4. **Task 2 - Nginx installimine:**
   ```yaml
       - name: "Installi Nginx"
         package:
           name: nginx
           state: present
   ```

5. **Task 3 - Veebi kausta loomine:**
   ```yaml
       - name: "Loo veebi kaust"
         file:
           path: "{{ web_root }}"
           state: directory
           owner: www-data
           group: www-data
           mode: '0755'
         when: ansible_os_family == "Debian"
   ```
   **Märkuseid:**
   - `{{ web_root }}` = kasutab muutujat
   - `owner/group: www-data` = nginx kasutaja

6. **Task 4 - Lihtsa HTML lehe loomine:**
   ```yaml
       - name: "Kopeeri HTML lehekülg"
         copy:
           dest: "{{ web_root }}/index.html"
           owner: www-data
           group: www-data
           mode: '0644'
           content: |
             <!DOCTYPE html>
             <html lang="et">
             <head>
                 <meta charset="UTF-8">
                 <title>{{ site_name }}</title>
                 <style>
                     body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                     .container { max-width: 600px; margin: 0 auto; }
                     .success { color: green; }
                     .info { background: #f0f0f0; padding: 20px; border-radius: 5px; }
                 </style>
             </head>
             <body>
                 <div class="container">
                     <h1 class="success">🎉 {{ site_name }}</h1>
                     <p>Nginx on edukalt paigaldatud Ansible'iga!</p>
                     <div class="info">
                         <h3>Serveri info:</h3>
                         <p><strong>Hostname:</strong> {{ inventory_hostname }}</p>
                         <p><strong>Süsteem:</strong> {{ ansible_distribution }} {{ ansible_distribution_version }}</p>
                         <p><strong>Paigaldatud:</strong> {{ ansible_date_time.iso8601 }}</p>
                     </div>
                 </div>
             </body>
             </html>
         when: ansible_os_family == "Debian"
   ```

7. **Task 5 - Nginx käivitamine:**
   ```yaml
       - name: "Käivita ja luba Nginx"
         service:
           name: nginx
           state: started
           enabled: yes
   ```
   **Selgitus:**
   - `state: started` = veendu, et teenus töötab
   - `enabled: yes` = käivita automaatselt boot'imisel

8. **Task 6 - Valideerimised:**
   ```yaml
       - name: "Kontrolli Nginx olekut"
         command: systemctl is-active nginx
         register: nginx_status
         failed_when: false
       
       - name: "Näita Nginx olekut"
         debug:
           msg: "Nginx olek: {{ nginx_status.stdout }}"
       
       - name: "Testi veebiserveri ühendust"
         uri:
           url: "http://localhost"
           return_content: yes
         register: web_test
         failed_when: false
       
       - name: "Näita veebiserveri vastust"
         debug:
           msg: "Veebiserver töötab! HTTP kood: {{ web_test.status | default('Ei saanud ühendust') }}"
   ```
   **Märkuseid:**
   - `uri` moodul = HTTP päringute tegemiseks
   - `failed_when: false` = ära lõpeta vea korral

9. **Salvestage fail**

**Nüüd testima Nginx playbook'i:**

1. **Süntaksi kontroll:**
   ```bash
   ansible-playbook --syntax-check nginx-setup.yml
   ```

2. **Kuiv käivitus:**
   ```bash
   ansible-playbook --check nginx-setup.yml
   ```
   **Vaadake:** Millised taskid näitavad "changed"?

3. **Tegelik käivitus:**
   ```bash
   ansible-playbook nginx-setup.yml
   ```

4. **Tulemuse testimine:**
   ```bash
   # Kontrolli Nginx protsessi
   sudo systemctl status nginx
   
   # Kontrolli, kas port 80 on avatud
   sudo netstat -tlnp | grep :80
   
   # Testi HTTP päringuga
   curl http://localhost
   ```

5. **Brauseris (kui GUI on):**
   - Avage http://localhost
   - Peaks näitama ilusat HTML lehte

**❓ Analüüsige:**
- Mitu "changed" oli esimesel käivitusel?
- Käivitage playbook uuesti - mitu "changed" nüüd?
- Miks see nii on? (Hint: idempotency!)

**🔧 Troubleshooting:**
- Kui Nginx ei käivitu, kontrollige: `sudo journalctl -u nginx`
- Kui port kinni, vaadake: `sudo ss -tlnp | grep :80`

---

## 📋 Samm 5: Ansible konfiguratsiooni optimeerimine (20 min)

### ansible.cfg seadistamine - Mugavuse suurendamine

**Miks ansible.cfg on kasulik:**
- Ei pea iga kord `-i inventory.ini` kirjutama
- Paremad vaikimisi seadistused
- SSH optimeeringud

**Loome konfiguratsiooni sammhaaval:**

1. **Loo fail:**
   ```bash
   touch ansible.cfg
   nano ansible.cfg
   ```

2. **Lisage põhiseadistused:**
   ```ini
   [defaults]
   # Inventory faili asukoht (nüüd ei pea -i iga kord kirjutama)
   inventory = inventory.ini
   ```

3. **SSH seadistused (et vältida vigu):**
   ```ini
   # SSH seadistused
   host_key_checking = False
   remote_user = kasutaja
   private_key_file = ~/.ssh/id_rsa
   ```
   **Selgitus:**
   - `host_key_checking = False` = ei küsi SSH fingerprinte
   - `remote_user` = default kasutajanimi serverites

4. **Väljundi parandused:**
   ```ini
   # Väljundi seadistused
   stdout_callback = yaml
   pipelining = True
   ```
   **Miks:** YAML väljund on inimesele loetavam

5. **Performance seadistused:**
   ```ini
   # Paralleelsus (kui palju serveritega korraga töötab)
   forks = 10
   
   # Logimise seadistused  
   log_path = ./ansible.log
   ```

6. **SSH optimeeringud (täiendav sektsioon):**
   ```ini
   [ssh_connection]
   # SSH optimeeringud
   ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o UserKnownHostsFile=/dev/null
   timeout = 30
   retries = 3
   ```

7. **Salvestage ja testiga:**
   ```bash
   # Nüüd saate käivitada ilma -i liputa!
   ansible all -m ping
   ```

**Teste konfiguratsiooni:**
```bash
# Nüüd ei pea -i inventory.ini määrama
ansible all -m ping

# Logi kontrollimise
tail -f ansible.log
```

---

## 📋 Samm 6: Veatuvastus ja probleemide lahendamine (20 min)

### Levinud probleemid ja lahendused

**1. SSH ühenduse probleemid:**
```bash
# Kontrolli SSH ühendust käsitsi
ssh -v kasutaja@target-host

# SSH võtme probleemid
ssh-add ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

**2. Sudo õiguste probleemid:**
```bash
# Testide sudo õiguseid
ansible all -m command -a "whoami" --become

# Sudo parooli küsimine
ansible all -m command -a "whoami" --become --ask-become-pass
```

**3. Python teegi probleemid:**
```bash
# Kontrolli Python'i
ansible all -m setup -a "filter=ansible_python*"

# Määra Python'i asukoht
ansible all -m ping -e ansible_python_interpreter=/usr/bin/python3
```

### Debugimise playbook - Õpime tõrkeid leidma

**Miks debug playbook on vajalik:**
- Aitab mõista, millised muutujad on saadaval
- Kontrollib SSH ja sudo seadistusi
- Näitab Python'i konfiguratsiooni

**Loome debug playbook etappide kaupa:**

1. **Alustage uue failiga:**
   ```bash
   touch debug-playbook.yml
   nano debug-playbook.yml
   ```

2. **Play definitsioon:**
   ```yaml
   ---
   - name: "Debug ja veatuvastus"
     hosts: all
     gather_facts: yes
     
     tasks:
   ```

3. **Task 1 - Näita süsteemi muutujaid:**
   ```yaml
       - name: "Näita operatsioonisüsteemi"
         debug:
           msg: "OS: {{ ansible_distribution }} {{ ansible_distribution_version }}"
   ```

4. **Task 2 - Kontrolli kasutajat:**
   ```yaml
       - name: "Kontrolli SSH kasutaja"
         command: whoami
         register: current_user
       
       - name: "Näita kasutaja infot"
         debug:
           msg: "SSH kasutaja: {{ current_user.stdout }}, Ansible kasutaja: {{ ansible_user_id }}"
   ```
   **Selgitus:** `register` salvestab käsu väljundi muutujasse

5. **Task 3 - Kontrolli sudo:**
   ```yaml
       - name: "Kontrolli sudo õiguseid"
         command: whoami
         become: yes
         register: sudo_user
         failed_when: false
   ```
   **Märkus:** `failed_when: false` = ära lõpeta vea korral

6. **Task 4 - Näita sudo tulemust:**
   ```yaml
       - name: "Näita sudo tulemust"
         debug:
           msg: "Sudo kasutaja: {{ sudo_user.stdout | default('Sudo ei toimi') }}"
   ```

7. **Task 5 - Kontrolli Python'i:**
   ```yaml
       - name: "Kontrolli Python'i"
         debug:
           msg: "Python: {{ ansible_python_interpreter | default(ansible_python.executable) }}"
   ```

8. **Käivita ja analüüsi:**
   ```bash
   ansible-playbook debug-playbook.yml -v
   ```
   **Märkus:** `-v` flag annab rohkem detaile

**Käivita debug playbook:**
```bash
ansible-playbook debug-playbook.yml -v
```

---

## 🎯 Samm 2: Labi hindamine ja reflektsioon

### Tehnilised saavutused

Kontrollige, et järgmised asjad toimivad:

- [ ] **Ansible töötab** - `ansible --version` näitab versiooni
- [ ] **SSH ühendus toimib** - saate serveritesse ühenduda ilma paroolita
- [ ] **Inventory on funktsionaalne** - `ansible all -m ping` tagastab "pong"
- [ ] **Ad-hoc käsud töötavad** - saate hallata faile ja pakette
- [ ] **YAML süntaks on selge** - mõistate taandrimist ja struktuuri
- [ ] **Esimene playbook toimib** - kõik taskid õnnestuvad (roheline väljund)
- [ ] **Muutujad töötavad** - saate muuta konfiguratsiooni muutujate kaudu
- [ ] **Nginx on käigus** - `curl http://localhost` tagastab HTML
- [ ] **Konfiguratsioon optimeeritud** - `ansible.cfg` on seadistatud

### Kontseptuaalne mõistmine

**❓ Kontrollige oma mõistmist:**

1. **Ansible arhitektuur:**
   - Selgitage oma sõnadega, miks Ansible on "agentless"
   - Mis vahe on "control node" ja "managed node" vahel?

2. **Idempotency:**
   - Miks saab playbook'e turvaliselt korduvalt käivitada?
   - Mis vahe on "changed" ja "ok" state'il?

3. **YAML ja muutujad:**
   - Miks on taandrimine YAML's nii oluline?
   - Kuidas muutujad teevad playbook'i korduvkasutatavaks?

4. **SSH ja turvalisus:**
   - Miks on SSH võtmed paremad kui paroolid?
   - Kuidas Ansible tagab turvalise kommunikatsiooni?

### Praktilised oskused

**🔧 Proovige ise:**

1. **Muutke Nginx playbook'i:**
   - Lisage uus muutuja `server_admin_email`
   - Muutke HTML template'i seda kasutama

2. **Looge uus playbook:**
   - Installige htop ja tree paketid
   - Looge `/opt/tools/` kaust
   - Kirjutage info fail installitud tööriistade kohta

3. **Eksperimenteerige ad-hoc käskudega:**
   - Kontrollige kõigi serverite disk space'i
   - Looge fail kõikides serverites praeguse kuupäeva ja ajaga

### Valmidus järgmiseks

**Te olete valmis kodutööks, kui:**
- Mõistate Ansible'i põhikontseptsioone
- Saate kirjutada lihtsat YAML süntaksit
- Oskate kasutada muutujaid ja template'e
- Mõistate playbook'ide struktuuri
- Saate tõrkeid diagnoosida ja lahendada

## 🚀 Järgmised sammud

**Valmis kodutööks:**
- Kasutage siin õpitud oskusi LAMP stack playbook'i loomiseks
- Rakendage learned patterns oma serverite automatiseerimiseks
- Praktiseerige YAML süntaksit ja playbook struktuuri

**Järgmine nädal (Ansible Advanced):**
- Roles ja Galaxy
- Templates ja Jinja2
- Conditional logic ja loops
- Multi-environment deployments

---

## 🚀 **BOONUSÜLESANDED** (juba Ansible'i oskajatele)

### B1: Advanced Playbook Patterns (30 min)

```yaml
# Advanced inventory and variables
---
- name: Advanced Ansible patterns
  hosts: webservers
  vars:
    nginx_configs:
      - { name: "api", port: 3000, upstream: "app_servers" }
      - { name: "admin", port: 4000, upstream: "admin_servers" }
    
  tasks:
    # Dynamic configuration generation
    - name: Generate nginx configs
      template:
        src: nginx-site.j2
        dest: "/etc/nginx/sites-available/{{ item.name }}"
      loop: "{{ nginx_configs }}"
      notify: reload nginx

    # Conditional deployments
    - name: Deploy based on environment
      git:
        repo: "{{ app_repo }}"
        dest: "/var/www/{{ app_name }}"
        version: "{{ 'main' if environment == 'production' else 'develop' }}"
      when: deployment_enabled | default(false)
```

### B2: Error Handling ja Performance (25 min)

```yaml
---
- name: Advanced error handling
  hosts: all
  tasks:
    # Retry with exponential backoff
    - name: Download with retries
      get_url:
        url: "{{ app_url }}"
        dest: "/tmp/app.tar.gz"
      register: download
      retries: 5
      delay: "{{ 2 ** (ansible_loop.index0) }}"
      until: download is succeeded

    # Block/rescue/always pattern
    - name: Safe deployment
      block:
        - name: Deploy application
          unarchive:
            src: "/tmp/app.tar.gz"
            dest: "/var/www/"
      rescue:
        - name: Rollback on failure
          debug:
            msg: "Deployment failed, rolling back..."
      always:
        - name: Cleanup
          file:
            path: "/tmp/app.tar.gz"
            state: absent
```

### B3: Custom Modules ja Advanced Features (20 min)

```bash
# Custom filter plugin
mkdir -p filter_plugins
cat > filter_plugins/custom.py << 'EOF'
class FilterModule(object):
    def filters(self):
        return {'custom_hash': self.custom_hash}
    
    def custom_hash(self, data):
        import hashlib
        return hashlib.md5(str(data).encode()).hexdigest()[:8]
EOF

# Use in playbook
ansible-playbook -i inventory advanced.yml
```

### B4: Ansible Vault ja Security (15 min)

```bash
# Create encrypted variables
ansible-vault create secrets.yml
ansible-vault edit secrets.yml

# Use in playbook
ansible-playbook site.yml --ask-vault-pass

# Vault in CI/CD
echo "vault_password" > .vault_pass
ansible-playbook site.yml --vault-password-file .vault_pass
```

**Hästi tehtud! 🎉** Te olete nüüd võimelised automatiseerima nii põhilisi kui ka keerukamaid serverihalduse ülesandeid Ansible'iga!
