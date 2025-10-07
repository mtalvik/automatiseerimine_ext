# Ansible Kodutöö: Veebirakendus Vault'iga

Looge Ansible lahendus, mis juurutab veebirakenduse kasutades Vault'i, template'eid ja handler'eid. Lahendus peab toetama kahte keskkonda (dev/prod) erinevate konfiguratsioonidega. See ülesanne võtab orienteeruvalt 4-6 tundi.

**Eeldused:** Ansible põhiteadmised, YAML süntaks, Jinja2 template'id, Linux süsteemihaldus  
**Esitamine:** GitHub avalik repositoorium koos README.md failiga  
**Tähtaeg:** Järgmise nädala alguseks

## OLULINE: Pilve Serverite Kasutamisel

Seda kodutööd saab teha kohalike VM'idega (VirtualBox/Vagrant) - see on TASUTA.

Kui kasutate pilve (AWS EC2, Azure VM, DigitalOcean):

1. Seadistage billing alerts
2. Kasutage väiksemaid instance'eid:
   - AWS: `t2.micro` või `t3.micro` (Free Tier)
   - Azure: `B1s`
   - DigitalOcean: $6/month droplet
3. KUSTUTAGE serverid pärast testimist```bash
# AWS
aws ec2 terminate-instances --instance-ids i-xxxxx

# Azure
az vm delete --name myvm --resource-group mygroup --yes

# Terraform
terraform destroy```

Kohalike VM'ide kasutamine:```bash
vagrant up
ansible-playbook -i inventory site.yml
vagrant destroy  # pärast testimist```

---

## 1. Ülesande Kirjeldus

Juurutage veebirakendus (teie valik) kasutades:
- Ansible Vault paroolide jaoks
- Template'e konfiguratsioonifailidele
- Handler'eid teenuste haldamiseks
- Kahte keskkonda (dev/prod)

Valige keerukus:

**Variant 1: Static website**
- Apache + HTML
- Template: Apache vhost
- Vault: Apache admin parool, SSL parool
- Dev: port 8080, prod: port 80

**Variant 2: Blog platform**
- Apache/Nginx + MySQL + PHP (WordPress või custom)
- Template'id: vhost, DB config, PHP config
- Vault: DB paroolid, admin parool
- Dev: vähem RAM ja debug logging, prod: optimeeritud

**Variant 3: API server**
- Nginx + PostgreSQL + Node.js/Go/Rust
- Redis cache, load balancing
- Template'id: Nginx upstream, DB tuning, API config
- Vault: DB paroolid, API tokens, Redis parool, SSL certs

---

## 2. Vault Nõuded (15%)

Looge Ansible Vault fail vähemalt 5 krüpteeritud muutujaga:```bash
# Loo vault fail
ansible-vault create group_vars/all/vault.yml

# Vaata sisu
ansible-vault view group_vars/all/vault.yml

# Käivita playbook
ansible-playbook site.yml --ask-vault-pass```

Vault failis:```yaml
vault_db_password: "tugevParool123"
vault_admin_user: "administrator"
vault_admin_password: "veel_tugevam"
vault_api_key: "secret_key_1234"
vault_ssl_cert_password: "cert_pass"```

Kasutamine template'ides:```jinja2
database_password: {{ vault_db_password }}
admin_user: {{ vault_admin_user }}```

Nõuded:
- [ ] Vähemalt 5 krüpteeritud muutujat
- [ ] Kõik paroolid vault'is (mitte plain text)
- [ ] Vault muutujad kasutatavad template'ides

---

## 3. Template'ide Nõuded (20%)

Looge vähemalt 2 Jinja2 template'i, mis kasutavad `{% if %}` tingimusi.

Apache vhost template (vhost.conf.j2):```jinja2
<VirtualHost *:{{ http_port }}>
    ServerName {{ server_name }}
    DocumentRoot {{ document_root }}

    {% if env_type == 'production' %}
    ErrorLog ${APACHE_LOG_DIR}/{{ app_name }}_error.log
    LogLevel warn
    {% else %}
    ErrorLog ${APACHE_LOG_DIR}/{{ app_name }}_dev_error.log
    LogLevel debug
    {% endif %}

    <Directory {{ document_root }}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>```

DB konfiguratsioon (my.cnf.j2):```jinja2
[client]
user = {{ vault_db_user }}
password = {{ vault_db_password }}
host = {{ db_host }}

