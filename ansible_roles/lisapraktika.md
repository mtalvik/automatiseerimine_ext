#  Ansible Rollid: Lisapraktika


**Eesmärk:** Süvenda Ansible rollide teadmisi ja õpi professionaalseid tehnikaid

---

##  Enne alustamist

Need ülesanded on **valikulised** ja mõeldud neile, kes:
-  Lõpetasid põhilabori ära
-  Mõistavad Ansible rollide struktuuri
-  Tahavad õppida advanced funktsioone
-  Valmistuvad tõeliseks DevOps tööks

**Vali üks või mitu väljakutset!**

---

##  Väljakutse 1: Multi-OS Role

**Eesmärk:** Loo roll, mis töötab mitmes operatsioonisüsteemis (Ubuntu, CentOS, Debian)

### Mida õpid?
- OS-spetsiifilised muutujad (`vars/`)
- Conditional tasks (`when:`)
- Package manager abstraktsioon
- OS detection (`ansible_facts`)

### Ülesanne:
```yaml
# roles/nginx-multiplatform/
# - Installeerib nginx Ubuntu'le (apt), CentOS'le (yum)
# - Kasutab OS-spetsiifilisi config template'eid
# - Tagab teenuse töötab kõikides OS'ides
```

### Sammud:
1. **Loo role struktuuri:**
   ```bash
   ansible-galaxy init roles/nginx-multiplatform
   ```

2. **Lisa OS-spetsiifilised muutujad:**
   ```yaml
   # vars/Ubuntu.yml
   nginx_package: nginx
   nginx_service: nginx
   nginx_config_path: /etc/nginx/nginx.conf
   
   # vars/CentOS.yml
   nginx_package: nginx
   nginx_service: nginx
   nginx_config_path: /etc/nginx/nginx.conf
   ```

3. **Lisa dynamic variable loading:**
   ```yaml
   # tasks/main.yml
   - name: Load OS-specific variables
     include_vars: "{{ ansible_os_family }}.yml"
   
   - name: Install nginx
     package:
       name: "{{ nginx_package }}"
       state: present
   ```

4. **Testi mitmes OS'is:**
   ```bash
   # Vajad erinevaid VM'e või container'eid
   ansible-playbook -i inventory site.yml
   ```

###  Boonus:
- Lisa support Arch Linux'ile
- Kasuta `block` ja `rescue` error handling'uks
- Loo automated tests Molecule'iga

---

##  Väljakutse 2: Role Dependencies ja Composition

**Eesmärk:** Loo kompleksne web stack kasutades role dependencies

### Mida õpid?
- Role dependencies (`meta/main.yml`)
- Role composition patterns
- Dependency ordering
- Shared variables across roles

### Ülesanne:
```
# Loo täielik web stack:
# - common (base packages, users, firewall)
# - database (PostgreSQL)
# - backend (Node.js API)
# - frontend (Nginx reverse proxy)
# - monitoring (Prometheus + Grafana)
```

### Sammud:
1. **Loo iga component eraldi role'ina:**
   ```bash
   ansible-galaxy init roles/common
   ansible-galaxy init roles/database
   ansible-galaxy init roles/backend
   ansible-galaxy init roles/frontend
   ansible-galaxy init roles/monitoring
   ```

2. **Määra dependencies:**
   ```yaml
   # roles/frontend/meta/main.yml
   dependencies:
     - role: common
     - role: backend
   
   # roles/backend/meta/main.yml
   dependencies:
     - role: common
     - role: database
   ```

3. **Share variables across roles:**
   ```yaml
   # group_vars/all/shared.yml
   app_user: webapp
   app_port: 3000
   db_name: myapp
   db_user: webapp
   ```

4. **Loo orchestration playbook:**
   ```yaml
   # playbooks/deploy_stack.yml
   - hosts: webservers
     roles:
       - frontend  # See automaatselt deployb kõik dependencies
   ```

###  Boonus:
- Lisa health checks
- Loo rollback strategy
- Lisa automated backup role
- Kasuta Ansible Tower/AWX

---

