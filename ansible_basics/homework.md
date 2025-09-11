# 📝 Ansible Kodutöö: LAMP Stack

**Tähtaeg:** [Kuupäev]  
**Esitamine:** GitHub repo `ansible_lamp`  
**Eesmärk:** Automatiseerida LAMP stack'i paigaldus Ansible'iga

---

## Ülesande kirjeldus

Looge Ansible lahendus, mis paigaldab täieliku LAMP stack'i (Linux, Apache, MySQL, PHP) ühele või mitmele serverile. Lahendus peab olema taaskasutatav ja konfigureeritav.

---

## Nõuded

### 1. Infrastruktuur (10 punkti)
- Vähemalt 2 VM-i (controller + server)
- SSH võtmepõhine autentimine
- **⚠️ OLULINE: Lahendus PEAB olema konfigureeritav!**

**Teie lahendus peab töötama kui õpetaja testib:**
```bash
# Õpetaja muudab ainult neid faile:
# 1. inventory.ini - oma IP-d
# 2. group_vars/all/main.yml - oma kasutajanimi

# Ja käivitab:
ansible-playbook playbooks/site.yml
```

**Näide inventory.ini:**
```ini
[lamp_servers]
server1 ansible_host=MUUDETAV_IP ansible_user=MUUDETAV_KASUTAJA
```

**Näide group_vars/all/main.yml:**
```yaml
# Muudetavad muutujad
student_username: "jaan.tamm"  # Õpetaja muudab oma nimeks
server_ip: "192.168.1.100"     # Õpetaja muudab oma IP-ks
domain_name: "lamp.local"
```

**❌ VALE - hardcoded väärtused:**
```yaml
- name: "Create user"
  user:
    name: "jaan.tamm"  # ❌ VALE - peab olema muutuja
    
- name: "Copy file"  
  copy:
    dest: "/home/jaan.tamm/file"  # ❌ VALE - hardcoded path
```

**✅ ÕIGE - muutujatega:**
```yaml
- name: "Create user"
  user:
    name: "{{ student_username }}"  # ✅ ÕIGE
    
- name: "Copy file"
  copy:
    dest: "/home/{{ student_username }}/file"  # ✅ ÕIGE
```

### 2. Süsteemi ettevalmistus (15 punkti)
Looge playbook mis:
- Uuendab süsteemi pakette
- Paigaldab vajalikud tööriistad (teie valik)
- Seadistab firewall'i (avage vajalikud pordid)
- Seadistab ajavööndi

**Vihje:** Uurige `apt`, `ufw` ja `timezone` mooduleid

### 3. Apache veebiserver (20 punkti)
- Paigaldage Apache2
- Lubage vajalikud moodulid (rewrite, ssl, headers)
- Looge virtual host konfiguratsioon
- Kasutage template'd konfiguratsiooni jaoks
- Handler teenuse restardiks

**Uurige:**
- Kuidas luua Apache virtual host?
- Mis on `a2ensite` ja `a2enmod`?
- Millal kasutada `notify` ja `handlers`?

### 4. MySQL andmebaas (20 punkti)
- Paigaldage MySQL server
- Turvake root kasutaja
- Looge andmebaas
- Looge kasutaja õigustega
- Paroolid ei tohi olla nähtavad koodis

**Nõuded:**
- Kasutage `vars_prompt` või Ansible Vault
- Python MySQL moodul peab olema installitud
- Andmebaasi nimi ja kasutaja peavad olema muutujad

### 5. PHP (15 punkti)
- Paigaldage PHP ja vajalikud laiendused
- Integreerige Apache'ga
- Looge PHP test leht mis:
  - Näitab serveri infot
  - Testib MySQL ühendust
  - Kuvab PHP versiooni

**Template peab sisaldama:**
- Dünaamilist sisu Ansible muutujatest
- Andmebaasi ühenduse testi

### 6. Organiseerimine (10 punkti)

**⚠️ OLULINE: Failid PEAVAD olema organiseeritud!**

```
ansible_lamp/
├── inventory.ini
├── ansible.cfg
├── playbooks/
│   ├── apache.yml       # AINULT apache taskid
│   ├── mysql.yml        # AINULT mysql taskid
│   └── site.yml         # Import playbook
├── templates/
│   ├── vhost.conf.j2
│   └── index.php.j2
├── group_vars/
│   ├── all/
│   │   └── main.yml     # Globaalsed muutujad
│   └── lamp_servers/
│       └── main.yml     # Grupi muutujad
├── host_vars/           # Kui vaja
├── handlers/            # VÕI handlers eraldi
│   └── main.yml
└── tasks/               # Taaskasutatavad taskid
    └── packages.yml
```

**❌ MITTE LUBATUD:**
- Kõik muutujad playbook'is (`vars:` sektsioonis)
- Kõik ühes suures playbook failis
- Handlers playbooki sees (lubatud ainult väikestes)

**✅ NÕUTUD:**
- Muutujad `group_vars/` või `host_vars/` kaustades
- Iga teenus eraldi playbook'is
- Templates `templates/` kaustas
- Master playbook kasutab `import_playbook`