[mysqld]
{% if env_type == 'production' %}
max_connections = 200
innodb_buffer_pool_size = 1G
{% else %}
max_connections = 50
innodb_buffer_pool_size = 256M
{% endif %}```

Nõuded:
- [ ] Vähemalt 2 template'i
- [ ] Kasutavad `{% if %}` tingimusi
- [ ] Erinevad konfiguratsioonid dev/prod jaoks

---

## 4. Handler'ite Nõuded (15%)

Looge vähemalt 2 handler'it teenuste haldamiseks.```yaml
tasks:
  - name: Deploy Apache vhost
    template:
      src: templates/vhost.conf.j2
      dest: /etc/apache2/sites-available/{{ app_name }}.conf
    notify: restart apache

  - name: Deploy DB config
    template:
      src: templates/my.cnf.j2
      dest: /etc/mysql/my.cnf
    notify: reload mysql

handlers:
  - name: restart apache
    service:
      name: apache2
      state: restarted

  - name: reload mysql
    service:
      name: mysql
      state: reloaded```

Nõuded:
- [ ] Vähemalt 2 handler'it
- [ ] Teenused restarditakse ainult muudatuste korral
- [ ] Handler'id `handlers:` sektsioonis, mitte `tasks:` sees

---

## 5. Projekti Struktuur (15%)```
teie-projekt/
├── inventory/
│   └── hosts.yml
├── group_vars/
│   ├── all/
│   │   ├── vars.yml
│   │   └── vault.yml
│   ├── dev/
│   │   └── vars.yml
│   └── production/
│       └── vars.yml
├── templates/
│   ├── vhost.conf.j2
│   └── my.cnf.j2
├── playbooks/
│   ├── site.yml
│   └── deploy.yml
├── screenshots/
│   ├── vault_encrypted.png
│   ├── playbook_success.png
│   └── app_running.png
└── README.md```

Inventory näide (hosts.yml):```yaml
all:
  children:
    dev:
      hosts:
        dev-server:
          ansible_host: 192.168.56.10
          ansible_user: vagrant
          env_type: development
    
    production:
      hosts:
        prod-server:
          ansible_host: 192.168.56.20
          ansible_user: ubuntu
          env_type: production```

Nõuded:
- [ ] Failid õigesti organiseeritud
- [ ] Vault fail group_vars/all/ kaustas
- [ ] Template'id templates/ kaustas
- [ ] Erinevad muutujad dev/prod jaoks

---

## 6. Esitamine

README.md peab sisaldama:```markdown
# [Projekti Nimi]

## Autor
[Teie nimi ja õpperühm]

## Kirjeldus
[Mis rakendus, mis komponendid]

## Eeldused
- Ubuntu 20.04/22.04
- Ansible 2.9+
- SSH juurdepääs

## Failide struktuur
[Kirjelda kataloogide sisu]

## Seadistamine

1. Kloonige repo
2. Muutke inventory/hosts.yml
3. Muutke group_vars/all/vars.yml
4. Käivitage: `ansible-playbook playbooks/site.yml --ask-vault-pass`

## Kasutamine

### Esimene käivitus```bash
ansible-playbook playbooks/site.yml --ask-vault-pass```

### Dev keskkond```bash
ansible-playbook -i inventory/hosts.yml playbooks/site.yml -l dev```

### Production keskkond```bash
ansible-playbook -i inventory/hosts.yml playbooks/site.yml -l production```

## Testimine
[Kuidas kontrollida, et töötab]

## Screenshot
[Lisa screenshot]

## Probleemid ja lahendused
[Mis raskused, kuidas lahendasid]```

### Kontroll Enne Esitamist

- [ ] GitHubis avalik repo
- [ ] Ansible project structure korrektne
- [ ] Template'id töötavad (dünaamilised configs)
- [ ] Vault kasutatud (paroolid krüpteeritud)
- [ ] Playbook töötab ilma vigadeta
- [ ] Rakendus funktsionaalne (testitud)
- [ ] README.md sisaldab:
  - [ ] Projekti kirjeldus
  - [ ] Arhitektuur
  - [ ] Seadistamisjuhend
  - [ ] Käivitamisjuhend
  - [ ] Screenshots
  - [ ] Refleksioon (5 küsimust)
- [ ] Kõik muudatused push'itud

