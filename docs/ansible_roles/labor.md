# Ansible Rollid Labor

**Eeldused:** Ansible playbook'ide kogemus, Linux CLI, YAML põhitundmine, Vagrant keskkond  
**Platvorm:** Ansible 2.9+, Ubuntu 20.04+, Vagrant 2.2+

## Õpiväljundid

Pärast seda laborit õppija:

- Loob Galaxy standardi järgi struktureeritud Ansible rolli
- Seadistab template'e Jinja2 süntaksiga konfiguratsioonide dünaamiliseks genereerimiseks
- Käivitab handlers'eid teenuste kontrollitud taaskäivitamiseks
- Debugib rolle isoleeritud testikeskkondades
- Rakendab rollide sõltuvusi infrastruktuuri komponentide koordineerimiseks

---

Selles laboris ehitate professionaalse nginx rolli, mis sisaldab SSL tuge, virtual hosts'e ja OS-abstraktsiooni. Eesmärk pole lihtsalt nginx paigaldamine - seda saaksite 5-realisena. Eesmärk on mõista kuidas roll struktureerida nii, et seda saaks kasutada kümnes erinevas projektis erinevate nõuetega.

## 1. Töökeskkonna Ettevalmistus

Esimene samm on luua puhta testkeskkonna. Vagrant võimaldab disposable virtuaalmasinaid, kus saate eksperimenteerida ilma oma süsteemi mõjutamata. Iga labor algab puhtalt lehelt.

Looge projekti kataloog ja liikuge sinna. See hoiab kõik labori failid organiseeritult ühes kohas.

```bash
mkdir -p ~/ansible-roles-lab
cd ~/ansible-roles-lab
```

### Vagrantfile loomine

Vagrantfile defineerib virtuaalmasina konfiguratsiooni. Kasutame Ubuntu 20.04 baasina koos port forwarding'uga, et saaksime nginx'i testimiseks brauseris avada.

```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "ansible-lab"
  
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 443, host: 8443
  
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 2
  end
  
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-pip
  SHELL
end
```

Port forwarding võimaldab ligi pääseda VM'is töötavale nginx'ile oma host masina brauserist. Port 80 VM'is → port 8080 hostis. See võimaldab testimist ilma VM'i sisse logimata.

### VM käivitamine ja ühenduse testimine

Käivitage virtuaalmasin ja ühenduge sellega SSH kaudu. Esimene `vagrant up` võtab mõned minutid, kuna see laeb alla Ubuntu image'i.

```bash
vagrant up
vagrant ssh
```

VM peaks käivituma paar minutit. Kui ühendus õnnestub, näete Ubuntu command prompti. Kontrollime kas Python on olemas - Ansible vajab seda target masinas.

Kontrollige, et Python3 on paigaldatud ja töötab. See on Ansible'i ainus sõltuvus target masinas.

```bash
python3 --version
# Python 3.8.10

which python3
# /usr/bin/python3
```

### Validation

- [ ] Vagrant VM käivitub ilma vigadeta
- [ ] SSH ühendus VM'iga töötab
- [ ] Python3 on paigaldatud
- [ ] Port forwarding on seadistatud (8080, 8443)

Kui mõni punkt ebaõnnestub, vaadake Vagrantfile süntaksi ja VirtualBox installatsioon. Tavalisemad vead: VirtualBox ei ole paigaldatud, VM memory liiga väike, port conflict hostis.

## 2. Rolli Struktuuri Loomine

Ansible Galaxy pakub init käsku, mis genereerib standardse rolli struktuuri. See on õige viis alustada - ära kunagi loo kaustu käsitsi.

Looge rollide kataloog ja initsialiseerige uus roll nimega `nginx-webserver`. Galaxy loob automaatselt kõik vajalikud kataloogid ja failid.

```bash
# VM'is
mkdir -p ~/roles
cd ~/roles
ansible-galaxy init nginx-webserver
```

Tulem on standardne rolli kataloogistruktuur. Iga kataloog omab spetsiifilist eesmärki Ansible roles arhitektuuris.

