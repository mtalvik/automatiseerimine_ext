#  Ansible Labor: Põhitõed (3×45 min)

## Lab'i eesmärk
Täna õpid Ansible põhitõdesid ja harjutad serverite automatiseerimist. Ansible on nagu kaugjuhtimispult sadadele serveritele korraga! 

##  Õpiväljundid
Pärast seda lab'i oskad:
- Seadistada SSH ja inventory faili
- Kirjutada esimesi playbook'e YAML'is
- Kasutada ad-hoc käske kiireks serverite haldamiseks
- Mõista idempotentsuse printsiipi

---

### Blokk 1 (45 min) – SSH setup ja esimene ad-hoc käsk
- **Tegevused:**
  - SSH võtmete genereerimine ja kopeerimine
  - Inventory faili loomine
  - `ansible all -m ping` - esimene test
  - `ansible all -m command` - ad-hoc käsud
- **Kontrollnimekiri:**
  - [ ] SSH töötab ilma paroolita
  - [ ] Inventory fail on loodud
  - [ ] `ansible all -m ping` tagastab SUCCESS
- **Kontrollküsimus:** "Miks on SSH võtmed paremad kui paroolid?"
- **Refleksioon (1 min):** "Kui Ansible oleks superjõud, siis milline? A) telepatia B) kloonimine C)  ajareisimine"

---

### Blokk 2 (45 min) – Esimene playbook ja YAML
- **Tegevused:**
  - YAML süntaksi tutvustus (indentation!)
  - Esimene playbook (nginx installimine)
  - `ansible-playbook` käsu kasutamine
  - Idempotentsuse testimine (jooksuta 2×)
- **Kontrollnimekiri:**
  - [ ] Playbook on kirjutatud (YAML korrektne)
  - [ ] Nginx on installeeritud
  - [ ] Teine run näitab "changed: 0" (idempotent!)
- **Kontrollküsimus:** "Mis on idempotence ja miks see oluline?"
- **Refleksioon (1 min):** "YAML on nagu... A) Python (tühikud on tähtsad!) B) JSON ilma sulgudeta C) mõlemad"

---

### Blokk 3 (45 min) – Variables ja handlers
- **Tegevused:**
  - Variables deklareerimine (`vars:`)
  - `{{ variable }}` kasutamine
  - Handlers (nginx restart on change)
  - `notify` direktiiv
- **Kontrollnimekiri:**
  - [ ] Variables toimivad playbook'is
  - [ ] Handler restartib nginx'i ainult muudatuse korral
  - [ ] Mõistad, millal handler triggerib
- **Kontrollküsimus:** "Mis vahe on task ja handler vahel?"
- **Refleksioon (1 min):** "Kuidas sa selgitaksid Ansible'i oma vanaisale? "

---

**Valmis? Alustame detailsete sammudega!** ⬇

---

##  SETUP: 2 VM ETTEVALMISTUS

### Teie VM-id:
- **VM1:** ansible-controller (näiteks 192.168.56.10)
- **VM2:** web-server (näiteks 192.168.56.11)

### SAMM 1: Kasutajate loomine

** KONTEKST:** Praegu oled kas root või ubuntu kasutajana. Loome uue kasutaja Ansible jaoks.

```bash
# MÕLEMAS VM-is teeme sama kasutaja
# Kontrolli kes sa praegu oled:
whoami                    # Näitab: root või ubuntu

# Loo uus kasutaja nimega 'ansible'
sudo adduser ansible
# Parool: ansible123
# Full Name jne: võid tühjaks jätta (Enter)

# Lisa sudo õigused
sudo usermod -aG sudo ansible

# NÜÜD VAHETA ansible kasutajale
su - ansible
# Sisesta äsja loodud parool: ansible123

# Kontrolli
whoami                    # Peaks näitama: ansible
pwd                       # Peaks näitama: /home/ansible
groups                    # Peaks näitama: ansible sudo
```

** KAS ANSIBLE VAJAB SUDO ÕIGUSI?**

**Lühike vastus:** JAH ja EI - oleneb mida teete!

** EI VAJA sudo õigusi:**
- Failide kopeerimine oma kausta
- Info kogumine (osaliselt)
- Käskude käivitamine tavakasutajana