Valideerimine:```bash
# Vault krüpteeritud?
file group_vars/all/vault.yml

# Syntax OK?
ansible-playbook site.yml --syntax-check

# Dry run?
ansible-playbook site.yml --check --ask-vault-pass

# Screenshots olemas?
ls screenshots/```

---

## 7. Refleksioon

Lisa README.md lõppu peatükk "Refleksioon" ja vasta (2-3 lauset igaühele):

### 1. Mis oli kõige raskem ja kuidas lahendasid?

Kirjelda konkreetset tehnilist probleemi ja lahendust.

### 2. Milline Ansible advanced kontseptsioon oli suurim "ahaa!" hetk?

Kirjelda, mis avas uue mõtteviisi või oli üllatav.

### 3. Kuidas saaksid Ansible'i advanced funktsioone kasutada teistes projektides?

Kirjelda konkreetseid kasutusjuhte.

### 4. Kui peaksid selgitama sõbrale, mis on Infrastructure as Code, siis mida ütleksid?

Lihtne selgitus mitteinfotehnoloogile.

### 5. Mis oli kursusel kõige väärtuslikum õppetund?

Mõtle laiemalt kui ainult tehnilised oskused.

---

## 8. Hindamiskriteeriumid

| Kriteerium | Osakaal | Kirjeldus |
|------------|---------|-----------|
| Funktsionaalsus | 30% | Rakendus töötab, kõik komponendid korrektselt seadistatud |
| Template'id | 20% | Jinja2 template'id dünaamilised, kasutavad `{% if %}`, genereerivad korrektseid config'e |
| Vault | 15% | Kõik paroolid krüpteeritud, vault õigesti integreeritud |
| Projekti struktuur | 15% | Organiseeritud kataloogstruktuur, järgib Ansible best practices |
| README | 10% | Projekti kirjeldus, käivitamisjuhised, arhitektuur, screenshots |
| Refleksioon | 10% | 5 küsimust vastatud, sisukad vastused |

**Kokku: 100%**

---

## 9. Sagedased Vead

**Vault parool Git'is:** `.vault_pass` peab olema `.gitignore` failis.

**Hardcoded paroolid:** Kui template'is on `password: admin123`, siis vault nõue pole täidetud.

**Handler'id valesti:** Handler peab olema `handlers:` sektsioonis ja käivituma `notify:` kaudu.

**Ainult üks keskkond:** Peab olema dev JA production erinevate seadistustega.

---

## 10. Abimaterjalid

**Ansible dokumentatsioon:**
- [Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
- [Jinja2 Templates](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html)
- [Handlers](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html)
- [Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)

**Jinja2:**
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

**Kui abi vaja:**
1. Vaata `lisapraktika.md` täiendavaid näiteid
2. Kasuta `ansible-playbook --syntax-check`
3. Kasuta `ansible-playbook --check` kuivaks käiguks
4. Küsi klassikaaslaselt või õpetajalt

---

## 11. Boonus (valikuline, +10%)

Valikulised täiendused lisapunktide saamiseks:

### Dynamic inventory (+3%)

Kasuta dynamic inventory AWS EC2 või Azure VM'idega:```yaml
# aws_ec2.yml
plugin: aws_ec2
regions:
  - eu-north-1
filters:
  tag:Environment:
    - dev
    - production```

### Ansible Tower/AWX (+3%)

Deploy projekti Tower/AWX'i ja loo job template.

### Molecule testing (+2%)

Lisa Molecule test suite:```bash
molecule init scenario
molecule test```

### Multiple environments (+2%)

Kolm keskkonda: Dev, Staging, Production (erinevad vault failid igaühele).```
group_vars/
  dev/vault.yml
  staging/vault.yml
  production/vault.yml```

### CI/CD integration (+2%)

Lisa GitLab CI või GitHub Actions pipeline:```yaml
# .gitlab-ci.yml
deploy:
  script:
    - ansible-playbook playbooks/site.yml --ask-vault-pass```

---

## 12. Debugimine

Verbose režiim:```bash
ansible-playbook site.yml -vvv```

Kuiv käivitus:```bash
ansible-playbook site.yml --check```

Vaata diff'i:```bash
ansible-playbook site.yml --diff```

---

## Mida MITTE teha

- Paroolid plain text'is
- `.vault_pass` Git'is
- Kõik ühes playbook'is
- Muutujad otse playbook'is `vars:` sektsioonis
- Handler'id `tasks:` sektsioonis
- Hardcoded IP aadressid või kasutajanimed

---

**Edu!**