```text
nginx-webserver/
├── README.md
├── defaults/
│   └── main.yml
├── files/
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── tasks/
│   └── main.yml
├── templates/
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/
    └── main.yml
```

Uurime struktuuri lähemalt. Iga kaust omab eesmärki.

Vaadake loodud struktuuri ja uurige esialgseid faile. Praegu on enamik faile tühjad või sisaldavad ainult placeholder teksti.

```bash
tree nginx-webserver/
cat nginx-webserver/tasks/main.yml  # Praegu tühi
cat nginx-webserver/meta/main.yml   # Galaxy info template
```

### Metadata konfiguratsioon

Muudame `meta/main.yml` faili, et kirjeldada meie rolli. See metadata on oluline kui kavatsete rolli Galaxy'sse üles laadida või jagada teistega.

```yaml
# nginx-webserver/meta/main.yml
---
galaxy_info:
  role_name: nginx_webserver
  author: "ITS-24 Student"
  description: "Production Nginx with SSL and virtual hosts"
  license: MIT
  min_ansible_version: "2.9"
  
  platforms:

    - name: Ubuntu
      versions:

        - focal
        - jammy
    - name: Debian
      versions:

        - bullseye
  
  galaxy_tags:

    - web
    - nginx
    - ssl
    - proxy

dependencies: []
```

Platforms seksioon määrab toetatud OS'id. Galaxy näitab seda kasutajatele. Min ansible version hoiatab kui keegi proovib vana versiooniga. Tags aitavad rolli otsimisel.

### Validation

- [ ] Role struktuur on loodud Galaxy init'iga
- [ ] Meta/main.yml on täidetud
- [ ] Kõik standard kaustad eksisteerivad
- [ ] Tree command näitab õiget struktuuri

Kontrollige, et roll on õigesti loodud ja Ansible suudab seda tuvastada. Need käsud kinnitavad, et struktuur on õige.

```bash
# Test
ansible-galaxy list
# Should show nginx-webserver role

cd nginx-webserver && ls -la
# Näitab kõiki kaustu
```

## 3. Variables ja Defaults Seadistamine

Rollid peavad olema konfigureeritavad. Defaults pakub mõistlikud vaikeväärtused, mida kasutaja saab üle kirjutada.

### Defaults loomine

Defineerige vaikeväärtused, mida roll kasutab kui kasutaja ei määra midagi teisiti. Need hõlmavad põhiseadeid, SSL konfiguratsiooni ja jõudluse parameetreid.

```yaml
# defaults/main.yml
---
# Basic config
nginx_user: "www-data"
nginx_worker_processes: "{{ ansible_processor_vcpus | default(2) }}"
nginx_worker_connections: 1024
nginx_pid_file: "/var/run/nginx.pid"

# Network
nginx_http_port: 80
nginx_https_port: 443
nginx_server_tokens: "off"

# SSL
nginx_ssl_enabled: false
nginx_ssl_cert_path: "/etc/ssl/certs/nginx.crt"
nginx_ssl_key_path: "/etc/ssl/private/nginx.key"

# Virtual hosts
nginx_vhosts: []
nginx_remove_default_vhost: true

# Performance
nginx_keepalive_timeout: 65
nginx_client_max_body_size: "1m"
```

Ansible facts nagu `ansible_processor_vcpus` detekteeritakse automaatselt. Default filter pakub fallback väärtust kui fact pole saadaval.

### OS-spetsiifilised variables

Looge `vars/main.yml` fail, mis sisaldab operatsioonisüsteemi-spetsiifilisi väärtusi. See võimaldab rollil töötada nii Debian kui RedHat baasil süsteemides.

```yaml
# vars/main.yml
---
_nginx_packages_map:
  Debian:

    - nginx
    - ssl-cert
    - curl
  RedHat:

    - nginx
    - mod_ssl
    - curl

nginx_packages: "{{ _nginx_packages_map[ansible_os_family] | default(_nginx_packages_map['Debian']) }}"

nginx_config_path: "/etc/nginx"
nginx_sites_available: "{{ nginx_config_path }}/sites-available"
nginx_sites_enabled: "{{ nginx_config_path }}/sites-enabled"
nginx_service_name: "nginx"
```

