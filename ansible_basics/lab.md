# 🧪 Ansible Basics Lab: Setup ja Esimene Playbook

**Kestus:** 2h  
**Eesmärk:** Ansible alused ja esimesed automatiseerimise skriptid

---

## 🎯 Õpiväljundid

Pärast laborit oskate:
- Installida ja konfigureerida Ansible
- Seadistada SSH võtmeid
- Luua inventory faile
- Kasutada ad-hoc käske
- Kirjutada YAML süntaksit
- Luua ja käivitada playbook'e
- Seadistada veebiserveri

---

## 📋 Samm 1: Ansible installimine (30 min)

### 1.1: Installimine

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ansible -y
ansible --version
```

**macOS:**
```bash
brew install ansible
ansible --version
```

### 1.2: SSH seadistamine

**SSH võtme loomine:**
```bash
ssh-keygen -t rsa -b 4096 -C "teie.email@example.com"
# Vajutage Enter kõikidele küsimustele
```

**Võtme kopeerimine:**
```bash
ssh-copy-id kasutaja@test-server.local
# Test: ssh kasutaja@test-server.local
```

### 1.3: Inventory loomine

**Töökaust:**
```bash
mkdir ~/ansible-praktikum
cd ~/ansible-praktikum
```

**Inventory fail (`inventory.ini`):**
```ini
[test]
localhost ansible_connection=local

[practice]
# server1.example.com ansible_user=ubuntu
```

**Test:**
```bash
ansible -i inventory.ini test -m ping
```

---

## 📋 Samm 2: Ad-hoc käsud (20 min)

```bash
# Ping test
ansible -i inventory.ini all -m ping

# Süsteemi info
ansible -i inventory.ini all -m setup -a "filter=ansible_distribution*"

# Failide haldamine
ansible -i inventory.ini all -m file -a "path=/tmp/ansible-test state=directory"
ansible -i inventory.ini all -m copy -a "content='Test' dest=/tmp/ansible-test/hello.txt"

# Pakettide haldamine
ansible -i inventory.ini all -m package -a "name=htop state=present" --become
```

---

## 📋 Samm 3: YAML ja playbook (40 min)

### YAML harjutus

**Test fail (`test.yml`):**
```yaml
---
nimi: "Ansible Test"
versioon: 1.0
serverid:
  - nimi: "test1"
    ip: "192.168.1.10"
    roll: "veebiserver"
seadistused:
  http_port: 80
  debug: true
```

### Esimene playbook

**Fail (`minu-esimene-playbook.yml`):**
```yaml
---
- name: "Esimene Ansible playbook"
  hosts: all
  gather_facts: yes
  
  tasks:
    - name: "Tervita maailma"
      debug:
        msg: "Tere! Ansible töötab {{ inventory_hostname }} serveris!"
    
    - name: "Näita süsteemi infot"
      debug:
        msg: "Server töötab {{ ansible_distribution }} {{ ansible_distribution_version }}"
    
    - name: "Loo test kataloog"
      file:
        path: /tmp/ansible-praktikum
        state: directory
        mode: '0755'
    
    - name: "Kirjuta info fail"
      copy:
        dest: /tmp/ansible-praktikum/info.txt
        mode: '0644'
        content: |
          Playbook käivitatud: {{ ansible_date_time.iso8601 }}
          Server: {{ inventory_hostname }}
          IP: {{ ansible_default_ipv4.address | default('ei tuvastatud') }}
```

**Käivitamine:**
```bash
ansible-playbook -i inventory.ini --check minu-esimene-playbook.yml
ansible-playbook -i inventory.ini minu-esimene-playbook.yml
```

### Muutujatega playbook

**Fail (`playbook-muutujatega.yml`):**
```yaml
---
- name: "Playbook muutujatega"
  hosts: all
  vars:
    rakenduse_nimi: "Minu Veebirakendus"
    versioon: "1.2.3"
    portnumber: 8080
    
  tasks:
    - name: "Loo rakenduse kaust"
      file:
        path: "/opt/{{ rakenduse_nimi | lower | replace(' ', '-') }}"
        state: directory
        mode: '0755'
      become: yes
    
    - name: "Kirjuta konfiguratsioon"
      copy:
        dest: "/opt/{{ rakenduse_nimi | lower | replace(' ', '-') }}/config.env"
        mode: '0644'
        content: |
          APP_NAME={{ rakenduse_nimi }}
          VERSION={{ versioon }}
          PORT={{ portnumber }}
          INSTALLED_ON={{ ansible_date_time.iso8601 }}
      become: yes
