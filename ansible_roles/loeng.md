#  Ansible rollid – labor: struktuur

Tänases laboris õpid rolle kasutama kui professionaalset viisi Ansible koodi organiseerimiseks ja taaskasutamiseks. Rollid aitavad hoida playbook'id lühikesed, struktuurne ja testitavad, et muudatused oleksid ohutud. Erinevalt tavalistest playbook'idest, kus kõik on ühes failis, võimaldavad rollid jagada koodi loogiliste komponentide vahel - nagu objektorienteeritud programmeerimises.

##  Õpiväljundid
Pärast seda lab'i oskad:
- Luua Ansible rolli Ansible Galaxy standardite järgi
- Mõista rolli struktuuri (tasks, handlers, templates, vars, defaults)
- Kasutada rolle playbook'ides
- Testida rolle isoleeritud keskkonnas
- Jagada rolle teiste arendajatega (Ansible Galaxy)

---

### 1. Rolli struktuur ja genereerimine
Selles blokis loote esimese rolli Galaxy standardi järgi ja uurite selle kaustastruktuuri. Eesmärk on mõista, kuhu milline osa (tasks, handlers, templates, vars, defaults) kuulub. Galaxy standard tagab, et kõik Ansible rollid järgivad sama struktuuri, mis teeb võõra koodi lugemise ja kasutamise lihtsamaks.
- **Tegevused:**
  - `ansible-galaxy init` - rolli genereerimine
  - Role struktuuri uurimine (tasks/, handlers/, templates/, vars/, defaults/)
  - `meta/main.yml` - metadata ja sõltuvused
  - Esimesed tasks rolli jaoks (nginx install)
- **Kontrollnimekiri:**
  - [ ] Role on genereeritud (`ansible-galaxy init`)
  - [ ] Mõistad iga kausta eesmärki
  - [ ] `meta/main.yml` on täidetud
  - [ ] Esimene task töötab
#### Kontrollküsimus
- Mis vahe on `defaults/` ja `vars/` kaustadel?

#### Refleksioon
- Ansible role on nagu... A) retsept  B) LEGO komplekt  C) moodul Pythonis

---

### 2. Templated ja handlerid
Fookus on Jinja2 templatel ja handleritel: kuidas muuta konfiguratsiooni dünaamiliseks ning taaskäivitada teenus ainult vajadusel. Lõpus testite rolli playbook'is. Templatede kasutamine on oluline, sest ühte template'i saab kasutada erinevates keskkondades, muutes ainult muutujate väärtusi - see on parem kui hoida kümneid peaaegu identset konfiguratsioonifaili.

- **Tegevused:**
  - Nginx config template loomine (`templates/nginx.conf.j2`)
  - Variables kasutamine template'ides (`{{ variable }}`)
  - Handler'ite seadistamine (nginx restart)
  - Rolli testimine playbook'iga
- **Kontrollnimekiri:**
  - [ ] Template fail on loodud (`templates/nginx.conf.j2`)
  - [ ] Variables toimivad template'is
  - [ ] Handler restartib nginx'i ainult muudatuse korral
  - [ ] Role töötab playbook'is
#### Kontrollküsimus
- Miks kasutada template'eid, mitte lihtsalt `copy` moodulit?

#### Refleksioon
- Jinja2 templated on nagu... A) Mad Libs mäng  B) kohandatav vorm  C) mõlemad

---

### 3. Rollide sõltuvused ja testimine
Õpite lisama rolli sõltuvusi ja kasutama mitut rolli samas playbook'is. Testimine toimub isoleeritud VM‑is, et käitumine oleks reprodutseeritav. Sõltuvuste haldamine on kriitiline keerulistes süsteemides - näiteks veebiserveri roll võib vajada tulemüüri rolli, mis peab käivituma enne.

- **Tegevused:**
  - Role sõltuvuste lisamine (`meta/main.yml` - dependencies)
  - Multiple roles playbook'is
  - Role testimine Vagrant VM'is
  - Ansible Galaxy rollide kasutamine