Sõnastik võimaldab OS-põhist valikut. RedHat süsteemid kasutavad teisi pakette kui Debian. Default fallback tagab töö isegi tundmatus OS'is.

### Validation

Testige muutujate laadimist ja töötlemist. Need käsud simuleerivad erinevaid süsteemi konfiguratsioone ja näitavad, kuidas Ansible neid väärtusi kasutab.

```bash
# Test variable loading
ansible localhost -m debug -a "var=nginx_worker_processes" \
  -e "ansible_processor_vcpus=4"
# Should show: 4

ansible localhost -m debug -a "var=nginx_packages" \
  -e "ansible_os_family=Debian"
# Should show: [nginx, ssl-cert, curl]
```

- [ ] Defaults/main.yml sisaldab dokumenteeritud muutujaid
- [ ] Vars/main.yml sisaldab OS-spetsiifilisi mappinguid
- [ ] Ansible facts'e kasutatakse default väärtusteks
- [ ] Variables testitakse debug mooduliga

## 4. Tasks Implementeerimine

Tasks kaust sisaldab tegelikku tööd. Hea praktika on eraldada task'id loogilistesse failidesse.

### Main tasks orchestration

Looge peamine `tasks/main.yml` fail, mis orkestreerib kõik teised task failid. See toimib koordinaatorina, kutsudes alamtaske õiges järjekorras.

```yaml
# tasks/main.yml
---
- name: "Include OS-specific variables"
  include_vars: "{{ ansible_os_family }}.yml"
  failed_when: false

- name: "Validate configuration"
  include_tasks: validate.yml

- name: "Install Nginx packages"
  include_tasks: install.yml

- name: "Configure Nginx"
  include_tasks: configure.yml

- name: "Setup SSL certificates"
  include_tasks: ssl.yml
  when: nginx_ssl_enabled | bool

- name: "Configure virtual hosts"
  include_tasks: vhosts.yml
  when: nginx_vhosts | length > 0

- name: "Ensure Nginx is running"
  include_tasks: service.yml
```

Include_tasks on dünaamiline - when conditionals töötavad. Failed_when false tähendab et kui OS-spetsiifilist faili pole, jätkame vaikimisi väärtustega.

### Validation tasks

Looge `tasks/validate.yml`, mis kontrollib kasutaja sisestatud väärtusi enne peamiste operatsioonide käivitamist. See hoiab ära vead hilisemates etappides.

```yaml
# tasks/validate.yml
---
- name: "Ensure nginx_http_port is valid"
  assert:
    that:

      - nginx_http_port is number
      - nginx_http_port > 0
      - nginx_http_port < 65536
    fail_msg: "nginx_http_port must be 1-65535, got {{ nginx_http_port }}"
    quiet: true

- name: "Ensure nginx_https_port is valid"
  assert:
    that:

      - nginx_https_port is number
      - nginx_https_port > 0
      - nginx_https_port < 65536
    fail_msg: "nginx_https_port must be 1-65535, got {{ nginx_https_port }}"
    quiet: true

- name: "Check sufficient RAM"
  assert:
    that:

      - ansible_memtotal_mb >= 256
    fail_msg: "Minimum 256MB RAM required, found {{ ansible_memtotal_mb }}MB"
    quiet: true
```

Assert moodul peatab playbook'i kui tingimus ebaõnnestub. Quiet flag peidab verbose output'i õnnestumise korral.

### Install tasks

Looge `tasks/install.yml`, mis paigaldab Nginx paketi ja seotud sõltuvused. See fail kasutab OS-agnostilist `package` moodulit.

```yaml
# tasks/install.yml
---
- name: "Update apt cache"
  apt:
    update_cache: yes
    cache_valid_time: 3600
  when: ansible_os_family == "Debian"

- name: "Install Nginx packages"
  package:
    name: "{{ nginx_packages }}"
    state: present

- name: "Ensure nginx service exists"
  service:
    name: "{{ nginx_service_name }}"
    enabled: yes
```

