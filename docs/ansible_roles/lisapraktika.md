# Ansible Rollid Lisapraktika

Need harjutused on mõeldud kogenud õppijatele, kes soovivad süvendada Ansible rollide oskusi produktsioonitaseme tehnikatega. Iga harjutus võtab 30-45 minutit ja õpetab praktilist tehnikat, mida DevOps insenerid igapäevaselt kasutavad.

**Eeldused:** Ansible rollide labor ja kodutöö läbitud, Galaxy standardiga tuttavus, variables ja templates valdamine

---

## 1. Multi-OS Rollide Implementatsioon

### 1.1 Probleem

Laboris loodud nginx roll töötab ainult Ubuntu/Debian süsteemides. Ettevõtetes on infrastruktuur heterogeenne - osa servereid on Ubuntu, osa CentOS, mõned võivad olla Amazon Linux. Iga OS jaoks eraldi rolli loomine tooks duplikatsiooni ja hoolduskoormust.

OS'ide erinevused pole triviasalsed. Paketihaldur on erinev (apt vs yum vs dnf). Paketinimed erinevad (nginx vs httpd). Konfiguratsioonifailide asukohad erinevad (/etc/nginx/sites-available vs /etc/nginx/conf.d). Service'i nimed võivad erineda. Iga erisus nõuab eraldi käsitlemist.

### 1.2 Lahendus

Lahendus kasutab Ansible facts'e OS tuvastamiseks ja conditional logic'ut õige konfiguratsiooni valimiseks. Facts nagu `ansible_os_family`, `ansible_distribution` ja `ansible_distribution_major_version` võimaldavad rolli käitumist dünaamiliselt kohandada.

Loome OS-spetsiifilised variables failid vars kaustas. Include_vars direktiiv laadib õige faili runtime'il. Tasks kasutavad when conditionals OS-spetsiifiliste operatsioonide jaoks.

```yaml
# vars/Debian.yml
---
nginx_package_name: "nginx"
nginx_service_name: "nginx"
nginx_config_path: "/etc/nginx"
nginx_sites_available: "{{ nginx_config_path }}/sites-available"
nginx_sites_enabled: "{{ nginx_config_path }}/sites-enabled"
nginx_user: "www-data"

# vars/RedHat.yml
---
nginx_package_name: "nginx"
nginx_service_name: "nginx"
nginx_config_path: "/etc/nginx"
nginx_conf_d: "{{ nginx_config_path }}/conf.d"
nginx_user: "nginx"
```

Tasks failis laadime õiged variables:

```yaml
# tasks/main.yml
---
- name: "Load OS-specific variables"
  include_vars: "{{ ansible_os_family }}.yml"

- name: "Install nginx (Debian-based)"
  apt:
    name: "{{ nginx_package_name }}"
    state: present
    update_cache: yes
  when: ansible_os_family == "Debian"

- name: "Install nginx (RedHat-based)"
  yum:
    name: "{{ nginx_package_name }}"
    state: present
  when: ansible_os_family == "RedHat"

- name: "Deploy config (Debian style)"
  include_tasks: debian_config.yml
  when: ansible_os_family == "Debian"

- name: "Deploy config (RedHat style)"
  include_tasks: redhat_config.yml
  when: ansible_os_family == "RedHat"
```

OS-agnostic alternatiiv on package moodul, mis automaatselt valib õige package manager'i:

```yaml
- name: "Install nginx (OS-agnostic)"
  package:
    name: "{{ nginx_package_name }}"
    state: present
```

### 1.3 Harjutus: Universal Nginx Role

Kohandage oma laboris loodud nginx rolli töötama nii Ubuntu kui CentOS süsteemides.

**Nõuded:**

- [ ] Role töötab Ubuntu 20.04 ja CentOS 8 VM'ides
- [ ] OS-spetsiifilised variables on eraldatud vars/ kausta
- [ ] Package paigaldamine kasutab package moodulit
- [ ] Config deployment kohandub OS struktuurile (sites-available vs conf.d)
- [ ] Service management töötab mõlemas OS'is
- [ ] Molecule test suite testib mõlemat OS'i

**Näpunäiteid:**

- Kasutage `ansible_os_family` fakti, mitte `ansible_distribution` - see on üldisem
- RedHat süsteemides pole sites-available/sites-enabled struktuuri - kasuta conf.d
- SELinux võib CentOS'is blokeerida nginx'i - lisa tasks SELinux konteksti seadistamiseks
- Molecule võimaldab testida mitut platvormi Docker container'ites

**Testimine:**

```bash
# Ubuntu VM
ansible-playbook -i ubuntu_host, site.yml

# CentOS VM
ansible-playbook -i centos_host, site.yml

# Molecule multi-platform test
molecule test
```

**Boonus:**

Lisa support Arch Linux'ile (pacman package manager). Kasuta block/rescue error handling'ut graceful failure'ks tundmatus OS'is.

---

## 2. Dynamic Environments ja Configuration Layering

### 2.1 Probleem