- **Kontrollnimekiri:**
  - [ ] Role sõltuvused on seadistatud
  - [ ] Playbook kasutab mitut rolli
  - [ ] Role töötab Vagrant VM'is
  - [ ] Tead, kuidas otsida rolle Ansible Galaxy'st
#### Kontrollküsimus
- Kuidas tagada, et role töötab erinevates keskkondades?

#### Refleksioon
- Kõige raskem osa oli... A) struktuur  B) templated  C) sõltuvused  D) sain hakkama!

---

**Valmis? Alustame detailsete sammudega!** ⬇

---

##  Ülevaade

**Loote:**
- Galaxy standard Nginx role
- Multi-OS tugi (Ubuntu/Debian)
- SSL sertifikaadid automaatselt
- Virtual hosts konfiguratsioon

**Role struktuuri põhimõte:** Ansible roles organiseerivad koodi modulaarselt. Iga komponent (tasks, templates, vars) on eraldatud, mis teeb koodi taaskasutatavaks ja hooldatavaks. Näiteks sama nginx rolli saab kasutada nii arendus-, test- kui ka produktsioonikeskkondades, muutes ainult muutujate väärtusi.

---

## Setup

### Role genereerimine
```bash
mkdir ~/ansible-roles-lab && cd ~/ansible-roles-lab
mkdir roles && cd roles
ansible-galaxy init nginx-webserver
tree nginx-webserver/
```

**Galaxy tool:** Genereerib standardse role struktuuri. Iga kaust omab spetsiifilist eesmärki - tasks (tegevused), templates (konfiguratsioonid), vars (muutujad). Ilma galaxy toolita peaks te ise käsitsi looma kõik kaustad ja failid - see tööriist säästab aega ja tagab standardse struktuuri.

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

**Metadata tähtsus:** Defineerib role sõltuvused, toetatud platvormid ja versiooniinfo. Galaxy kasutab seda role jagamisel. Kui keegi otsib Ansible Galaxy'st nginx rolli, siis need tags ja kirjeldus aitavad teie rolli leida.

---

## Variables

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

**Defaults vs vars:** Defaults on madalaima prioriteediga muutujad. Kasutaja saab neid kergesti üle kirjutada. Vars on kõrgema prioriteediga. Praktikas: defaults on "mõistlikud vaikeväärtused", vars on "need peavad sellised olema". Kui kasutaja määrab playbook'is `nginx_http_port: 8080`, siis see kirjutab default väärtuse üle.

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

**OS-specific variables:** Erinevad operatsioonisüsteemid vajavad erinevaid pakette. Sõnastikud võimaldavad dynaamiliset valikut. Näiteks CentOS'is võib nginx paketi nimi olla erinev või konfiguratsioonifailide asukohad võivad erineda - see lähenemine võimaldab ühel rollil töötada mitmes OS'is.

---

## Tasks struktuuri

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

**Modulaarne struktuur:** Igal alamülesandel on oma fail. See teeb koodi loetavaks ja debug'imist lihtsamaks. Kui midagi läheb valesti SSL seadistamisel, siis te täpselt teate, et vaadata `ssl.yml` faili, mitte otsida 500-realist main.yml'i läbi. See on nagu raamatu peatükkideks jagamine.

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

**Input validation:** Kontrollib kasutaja sisendeid enne rakendamist. Ennetab konfiguratsioonivigu ja süsteemitõrkeid. `assert` moodul on nagu programmeerimiskeeltes try-catch - kui tingimus ebaõnnestub, siis playbook peatub kohe selge veateate, mitte ei proovi poolelioleva konfiguratsiooniga edasi minna.

---

## SSL ja Virtual Hosts

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

**SSL sertifikaadid:** Ise-allkirjastatud sertifikaadid testiks. Produktsioonis kasutaksite CA sertifikaate. `creates` parameter tagab idempotentsuse. `creates` tähendab "kui see fail juba eksisteerib, siis ära käivita seda käsku uuesti" - muidu tekitaks Ansible iga käivitamisel uue sertifikaadi ja nginx peaks restartidata, mis on tarbetu. Privaatvõtme õigused `0600` tähendavad, et ainult omanik saab faili lugeda - turvaline praktika.

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