Cache_valid_time:

- 3600 tähendab "kui apt cache on värskem kui 1h, ära uuenda". See kiirendab korduvaid käivitamisi. Package moodul on OS-agnostic
- töötab nii apt kui yum'iga.

### Validation

Testme kas install töötab. Käivitage roll lokaalselt, et näha kas Nginx paigaldus õnnestub.

```bash
cd ~/roles
ansible-playbook -i localhost, -c local tests/test.yml

# Või otse role apply
ansible localhost -m include_role -a name=nginx-webserver --become
```

Kontrollige tulemust. Need käsud kinnitavad, et Nginx on korralikult paigaldatud ja töötab.

```bash
systemctl status nginx
# Should be active (running)

nginx -v
# nginx version: nginx/1.18.0 (Ubuntu)

which nginx
# /usr/sbin/nginx
```

- [ ] Nginx pakett on paigaldatud
- [ ] Nginx service on enabled
- [ ] Nginx on aktiivselt käimas
- [ ] Nginx binary on leitav PATH'is

## 5. Templates ja Konfiguratsioon

Templates võimaldavad dünaamilisi konfiguratsioone. Jinja2 süntaks on sarnane Python'i string formatting'ule.

### Peamine nginx.conf template

Looge `templates/nginx.conf.j2` fail, mis genereerib peamise Nginx konfiguratsiooni. Template kasutab muutujaid, mida me varem defineerisime.

```jinja2
# templates/nginx.conf.j2
# {{ ansible_managed }}
# DO NOT EDIT MANUALLY - managed by Ansible

user {{ nginx_user }};
worker_processes {{ nginx_worker_processes }};
pid {{ nginx_pid_file }};

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
    keepalive_timeout {{ nginx_keepalive_timeout }};
    types_hash_max_size 2048;
    server_tokens {{ nginx_server_tokens }};
    client_max_body_size {{ nginx_client_max_body_size }};

    # MIME types
    include {{ nginx_config_path }}/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

{% if nginx_ssl_enabled %}
    # SSL Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
{% endif %}

    # Virtual Host Configs
    include {{ nginx_sites_enabled }}/*;
}
```

Ansible_managed muutuja genereerib kommentaari "This file is managed by Ansible". Conditional blocks (`{% if %}`) lubavad SSL konfiguratsiooni ainult vajadusel.

### Virtual host template

Looge `templates/vhost.conf.j2`, mis defineerib individuaalse virtual host'i konfiguratsiooni. Template toetab nii HTTP kui HTTPS režiime ja teeb automaatse redirecti SSL-i kasutamisel.

```jinja2
# templates/vhost.conf.j2
{% if item.ssl | default(nginx_ssl_enabled) %}
# HTTPS server for {{ item.name }}
server {
    listen {{ nginx_https_port }} ssl http2;
    server_name {{ item.name }};

    ssl_certificate {{ nginx_ssl_cert_path }};
    ssl_certificate_key {{ nginx_ssl_key_path }};

    root {{ item.root | default('/var/www/' + item.name) }};
    index {{ item.index | default('index.html index.htm') }};

    location / {
        try_files $uri $uri/ =404;
    }
}

# HTTP redirect to HTTPS
server {
    listen {{ nginx_http_port }};
    server_name {{ item.name }};
    return 301 https://$server_name$request_uri;
}

{% else %}
# HTTP server for {{ item.name }}
server {
    listen {{ nginx_http_port }};
    server_name {{ item.name }};

    root {{ item.root | default('/var/www/' + item.name) }};
    index {{ item.index | default('index.html index.htm') }};

    location / {
        try_files $uri $uri/ =404;
    }
}
{% endif %}
```

Item viitab loop muutujale. Template renderdatakse iga virtual hosti jaoks eraldi. Default filter pakub fallback väärtusi.

### Configure tasks

Looge `tasks/configure.yml`, mis deploy'b template'id serverisse. See fail kasutab `validate` parameetrit, et testida konfiguratsiooni enne rakendamist.

