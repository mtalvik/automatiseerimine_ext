# Ansible Labor

**Eeldused:** Linux CLI põhitõed, SSH baasoskused, YAML süntaksi tutvustus loengust  
**Platvorm:** Ubuntu 24.04 (töötab ka Ubuntu 20.04/22.04)

---

## Õpiväljundid

Pärast seda labori oskate:

- Seadistada SSH võtmepõhist autentimist Ansible serverite jaoks
- Luua ja konfigureerida inventory faile serverite haldamiseks
- Kirjutada YAML süntaksiga playbook'e ja kasutada põhilisi mooduleid
- Käivitada ad-hoc käske kiireks serverite haldamiseks
- Rakendada idempotentsuse printsiipi praktilises töös

---

## Labori Ülevaade

See labor võtab umbes 3-4 tundi ja koosneb üheksast praktilisest ülesandest. Loote kaks virtuaalmasinat, seadistate SSH ühenduse, paigaldate Ansible'i ja töötate läbi põhilised ülesanded alates lihtsatest ping testidest kuni nginx veebiserveri paigalduseni template'idega. Iga ülesande järel on valideerimise samm, et kontrollida kas kõik töötab.

---

## 1. Virtuaalmasinate ettevalmistus

Selles ülesandes seadistate kaks virtuaalmasinat - ühe control node'iks (kust Ansible käivitatakse) ja teise target serveriks (kuhu tarkvara paigaldatakse). See võtab umbes 20-30 minutit.

### 1.1. VM-ide loomine

Looge kaks Ubuntu 24.04 virtuaalmasinat:

- **VM1:** ansible-controller (192.168.56.10)
- **VM2:** web-server (192.168.56.11)

Mõlemad peavad olema samas võrgus ja omavahel suhtlema saama.

### 1.2. Kasutaja loomine mõlemas VM-is

Ansible vajab spetsiaalset kasutajat, kellel on sudo õigused. Tehke järgmist MÕLEMAS virtuaalmasinas:

```bash
# Kontrolli kes sa praegu oled
whoami

# Loo uus kasutaja nimega 'ansible'
sudo adduser ansible
# Parool: ansible123
# Full Name jne: võid tühjaks jätta (Enter)

# Lisa sudo õigused
sudo usermod -aG sudo ansible

# Vaheta ansible kasutajale
su - ansible
# Sisesta parool: ansible123

# Kontrolli
whoami                    # Peaks näitama: ansible
pwd                       # Peaks näitama: /home/ansible
groups                    # Peaks sisaldama: ansible sudo
```

OLULINE: Kõik järgnevad sammud tehke ansible kasutajana, mitte root'ina.

### 1.3. SSH teenuse kontrollimine VM2-s

```bash
# VM2 peal kontrolli et SSH server töötab
sudo systemctl status ssh

# Kui ei tööta, paigalda
sudo apt update
sudo apt install openssh-server -y
sudo systemctl enable --now ssh

# Kontrolli et port 22 on avatud
sudo ss -tulpn | grep :22
```

### Valideeriminen

- [ ] Mõlemad VM-id on töös
- [ ] Ansible kasutaja on loodud mõlemas VM-is
- [ ] SSH teenus töötab VM2-s
- [ ] Saad VM1-st pingida VM2: `ping -c 3 192.168.56.11`

---

## 2. SSH võtmete seadistamine

SSH võtmed võimaldavad turvalist, paroolivaba ühendust serverite vahel. See on Ansible'i jaoks kriitilise tähtsusega, kuna Ansible teeb palju SSH ühendusi. Selle ülesande täitmine võtab umbes 15 minutit.

### 2.1. SSH võtmepaari genereerimine VM1-s

```bash
# VM1 peal, ansible kasutajana
# Kontrolli et oled õiges kasutajas
whoami    # Peab olema: ansible

# Genereeri SSH võtmepaar
ssh-keygen -t ed25519
# Enter file: vajuta ENTER (vaikimisi /home/ansible/.ssh/id_ed25519)
# Passphrase: vajuta ENTER (ilma paroolita labori jaoks)
# Passphrase again: vajuta ENTER

# Vaata genereeritud võtmeid
ls -la ~/.ssh/
# Peaksid nägema:
# id_ed25519        (privaatne võti - hoia saladuses!)
# id_ed25519.pub    (avalik võti - selle kopeerid serveritesse)

# Vaata avaliku võtme sisu
cat ~/.ssh/id_ed25519.pub
```