Produktsiooni infrastruktuuris on mitu environment'i: development, staging, production. Iga environment vajab erinevat konfiguratsiooni. Development vajab debug logging'u ja madalamat performance optimeerimist. Staging on production'ile sarnane, aga väiksema scale'iga. Production vajab maksimaalset performance'i, minimaalset logging'u, tugevat turvalisust.

Halvim lähenemine on luua kolm erinevat rolli või kolm koopiat samast konfiguratsioonist. See toob duplikatsiooni - bug fix peab rakendama kolmes kohas. Parem on üks roll, mis kohandub environment'ile.

### 2.2 Lahendus

Lahendus on variables layering - mitmetasandiline muutujate süsteem, kus üldised defaults kirjutatakse üle environment-specific variables'iga. Ansible variables precedence order võimaldab seda loomulikult.

Defaults määravad base configuration. Group_vars kirjeldavad environment'i. Extra_vars lubavad runtime override'e. Iga kiht lisab või kirjutab üle eelmist.

```yaml
# defaults/main.yml - Base configuration
---
nginx_worker_processes: 2
nginx_worker_connections: 1024
nginx_log_level: "warn"
nginx_access_log_enabled: true
nginx_error_log_enabled: true
nginx_gzip_enabled: true
nginx_gzip_level: 6

# group_vars/development.yml
---
environment: "development"
nginx_worker_processes: 1
nginx_log_level: "debug"
nginx_access_log_format: "combined"  # Verbose
debug_mode: true

# group_vars/production.yml
---
environment: "production"
nginx_worker_processes: "{{ ansible_processor_vcpus }}"
nginx_worker_connections: 4096
nginx_log_level: "error"
nginx_access_log_enabled: false  # Performance
nginx_gzip_level: 9  # Max compression
ssl_stapling: true
ssl_session_cache: "shared:SSL:10m"
```

Template kasutab conditionals environment-specific käitumiseks:

```jinja2
# templates/nginx.conf.j2
worker_processes {{ nginx_worker_processes }};

events {
    worker_connections {{ nginx_worker_connections }};
}

http {
    {% if environment == 'development' %}
    # Development-specific settings
    error_log /var/log/nginx/error.log {{ nginx_log_level }};
    access_log /var/log/nginx/access.log {{ nginx_access_log_format }};
    {% else %}
    # Production-optimized logging
    error_log /var/log/nginx/error.log {{ nginx_log_level }};
    {% if nginx_access_log_enabled %}
    access_log /var/log/nginx/access.log;
    {% else %}
    access_log off;
    {% endif %}
    {% endif %}
    
    {% if environment == 'production' and ssl_stapling is defined %}
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_session_cache {{ ssl_session_cache }};
    {% endif %}
}
```

### 1.3 Harjutus: Environment-Aware Deployment

Implementeerige kolme environment'i tugi oma nginx rollile: dev, staging, prod.

**Nõuded:**

- [ ] Kolm inventory group'i: development, staging, production
- [ ] Iga environment omab group_vars faili
- [ ] Development: debug mode, üks worker, max logging
- [ ] Staging: production-like config, medium logging
- [ ] Production: auto-detect CPU, minimal logging, max performance
- [ ] Playbook deploy'b õigesse environment'i ansible-playbook -i inventory/production site.yml
- [ ] SSL on mandatory production'is, optional dev/staging'us

**Näpunäiteid:**

- Kasutage assert moodulit valideerimaks et production environment omab SSL'i
- Environment tuvastamiseks kasuta inventory_hostname või group_names
- Template'is lisa {% if environment == 'production' %} blocks kriitiliste security seadete jaoks
- Loo Makefile või wrapper script kergeks environment switch'imiseks

**Testimine:**

```bash
# Deploy development
ansible-playbook -i inventory/development site.yml
curl http://dev-server  # Should work

# Deploy production
ansible-playbook -i inventory/production site.yml
curl https://prod-server  # Should work with SSL
curl http://prod-server   # Should redirect to HTTPS
```

**Boonus:**

Lisa canary deployment tugi - võimalus deploy'da production environment'is ainult 10% serveritest, testida, siis rollout ülejäänutele. Kasuta serial parameter playbook'is ja custom inventory groups.

---

## 3. Ansible Vault Integratsioon Rollidega

### 3.1 Probleem

Rollid sisaldavad tihti sensitiivset infot - SSL private key'sid, API token'eid, andmebaasi paroole. Neid ei tohi commit'ida Git repositoorysse plain text'ina. Aga kuidas jagada neid turvaliselt meeskonnaga? Kuidas deployment käivitada CI/CD pipeline'is ilma paroole käsitsi sisestamata?

Mõned proovivad eraldi secrets management süsteeme (HashiCorp Vault, AWS Secrets Manager), mis lisab komplekssust. Teised hoiavad secrets'e väljaspool repositooryt, mis raskendab deployment'i. Ansible Vault pakub built-in lahendust.

### 3.2 Lahendus

Ansible Vault krüpteerib faile või üksikuid muutujaid AES256 krüpteerimisega. Vault'itud failid on turvalised commit'ida Git'i. Deployment'i ajal Ansible dekrüpteerib need vault password'iga.