```yaml
# tasks/configure.yml
---
- name: "Remove default vhost"
  file:
    path: "{{ nginx_sites_enabled }}/default"
    state: absent
  when: nginx_remove_default_vhost
  notify: reload nginx

- name: "Deploy main nginx.conf"
  template:
    src: nginx.conf.j2
    dest: "{{ nginx_config_path }}/nginx.conf"
    owner: root
    group: root
    mode: '0644'
    validate: 'nginx -t -c %s'
  notify: reload nginx

- name: "Ensure sites-available directory exists"
  file:
    path: "{{ nginx_sites_available }}"
    state: directory
    mode: '0755'

- name: "Ensure sites-enabled directory exists"
  file:
    path: "{{ nginx_sites_enabled }}"
    state: directory
    mode: '0755'
```

Validate parameeter testib konfiguratsiooni enne deployment'i. %s asendatakse temp failiga. Kui nginx -t ebaõnnestub, template ei deploy'ta.

### Validation

Testige konfiguratsiooni deployment'i. Käivitage roll uuesti ja kontrollige, kas Nginx conf failid on korrektselt genereeritud.

```bash
# Apply role
ansible-playbook tests/test.yml

# Check config
sudo nginx -t
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# Check rendered config
sudo cat /etc/nginx/nginx.conf
# Should see actual values, not {{ variables }}
```

- [ ] Template on renderdatud ilma vigadeta
- [ ] Nginx -t valideerib konfiguratsiooni
- [ ] Muutujad on asendatud tegelike väärtustega
- [ ] Conditional blocks töötavad ootuspäraselt

## 6. SSL ja Virtual Hosts

SSL võimaldab HTTPS ühendusi. Isegi kui kasutate ise-allkirjastatud sertifikaate (testimiseks), on konfiguratsioon sama mis produktsioonis CA sertifikaatidega.

### SSL tasks

Looge `tasks/ssl.yml`, mis genereerib ise-allkirjastatud SSL sertifikaadi. Produktsioonis asendaksite selle Let's Encrypt või CA sertifikaadiga, aga loogika jääb samaks.

```yaml
# tasks/ssl.yml
---
- name: "Ensure SSL directories exist"
  file:
    path: "{{ item }}"
    state: directory
    owner: root
    group: root
    mode: '0755'
  loop:

    - /etc/ssl/certs
    - /etc/ssl/private

- name: "Generate self-signed SSL certificate"
  command: >
    openssl req -x509 -nodes -days 365
    -newkey rsa:2048
    -keyout {{ nginx_ssl_key_path }}
    -out {{ nginx_ssl_cert_path }}
    -subj "/C=EE/ST=Harjumaa/L=Tallinn/O=ITS-24/CN={{ ansible_fqdn }}"
  args:
    creates: "{{ nginx_ssl_cert_path }}"
  notify: restart nginx

- name: "Set private key permissions"
  file:
    path: "{{ nginx_ssl_key_path }}"
    owner: root
    group: root
    mode: '0600'
```

Creates parameeter tagab idempotentsuse. Kui sertifikaat eksisteerib, käsk ei käivitu. Mode 0600 tähendab ainult owner saab lugeda private key't.

### Virtual hosts tasks

Looge `tasks/vhosts.yml`, mis seadistab mitut virtual host'i. See fail loob document root'id, deploy'b konfiguratsioone ja aktiveerib need symlink'ide kaudu.