### 2.2. Avaliku võtme kopeerimine VM2-sse

```bash
# VM1 peal
ssh-copy-id ansible@192.168.56.11
# Sisesta ansible@VM2 parool: ansible123

# See käsk:
# 1. Võtab sinu avaliku võtme ~/.ssh/id_ed25519.pub
# 2. Kopeerib selle VM2 ansible kasutaja kausta
# 3. Lisab selle faili ~/.ssh/authorized_keys VM2-s
```

### 2.3. Ühenduse testimine

```bash
# VM1 peal - nüüd peaks saama sisse logida ilma paroolita
ssh ansible@192.168.56.11
# Ei tohiks parooli küsida!

# VM2-s sisselogituna
hostname    # Peaks näitama: web-server
exit        # Tagasi VM1-sse
```

### Valideeriminen

- [ ] SSH võti on genereeritud VM1-s
- [ ] Võti on edukalt kopeeritud VM2-sse
- [ ] Saad VM1-st VM2-sse logida ilma parooli küsimiseta
- [ ] `ssh ansible@192.168.56.11` töötab kohe

Troubleshooting: Kui palub parooli, kontrolli:

- Kas oled ansible kasutajana mõlemas VM-is
- Kas ssh-copy-id käsk õnnestus
- Kas võtmed on õiges kaustas: `ls ~/.ssh/`

---

## 3. Ansible installimine ja seadistamine

Ansible paigaldatakse ainult control node'i (VM1). Target serverid ei vaja Ansible'i installimist. See ülesanne võtab umbes 10 minutit.

### 3.1. Ansible installimine VM1-s

```bash
# VM1 peal, ansible kasutajana
sudo apt update
sudo apt install ansible -y

# Kontrolli installatsiooni
ansible --version

# Peaks näitama umbes:
# ansible [core 2.XX.X]
#   python version = 3.XX.X
```

### 3.2. Projekti kausta loomine

```bash
# VM1 peal
mkdir ~/ansible_tutorial
cd ~/ansible_tutorial

# Kontrolli kus oled
pwd    # Peaks näitama: /home/ansible/ansible_tutorial
```

### 3.3. Inventory faili loomine

Inventory fail sisaldab serverite nimekirja ja nende konfiguratsiooni. Looge fail nimega `inventory.ini`:

```bash
nano inventory.ini
```

Sisestage järgmine sisu (kohandage IP aadresse vastavalt oma VM-idele):

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

OLULINE: Muutke `192.168.56.11` oma VM2 tegeliku IP aadressiga.

### Valideeriminen

- [ ] Ansible on installitud: `ansible --version` töötab
- [ ] Projekti kaust on loodud
- [ ] Inventory fail eksisteerib: `cat inventory.ini`
- [ ] IP aadress inventory failis vastab VM2 IP-le

---

## 4. Esimesed ad-hoc käsud

Ad-hoc käsud võimaldavad kiireid ühekordseid toiminguid serverites ilma playbook'e kirjutamata. Need on ideaalsed testimiseks ja kiireks info kogumiseks. Selle ülesande läbitegemiseks kulub umbes 20 minutit.

### 4.1. Ping test

```bash
# VM1 peal, ~/ansible_tutorial kaustas
ansible -i inventory.ini all -m ping

# Peaksite nägema:
# localhost | SUCCESS => { "ping": "pong" }
# web1 | SUCCESS => { "ping": "pong" }
```

Kui näete SUCCESS, siis Ansible saab mõlema serveriga ühendust.

### 4.2. Süsteemiinfo kogumine

```bash
# Küsi serverite hostname
ansible -i inventory.ini all -m shell -a "hostname"

# Küsi OS infot
ansible -i inventory.ini webservers -m shell -a "lsb_release -a"

# Vaata mälu kasutust
ansible -i inventory.ini all -m shell -a "free -h"

# Kontrolli kettaruumi
ansible -i inventory.ini all -m shell -a "df -h"
```

### 4.3. Failide kopeerimine