** VAJAB sudo õigusi:**
- Tarkvara installimine (apt, yum)
- Süsteemifailide muutmine (/etc/...)
- Teenuste haldamine (nginx restart)
- Kasutajate loomine
- Firewall reeglid

** KUIDAS ANSIBLE SUDO KASUTAB:**

```yaml
# Playbook'is - kogu playbook sudo õigustega
- name: "Install software"
  hosts: webservers
  become: yes                     # Kasuta sudo KÕIGI taskide jaoks
  become_user: root              # Millise kasutajana (vaikimisi root)
  
  tasks:
    - name: "Install nginx"      # See käivitatakse kui: sudo apt install nginx
      apt:
        name: nginx
        state: present
```

```yaml
# VÕI ainult kindla taski jaoks
- name: "Mixed tasks"
  hosts: webservers
  
  tasks:
    - name: "Check file"          # See EI kasuta sudo
      stat:
        path: /tmp/test.txt
    
    - name: "Install package"     # See KASUTAB sudo
      apt:
        name: htop
        state: present
      become: yes                 # Ainult see task vajab sudo
```

** KASUTAJA KONTEKST:**
- **Alguses:** root või ubuntu (VM-i vaikekasutaja)
- **Pärast:** ansible (meie loodud kasutaja)
- **Edaspidi:** KÕIK tegevused ansible kasutajana!

### SAMM 2: SSH setup

** OLULINE:** SSH võtmed on KASUTAJA-PÕHISED! Iga kasutaja hoiab oma võtmeid oma kodukaustas.

```bash
# KONTROLL - kes sa oled ja kus sa oled?
whoami                    # Peaks näitama: ansible
pwd                       # Peaks näitama: /home/ansible

# VM2 - kontrolli et SSH server töötab
sudo systemctl status ssh
# Kui ei tööta:
sudo apt install openssh-server -y
sudo systemctl enable --now ssh

# VM1 - genereeri SSH võti ANSIBLE kasutaja jaoks
# Oled ansible kasutajana? Kui ei, siis:
su - ansible
# Sisesta ansible kasutaja parool

# Nüüd genereeri võti
ssh-keygen -t ed25519
# Enter file: vajuta ENTER (vaikimisi /home/ansible/.ssh/id_ed25519)
# Passphrase: vajuta ENTER (ilma paroolita)
# Passphrase again: vajuta ENTER

# VAATA kus su võtmed on:
ls -la ~/.ssh/
# Peaksid nägema:
# id_ed25519        (PRIVATE KEY - hoia saladuses!)
# id_ed25519.pub    (PUBLIC KEY - selle kopeerid teistesse serveritesse)

# Vaata oma avalikku võtit
cat ~/.ssh/id_ed25519.pub
# Näed midagi sellist:
# ssh-ed25519 AAAAC3NzaC1... ansible@ansible-controller

# Kopeeri võti VM2-te ANSIBLE kasutajale
ssh-copy-id ansible@192.168.56.11
# See käsk:
# 1. Võtab SU avaliku võtme (/home/ansible/.ssh/id_ed25519.pub)
# 2. Kopeerib selle VM2 ansible kasutaja kausta
# 3. Lisab selle faili /home/ansible/.ssh/authorized_keys VM2-s

# Sisesta VIIMAST korda ansible@VM2 parool

# TEST - ei tohi parooli küsida
ssh ansible@192.168.56.11
hostname
exit
```

** KUS VÕTMED ASUVAD:**
- **VM1:** `/home/ansible/.ssh/` - ansible kasutaja kodukaustas
  - `id_ed25519` - privaatne võti (ÄRA jaga!)
  - `id_ed25519.pub` - avalik võti (selle kopeerid)
  
- **VM2:** `/home/ansible/.ssh/authorized_keys` - lubatud võtmete nimekiri

** MIS JUHTUB:**
1. ansible@VM1 genereerib võtmepaari
2. Avalik võti kopeeritakse ansible@VM2 authorized_keys faili
3. Nüüd saab ansible@VM1 logida ansible@VM2 ilma paroolita

** TÄHTIS:**
- Võtmed on KASUTAJA kohased - ansible kasutaja võti töötab ainult ansible kasutajaga
- Kui lood root võtme, see töötab ainult root'iga
- Iga kasutaja hoiab võtmeid oma ~/.ssh/ kaustas

---