```yaml
# tasks/vhosts.yml
---
- name: "Create document root directories"
  file:
    path: "{{ item.root | default('/var/www/' + item.name) }}"
    state: directory
    owner: "{{ nginx_user }}"
    group: "{{ nginx_user }}"
    mode: '0755'
  loop: "{{ nginx_vhosts }}"

- name: "Deploy virtual host configs"
  template:
    src: vhost.conf.j2
    dest: "{{ nginx_sites_available }}/{{ item.name }}.conf"
    owner: root
    group: root
    mode: '0644'
    validate: 'nginx -t -c /dev/null -p {{ nginx_config_path }}'
  loop: "{{ nginx_vhosts }}"
  notify: reload nginx

- name: "Enable virtual hosts"
  file:
    src: "{{ nginx_sites_available }}/{{ item.name }}.conf"
    dest: "{{ nginx_sites_enabled }}/{{ item.name }}.conf"
    state: link
  loop: "{{ nginx_vhosts }}"
  notify: reload nginx

- name: "Create index.html for virtual hosts"
  copy:
    content: |
      <!DOCTYPE html>
      <html>
      <head><title>{{ item.name }}</title></head>
      <body>
        <h1>{{ item.name }}</h1>
        <p>Configured by Ansible nginx-webserver role</p>
      </body>
      </html>
    dest: "{{ item.root | default('/var/www/' + item.name) }}/index.html"
    owner: "{{ nginx_user }}"
    mode: '0644'
  loop: "{{ nginx_vhosts }}"
```

Symlink sites-enabled'is aktiveerib virtual hosti. Selle eemaldamine deaktiveerib ilma config faili kustutamata.

### Test playbook virtual hostidega

Looge täiendatud `tests/test.yml` fail, mis testib rolli koos SSL ja mitme virtual host'iga. See simuleerib reaalset kasutusjuhtu.

```yaml
# tests/test.yml
---
- name: "Test nginx-webserver role"
  hosts: localhost
  become: yes
  
  vars:
    nginx_ssl_enabled: true
    nginx_vhosts:

      - name: test.local
        ssl: true
      - name: demo.local
        ssl: false
        root: /var/www/demo
  
  roles:

    - nginx-webserver
```

### Validation

Käivitage playbook ja testige, kas virtual hostid ja SSL töötavad korrektselt. Need käsud kontrollivad erinevaid aspekte teie seadistusest.

```bash
# Apply
ansible-playbook tests/test.yml

# Test SSL
curl -k https://localhost
# Should return HTML

# Test HTTP redirect
curl -I http://localhost
# Should see 301 redirect

# Check vhosts
ls -la /etc/nginx/sites-enabled/
# test.local.conf -> ../sites-available/test.local.conf
# demo.local.conf -> ../sites-available/demo.local.conf

# Test document roots
ls -la /var/www/
# test.local/
# demo/
```

- [ ] SSL sertifikaat on genereeritud
- [ ] Private key permissions on 0600
- [ ] Virtual hosts config failid on loodud
- [ ] Symlinks sites-enabled'is töötavad
- [ ] Document roots eksisteerivad õigete õigustega
- [ ] Curl testid õnnestuvad

## 7. Handlers ja Service Management

Handlers käivitavad teenuse restardi ainult muudatuste korral. See on efektiivsem kui restart iga task'i järel.

### Handlers definitsioon

Looge `handlers/main.yml`, mis defineerib kolm handler'it: restart, reload ja validate. Reload on kiirem kui restart, sest ei katkesta aktiivseid ühendusi.

```yaml
# handlers/main.yml
---
- name: restart nginx
  service:
    name: "{{ nginx_service_name }}"
    state: restarted
  listen: restart nginx

- name: reload nginx
  service:
    name: "{{ nginx_service_name }}"
    state: reloaded
  listen: reload nginx

- name: validate nginx config
  command: nginx -t
  changed_when: false
  listen: validate nginx config
```

Listen direktiiv võimaldab mitmel handleriel sama nime. Changed_when: false tähendab et see task ei muuda süsteemi olekut.

### Service tasks

Looge `tasks/service.yml`, mis tagab, et Nginx teenus on alati käimas ja süsteemi käivitamisel aktiveerib. See fail valideerib ka konfiguratsiooni.

```yaml
# tasks/service.yml
---
- name: "Ensure nginx is started and enabled"
  service:
    name: "{{ nginx_service_name }}"
    state: started
    enabled: yes

- name: "Validate nginx configuration"
  command: nginx -t
  changed_when: false
  check_mode: no
```

Check_mode: no tähendab et see task käivitatakse ka dry-run režiimis. Validatsioon on safe operation.

### Validation

Testme kas handlers töötavad korrektselt. Muudame konf faili ja kontrollime, kas handler käivitub. Seejärel testame ilma muudatusteta.