```

---

## 📋 Samm 4: Nginx seadistamine (30 min)

**Fail (`nginx-setup.yml`):**
```yaml
---
- name: "Nginx veebiserveri seadistamine"
  hosts: all
  become: yes
  vars:
    web_root: "/var/www/html"
    site_name: "Minu Test Sait"
    
  tasks:
    - name: "Uuenda pakettide nimekirja"
      package:
        update_cache: yes
      when: ansible_os_family == "Debian"
    
    - name: "Installi Nginx"
      package:
        name: nginx
        state: present
    
    - name: "Loo veebi kaust"
      file:
        path: "{{ web_root }}"
        state: directory
        owner: www-data
        group: www-data
        mode: '0755'
      when: ansible_os_family == "Debian"
    
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
                  <h1 class="success">{{ site_name }}</h1>
                  <p>Nginx edukalt paigaldatud Ansible'iga!</p>
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
    
    - name: "Käivita Nginx"
      service:
        name: nginx
        state: started
        enabled: yes
    
    - name: "Kontrolli Nginx olekut"
      command: systemctl is-active nginx
      register: nginx_status
      failed_when: false
    
    - name: "Testi veebiserveri ühendust"
      uri:
        url: "http://localhost"
        return_content: yes
      register: web_test
      failed_when: false
    
    - name: "Näita tulemust"
      debug:
        msg: "Nginx: {{ nginx_status.stdout }}, HTTP: {{ web_test.status | default('Viga') }}"
```

**Testimine:**
```bash
ansible-playbook --syntax-check nginx-setup.yml
ansible-playbook --check nginx-setup.yml
ansible-playbook nginx-setup.yml
curl http://localhost
```

---

## 📋 Samm 5: Konfiguratsiooni optimeerimine (20 min)

**Fail (`ansible.cfg`):**
```ini
[defaults]
inventory = inventory.ini
host_key_checking = False
stdout_callback = yaml
pipelining = True
forks = 10
log_path = ./ansible.log

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
timeout = 30
retries = 3
```

**Test:**
```bash
ansible all -m ping  # Enam ei vaja -i lippu
```

---

## 📋 Samm 6: Veatuvastus (20 min)

**Debug playbook (`debug-playbook.yml`):**
```yaml
---
- name: "Debug ja veatuvastus"
  hosts: all
  gather_facts: yes
  
  tasks:
    - name: "Näita OS infot"
      debug:
        msg: "OS: {{ ansible_distribution }} {{ ansible_distribution_version }}"
    
    - name: "Kontrolli kasutajat"
      command: whoami
      register: current_user
    
    - name: "Kontrolli sudo"
      command: whoami
      become: yes
      register: sudo_user
      failed_when: false
    
    - name: "Näita tulemust"
      debug:
        msg: "SSH: {{ current_user.stdout }}, Sudo: {{ sudo_user.stdout | default('Ei toimi') }}"
```

**Levinud probleemid:**
```bash
# SSH debug
ssh -v kasutaja@target-host

# Python kontroll
ansible all -m setup -a "filter=ansible_python*"

# Sudo test
ansible all -m command -a "whoami" --become --ask-become-pass
```

---

## 🎯 Kontrollige saavutusi

- [ ] Ansible installimine toimib
- [ ] SSH ühendus töötab
- [ ] Inventory funktsionaalne
- [ ] Ad-hoc käsud töötavad
- [ ] YAML süntaks selge
- [ ] Playbook käivitub
- [ ] Muutujad töötavad
- [ ] Nginx käigus
- [ ] Konfiguratsioon optimeeritud

**Järgmine samm:** LAMP stack kodutöö