##  OSA 1: ANSIBLE INSTALL JA INVENTORY

### SAMM 3: Ansible installimine

```bash
# AINULT VM1 vajab Ansible't!
# VM1 peal (ansible kasutajana)
sudo apt update
sudo apt install ansible -y

# Kontrolli
ansible --version
```

### SAMM 4: Projekt ja inventory

```bash
# VM1 peal
mkdir ~/ansible_tutorial
cd ~/ansible_tutorial

# Inventory fail - serverite nimekiri
nano inventory.ini
```

```ini
# Ansible controller (VM1)
[control]
localhost ansible_connection=local

# Web server (VM2) 
[webservers]
web1 ansible_host=192.168.56.11 ansible_user=ansible

# Kõik serverid
[all:children]
control
webservers
```

** MUUDA:** `192.168.56.11` asenda oma VM2 IP-ga!

### SAMM 5: Testi ühendust

```bash
# Ping test - kontrollib kas Ansible saab ühendust
ansible -i inventory.ini all -m ping

# Peate nägema:
# localhost | SUCCESS => { "ping": "pong" }
# web1 | SUCCESS => { "ping": "pong" }
```

** Kui ei tööta:**
- Kontrolli IP: `ip addr show`
- Kontrolli SSH: `ssh ansible@<VM2-IP>`
- Kontrolli inventory fail

---

##  OSA 2: AD-HOC KÄSUD

Sedalaadi kasutamist nimetatakse tavaliselt ad-hoc kasutamiseks ning kasutada saab kõiki moodulite parameetreid. Ansible kasutab kõigi asjade tegemiseks mooduleid. Nende abil paigaldab ta tarkvara, kopeerib faile jne.

```bash
# Käivitame kõigi hosts failis olevate masinate pihta moodulit ping 
# ja kontrollime kas serverid on võimelised meile vastama
ansible -i inventory.ini all -m ping

# Küsime serveritelt hostname käsku
ansible -i inventory.ini all -m shell -a "hostname"

# Küsime infot operatsioonisüsteemi kohta
ansible -i inventory.ini webservers -m shell -a "lsb_release -a"

# Kopeerime faili kõigisse masinatesse aktiivses kataloogis oleva test.txt faili
echo "Test from Ansible" > test.txt
ansible -i inventory.ini webservers -m copy -a "src=test.txt dest=/tmp/"

# Kontrollime kas fail jõudis kohale
ansible -i inventory.ini webservers -m shell -a "cat /tmp/test.txt"

# Samamoodi võib käsurealt otse teha ka jõhkramaid toiminguid, nt midagi installida
ansible -i inventory.ini webservers -m apt -a "name=htop state=present" --become --ask-become-pass

# Tekitame kasutaja ja genereerime talle parooli
ansible -i inventory.ini webservers -m user -a "name=testuser shell=/bin/bash home=/home/testuser password={{ 'parool123' | password_hash('sha512') }}" --become --ask-become-pass

# Kõigi masina poolt saadaolevate muutujate vaatamiseks
ansible -i inventory.ini webservers -m setup -a "filter=ansible_distribution*"

# Kindlas grupis nt grupis webservers käskude käivitamiseks
ansible -i inventory.ini webservers -m ping
```

** PARAMEETRITE SELGITUS:**
- `-i inventory.ini` = millisest failist serverite nimekirja võtta
- `-m mooduli_nimi` = millist moodulit kasutada (ping, shell, copy, apt, user, setup)
- `-a "argumendid"` = argumendid moodulile
- `--become` = kasuta sudo õigusi (varem oli -s)
- `--ask-become-pass` = küsi sudo parooli
- `-l grupp` = käivita ainult kindlas grupis

**Kõigi kasutatavate moodulite nimekirja leiab:** https://docs.ansible.com/ansible/latest/modules/modules_by_category.html

** PARAMEETRID:**
- `-i inventory.ini` = kasuta seda inventory't
- `-m module_name` = moodul (ping, shell, copy, apt)
- `-a "arguments"` = argumendid moodulile
- `--become` = kasuta sudo

---

##  OSA 3: ESIMENE PLAYBOOK

Playbook = YAML fail ülesannetega

```bash
# Loo playbooks kaust
mkdir playbooks
nano playbooks/01_info.yml
```