**Sites-available/enabled pattern:** Debian/Ubuntu standard. Konfiguratsioonid salvestatakse sites-available'sse, sites-enabled sisaldab symlinke aktiivsete saitide jaoks. See lähenemine võimaldab teil hoida kõiki saidi konfiguratsioone alles, aga aktiveerida/deaktiveerida neid ilma faile kustutamata - lihtsalt loote või kustutate symlinki.

---

## Templates

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

**Jinja2 templating:** Võimaldab dünaamilisi konfiguratsioone. Conditional blocks (`{% if %}`) ja muutujad (`{{ }}`) teevad template'i kohandatavaks. `{{ ansible_managed }}` on kommentaar, mis ütleb "see fail on Ansible poolt genereeritud, ära muuda käsitsi" - kasulik meeldetuletus administraatoritele. Jinja2 süntaks on sama, mida kasutatakse Flaskis ja Django's, seega need oskused on ülekantavad.

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

**Conditional SSL:** Template kohandub automaatselt SSL seadistuse järgi. HTTP redirect HTTPS'ile kui SSL on lubatud. `default()` filter Jinja2's tähendab "kui see muutuja pole määratud, siis kasuta seda vaikeväärtust" - see muudab template'i vastupidavamaks vigadele.

---

## Testimine

Selles jaotises käivitame rolli lokaalsetes tingimustes ja kontrollime, et nii HTTP kui ka HTTPS töötab. Eesmärk on kinnitada, et templated, handlerid ja muutujad käituvad ootuspäraselt. Testimine lokaalselt on kiirem kui Vagrant VM'i käivitamine ja võimaldab kiiresti itereerida.

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
Käivita testplaybook ja kontrolli tulemusi käsurealt. Veendu, et HTTP suunab HTTPS‑ile ja teenus on aktiivne. `connection: local` tähendab, et Ansible ei kasuta SSH'd, vaid käivitab käsud otse localhostis - see on kiirem testimiseks.

```bash
ansible-playbook test-nginx.yml

# Testimine
curl http://localhost          # peaks redirect'ima HTTPS'ile
curl -k https://localhost      # SSL test
sudo systemctl status nginx   # teenuse olek
```

**Testing strategy:** Alati testida nii HTTP kui HTTPS ühendusi. Kontrollida teenuse olekut ja logisid veakindluse tagamiseks. `-k` flag curl'is tähendab "eira SSL sertifikaadi vigu" - vajalik, sest kasutame ise-allkirjastatud sertifikaati, mida brauserid ei usalda.

---

## Handlers ja dokumentatsioon

Selles jaotises lisame handlerid muudatuste kontrollitud rakendamiseks ning kirjutame lühikese README, et roll oleks teistele arusaadav. Hästi dokumenteeritud roll vähendab vigu ja kiirendab kasutuselevõttu. README on esimene fail, mida keegi vaatab, kui proovib teie rolli kasutada.

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

**Handlers:** Käivitatakse ainult muudatuste korral. `notify` direktiiv tasks'ides käivitab handler'eid konfiguratsiooni muutmisel. Oluline detail: handlerid käivitatakse alati playbook'i lõpus, mitte kohe pärast notifyt - see tähendab, et kui kolm erinevat taski notifyvad sama handlerit, siis ta käivitatakse ainult üks kord. `reload` vs `restart`: reload loeb konfiguratsiooni uuesti ilma ühendusi katkestamata, restart on agressiivsem.

### README dokumentatsioon
Nimi ja eesmärk, lühike kasutusnäide ning peamised muutujad.

Näide kasutusest:
```yaml
- hosts: webservers
  roles:
    - nginx-webserver
```

Olulisemad muutujad:
- `nginx_ssl_enabled: false` – kasuta SSL‑i
- `nginx_vhosts: []` – virtuaalhostide nimekiri

**Dokumentatsiooni tähtsus:** Selgitab role kasutamist, muutujaid ja näiteid. Hea dokumentatsioon teeb role'i kasutatavaks teiste poolt. Lisage alati näited - inimesed õpivad paremini näidete kaudu kui abstraktsete kirjelduste kaudu.

Role on nüüd kasutamiseks valmis.