##  Väljakutse 3: Dynamic Role Behavior

**Eesmärk:** Loo role, mis käitub erinevalt vastavalt environment'ile

### Mida õpid?
- Environment-based logic
- Template conditionals
- Ansible facts advanced usage
- Performance optimization

### Ülesanne:
```
# Loo nginx role, mis:
# - Dev: debug mode, slow performance, detailed logging
# - Staging: medium performance, moderate logging
# - Prod: max performance, minimal logging, security hardened
```

### Sammud:
1. **Loo environment detection:**
   ```yaml
   # defaults/main.yml
   environment: "{{ lookup('env', 'ENVIRONMENT') | default('dev') }}"
   ```

2. **Loo environment-specific configs:**
   ```yaml
   # vars/dev.yml
   nginx_worker_processes: 1
   nginx_worker_connections: 512
   nginx_log_level: debug
   nginx_cache_enabled: false
   
   # vars/prod.yml
   nginx_worker_processes: auto
   nginx_worker_connections: 4096
   nginx_log_level: error
   nginx_cache_enabled: true
   nginx_ssl_enabled: true
   ```

3. **Kasuta dynamic templates:**
   ```jinja2
   # templates/nginx.conf.j2
   worker_processes {{ nginx_worker_processes }};
   
   {% if nginx_ssl_enabled %}
   ssl_protocols TLSv1.2 TLSv1.3;
   ssl_ciphers HIGH:!aNULL:!MD5;
   {% endif %}
   
   {% if environment == 'dev' %}
   # Development-specific settings
   error_log /var/log/nginx/error.log debug;
   {% else %}
   error_log /var/log/nginx/error.log {{ nginx_log_level }};
   {% endif %}
   ```

4. **Test erinevates environment'ides:**
   ```bash
   ENVIRONMENT=dev ansible-playbook site.yml
   ENVIRONMENT=prod ansible-playbook site.yml
   ```

###  Boonus:
- Lisa A/B testing support
- Loo canary deployment
- Lisa feature flags
- Integreeri Consul service discovery'ga

---

##  Väljakutse 4: Ansible Galaxy Publication

**Eesmärk:** Avalda oma role Ansible Galaxy'sse ja tee see community-friendly

### Mida õpid?
- Ansible Galaxy best practices
- Role documentation
- Semantic versioning
- Community contribution

### Sammud:
1. **Valmista role ette publikatsiooniks:**
   ```yaml
   # meta/main.yml - täida kõik väljad
   galaxy_info:
     author: your_name
     description: Professional Nginx role with SSL and caching
     license: MIT
     min_ansible_version: 2.9
     platforms:
       - name: Ubuntu
         versions:
           - focal
           - jammy
     galaxy_tags:
       - nginx
       - webserver
       - ssl
   ```

2. **Kirjuta hea README:**
   ```markdown
   # Ansible Role: nginx-pro
   
   ## Description
   Professional-grade Nginx role...
   
   ## Requirements
   - Ansible 2.9+
   - Ubuntu 20.04+
   
   ## Role Variables
   ...
   
   ## Example Playbook
   ...
   
   ## License
   MIT
   ```

3. **Lisa tests (Molecule):**
   ```bash
   pip install molecule molecule-docker
   molecule init scenario
   molecule test
   ```

4. **Publish Galaxy'sse:**
   ```bash
   ansible-galaxy login
   ansible-galaxy import your_github_username your_role_repo
   ```

###  Boonus:
- Loo CI/CD pipeline (GitHub Actions)
- Lisa automated testing erinevates OS'ides
- Kirjuta contribution guidelines
- Lisa badges README'sse (build status, downloads, rating)

---

##  Väljakutse 5: Ansible Vault Integration

**Eesmärk:** Integreeri Ansible Vault role'idega turvalise secrets management'i jaoks

### Mida õpid?
- Vault best practices roles kontekstis
- Encrypted variables in roles
- Vault password strategies
- Secret rotation

