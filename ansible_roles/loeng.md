#  Ansible Rollid ja Puppet: Edasijõudnud Automatiseerimine

**Teemad:** Ansible rollid, Galaxy, Vagrant testimine, Puppet võrdlus

---

##  Õpiväljundid

Pärast seda loengut oskate:
- Mõista Ansible rollide struktuuri ja eeliseid
- Luua professionaalseid, taaskasutatavaid rolle
- Kasutada Ansible Galaxy kogukonda
- Testida rollide funktsionaalsust Vagrant'iga
- Võrrelda Ansible ja Puppet lähenemisi

---

## Vagrant testimiskeskkond

Selles jaotises loome eraldatud VM‑id rollide ohutuks testimiseks. Vagrant võimaldab kiiresti katsetada ja taastada keskkonda ilma päris servereid mõjutamata.

### Setup ja kasutamine
```bash
# Projekti alustamine
mkdir vagrant-test && cd vagrant-test
vagrant init ubuntu/jammy64
vagrant up
vagrant ssh
```

**Vagrant eesmärk:** Isoleeritud VM-id testimiseks. Saate lõhkuda ja kiiresti uuesti luua ilma päris servereid puudutamata.

### Multi-VM konfiguratsioon
```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.define "ansible-vm" do |ansible|
    ansible.vm.box = "ubuntu/jammy64"
    ansible.vm.network "private_network", ip: "192.168.56.11"
    ansible.vm.provision "ansible" do |a|
      a.playbook = "site.yml"
    end
  end
  
  config.vm.define "puppet-vm" do |puppet|
    puppet.vm.box = "ubuntu/jammy64"
    puppet.vm.network "private_network", ip: "192.168.56.12"
  end
end
```

**VM lifecycle:**
```bash
vagrant up [vm-name]      # käivita
vagrant halt [vm-name]    # peata
vagrant destroy [vm-name] # kustuta
vagrant snapshot save     # salvesta snapshot
```

---

## Ansible rollide arhitektuur

Selgitame, kuidas rollid muudavad playbook'i hooldatavaks: struktuur, üks vastutus korraga ja taaskasutus. Näitame, kuidas suur „ühe faili” playbook jagada loogilisteks rollideks.

### Spagettikood probleem
**Halb lähenemine:**
```yaml
# 800+ rea monster playbook - ärge tehke nii!
- name: Kõik ühes failis
  hosts: all
  tasks:
    # 100 nginx task'i
    # 80 mysql task'i  
    # 60 monitoring task'i
    # jne...
```

**Role'ide lahendus:**
```yaml
# Modulaarne, selge struktuur
- hosts: webservers
  roles:
    - common    # taaskasutatav
    - nginx     # üks vastutus
    - ssl       # isoleeritud

- hosts: dbservers  
  roles:
    - common    # sama role uuesti
    - mysql     # erinevad komponendid
```

### Role struktuur
```
nginx-role/
├── tasks/main.yml         # sammud järjest
├── defaults/main.yml      # vaikimisi seaded (nõrgad)
├── vars/main.yml          # sisemised muutujad (tugevad)
├── templates/nginx.conf.j2 # dünaamilised konfid
├── handlers/main.yml      # reaktsioonid muudatustele
├── meta/main.yml          # dependencies ja metadata
└── README.md              # kasutamise juhend
```

**Variable precedence (madal → kõrge):**
1. Role defaults
2. Group vars
3. Host vars
4. Play vars
5. Task vars
6. Command line (`-e`)

---

## Rollide parimad tavad

Praktilised soovitused rollide ülesehituseks: selged vaikeseaded, sisendi valideerimine ja modulaarne struktuur. Need põhimõtted hoiavad projektid loetavad ja töökindlad.

### Single Responsibility Principle
```
 Hea:                     Halb:
roles/                     roles/
├── nginx/                 └── web-stack/
├── mysql/                     (teeb kõike korraga)
├── php/
└── ssl/
```

### 80/20 konfigureeritavus
**Defaults - 80% juhtudest töötab:**
```yaml
# defaults/main.yml
nginx_port: 80
nginx_ssl_enabled: false
nginx_worker_processes: 2
```

**Advanced kasutamine - 20% juhtudest:**
```yaml
# playbook.yml
- role: nginx
  vars:
    nginx_port: 443
    nginx_ssl_enabled: true
    nginx_custom_config: |
      gzip on;
      gzip_types text/css;
```

### Input validation
```yaml
# tasks/validate.yml
- name: "Validate port number"
  assert:
    that:
      - nginx_port is number
      - nginx_port > 0
      - nginx_port < 65536
    fail_msg: "Port must be 1-65535, got: {{ nginx_port }}"

- name: "Check minimum RAM"
  assert:
    that:
      - ansible_memtotal_mb >= 512
    fail_msg: "Need at least 512MB RAM"
```