```bash
# Loo testfail
echo "Test from Ansible" > test.txt

# Kopeeri kõikidesse serveritesse
ansible -i inventory.ini webservers -m copy -a "src=test.txt dest=/tmp/"

# Kontrolli kas fail jõudis kohale
ansible -i inventory.ini webservers -m shell -a "cat /tmp/test.txt"
```

### 4.4. Tarkvara paigaldamine

```bash
# Paigalda htop (vajab sudo õigusi)
ansible -i inventory.ini webservers -m apt -a "name=htop state=present" --become --ask-become-pass
# Sisesta sudo parool: ansible123

# Kontrolli installatsiooni
ansible -i inventory.ini webservers -m shell -a "which htop"
```

### 4.5. Kasutaja loomine

```bash
# Loo testkasutaja
ansible -i inventory.ini webservers -m user -a "name=testuser shell=/bin/bash" --become --ask-become-pass

# Kontrolli
ansible -i inventory.ini webservers -m shell -a "id testuser" --become --ask-become-pass
```

### 4.6. Faktide kogumine

```bash
# Kogu kõik faktid serverite kohta
ansible -i inventory.ini webservers -m setup

# Filtreeri ainult OS info
ansible -i inventory.ini webservers -m setup -a "filter=ansible_distribution*"

# Filtreeri ainult võrgu info
ansible -i inventory.ini webservers -m setup -a "filter=ansible_default_ipv4"
```

### Valideeriminen

- [ ] Ping test töötab kõigi serveritega
- [ ] Hostname käsk tagastab õige serveri nime
- [ ] Test fail kopeeriti edukalt /tmp/ kausta
- [ ] htop on installitud VM2-s
- [ ] Testkasutaja on loodud

Troubleshooting:

- Kui "Permission denied": kasutage `--become --ask-become-pass`
- Kui "Host unreachable": kontrollige inventory IP aadresse
- Kui "Module not found": kontrollige mooduli nime kirjaviisi

---

## 5. Esimene playbook

Playbook on YAML vormingus fail, mis sisaldab ülesannete jada. Erinevalt ad-hoc käskudest saate playbook'ides kirjeldada keerukamaid töövoogusid. Selle ülesande täitmine võtab umbes 30 minutit.

### 5.1. Playbook'ide kausta loomine

```bash
# VM1 peal, ~/ansible_tutorial kaustas
mkdir playbooks
```

### 5.2. Info kogumise playbook

Looge fail `playbooks/01_info.yml`:

```bash
nano playbooks/01_info.yml
```

Sisestage järgmine sisu:

```yaml
---
- name: "System information gathering"
  hosts: all
  gather_facts: yes
  
  tasks:
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

### 5.3. Playbook'i käivitamine

```bash
# Käivita playbook
ansible-playbook -i inventory.ini playbooks/01_info.yml

# Vaata väljundit:
# PLAY [System information gathering]
# TASK [Gathering Facts]
# TASK [Print hostname]
# ok: [localhost]
# ok: [web1]
# ...
# PLAY RECAP
```

Väljundi selgitus:

- `ok` - ülesanne õnnestus, midagi ei muutunud
- `changed` - ülesanne õnnestus ja midagi muudeti
- `failed` - ülesanne ebaõnnestus

### 5.4. Idempotentsuse testimine

```bash
# Käivita sama playbook teist korda
ansible-playbook -i inventory.ini playbooks/01_info.yml