### Sammud:
1. **Loo vault structure:**
   ```bash
   # roles/nginx-secure/
   ├── defaults/
   │   └── main.yml          # Public defaults
   ├── vars/
   │   └── vault.yml         # Encrypted secrets
   └── tasks/
       └── main.yml
   ```

2. **Encrypt sensitive variables:**
   ```bash
   ansible-vault create roles/nginx-secure/vars/vault.yml
   ```
   
   ```yaml
   # vars/vault.yml (encrypted)
   vault_ssl_key: |
     -----BEGIN PRIVATE KEY-----
     ...
     -----END PRIVATE KEY-----
   vault_api_token: "super-secret-token"
   vault_db_password: "very-secret-password"
   ```

3. **Reference vault variables:**
   ```yaml
   # defaults/main.yml (references)
   ssl_private_key: "{{ vault_ssl_key }}"
   api_token: "{{ vault_api_token }}"
   db_password: "{{ vault_db_password }}"
   ```

4. **Use in playbook:**
   ```bash
   ansible-playbook --ask-vault-pass site.yml
   # või
   ansible-playbook --vault-password-file ~/.vault_pass site.yml
   ```

###  Boonus:
- Kasuta multiple vault passwords (vault-id)
- Integreeri HashiCorp Vault'iga
- Loo automated secret rotation
- Lisa vault rekey automation

---

##  Väljakutse 6: Performance Optimization

**Eesmärk:** Optimeeri role performance suurtes infrastructure'ides

### Mida õpid?
- Ansible performance tuning
- Parallel execution strategies
- Fact caching
- Playbook optimization

### Tehnikad:
1. **Strategy optimization:**
   ```yaml
   # roles/fast-deploy/meta/main.yml
   - hosts: webservers
     strategy: free  # Don't wait for slowest host
     gather_facts: false  # Skip if not needed
   ```

2. **Fact caching:**
   ```ini
   # ansible.cfg
   [defaults]
   gathering = smart
   fact_caching = jsonfile
   fact_caching_connection = /tmp/ansible_facts
   fact_caching_timeout = 3600
   ```

3. **Task optimization:**
   ```yaml
   # Use async for long-running tasks
   - name: Install packages
     package:
       name: "{{ item }}"
     loop: "{{ packages }}"
     async: 300
     poll: 0
     register: install_async
   
   - name: Wait for installation
     async_status:
       jid: "{{ item.ansible_job_id }}"
     loop: "{{ install_async.results }}"
     register: install_result
     until: install_result.finished
     retries: 30
   ```

4. **Pipelining:**
   ```ini
   # ansible.cfg
   [ssh_connection]
   pipelining = True
   ```

###  Boonus:
- Profile playbook execution (`ANSIBLE_PROFILE_TASKS=1`)
- Use `mitogen` for faster execution
- Implement connection pooling
- Optimize template rendering

---

##  Täiendavad ressursid

### Dokumentatsioon:
- [Ansible Galaxy Best Practices](https://docs.ansible.com/ansible/latest/dev_guide/developing_galaxy.html)
- [Role Development Tips](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
- [Ansible Performance Tuning](https://docs.ansible.com/ansible/latest/user_guide/playbooks_strategies.html)

### Tööriistad:
- **Molecule:** Role testing framework
- **Ansible Lint:** Code quality checker
- **Ansible Tower/AWX:** Enterprise automation platform

### Community:
- [Ansible Galaxy](https://galaxy.ansible.com/) - Browse existing roles
- [Ansible GitHub](https://github.com/ansible) - Source code and examples
- [r/ansible](https://reddit.com/r/ansible) - Community discussions

---

##  Näpunäited

1. **Alusta lihtsast:** Ära ürita kõike korraga. Vali üks väljakutse ja keskendu sellele.
2. **Testi, testi, testi:** Iga muudatus peaks olema testitud enne production'i.
3. **Kasuta versioonikontrolli:** Iga role peaks olema Git repo's.
4. **Dokumenteeri:** Hea README on pool võitu.
5. **Õpi teistelt:** Vaata populaarseid Galaxy rolle ja õpi nende struktuurist.

---

**Edu ja head automatiseerimist!** 