```bash
# Muuda config
echo "# test comment" | sudo tee -a /etc/nginx/nginx.conf

# Run playbook
ansible-playbook tests/test.yml

# Check logs - peaks nägema reload nginx
# Handler peaks käivituma

# Test ilma muudatusteta
ansible-playbook tests/test.yml
# Handlers ei käivitu kui pole muudatusi
```

- [ ] Handlers on defineeritud
- [ ] Service on enabled ja running
- [ ] Reload handler käivitub config muudatuse korral
- [ ] Handlers ei käivitu kui pole muudatusi

## Kontrollnimekiri

Enne töö lõpetamist kontrollige:

- [ ] Role struktuur järgib Galaxy standardit
- [ ] Kõik tasks failid on loogiliselt eraldatud
- [ ] Templates renderdavad korrektselt
- [ ] Validation tasks kontrollivad sisendeid
- [ ] SSL sertifikaadid genereeritakse automaatselt
- [ ] Virtual hosts konfiguratsioon töötab
- [ ] Handlers käivituvad ainult muudatuste korral
- [ ] Role töötab Ubuntu 20.04 VM'is
- [ ] Nginx on kättesaadav localhost:8080 kaudu
- [ ] SSL töötab localhost:8443 kaudu

## Troubleshooting

### Vagrant VM ei käivitu

Kui VM ei käivitu, kontrollige VirtualBox'i paigaldust ja VM staatust. Vahel aitab VM täielik kustutamine ja uuesti loomine.

```bash
# Check VirtualBox
vboxmanage --version

# Check VM status
vagrant status

# Destroy and recreate
vagrant destroy -f
vagrant up
```

### Ansible ei leia rolli

Kui Ansible ei leia teie rolli, kontrollige roles path'i. Vaikimisi otsib Ansible ./roles kataloogist ja süsteemsest asukohast.

```bash
# Check roles path
ansible-config dump | grep ROLES_PATH

# List roles
ansible-galaxy list

# Set roles path explicitly
export ANSIBLE_ROLES_PATH=~/roles
```

### Nginx config test ebaõnnestub

Kui Nginx konfiguratsiooni valideerimine ebaõnnestub, kontrollige süntaksit ja failide olemasolu. Journalctl näitab detailset vea kirjeldust.

```bash
# Manual test
sudo nginx -t

# Check syntax
sudo cat /etc/nginx/nginx.conf

# Check includes
ls -la /etc/nginx/sites-enabled/

# See error details
sudo journalctl -u nginx -n 50
```

### SSL sertifikaat ei genereeru

Kui SSL sertifikaadi genereerimine ebaõnnestub, kontrollige OpenSSL paigaldust ja kataloogide õigusi. Proovige ka manuaalset genereerimist.

```bash
# Check openssl
which openssl
openssl version

# Check directories
ls -la /etc/ssl/certs
ls -la /etc/ssl/private

# Manual generation
sudo openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx.key \
  -out /etc/ssl/certs/nginx.crt \
  -subj "/C=EE/CN=localhost"
```

### Handlers ei käivitu

Kui handlers ei käivitu, kontrollige kas tasks tõepoolest muutsid midagi. Verbose režiim näitab "changed" staatust. Saate ka sundida handler'eid käivituma.

```bash
# Check if tasks changed
ansible-playbook tests/test.yml -v
# Look for "changed: [localhost]"

# Force handlers
ansible-playbook tests/test.yml --force-handlers

# Check handler syntax
ansible-playbook tests/test.yml --syntax-check
```

### Port forwarding ei tööta

Kui ei saa brauserist Nginx'ile ligi, kontrollige Vagrant port forwarding'u ja Nginx porte. Reload aitab kui konfiguratsioon muutus.

```bash
# Check Vagrant
vagrant reload

# Check nginx ports
sudo netstat -tlnp | grep nginx

# Test from host
curl http://localhost:8080
curl -k https://localhost:8443

# Check firewall
sudo ufw status
```

Edu laboriga! Järgmine samm on kodutöö, kus rakendad neid oskusi iseseisva projekti jaoks.