# Tähelepanek:
# - "Create test directory" task näitab "ok" mitte "changed"
# - See on idempotentsus - teine käivitus ei muuda midagi
```

### Valideeriminen

- [ ] Playbook käivitus õnnestus ilma vigadeta
- [ ] Näete hostname ja OS infot kõigi serverite kohta
- [ ] Kaust /tmp/ansible-test on loodud
- [ ] Teine käivitus näitab "changed: 0" (idempotentne)

---

## 6. Nginx veebiserveri paigaldamine

Selles ülesandes paigaldate nginx veebiserveri kasutades Ansible playbook'i. Õpite tundma handlers'eid ja teenuste haldamist. Ülesanne võtab umbes 30 minutit.

### 6.1. Nginx playbook loomine

Looge fail `playbooks/02_nginx.yml`:

```bash
nano playbooks/02_nginx.yml
```

Sisestage järgmine sisu:

```yaml
---
- name: "Install and configure Nginx"
  hosts: webservers
  become: yes
  
  tasks:
    - name: "Update apt cache"
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: "Install nginx"
      apt:
        name: nginx
        state: present
      notify: start nginx
    
    - name: "Create custom index page"
      copy:
        dest: /var/www/html/index.html
        content: |
          <!DOCTYPE html>
          <html>
          <head><title>Ansible Test</title></head>
          <body>
            <h1>Deployed by Ansible!</h1>
            <p>Server: {{ ansible_hostname }}</p>
            <p>IP: {{ ansible_default_ipv4.address }}</p>
          </body>
          </html>
      notify: restart nginx
  
  handlers:
    - name: start nginx
      service:
        name: nginx
        state: started
        enabled: yes
    
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```

### 6.2. Playbook'i käivitamine

```bash
# Käivita playbook (küsib sudo parooli)
ansible-playbook -i inventory.ini playbooks/02_nginx.yml --ask-become-pass
# Sisesta: ansible123
```

### 6.3. Tulemuse kontrollimine

```bash
# Kontrolli kas nginx töötab
ansible -i inventory.ini webservers -m service -a "name=nginx" --become --ask-become-pass

# Testi veebilehte käsurealt
curl http://192.168.56.11

# VÕI ava brauseris
# http://192.168.56.11
```

### 6.4. Handlerite mõistmine

Handlers on spetsiaalsed taskid mis:

- Käivitatakse ainult kui mõni task tegi muudatuse (changed=true)
- Käivitatakse playbook'i lõpus
- Käivitatakse ainult üks kord isegi kui mitu notify

Näide: Kui muudate nginx konfiguratsiooni 3 korda ja kõik kutsuvad "restart nginx", siis restart toimub ainult üks kord lõpus.

### 6.5. Idempotentsuse test

```bash
# Käivita sama playbook teist korda
ansible-playbook -i inventory.ini playbooks/02_nginx.yml --ask-become-pass

# Tähelepanek:
# - "Install nginx" näitab "ok" (ei installi uuesti)
# - Handler EI käivitu sest midagi ei muutunud
```

### Valideeriminen

- [ ] Nginx paigaldus õnnestus
- [ ] Nginx teenus töötab: `systemctl status nginx` VM2-s
- [ ] Veebileht on kättesaadav: `curl http://192.168.56.11`
- [ ] Leht näitab serveri hostname ja IP
- [ ] Teine käivitus ei muuda midagi (idempotentne)

---

## 7. Template'ide kasutamine

Template'd võimaldavad luua dünaamilisi konfiguratsiooni- või HTML faile kasutades Jinja2 süntaksit. See on võimas vahend, mis võimaldab sama template'i kasutada erinevates serverites erineva sisuga. Ülesanne võtab umbes 25 minutit.

### 7.1. Templates kausta loomine

```bash
# VM1 peal
mkdir templates
```

### 7.2. HTML template loomine

Looge fail `templates/website.html.j2`:

```bash
nano templates/website.html.j2
```

Sisestage:

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
        
        {% if show_debug %}
        <h3>Debug Info:</h3>
        <ul style="text-align: left;">
            <li>Server: {{ ansible_hostname }}</li>
            <li>OS: {{ ansible_distribution }}</li>
            <li>Memory: {{ ansible_memtotal_mb }} MB
            <li>Deployed: {{ ansible_date_time.iso8601 }}</li>
        </ul>
        {% else %}
        <p>Debug mode disabled</p>
        {% endif %}
        
        <h3>Services:</h3>
        {% for service in services %}
        <p>{{ service.name }} on port {{ service.port }}</p>
        {% endfor %}
    </div>
</body>
</html>
```

### 7.3. Template playbook loomine

Looge fail `playbooks/03_template.yml`:

```bash
nano playbooks/03_template.yml
```

Sisestage:

```yaml
---
- name: "Deploy website from template"
  hosts: webservers
  become: yes
  vars:
    page_title: "IT College Lab"
    site_name: "Ansible Deployment Test"
    environment: "Development"
    show_debug: true
    services:
      - { name: "Web Server", port: 80 }
      - { name: "SSH", port: 22 }
  
  tasks:
    - name: "Deploy HTML from template"
      template:
        src: ../templates/website.html.j2
        dest: /var/www/html/index.html
      notify: reload nginx
  
  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded
```

### 7.4. Käivitamine ja testimine

```bash
# Käivita playbook
ansible-playbook -i inventory.ini playbooks/03_template.yml --ask-become-pass

# Vaata tulemust
curl http://192.168.56.11
# VÕI ava brauseris ja vaata ilus gradient background
```

### Valideeriminen

- [ ] Template fail on loodud
- [ ] Playbook käivitus õnnestus
- [ ] Veebileht näitab õigeid muutujate väärtusi
- [ ] Debug info on nähtav (hostname, OS, memory)
- [ ] Services loend kuvatakse korrektselt

---

## 8. Muutujad ja tsüklid

Selles ülesandes õpite kasutama muutujaid ja loop tsükleid, et vältida koodi kordamist. Loote mitu kasutajat ja paigaldate mitu paketti kasutades tsükleid. Ülesanne võtab umbes 20 minutit.

### 8.1. Kasutajate ja pakettide playbook

Looge fail `playbooks/04_users.yml`:

```bash
nano playbooks/04_users.yml
```

Sisestage:

```yaml
---
- name: "User and package management"
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
        msg: "User {{ item.item.name }} exists with shell {{ item.item.shell }}"
      loop: "{{ user_check.results }}"
      when: item.rc == 0
```

### 8.2. Käivitamine

```bash
ansible-playbook -i inventory.ini playbooks/04_users.yml --ask-become-pass
```

### 8.3. Kontrollimine

```bash
# Kontrolli kasutajaid
ansible -i inventory.ini webservers -m shell -a "cat /etc/passwd | grep -E 'developer|tester'" --become --ask-become-pass

# Kontrolli pakette
ansible -i inventory.ini webservers -m shell -a "dpkg -l | grep -E 'htop|curl|wget|git'"
```

### Valideeriminen

- [ ] Kõik 4 paketti on installitud
- [ ] Mõlemad kasutajad (developer, tester) on loodud
- [ ] Kasutajatel on õiged shellid (/bin/bash, /bin/sh)
- [ ] Debug väljund näitab kasutajate infot

---

## 9. Projekti organiseerimine

Professionaalsed Ansible projektid kasutavad eraldi kaustasid muutujatele ja ülesannetele. Selles ülesandes organiseerite projekti paremini. Ülesanne võtab umbes 20 minutit.

### 9.1. Group variables loomine

```bash
# Loo group_vars kaustad
mkdir -p group_vars/all
mkdir -p group_vars/webservers

# Globaalsed muutujad (kehtivad kõigile)
nano group_vars/all/main.yml
```

Sisestage `group_vars/all/main.yml`:

```yaml
---
company: "IT College"
admin_email: "admin@itcollege.ee"
timezone: "Europe/Tallinn"
```

Looge `group_vars/webservers/main.yml`:

```bash
nano group_vars/webservers/main.yml
```

Sisestage:

```yaml
---
nginx_port: 80
nginx_worker_processes: auto
mysql_port: 3306
```

### 9.2. Taaskasutatavad taskid

```bash
# Loo tasks kaust
mkdir tasks

nano tasks/install_packages.yml
```

Sisestage:

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

### 9.3. Peamine playbook

Looge `playbooks/05_main.yml`:

```bash
nano playbooks/05_main.yml
```

Sisestage:

```yaml
---
- name: "Main playbook using includes"
  hosts: webservers
  become: yes
  
  tasks:
    - name: "Show variables from group_vars"
      debug:
        msg: "Company: {{ company }}, Nginx port: {{ nginx_port }}"
    
    - name: "Install packages"
      include_tasks: ../tasks/install_packages.yml
```

### 9.4. Ansible.cfg loomine

Looge projekti juurkausta `ansible.cfg`:

```bash
nano ansible.cfg
```

Sisestage:

```ini
[defaults]
inventory = inventory.ini
remote_user = ansible
host_key_checking = False
stdout_callback = yaml