```yaml
---
# Kolm kriipsu = YAML algus
- name: "System information gathering"
  hosts: all                      # Kõik serverid
  gather_facts: yes                # Kogu automaatselt infot
  
  tasks:                          # Ülesanded
    - name: "Print hostname"
      debug:
        msg: "Hostname: {{ ansible_hostname }}"
    
    - name: "Print OS info"
      debug:
        msg: |
          OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
          IP: {{ ansible_default_ipv4.address }}
          Memory: {{ ansible_memtotal_mb }} MB
          CPU cores: {{ ansible_processor_cores }}
    
    - name: "Create test directory"
      file:
        path: /tmp/ansible-test
        state: directory
        mode: '0755'
```

```bash
# Käivita
ansible-playbook -i inventory.ini playbooks/01_info.yml
```

** OUTPUT:**
- `ok` = ülesanne õnnestus
- `changed` = midagi muudeti
- `failed` = viga (playbook peatub)

---

##  OSA 4: NGINX INSTALLIMINE

Keerukam lahendus, mis lisaks paigaldab nginx veebiserveri, loob konfiguratsiooni ja paigaldab veebiserverisse sisu.

```bash
nano playbooks/02_nginx.yml
```

```yaml
---
- name: "Install and configure Nginx"
  hosts: webservers               # Ainult web serverid grupist
  become: yes                     # sudo: yes - kasuta sudo õigusi
  
  tasks:
    # Esimene task - uuenda pakettide nimekirja
    - name: "Update apt cache"
      apt:                        # apt moodul Debian/Ubuntu jaoks
        update_cache: yes         # apt-get update
        cache_valid_time: 3600    # Cache kehtib 1 tund
    
    # Teine task - paigaldame nginx
    - name: "Install nginx"
      apt:
        name: nginx               # Paketi nimi
        state: present            # present = peab olema installitud
      notify: start nginx         # Kui midagi muutus, käivita handler
    
    # Kolmas task - loome oma HTML lehe
    - name: "Create custom index page"
      copy:                       # copy moodul kopeerib või loob faile
        dest: /var/www/html/index.html
        content: |                # Sisu mis faili kirjutatakse
          <!DOCTYPE html>
          <html>
          <head><title>Ansible Test</title></head>
          <body>
            <h1>Deployed by Ansible!</h1>
            <p>Server: {{ ansible_hostname }}</p>
            <p>IP: {{ ansible_default_ipv4.address }}</p>
            <p>Time: {{ ansible_date_time.iso8601 }}</p>
          </body>
          </html>
      notify: restart nginx       # Kui fail muutus, restart nginx
  
  handlers:                       # Handlerid käivituvad ainult kui notify kutsub
    - name: start nginx
      service:                    # service moodul teenuste haldamiseks
        name: nginx
        state: started            # Käivita teenus
        enabled: yes              # Luba autostart bootil
    
    - name: restart nginx
      service:
        name: nginx
        state: restarted          # Taaskäivita teenus
```

** HANDLERITE SELGITUS:**
Handlers on taskid mis käivitatakse teiste taskide eduka lõpetamise korral. Näiteks teenustele tehtavad restardid. Need käivituvad:
- AINULT kui task tegi muudatuse (changed=true)
- Alles playbooki LÕPUS
- Ainult ÜKS kord (isegi kui mitu notify)

```bash
# Käivitage playbook (küsib sudo parooli)
ansible-playbook -i inventory.ini playbooks/02_nginx.yml --ask-become-pass
# Sisesta: ansible123 (ansible kasutaja sudo parool)

# Testige kas nginx töötab - avage brauseris VM2 IP
curl http://192.168.56.11

# VÕI kontrollida teenuse staatust
ansible -i inventory.ini webservers -m service -a "name=nginx state=started" --check
```

** SUDO PAROOLI VARIANDID:**

**1. Küsi iga kord:**
```bash
ansible-playbook playbook.yml --ask-become-pass
```

**2. Ansible.cfg failis (ebaturvaline!):**
```ini
[privilege_escalation]
become_ask_pass = False  # Ei küsi parooli - töötab ainult kui NOPASSWD
```

**3. NOPASSWD sudo (mugav labori jaoks):**
```bash
# VM2 peal seadista ansible kasutajale paroolivaba sudo
sudo visudo
# Lisa rida lõppu:
ansible ALL=(ALL) NOPASSWD: ALL
```

