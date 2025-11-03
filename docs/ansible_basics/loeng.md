# Ansible Alused

**Eeldused:** Linux CLI, SSH, teksteditor

**Platvorm:** Ansible (agentless)

**Dokumentatsioon:** [docs.ansible.com](https://docs.ansible.com/)

## Õpiväljundid

Pärast seda loengut õpilane:

- Selgitab miks käsitsi serverhaldus ei skaleeru ja kuidas automatiseerimine lahendab seda
- Kirjeldab Ansible'i agentless arhitektuuri eeliseid ja piiranguid
- Eristab push ja pull mudeleid ning põhjendab millal kumba kasutada
- Mõistab idempotentsuse tähtsust ja tunneb ära idempotentseid operatsioone
- Loeb inventory faile ja suudab kirjutada lihtsaid playbook'e
- Käivitab ad-hoc käske kiireks testimiseks

---

## 1. Probleem: Käsitsi Serverhaldus Ei Skaleeru

![IT admin serverisaalis, käsitsi töö](https://www.pacw.org/wp-content/uploads/2024/11/Figure-14.jpg)

### Tüüpiline Esmaspäev

Kell 9:00 hommikul saate kollegi sõnumi: "Kriitilise turvavea parandus. Peame täna uuendama nginx'i kõikides veebiserveritest. Meil on 50 serverit."
Te arvutate peas:
```
50 serverit × 5 minutit = 250 minutit = 4+ tundi
```
Te hakkate tööle:

```bash
ssh admin@web1.example.com
sudo apt update && sudo apt upgrade nginx -y
sudo systemctl restart nginx
exit

ssh admin@web2.example.com
sudo apt update && sudo apt upgrade nginx -y
sudo systemctl restart nginx
exit

# ... 48 serverit veel
```

Kell 13:00 olete server 25 juures. Olete juba väsinud. Copy-paste hakkab segamini minema.
Kell 14:30, server 37 - teete vea. Kirjutate `systemctl stop nginx` asemel `systemctl disable nginx`. Server ei tule peale rebooti enam üles.
Kell 15:00 helistab CEO. Kliendid ei saa lehte avada. "Mis toimub?"

Kell 18:00 olete lõpuks valmis. 9 tundi tööd. Olete läbipõlenud. Ja te ei ole 100% kindel kas kõik 50 serverit on täpselt samas seisus. See ei ole teie süü. Probleem on **meetodis**. Kui teil on rohkem kui 5-10 serverit, on käsitsi haldamine halb idee. Kui rohkem kui 20 serverit, on see võimatu idee.

### Kuidas Peaks Olema?

Ideaalis kirjutate ühe käsu:

```bash
ansible-playbook update-nginx.yml
```
3 minutit hiljem on kõik 50 serverit uuendatud. Identselt. Õigesti. Logitud.
Kas see on ulme? Ei. See on Ansible.

---

## 2. Mis on Ansible?

### Definitsioon

Ansible on **automatiseerimisvahend** mis laseb teil hallata kümneid, sadu või tuhandeid servereid **nagu üht**. Te kirjeldate MIDA te tahate ja Ansible teeb selle teoks.

Kujutlege kaugjuhtimispulti. Üks nupp, kõik televiisorid muudavad kanalit. Ansible on kaugjuhtimispult serveritele.

### Kolm Põhiomadust

#### 1. Agentless - Kasutab SSH-d

![Agentless vs Agent-based architecture](https://www.aquasec.com/wp-content/uploads/2023/03/large-Agents-charts.jpg)

**Agent-based lahendused** (Puppet, Chef):

```
[Teie arvuti] → [Master server] ← [Agent][Server1]
                                 ← [Agent][Server2]
                                 ← [Agent][Server3]
```

Igasse serverisse tuleb installida agent. Agent töötab taustal 24/7, küsib iga 15-30 min: "Kas on tööd?"

**Ansible (agentless):**

```
[Teie arvuti] --SSH--> [Server1]
              --SSH--> [Server2]
              --SSH--> [Server3]
```

SSH on juba olemas. Python on juba olemas. Midagi täiendavat ei pea installima.

**Miks see oluline?**

| Omadus | Agent-based | Agentless (Ansible) |
|--------|-------------|---------------------|
| Setup | Pead agendi installima | SSH töötab kohe |
| Ressursid | Agent kasutab RAM/CPU | Midagi ei tööta taustal |
| Hooldus | Agent vajab uuendusi | SSH on OS osa |
| Security | Veel üks rünnakupind | SSH on nagunii turvaline |
| Latentsus | 0-30 min (pull) | 0 (kohe kui käivitad) |

**Trade-off:** Ansible vajab SSH juurdepääsu. Kui serverid on tulemüüri taga või ei toeta SSH-d, on raskem. Agent-based lahendused töötavad seal paremini.

#### 2. Push Model - Teie Otsustate Millal

![Push vs Pull model comparison](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*-chzBHbzBA1BbBQo7a-q3w.png)

**Pull mudel** (Puppet, Chef):

Agent küsib ise iga 30 minuti tagant. Kui te teete muudatuse, võib minna 0-30 minutit enne kui kõik serverid selle saavad.

```
09:00 - Te: "Turvaprobleem! Uuenda KOHE!"
09:00 - Te muudate Puppet configi
09:05 - Server1 küsib: "Kas tööd?" → Saab uuenduse
09:15 - Server2 küsib → Saab uuenduse  
09:28 - Server3 küsib → Saab uuenduse
09:30 - Kõik uuendatud (30 min hiljem)
```

**Push mudel** (Ansible):

Te käivitate käsu. Ansible avab SSH ühendused ja teeb töö KOHE.

```
09:00 - Te: "Turvaprobleem! Uuenda KOHE!"
09:00 - ansible-playbook update.yml
09:03 - Kõik 50 serverit uuendatud (3 min)
```

**Miks see oluline?**

Kontroll. Teie otsustate TÄPSELT millal asjad juhtuvad:
- Kriitilise parandus? Kohe.
- Plaaniline muudatus? Kell 2 öösel maintenance window ajal.
- Testimine? Ainult dev serverites.

**Trade-off:** Peate käsu käivitama. Pull mudel töötab "iseenesest" - kui server lükatakse tagasi pärast krahhi, agent taastab konfiguratsiooni automaatselt. Ansible'iga peate te midagi tegema (või seadistama cron job'i).

#### 3. Idempotent - Turvaline Käivitada Mitu Korda

![Idempotent vs non-idempotent operations](https://media.licdn.com/dms/image/v2/D5612AQEp3iL1Zn9Czg/article-inline_image-shrink_1000_1488/article-inline_image-shrink_1000_1488/0/1718953580431?e=2147483647&v=beta&t=CDRoZci-6-ezcoShpWvtnwk8bhxHM3oO9hgE84ngg8k)

**Idempotentsus** tähendab: kui käivitate sama käsu 100 korda, on tulemus sama nagu 1 kord.

**Ei-idempotent shell script:**

```bash
echo "port 8080" >> config.txt
```

- 1. kord: lisab "port 8080"
- 2. kord: lisab veel "port 8080" 
- 10. kord: 10 rida "port 8080"

Fail rikutud. Probleem.

**Idempotent Ansible:**

```yaml
- lineinfile:
    path: config.txt
    line: "port 8080"
```

- 1. kord: Ansible vaatab → rida puudub → lisab
- 2. kord: Ansible vaatab → rida on olemas → ei tee midagi
- 10. kord: Ansible vaatab → rida on olemas → ei tee midagi
Failis on ALATI täpselt üks rida.

**Miks see NII oluline?**
Ohutu. Võite playbook'i käivitada nii palju kordi kui tahate:
- Testimine? Käivita 5 korda dev'is
- Midagi läks valesti? Käivita uuesti
- Kas kõik õige? Käivita kontrolliks
Ansible kontrollib alati: "Kas see on juba õige?" Kui jah → ei puutu. Kui ei → parandab.

---

## 3. Lühike Ajalugu: Kuidas Siia Jõudsime?

### 1990-2000: Käsitsi + Füüsiliselt
IT admin läks **füüsiliselt** serveri juurde, ühendas klaviatuuri ja ekraani, logi sisse. Firmal oli 5-10 serverit. Muudatused harva - kord kuus. See toimis. Aga Iga server muutus ajapikku erinevaks. Dokumentatsiooni ei olnud. Kõik teadmised IT admini peas.

### 2000-2005: SSH + Shell Skriptid
Servereid rohkem (50-100). SSH võimaldas kaugühendust. Inimesed kirjutasid shell skripte:

```bash
for server in server1 server2 server3; do
  ssh admin@$server "apt update && apt install nginx"
done
```
Skriptid ei olnud nutikad. Üritasid iga kord installida ka kui juba olemas. Vead ei käsitlenud.

### 2005-2009: Puppet ja Chef
![Puppet ja Chef logod](https://media.licdn.com/dms/image/v2/D4D12AQFhrjy0ozGShQ/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1690917230934?e=2147483647&v=beta&t=5yNZoMKZbOz-vJ9ENMP6DduR8Yywb1Utls07ajfRz8s)

Esimesed professionaalsed automatiseerimisvahendid. Deklaratiivne süntaks, nutikad, võimsad. Kasutasid agente (keeruline setup), oma keelt (uuesti õppida), pull mudelit (latentsus).

### 2012: Ansible
![Michael DeHaan (Ansible looja)](https://image.slidesharecdn.com/devopswithansible-170120102347/75/DevOps-with-Ansible-4-2048.jpg)

Michael DeHaan (ex-Puppet insineer) mõtles: "Miks nii keeruline? SSH on juba olemas. Python on juba olemas. Kasutame neid."
Lõi Ansible:
- Agentless (SSH)
- Push-based (kohe)
- YAML (lihtne)
- Tasuta
  
2015: Red Hat ostis 150M dollariga
2019: IBM ostis Red Hati (34B), seega ka Ansible'i

**Täna:** ~70% DevOps meeskondadest kasutab Ansible't. De facto standard.

---

## 4. Kuidas Ansible Töötab? Arhitektuur

### Control Node ja Managed Nodes

```
┌─────────────────┐
│  Control Node   │  ← Teie arvuti (kus Ansible on)
│  (Ansible CLI)  │
└────────┬────────┘
         │ SSH
    ┌────┼────┬─────────┐
    │    │    │         │
┌───▼┐ ┌─▼──┐ ┌▼───┐ ┌─▼──┐
│ S1 │ │ S2 │ │ S3 │ │ S4 │  ← Managed nodes (serverid)
└────┘ └────┘ └────┘ └────┘
```

**Control node:** Masin kus Ansible on installitud. Tavaliselt teie lauaarvuti või jumpbox.

**Managed nodes:** Serverid mida te haldate. Seal EI PEA Ansible't olema.

### Täpne Töövoog

![Ansible execution steps](https://toptechtips.github.io/img/ansible-parallel/default.png)

Kui te käivitate `ansible-playbook install-nginx.yml`:

**1. Ansible loeb playbook faili**
```yaml
- name: Install nginx
  hosts: webservers
  tasks:
    - apt: name=nginx state=present
```

**2. Ansible loeb inventory faili**

Vaatab: kelle IP aadressid on `webservers` grupis?

```ini
[webservers]
web1 ansible_host=10.0.0.10
web2 ansible_host=10.0.0.11
```

**3. Ansible avab SSH ühendused**

Vaikimisi 5 paralleelselt. Kiiresti - 50 serverit = ~10 batch'i.

**4. Gathering Facts**

**EI ALUSTA** kohe muutmisega! Esimene asi: kogub info:
- Mis OS? Ubuntu 22.04
- Mis Python? 3.10
- Kas nginx installitud? Ei
- RAM? 4GB
- IP? 10.0.0.10

**5. Võrdleb: soovitud vs tegelik**

Playbook ütleb: `nginx state=present`
Facts ütlevad: nginx puudub

Järeldus: tuleb installida.

**6. Genereerib ja saadab Python mooduli**

Ansible võtab `apt` mooduli, teeb väikese Python skripti, saadab SSH üle serverisse.

**7. Server käivitab skripti**

Python skript käivitab `apt-get install nginx`, vaatab tulemust, saadab tagasi.

**8. SSH ühendus suletakse**

Töö tehtud. Midagi ei jää taustal tööle.

**9. Ansible näitab tulemust**

```
TASK [Install nginx]
changed: [web1]
ok: [web2]
```

`changed` = muutis midagi
`ok` = oli juba õige

### Miks See On Geniaalne?

- **Ei jäta jälgi.** Server ei tea et Ansible oli seal. Lihtsalt käivitus Python skript ja sai valmis.
- **Minimaalne koormus.** Server ei tee midagi kui Ansible't ei käivitata.
- **Turvaline.** SSH on tuntud, testitud, turvaline protokoll.
- **Lihtne debug.** Kui midagi läheb valesti, võite käsitsi SSH'ga sisse minna ja vaadata.

---

## 5. Kolm Komponenti: Inventory, Ad-hoc, Playbooks

### 5.1 Inventory - Kellele Käske Saatma?

![Inventory file structure](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Ywp-CLRXKEGiRyvFCqRQUw.png)

Inventory on fail kus on **kõikide serverite nimekiri**.

**Lihtne inventory (INI formaat):**

```ini
[webservers]
web1 ansible_host=10.0.0.10 ansible_user=ubuntu
web2 ansible_host=10.0.0.11 ansible_user=ubuntu

[databases]
db1 ansible_host=10.0.0.20 ansible_user=admin
db2 ansible_host=10.0.0.21 ansible_user=admin

[all:vars]
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

**Komponendid:**

`[webservers]` - Grupi nimi. Võite nimetada kuidas tahate.

`web1` - Alias. Mugav nimi mida kasutate käskudes.

`ansible_host=10.0.0.10` - Tegelik IP või hostname.

`ansible_user=ubuntu` - Millisesse kasutajasse sisse logida.

`[all:vars]` - Muutujad mis kehtivad KÕIGILE serveritele.

**Miks grupid?**

Suunamine. Erinevad käsud erinevatele serveritele:

```bash
ansible webservers -m service -a "name=nginx state=restarted"
ansible databases -m service -a "name=mysql state=restarted"
```

**Pesastatud grupid:**

```ini
[ubuntu]
web1 ansible_host=10.0.0.10
web2 ansible_host=10.0.0.11

[alma]
db1 ansible_host=10.0.0.20
db2 ansible_host=10.0.0.21

[webservers:children]
ubuntu

[databases:children]
alma
```

`:children` tähendab et see grupp sisaldab teisi gruppe.

Nüüd võite teha:
- `ansible ubuntu -m apt -a "update_cache=yes"` ← ainult Ubuntu serverid
- `ansible webservers ...` ← kõik veebiservid (mis juhuvad Ubuntu's olema)

**Grupimuutujad:**

```ini
[webservers:vars]
nginx_port=80
ssl_enabled=true
```

Playbook'is saate kasutada `{{ nginx_port }}` → asendub 80-ga.

### 5.2 Ad-hoc Käsud - Kiired Testid

![Ad-hoc command examples](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*GJP11bPQkG5ng30X-8wTDw.png)

Ad-hoc = "selleks korraks". Ühekordsed käsud ilma playbook'i kirjutamata.

**Struktuur:**

```bash
ansible <target> -m <module> -a "<arguments>"
```

**Näited:**

**1. Ping - kas ühendus töötab?**

```bash
ansible all -m ping
```

Väljund:
```
web1 | SUCCESS => {"ping": "pong"}
web2 | SUCCESS => {"ping": "pong"}
```

See ei ole ICMP ping. See kontrollib: SSH töötab? Python olemas? Ansible saab käske käivitada?

**2. Käsu käivitamine:**

```bash
ansible all -m command -a "uptime"
```

Väljund:
```
web1 | CHANGED | rc=0 >>
 14:30:15 up 2 days,  5:23,  1 user

web2 | CHANGED | rc=0 >>
 14:30:15 up 5 days, 12:45,  2 users
```

`rc=0` = return code 0 = õnnestus.

**3. Paketi paigaldamine:**

```bash
ansible webservers -m apt -a "name=htop state=present" --become
```

`--become` = sudo. Paljud toimingud vajavad admin õigusi.

**4. Teenuse restart:**

```bash
ansible webservers -m service -a "name=nginx state=restarted" --become
```

**5. Faili kopeerimine:**

```bash
ansible all -m copy -a "src=test.txt dest=/tmp/test.txt"
```

**Millal kasutada ad-hoc käske?**

- Kiire test: kas serverid on üleval?
- Info kogumine: kas nginx on installitud?
- Ühekordsed asjad: restart teenust, kopeeri fail

**Millal EI kasuta?**

Kui teete midagi keerukat või korratavat → kirjutage playbook.

### 5.3 Playbooks - Automatiseeritud Töövood

![Simple playbook structure](https://hkrtrainings.com/storage/photos/843/Playbook%20structure.png)

Playbook on YAML fail kus on **ülesannete jada**. See on põhiline viis kuidas Ansible'iga töötada.

**Lihtne playbook:**

```yaml
---
- name: Install and start nginx
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install nginx package
      apt:
        name: nginx
        state: present
    
    - name: Ensure nginx is running
      service:
        name: nginx
        state: started
        enabled: yes
```

**Lahti seletatult:**

`---` - YAML dokumendi algus (standard).

`- name: Install and start nginx` - Play'i nimi. Inimestele, Ansible ei kasuta.

`hosts: webservers` - Kus see play jookseb? Kõik `webservers` grupis.

`become: yes` - Kasuta sudo õigusi.

`tasks:` - Ülesannete loend.

**Esimene task:**

`name: Install nginx package` - Task'i kirjeldus. Näed ekraanil kui käivitad.

`apt:` - Mooduli nimi. Debian/Ubuntu paketihaldur.

`name: nginx` - Paketi nimi.

`state: present` - Soovitud olek. "Present" = peab olemas olema.

**Teine task:**

`service:` - Teenuste haldamise moodul.

`state: started` - Peab töötama.

`enabled: yes` - Peab käivituma boot'imisel.

**Käivitamine:**

```bash
ansible-playbook -i inventory.ini install-nginx.yml
```

**Väljund:**

```
PLAY [Install and start nginx] ***************

TASK [Gathering Facts] ***********************
ok: [web1]
ok: [web2]

TASK [Install nginx package] *****************
changed: [web1]
ok: [web2]

TASK [Ensure nginx is running] ***************
changed: [web1]
ok: [web2]

PLAY RECAP ***********************************
web1    : ok=3    changed=2
web2    : ok=3    changed=0
```

`changed=2` - web1 muudeti (nginx paigaldati + käivitati)
`changed=0` - web2 oli juba õige

**Idempotentsus praktikas:**

```bash
ansible-playbook install-nginx.yml  # 1. kord → changed
ansible-playbook install-nginx.yml  # 2. kord → ok (ei muuda)
ansible-playbook install-nginx.yml  # 3. kord → ok (ei muuda)
```

Turvaline käivitada mitu korda!

**Keerulisem näide - muutujatega:**

```yaml
---
- name: Configure webserver
  hosts: webservers
  become: yes
  
  vars:
    nginx_port: 8080
    server_name: example.com
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    
    - name: Copy nginx config from template
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/default
      notify: restart nginx
  
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```

**Uued elemendid:**

`vars:` - Muutujate määramine. Saab kasutada `{{ nginx_port }}` playbook'is.

`template:` - Moodul mis loob faili template'ist. Template võib sisaldada muutujaid.

`notify: restart nginx` - Kui see task muudab midagi, siis **käivita handler**.

`handlers:` - Spetsiaalsed task'id mis käivituvad AINULT kui neid "notifyatakse". Kasutatakse teenuste restartimiseks - ei taha ju iga kord restartida, ainult kui config muutus.

---

## 6. YAML Põhitõed

![YAML syntax examples](https://thedeveloperstory.com/wp-content/uploads/2021/12/yaml-syntax.png)

YAML = "YAML Ain't Markup Language". Struktureeritud andmeformaat. Inimloetav.

### Võti-Väärtus Paarid

```yaml
name: nginx
port: 80
enabled: true
```

**KRIITILINE:** Pärast koolonit `:` PEAB olema tühik!

```yaml
name:nginx     # VALE
name: nginx    # ÕIGE
```

### Loendid

```yaml
packages:
  - nginx
  - php
  - mysql
```

Kriipsuga `-` algavad read on loendi elemendid. Taanded peavad olema õiged.

### Pesastatud Struktuurid

```yaml
server:
  name: web1
  ip: 10.0.0.10
  port: 80
```

Taanded näitavad hierarhiat.

### Mitme Rea Stringid

```yaml
message: |
  See on
  mitme rea
  tekst.
```

`|` säilitab reavahetused.

### Muutujad

```yaml
port: 8080
url: "http://example.com:{{ port }}"
```

`{{ port }}` asendatakse väärtusega `8080`.

### Kommentaarid

```yaml
# See on kommentaar
name: nginx  # See ka on kommentaar
```

### Tavalised Vead

**1. TAB kasutamine:**

YAML EI LUBA tab'e. Ainult tühikud. Tavaliselt 2 või 4 tühikut per tase.

```yaml
tasks:
[TAB]- name: Bad          # VALE - saad vea
  - name: Good            # ÕIGE
```

**2. Puuduv tühik pärast koolonit:**

```yaml
name:nginx    # VALE
name: nginx   # ÕIGE
```

**3. Valed taanded:**

```yaml
tasks:
  - name: Task 1
  apt:              # VALE - peaks olema 4 tühikut
    name: nginx
```

**4. Jutumärkide probleem:**

Tavaliselt ei vaja:
```yaml
name: nginx           # OK
name: "nginx"         # OK, aga mitte vajalik
```

Vajad kui on erisümbolid:
```yaml
message: "Port: {{ port }}"    # Vajab jutumärke
```

### YAML Validator

Kui kahtled, kasuta [yamllint.com](http://www.yamllint.com/) või:

```bash
ansible-playbook --syntax-check playbook.yml
```

---

## 7. Moodulid - Ansible'i Tööriistad

![Popular Ansible modules](https://www.middlewareinventory.com/wp-content/uploads/2022/11/ansible-uri-module-parameters-1024x906.png)

Ansible'is on üle 3000 moodulit. Ei pea kõiki teadma - umbes 20-30 katab 90% juhtudest.

### Paketihaldus

**apt** - Debian/Ubuntu:
```yaml
- apt:
    name: nginx
    state: present
    update_cache: yes
```

**yum/dnf** - RedHat/Alma/Rocky:
```yaml
- yum:
    name: nginx
    state: present
```

**package** - OS-agnostiline:
```yaml
- package:
    name: nginx
    state: present
```

### Teenuste Haldus

**service/systemd:**
```yaml
- service:
    name: nginx
    state: started
    enabled: yes
```

`state: started` - käivita kui ei tööta
`enabled: yes` - käivitu boot'imisel

### Failide Haldus

**copy** - kopeeri fail:
```yaml
- copy:
    src: local_file.txt
    dest: /tmp/remote_file.txt
    owner: ubuntu
    mode: '0644'
```

**template** - genereeri failist template'ist:
```yaml
- template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
```

**file** - halda faile/kaustu:
```yaml
- file:
    path: /opt/app
    state: directory
    mode: '0755'
```

`state: directory` - loo kaust
`state: absent` - kustuta
`state: touch` - loo tühi fail

**lineinfile** - halda ridu failis:
```yaml
- lineinfile:
    path: /etc/hosts
    line: "10.0.0.10 web1.local"
```

Idempotent - lisab ainult kui puudub.

### Kasutajad ja Grupid

**user:**
```yaml
- user:
    name: deploy
    shell: /bin/bash
    groups: sudo
    append: yes
```

**group:**
```yaml
- group:
    name: developers
    state: present
```

### Käsud

**command** - turvaline, piiratud:
```yaml
- command: /usr/bin/uptime
```

Ei luba pipe'e `|`, redirection'i `>`, environment muutujaid.

**shell** - võimsam, ohtlikum:
```yaml
- shell: cat /var/log/nginx/access.log | grep ERROR > /tmp/errors.txt
```

Lubab kõike. Kasuta ainult kui `command` ei piisa.

### Debugimine

**debug** - prindi info:
```yaml
- debug:
    msg: "Server IP: {{ ansible_default_ipv4.address }}"
```

**assert** - kontrolli tingimust:
```yaml
- assert:
    that:
      - ansible_distribution == "Ubuntu"
    fail_msg: "Must be Ubuntu!"
```

### Dokumentatsioon

```bash
ansible-doc <module>
```

Näiteks:
```bash
ansible-doc apt
ansible-doc service
ansible-doc copy
```

Näitab kõiki parameetreid, näiteid, selgitusi.

---

## 8. Praktiline Demo (Illustratsioon)

See on lühike illustratsioon. Labor algab järgmisel tunnil.

### Setup

Meil on:
- Windows jumpbox (VS Code, WSL2)
- WSL2'is Ansible installitud
- 4 Linux serverit (2 Ubuntu, 2 Alma)
- Inventory fail valmis

### 1. Ping Test

```bash
ansible -i inventory.ini all -m ping
```

Väljund:
```
ubuntu1 | SUCCESS => {"ping": "pong"}
ubuntu2 | SUCCESS => {"ping": "pong"}
alma1   | SUCCESS => {"ping": "pong"}
alma2   | SUCCESS => {"ping": "pong"}
```

Kõik ühendused töötavad!

### 2. Ad-hoc - Uptime

```bash
ansible -i inventory.ini all -m command -a "uptime"
```

Väljund:
```
ubuntu1 | CHANGED | rc=0 >>
 15:23:11 up 2 days, 4:15

ubuntu2 | CHANGED | rc=0 >>
 15:23:11 up 2 days, 4:15

alma1 | CHANGED | rc=0 >>
 15:23:11 up 5 days, 10:32

alma2 | CHANGED | rc=0 >>
 15:23:11 up 5 days, 10:32
```

### 3. Lihtne Playbook

Fail `demo.yml`:

```yaml
---
- name: Show system info
  hosts: all
  
  tasks:
    - name: Display server details
      debug:
        msg: |
          Hostname: {{ ansible_hostname }}
          OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
          IP: {{ ansible_default_ipv4.address }}
          Memory: {{ ansible_memtotal_mb }} MB
```

Käivitame:

```bash
ansible-playbook -i inventory.ini demo.yml
```

Väljund näitab iga serveri kohta:
```
TASK [Display server details]
ok: [ubuntu1] => 
  msg: |-
    Hostname: ubuntu1
    OS: Ubuntu 22.04
    IP: 10.0.0.10
    Memory: 4096 MB
...
```

Idempotentne - võib käivitada mitu korda, tulemus sama.

---

## 9. Millal EI Kasuta Ansible'it?

Ansible ei ole universaalne lahendus. On olukordi kus teised tööriistad on paremad.

### Ei Sobi:

**1. Rakenduste Deployment**

Ansible loob infrastruktuuri, aga ei deploy rakendusi. Selle jaoks:
- **Docker + Docker Compose** - containerid
- **Kubernetes** - orkestratsioon
- **CI/CD** (GitLab CI, GitHub Actions) - automaatne deployment

**2. Keeruline State Management**

Ansible ei hoia "state'i" nagu Terraform. Kui kustutate playbook'ist ressursi, Ansible EI KUSTUTA seda serverist. Terraform jälgib state'i ja kustutab.

**3. Reaalajas Monitoring**

Ansible käivitab käsud kui TEIE käivitate. See ei jälgi servereid 24/7. Selleks:
- **Prometheus + Grafana** - monitoring
- **ELK Stack** - logide analüüs
- **Zabbix, Nagios** - alerting

**4. Windows Serverid (osaliselt)**

Ansible toetab Windows'i aga SSH ei tööta seal hästi. Windows kasutab WinRM. Kui peamine platvorm on Windows, võib Puppet või PowerShell DSC olla parem valik.

**5. Agent-Based Eelistus**

Kui te TAHATE et serverid hoiavad end ise soovitud seisundis ilma teie sekkumiseta, siis pull mudel (Puppet, Chef) võib olla parem.

### Parim Kasutusviis

**Ansible + Teised:**

```
Terraform → loob infrastruktuuri (serverid, võrk)
     ↓
Ansible → seadistab servereid (paigaldab tarkvara)
     ↓
Docker/K8s → deploy'b rakendusi
     ↓
Prometheus → jälgib süsteemi
```

Igaüks teeb seda milles ta on hea.

---

## Kokkuvõte

### Meeles Pidada

**Ansible on:**
- Automatiseerimisvahend serverite haldamiseks
- Agentless (kasutab SSH-d)
- Push-based (te otsustate millal)
- Idempotent (turvaline mitu korda)
- Lihtne õppida (YAML, ei vaja programmeerimist)

**Komponendid:**
- **Inventory** - kellele käske saata
- **Ad-hoc** - kiired testid
- **Playbooks** - automatiseeritud töövood

**Millal kasutada:**
- Serverite provisioneerimine
- Konfiguratsioonihaldus
- Mitmete serverite paralleelne haldamine
- Korratavad deployment'id

**Millal EI kasuta:**
- Rakenduste deployment (Kubernetes parem)
- State management (Terraform parem)
- 24/7 monitoring (Prometheus parem)

### Järgmine Samm

Järgmisel tunnil - **Labor**. Te teete kõike ise:
- Seadistate SSH key'd
- Kirjutate inventory faili
- Käivitate ad-hoc käske
- Kirjutate playbook'e
- Paigaldate nginx'i

### Ressursid

**Dokumentatsioon:**
- [docs.ansible.com](https://docs.ansible.com/) - ametlik dokumentatsioon
- [galaxy.ansible.com](https://galaxy.ansible.com/) - valmis playbook'id ja rollid

**Õppimine:**
- `ansible-doc <module>` - mooduli dokumentatsioon
- [yamllint.com](http://www.yamllint.com/) - YAML validaator

**Kogukond:**
- Reddit r/ansible
- Ansible GitHub discussions
- DevOps Estonia meetup'id

---

**Viimane Mõte:**

Käsitsi serverhaldus võtab 4+ tundi ja on vigadega. Ansible võtab 3 minutit ja on õige iga kord.

Valik on lihtne.

Näeme laboris! 🚀