**Näide VALE struktuuri kohta:**
```yaml
# ❌ HALB - kõik ühes failis
- name: "Everything in one file"
  hosts: servers
  vars:              # ❌ Muutujad peaks olema group_vars
    mysql_pass: xyz
  tasks:
    - name: "Install Apache"
    - name: "Install MySQL"  # ❌ Erinevad teenused segamini
  handlers:          # ❌ Handlers võiks olla eraldi
    - name: restart
```

**Näide ÕIGE struktuuri kohta:**
```yaml
# ✅ HEA - apache.yml
- name: "Apache setup"
  hosts: lamp_servers
  tasks:
    - name: "Install Apache"
      # ...
    
# ✅ HEA - mysql.yml  
- name: "MySQL setup"
  hosts: lamp_servers
  tasks:
    - name: "Install MySQL"
      # ...

# ✅ HEA - site.yml
- import_playbook: apache.yml
- import_playbook: mysql.yml
```

### 7. Idempotentsus ja testimine (10 punkti)
- Playbook peab olema idempotentne
- Lisage kontrollid:
  - Apache töötab?
  - MySQL vastab?
  - PHP toimib?
  - Veebileht on kättesaadav?

**Vihje:** `uri` moodul, `wait_for`, `stat`

---

## Lisaülesanded (valikulised)

### SSL sertifikaat (+10 punkti)
- Self-signed või Let's Encrypt
- HTTPS redirect

### WordPress (+15 punkti)  
- Automaatne paigaldus
- Andmebaasi seadistus
- wp-config.php genereerimine

### Backup lahendus (+10 punkti)
- Automaatne MySQL backup
- Veebifailide backup
- Cron job

### Monitoring (+5 punkti)
- Lihtsad kontrollid
- Email teavitused

---

## Nõuanded

**📝 TÄHTIS ERINEVUS:**
- **Laboris:** Näitasime kõik ühes failis (algajatele lihtsam)
- **Kodutöös:** PEATE organiseerima õigesti!

Labor oli õppimiseks - seal oli OK kõik ühes:
```yaml
# Laboris oli lubatud (õppimise jaoks)
- hosts: servers
  vars:
    my_var: value
  tasks:
    - name: task1
  handlers:
    - name: handler1
```

Kodutöös peab olema professionaalne struktuur!

**Kust alustada:**
1. Tehke lihtne ping test
2. Installige Apache käsitsi, siis automatiseerige
3. Kasutage `ansible-doc <module>` abi saamiseks

**Kasulikud moodulid:**
- `apt` / `yum` - pakettide haldus
- `service` / `systemd` - teenuste haldus
- `template` - konfiguratsioonifailid
- `mysql_db` / `mysql_user` - MySQL
- `ufw` / `firewalld` - tulemüür
- `uri` - veebilehe test

**Dokumentatsioon:**
- https://docs.ansible.com/ansible/latest/modules/
- Iga mooduli lehel on näited

---

## Mida EI tohiks teha

❌ Paroolid otse koodis  
❌ Kõik ühes suures playbook'is  
❌ SSH parooliga autentimine  
❌ Root kasutaja kasutamine  
❌ Muutujad otse playbook'is  

---

## Hindamine

**Funktsionaalsus (60%):**
- Apache töötab ja serveerib lehte
- MySQL töötab ja on ligipääsetav
- PHP töötab ja ühendub andmebaasiga

**Koodikvaliteet (25%):**
- Organiseerimine
- Muutujate kasutamine
- Idempotentsus
- Error handling

**Dokumentatsioon (15%):**
- README.md
- Kommentaarid koodis
- Screenshot tulemusest

---

## Esitamine

### README.md peab sisaldama:
```markdown
# LAMP Stack Ansible

## Autor
[Nimi]

## Kirjeldus
[Mida lahendus teeb]

## Eeldused
- [VM nõuded]
- [Tarkvara versioonid]

## Kasutamine
[Kuidas käivitada]

## Struktuur
[Failide kirjeldus]

## Testimine
[Kuidas testida]

## Screenshot
[Töötava rakenduse pilt]

## Probleemid
[Mis oli keeruline]

## Allikad
[Kasutatud materjalid]
```

### Kontroll-nimekiri:
- [ ] Inventory fail VM IP-dega
- [ ] Vähemalt 3 playbook'i
- [ ] Template'd kasutatud
- [ ] Muutujad group_vars kaustas
- [ ] Apache virtual host töötab
- [ ] MySQL andmebaas ja kasutaja loodud
- [ ] PHP test leht nähtav
- [ ] README täidetud
- [ ] Screenshot lisatud
- [ ] GitHub repo avalik

---

## Vihjed

**Alusta lihtsalt:**
```yaml
- name: "Test playbook"
  hosts: lamp_servers
  tasks:
    - name: "Ping test"
      ping:
```

**Debugimine:**
```bash
ansible-playbook playbook.yml -vvv
ansible-playbook playbook.yml --check
```

**MySQL parool:**
```yaml
vars_prompt:
  - name: mysql_root_pass
    prompt: "Enter MySQL root password"
    private: yes
```

---

## Tähtis

- Tehke GitHubi commit'e tihti
- Alustage lihtsast, lisage keerukust
- Testige iga sammu
- Küsige abi kui jääte kinni
- Google ja StackOverflow on lubatud!