Rolli struktuuris loome eraldi vault.yml faili vars kaustas, krüpteerime selle, ja viitame krüpteeritud muutujatele defaults'ist.

```bash
# Loo vault fail
cat > roles/nginx/vars/vault.yml << 'EOF'
---
vault_ssl_private_key: |
  -----BEGIN PRIVATE KEY-----
  MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7...
  -----END PRIVATE KEY-----

vault_api_token: "sk-1234567890abcdef"
vault_db_password: "super_secret_password_123"
EOF

# Krüpteeri
ansible-vault encrypt roles/nginx/vars/vault.yml
# Küsib vault password'i

# Vault.yml on nüüd krüpteeritud
cat roles/nginx/vars/vault.yml
# $ANSIBLE_VAULT;1.1;AES256
# 616234656...
```

Defaults viitab vault muutujatele:

```yaml
# defaults/main.yml
---
ssl_private_key: "{{ vault_ssl_private_key }}"
api_token: "{{ vault_api_token }}"
db_password: "{{ vault_db_password }}"
```

Tasks kasutab neid nagu tavalist muutujat:

```yaml
# tasks/ssl.yml
---
- name: "Deploy SSL private key"
  copy:
    content: "{{ ssl_private_key }}"
    dest: /etc/ssl/private/nginx.key
    mode: '0600'
  no_log: true  # Ei logi sensitiivset sisu
```

Playbook käivitamine vault password'iga:

```bash
# Küsi interactively
ansible-playbook site.yml --ask-vault-pass

# Kasuta password file'i
echo "my_vault_password" > .vault_pass
chmod 600 .vault_pass
ansible-playbook site.yml --vault-password-file .vault_pass

# Kasuta environment variable'it
export ANSIBLE_VAULT_PASSWORD_FILE=.vault_pass
ansible-playbook site.yml
```

### 3.3 Harjutus: Secure Secrets Management

Lisage oma nginx rollile Ansible Vault tugi SSL private key'de ja API token'ite jaoks.

**Nõuded:**

- [ ] Loo vars/vault.yml krüpteeritud failiga
- [ ] Vault sisaldab SSL private key, API token, DB password
- [ ] Defaults/main.yml viitab vault muutujatele
- [ ] Tasks kasutavad no_log: true sensitiivsetele operatsioonidele
- [ ] README dokumenteerib vault usage'i
- [ ] .gitignore sisaldab .vault_pass
- [ ] CI/CD pipeline kasutab encrypted vault password'i (GitHub Secrets)

**Näpunäiteid:**

- Hoia vault password .vault_pass failis lokaalseks arendusleks
- CI/CD pipeline'is kasuta GitHub Secrets või GitLab CI Variables
- ansible-vault edit vault.yml võimaldab muuta krüpteeritud faili
- ansible-vault rekey vault.yml muudab vault password'i
- Kaasluge ansible.cfg default vault_password_file path

**Testimine:**

```bash
# Krüpteeri vault
ansible-vault create roles/nginx/vars/vault.yml

# Vaata krüpteeritud faili
cat roles/nginx/vars/vault.yml
# $ANSIBLE_VAULT;1.1;AES256...

# Edit vault'i
ansible-vault edit roles/nginx/vars/vault.yml

# Deploy'i kasutades vault'i
ansible-playbook site.yml --vault-password-file .vault_pass

# Valideeri et secrets ei lokaalu
ansible-playbook site.yml --vault-password-file .vault_pass -v
# Check output ei näita private key sisu
```

**Boonus:**

Implementeerige multiple vault passwords (vault-id feature). Erinev password development ja production secrets'te jaoks. Lisa automated secret rotation script, mis genereerib uued passwords, re-encrypt'ib vault'id, deploy'b muudatused.

---

## Kasulikud Ressursid

**Dokumentatsioon:**

- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html) - Ametlik guide role struktureerimiseks
- [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) - Secrets management dokumentatsioon
- [Galaxy Role Development](https://docs.ansible.com/ansible/latest/dev_guide/developing_galaxy.html) - Role'ide jagamine ja parimad praktikad
- [Jinja2 Templates](https://jinja.palletsprojects.com/en/3.1.x/templates/) - Template süntaks ja filters

**Tööriistad:**

- **Molecule** - Role testing framework: `pip install molecule molecule-docker`
- **Ansible Lint** - Code quality checker: `pip install ansible-lint`
- **Yamllint** - YAML syntax validator: `pip install yamllint`
- **pre-commit** - Git hooks automated testing'uks: `pip install pre-commit`

**Näited:**

- [Geerlingguy Roles](https://github.com/geerlingguy) - Jeff Geerling'i produktsioonitaseme rollid (nginx, postgresql, docker)
- [Ansible for DevOps](https://www.ansiblefordevops.com/) - Jeff Geerling'i raamat praktiliste näidetega
- [Ansible Galaxy](https://galaxy.ansible.com/) - Tuhandeid community rolle uurimiseks ja õppimiseks

---

Need harjutused on mõeldud süvendama teie Ansible rollide oskusi. Alustage esimesest ja liikuge järk-järgult keerulisemate poole.