[privilege_escalation]
become_ask_pass = False
```

### 9.5. Testimine

```bash
# Nüüd ei vaja enam -i inventory.ini
ansible all -m ping

# Ega --ask-become-pass kui seadistatud
ansible-playbook playbooks/05_main.yml
```

### Valideeriminen

- [ ] group_vars kaustad on loodud
- [ ] Muutujad laetakse automaatselt playbook'ides
- [ ] Tasks include toimib
- [ ] ansible.cfg võimaldab lihtsamaid käske
- [ ] `ansible all -m ping` töötab ilma -i liputa

---

## Lõplik kontroll-nimekiri

Enne labori lõpetamist kontrollige:

- [ ] Mõlemad VM-id töötavad ja on omavahel ühenduses
- [ ] SSH võtmepõhine autentimine töötab
- [ ] Ansible on installitud VM1-s
- [ ] Kõik 5 playbook'i on loodud ja testitud
- [ ] Nginx töötab VM2-s
- [ ] Template genereerib korrektselt HTML
- [ ] Group_vars failid laetakse automaatselt
- [ ] Projekti struktuur on korras

Projekti lõplik struktuur peaks olema:

```
ansible_tutorial/
├── ansible.cfg
├── inventory.ini
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
└── tasks/
    └── install_packages.yml
```

---

## Troubleshooting

### SSH ühenduse probleemid

Probleem: "Permission denied (publickey)"

Lahendus:
```bash
# Kontrolli kas võti on õiges kohas
ls -la ~/.ssh/

# Kontrolli kas võti on VM2-s authorized_keys failis
ssh ansible@192.168.56.11 "cat ~/.ssh/authorized_keys"

# Proovi uuesti ssh-copy-id
ssh-copy-id -i ~/.ssh/id_ed25519.pub ansible@192.168.56.11
```

### Playbook ebaõnnestub

Probleem: "Failed to connect to host"

Lahendus:
```bash
# Kontrolli inventory IP aadresse
cat inventory.ini

# Testi ühendust käsitsi
ssh ansible@192.168.56.11

# Kasuta verbose režiimi rohkem info saamiseks
ansible-playbook playbooks/02_nginx.yml -vvv
```

### Sudo parool

Probleem: "sudo: a password is required"

Lahendus:
```bash
# Kasuta --ask-become-pass lippu
ansible-playbook playbooks/02_nginx.yml --ask-become-pass

# VÕI seadista passwordless sudo VM2-s
sudo visudo
# Lisa lõppu:
ansible ALL=(ALL) NOPASSWD: ALL
```

### YAML süntaksi vead

Probleem: "Syntax Error while loading YAML"

Lahendus:
- Kontrolli taandeid (kasuta ainult tühikuid, mitte tab'e)
- Kontrolli koolonite järel on tühik
- Kasuta online YAML validatorit

---

## Kasulikud käsud

Debugimine:

```bash
# Verbose režiim (rohkem infot)
ansible-playbook playbook.yml -v
ansible-playbook playbook.yml -vvv

# Kuiv käivitus (ei tee muudatusi)
ansible-playbook playbook.yml --check

# Vaata muudatuste diff'i
ansible-playbook playbook.yml --diff

# Käivita ainult kindlad tagid
ansible-playbook playbook.yml --tags "install"

# Piira servereid
ansible-playbook playbook.yml --limit webservers
```

Moodulite dokumentatsioon:

```bash
# Näita kõiki mooduleid
ansible-doc -l

# Konkreetse mooduli dokumentatsioon
ansible-doc apt
ansible-doc service
ansible-doc template
```

---

## Järgmised sammud

Kui olete selle laboriga valmis, järgmised teemad:

1. Ansible rollid - korduvkasutatavad playbook'i komplektid
2. Ansible Vault - paroolide ja tundliku info krüpteerimine
3. Ansible Galaxy - valmis rollide kasutamine
4. CI/CD integratsioon - Ansible GitLab/GitHub pipeline'ides

Kasulikud ressursid:

- Ansible dokumentatsioon: https://docs.ansible.com/
- Ansible Galaxy: https://galaxy.ansible.com/
- YAML süntaks: https://yaml.org/
- Jinja2 template'id: https://jinja.palletsprojects.com/