---

## Ansible Galaxy

Ansible Galaxy on kogukonna rollide kataloog. Õpime rolle otsima, paigaldama ja haldama koos fikseeritud versioonidega.

### Role'ide allalaadimine
```bash
# Otsimine
ansible-galaxy search nginx
ansible-galaxy search --author geerlingguy

# Installimine
ansible-galaxy install geerlingguy.nginx
ansible-galaxy install geerlingguy.nginx,2.8.0  # fikseeritud versioon
```

### Requirements fail
```yaml
# requirements.yml
---
- name: geerlingguy.nginx
  version: "2.8.0"
- name: geerlingguy.mysql
  version: "4.3.0"
- src: https://github.com/company/custom-role.git
  name: company.custom
```

```bash
ansible-galaxy install -r requirements.yml
```

### LAMP stack näide
```yaml
# 10 minutiga valmis LAMP
- hosts: webservers
  become: yes
  vars:
    mysql_databases:
      - name: myapp_db
    apache_vhosts:
      - servername: mysite.com
        documentroot: /var/www/mysite
  roles:
    - geerlingguy.apache
    - geerlingguy.mysql
    - geerlingguy.php
    - geerlingguy.certbot  # automaatne HTTPS
```

---

## Puppet vs Ansible

Võrdleme agentless push‑mudelit (Ansible) ja agent‑põhist pull‑mudelit (Puppet). Fookus: millal kumb sobib, arvestades meeskonna oskusi, skaleeritavust ja compliance’i.

### Arhitektuuriline erinevus

**Ansible (Push-based, agentless):**
```
Control node → SSH → Target servers
- Te kontrollite, millal muudatused toimuvad
- Vajab SSH ühendust
- "Fire and forget" lähenemine
```

**Puppet (Pull-based, agent-based):**
```
Puppet Master ← Agents (iga 30min) ← Target servers
- Serverid küsivad ise uuendusi
- Pidev drift detection
- Automaatne compliance enforcement
```

### Keele erinevus

**Ansible YAML:**
```yaml
- name: Install and start Apache
  package:
    name: apache2
    state: present
- name: Start service
  service:
    name: apache2
    state: started
```

**Puppet DSL:**
```puppet
package { 'apache2':
  ensure => installed,
}
service { 'apache2':
  ensure  => running,
  enable  => true,
  require => Package['apache2'],
}
```

### Millal kasutada mida

**Ansible paremaks sobib:**
- Väiksemad keskkonnad (< 500 serverit)
- DevOps meeskonnad (YAML tuttav)
- Kiire arendus ja deployment
- CI/CD pipeline automation
- Multi-cloud keskkonnad

**Puppet paremaks sobib:**
- Suuremad keskkonnad (1000+ serverit)
- Enterprise compliance nõuded
- Pidev configuration drift monitoring
- Traditional IT meeskonnad
- Regulatory compliance (SOX, HIPAA)

### Skaleeritavuse võrdlus

**Ansible limitatsioonid:**
```bash
# SSH ei skaleeeru hästi
ansible-playbook -f 50 site.yml  # max 50 paralleelset
```

**Puppet eelised:**
- 10,000+ serverit pole probleem
- Hajutatud arhitektuur
- Agents töötavad paralleelselt

### Infrastructure drift

**Ansible:**
1. Käivitate playbook → serverid õiges olekus
2. Keegi muudab käsitsi → drift toimub
3. Ansible ei tea sellest
4. Järgmine deployment parandab

**Puppet:**
1. Agent kontrollib iga 30 min
2. Avastab drift'i automaatselt
3. Parandab konfiguratsiooni
4. Raporteerib muudatused

---

## Praktiline soovitus

**Algajatele ja väiksematele projektidele:**
Alustage **Ansible'iga**:
- Lihtsam õppida (YAML)
- Kiirem setup (SSH piisab)
- Hea CI/CD integratsioon

**Enterprise keskkondades:**
Kaaluge **Puppet'i**:
- Parem skaleeritavus
- Pidev compliance
- Built-in auditing
- RBAC ja reporting

**Hybrid lähenemine:**
Paljud kasutavad mõlemat:
- Ansible initial provisioning'ks
- Puppet ongoing management'ks

---

## Kokkuvõte

**Roles lahendavad:**
- Korduvkasutatavus (sama role mitmes projektis)
- Modulaarsus (üks vastutus per role)
- Testitavus (komponendid eraldi)
- Hooldatavus (isoleeritud muudatused)

**Galaxy ökosüsteem:**
- 20,000+ valmis role'i
- Professional quality (geerlingguy)
- Versioonide juhtimine

**Puppet vs Ansible:**
- Ansible = kiire, lihtne, DevOps-friendly
- Puppet = enterprise, skaleeritav, compliance-focused

Järgmine samm: praktiline nginx role loomine!
