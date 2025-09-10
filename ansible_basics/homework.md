# 📝 Kodutöö: LAMP Stack Playbook

**Tähtaeg:** Järgmise nädala algus  
**Aeg:** 2-3h  
**Eesmärk:** Iseseisev Ansible LAMP stack loomine

---

## 🎯 Ülevaade

Ehitad LAMP stacki Ansible'iga. Kood kirjutad ise - saad ülesanded ja kontrollviisid.

---

## 📋 Setup

### Projekti struktuur
```
ansible-lamp/
├── inventory/hosts.yml
├── group_vars/webservers.yml  
├── templates/
├── lamp-stack.yml
├── ansible.cfg
└── README.md
```

**Kontroll:** `tree ansible-lamp`

---

## 🔧 Probleem 1: Inventory

### 1.1 Hosts fail
**Fail:** `inventory/hosts.yml`

**Nõuded:**
- YAML formaat
- Grupp: `webservers`
- Localhost: `ansible_connection: local`
- Kommentaaris: teise serveri näide

**Test:** `ansible webservers -m ping`

### 1.2 Muutujad
**Fail:** `group_vars/webservers.yml`

**Defineeri:**
- MySQL root parool
- DB nimi, kasutaja, parool
- PHP pakettide list
- Document root
- App nimi/versioon

**Test:** `ansible webservers -m debug -a "var=hostvars[inventory_hostname]"`

---

## 🐛 Probleem 2: Vigane playbook

**Paranda need vead:**

```yaml
---
- name: LAMP Stack Setup
  hosts: all                    # VIGA: vale grupp
  become: true
  
  tasks:
    - name: Update cache
      package:
        update_cache: true      # VIGA: vale moodul
        
    - name: Install Apache
      apt:
        name: apache            # VIGA: vale nimi
        state: present
      notify: restart apache
      
    - name: Start Apache
      systemd:                  # VIGA: miks mitte service?
        name: apache2
        state: started
        
  handlers:                     # VIGA: vale asukoht?
    - name: restart apache
      service:
        name: apache2
        state: restarted
```

**Test:** `ansible-playbook --syntax-check lamp-stack.yml`

---

## 🗄️ Probleem 3: MySQL

**Ülesanded:**
1. Installi `mysql-server` + `python3-pymysql`
2. Käivita teenus
3. Seadista root parool
4. Loo app DB ja kasutaja

**Moodulid:** `apt`, `service`, `mysql_user`, `mysql_db`

**Keeruline osa:** Root parooli seadistamine - kasuta `login_unix_socket`

**Test:** `mysql -u [user] -p [db] -e "SELECT 'OK';"`

---

## 📄 Probleem 4: Template'id

### 4.1 PHP info leht
**Fail:** `templates/info.php.j2`

**Lõpeta see:**
```php
<?php
echo "<h1>{{ ??? }}</h1>";  // app_name
echo "<h2>Server: {{ ??? }}</h2>";  // hostname
$database = '{{ ??? }}';  // db_name
// Lisa PDO test + phpinfo()
?>
```

### 4.2 HTML põhileht  
**Fail:** `templates/index.html.j2`

**Nõuded:**
- Serveri info (hostname, OS, kuupäev)
- Link info.php'le
- CSS styling
- Kõik Ansible muutujatest

---

## ⚙️ Probleem 5: Playbook tasks

**Vajalikud sammud:**
1. Cache update
2. Apache install + config
3. MySQL setup
4. PHP install
5. Template deploy
6. Firewall (ufw)
7. Validation

**Moodulid:** `apt`, `service`, `file`, `template`, `ufw`, `uri`

**Handlers:** Apache/MySQL restart

---

## 🧪 Probleem 6: Testimine

**Testiplaan:**
1. `--syntax-check`
2. `--check` (dry run)
3. Tegelik käivitamine
4. HTTP test
5. Idempotency test

**Levinud vead:**
- `No package matching 'php'` → Vale paketi nimi
- `unable to connect to database` → MySQL config
- `template not found` → Vale tee

---

## 📚 Probleem 7: Dokumentatsioon

**README.md sektsioonid:**
- Projekti kirjeldus
- Eeltingimused
- Käivitamise juhend
- Konfiguratsioon
- Testimine
- Troubleshooting

**Koodikommentaarid:**
- Selged task nimed
- Keeruliste osade selgitused
- Muutujate dokumenteerimine

---

## 📤 Esitamine

**GitHub repo nõuded:**
- Public repo
- Funktsionaalne kood
- Täielik README
- Screenshots/logid

**Peab toimima:**
- Clone → setup → run → validate

---

## 🚀 Nipid

**Strateegia:**
1. Alusta Apachega
2. Testi iga sammu
3. MySQL viimasena
4. Kasuta `ansible-doc`

**Debug:**
- `--syntax-check`
- `-vvv` verbose
- `journalctl -u service`
- Käsitsi testimine

**Ajakulu:**
- Päev 1: Setup + Apache
- Päev 2: MySQL + PHP  
- Päev 3: Template'id + test
- Päev 4: Dokumentatsioon

Hooa sisse! 🎉