** PRODUCTION'is:** Kasutage Ansible Vault parooli krüpteerimiseks!

---

##  OSA 5: TEMPLATE KASUTAMINE

Templatedega saab luua vaikekonfe, mis paigaldamise ajal täidetakse vastavalt masinale sobiva infoga. Templates = dünaamilised failid muutujatega, kasutavad Jinja2 süntaksit.

```bash
# Loome templates kausta
mkdir templates

# Loome HTML template faili
nano templates/website.html.j2
```

```jinja2
<!DOCTYPE html>
<html>
<head>
    <title>{{ page_title }}</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 50px;
            text-align: center;
        }
        .info-box {
            background: rgba(255,255,255,0.2);
            padding: 30px;
            border-radius: 10px;
            max-width: 600px;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div class="info-box">
        <h1>{{ site_name }}</h1>
        <p>Environment: {{ environment }}</p>
        
        {# See on Jinja2 kommentaar - ei näe HTML-is #}
        
        {% if show_debug %}  {# if-else tingimus #}
        <h3>Debug Info:</h3>
        <ul style="text-align: left;">
            <li>Server: {{ ansible_hostname }}</li>
            <li>OS: {{ ansible_distribution }}</li>
            <li>Memory: {{ ansible_memtotal_mb }} MB</li>
            <li>Deployed: {{ ansible_date_time.iso8601 }}</li>
        </ul>
        {% else %}
        <p>Debug mode disabled</p>
        {% endif %}
        
        <h3>Services:</h3>
        {% for service in services %}  {# Tsükkel üle listi #}
        <p>{{ service.name }} on port {{ service.port }}</p>
        {% endfor %}
    </div>
</body>
</html>
```

** JINJA2 SÜNTAKS:**
- `{{ muutuja }}` = muutuja väärtus
- `{% if tingimus %}` = tingimuslause
- `{% for item in list %}` = tsükkel
- `{# kommentaar #}` = ei näe väljundis
- `| filter` = filtrid muutujatele (upper, lower, default)

```bash
nano playbooks/03_template.yml
```

```yaml
---
- name: "Deploy website from template"
  hosts: webservers
  become: yes
  vars:                           # Muutujad mida template kasutab
    page_title: "IT College Lab"
    site_name: "Ansible Deployment Test"
    environment: "Development"
    show_debug: true              # Boolean muutuja
    services:                     # List objektidest
      - { name: "Web Server", port: 80 }
      - { name: "SSH", port: 22 }
  
  tasks:
    - name: "Deploy HTML from template"
      template:                   # template moodul (mitte copy!)
        src: templates/website.html.j2    # Lähtefail !!!!TRY FULL PATH, IF NOT WORKING
        dest: /var/www/html/index.html    # Sihtfail
      notify: reload nginx
  
  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded           # reload on kergem kui restart
```

```bash
# Käivitage playbook
ansible-playbook -i inventory.ini playbooks/03_template.yml

# Vaadake tulemust brauseris või:
curl http://192.168.56.11
```

---

##  OSA 6: MUUTUJAD JA LOOPS

```bash
nano playbooks/04_users.yml
```

```yaml
---
- name: "User management"
  hosts: webservers
  become: yes
  vars:
    users_to_create:
      - { name: "developer", groups: "www-data", shell: "/bin/bash" }
      - { name: "tester", groups: "www-data", shell: "/bin/sh" }
    packages_to_install:
      - htop
      - curl
      - wget
      - git
  
  tasks:
    - name: "Install packages"
      apt:
        name: "{{ item }}"
        state: present
      loop: "{{ packages_to_install }}"
    
    - name: "Create users"
      user:
        name: "{{ item.name }}"
        groups: "{{ item.groups }}"
        shell: "{{ item.shell }}"
        state: present
      loop: "{{ users_to_create }}"
    
    - name: "Check if users were created"
      command: "id {{ item.name }}"
      loop: "{{ users_to_create }}"
      register: user_check
      changed_when: false
    
    - name: "Show results"
      debug:
        msg: "User {{ item.item.name }} exists"
      loop: "{{ user_check.results }}"
      when: item.rc == 0
```

---

##  OSA 7: ORGANISEERIMINE

### Group variables

```bash
# Muutujad eraldi failides
mkdir -p group_vars/all
nano group_vars/all/main.yml
```

```yaml
---
# Kehtib kõigile serveritele
company: "IT College"
admin_email: "admin@itcollege.ee"
timezone: "Europe/Tallinn"
```

```bash
mkdir -p group_vars/webservers
nano group_vars/webservers/main.yml
```

```yaml
---
# Ainult webservers grupile
nginx_port: 80
nginx_worker_processes: auto
mysql_port: 3306
```

### Tasks eraldi failides

```bash
mkdir tasks
nano tasks/install_packages.yml
```

```yaml
---
- name: "Update apt cache"
  apt:
    update_cache: yes
    cache_valid_time: 3600

- name: "Install basic packages"
  apt:
    name:
      - htop
      - curl
      - wget
      - vim
    state: present
```

```bash
nano playbooks/05_main.yml
```

```yaml
---
- name: "Main playbook using includes"
  hosts: webservers
  become: yes
  
  tasks:
    - name: "Show variables from group_vars"
      debug:
        msg: "Company: {{ company }}, Port: {{ nginx_port }}"
    
    - name: "Install packages"
      include_tasks: ../tasks/install_packages.yml
```

---

##  OSA 8: ANSIBLE.CFG

```bash
# Konfiguratsioonifail - teeb elu lihtsamaks
nano ansible.cfg
```

```ini
[defaults]
inventory = inventory.ini
remote_user = ansible
host_key_checking = False
stdout_callback = yaml

[privilege_escalation]
#become = True
#become_method = sudo
#become_user = root
become_ask_pass = False
```

```bash
# Nüüd saate lihtsalt:
ansible all -m ping              # Ei vaja -i inventory.ini
ansible-playbook playbooks/05_main.yml
```

---

##  OSA 9: DEBUGGING

```bash
nano playbooks/99_debug.yml
```

```yaml
---
- name: "Debug playbook"
  hosts: all
  gather_facts: yes
  
  tasks:
    - name: "Check connectivity"
      ping:
    
    - name: "Show all variables"
      debug:
        var: hostvars[inventory_hostname]
      tags: full
    
    - name: "Test sudo access"
      command: whoami
      become: yes
      register: sudo_test
    
    - name: "Show sudo result"
      debug:
        msg: "Sudo user is: {{ sudo_test.stdout }}"
```

```bash
# Käivita verbose mode'is
ansible-playbook playbooks/99_debug.yml -v

# Ainult kindlad tagid
ansible-playbook playbooks/99_debug.yml --tags full

# Dry run
ansible-playbook playbooks/02_nginx.yml --check
```

---

##  GITHUB REPO STRUKTUUR

```
ansible_tutorial/
├── README.md
├── inventory.ini
├── ansible.cfg
├── playbooks/
│   ├── 01_info.yml
│   ├── 02_nginx.yml
│   ├── 03_template.yml
│   ├── 04_users.yml
│   └── 05_main.yml
├── templates/
│   └── website.html.j2
├── group_vars/
│   ├── all/
│   │   └── main.yml
│   └── webservers/
│       └── main.yml
├── tasks/
│   └── install_packages.yml
└── screenshots/
    ├── 01_ping_test.png
    ├── 02_nginx_running.png
    └── 03_website.png
```

---

##  KONTROLL-NIMEKIRI

- [ ] VM1 ja VM2 seadistatud
- [ ] SSH võti töötab ilma paroolita
- [ ] Ansible installitud VM1
- [ ] Inventory fail õigete IP-dega
- [ ] Ping test töötab mõlemale VM-ile
- [ ] Nginx installitud ja töötab VM2
- [ ] Template genereerib HTML
- [ ] Group_vars laaditakse automaatselt
- [ ] Screenshots tehtud
- [ ] GitHub repo avalik

---

##  DOKUMENTATSIOON

- **Ansible Docs:** https://docs.ansible.com/
- **Moodulid:** `ansible-doc -l` või `ansible-doc <moodul>`
- **YAML:** https://yaml.org/
- **Jinja2:** https://jinja.palletsprojects.com/

---

##  HINDAMINE

**A:** Kõik töötab + organiseeritud + dokumenteeritud  
**B:** Põhiülesanded töötavad  
**C:** Enamus töötab  
**F:** Ei tööta või repo puudub
