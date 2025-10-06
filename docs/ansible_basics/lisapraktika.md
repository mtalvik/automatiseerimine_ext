# Ansible Lisapraktika

**Eeltingimused:** Ansible põhiteadmised, SSH setup, YAML

---

##  Ülevaade

See fail sisaldab lisapraktikaid Ansible mooduli jaoks, sealhulgas advanced playbooks, complex Jinja2, custom facts, ja troubleshooting techniques.

---

## Õpiväljundid

Pärast lisapraktikat oskate:

- Kirjutada keerulisi Jinja2 template'eid filters ja loops'iga
- Kasutada advanced Ansible modules (lineinfile, blockinfile, replace)
- Custom facts ja dynamic inventory
- Error handling ja retry logic
- Performance optimization (async, forks)

---

##  Advanced Jinja2 Templates

### Filters

```yaml
- name: "Advanced Jinja2 filters"
  debug:
    msg: |
      Uppercase: {{ "hello" | upper }}
      Default: {{ undefined_var | default("fallback") }}
      Join list: {{ ['a', 'b', 'c'] | join('-') }}
      Random: {{ ['red', 'blue', 'green'] | random }}
      Unique: {{ [1, 2, 2, 3] | unique }}
      JSON: {{ my_dict | to_json }}
      YAML: {{ my_dict | to_yaml }}
```

### Loops in Templates

```jinja
{# nginx upstream config #}
upstream backend {
  {% for server in backend_servers %}
  server {{ server.ip }}:{{ server.port }} weight={{ server.weight | default(1) }};
  {% endfor %}
}

{# Conditional blocks #}
server {
  listen 80;
  {% if enable_ssl %}
  listen 443 ssl;
  ssl_certificate {{ ssl_cert }};
  ssl_certificate_key {{ ssl_key }};
  {% endif %}
  
  {% for domain in domains %}
  server_name {{ domain }};
  {% endfor %}
}
```

### Complex Logic

```jinja
{# Generate different configs per environment #}
{% if ansible_hostname starts with 'prod' %}
log_level = ERROR
max_connections = 1000
{% elif ansible_hostname starts with 'staging' %}
log_level = WARNING
max_connections = 500
{% else %}
log_level = DEBUG
max_connections = 100
{% endif %}

{# Math operations #}
Total memory: {{ ansible_memtotal_mb }} MB
Cache size: {{ (ansible_memtotal_mb * 0.25) | int }} MB
```

### Ülesanne 1: Dynamic Nginx Config Generator

Loo playbook, mis genereerib nginx config:
- Variables: list of apps (name, port, replicas, health_check_path)
- Template: upstream blocks, server blocks, health checks
- Kasuta filters: `default`, `reject`, `map`

---

## Advanced File Manipulation

### lineinfile - Täpne Rea Muutmine

```yaml
- name: "Ensure SSH port is 2222"
  lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^#?Port '
    line: 'Port 2222'
    validate: '/usr/sbin/sshd -t -f %s'
  notify: restart sshd

- name: "Add custom setting if not exists"
  lineinfile:
    path: /etc/myapp.conf
    line: 'custom_setting = enabled'
    insertafter: '^# Custom settings'
    state: present
```

### blockinfile - Multi-Line Blocks

```yaml
- name: "Add custom Apache config block"
  blockinfile:
    path: /etc/apache2/sites-available/mysite.conf
    marker: "# {mark} ANSIBLE MANAGED BLOCK - SSL"
    block: |
      SSLEngine on
      SSLCertificateFile /etc/ssl/certs/mysite.crt
      SSLCertificateKeyFile /etc/ssl/private/mysite.key
      SSLProtocol all -SSLv2 -SSLv3
```

### replace - Regex Replace

```yaml
- name: "Replace all occurrences"
  replace:
    path: /etc/hosts
    regexp: 'old\.domain\.com'
    replace: 'new.domain.com'
```

### Ülesanne 2: Configuration Migration

Loo playbook, mis:
- Loeb olemasoleva config faili
- Asendab deprecated settings uutega (regex)
- Lisab uusi settings plokke
- Validates syntax enne commit'i
- Backup original file

---

##  Loops ja Conditionals

### Loop Over Complex Structures

```yaml
- name: "Create users with specific settings"
  user:
    name: "{{ item.name }}"
    groups: "{{ item.groups | join(',') }}"
    shell: "{{ item.shell | default('/bin/bash') }}"
    state: present
  loop:
    - { name: 'alice', groups: ['sudo', 'docker'], shell: '/bin/zsh' }
    - { name: 'bob', groups: ['docker'] }
    - { name: 'charlie', groups: ['www-data'], shell: '/bin/bash' }
  when: item.name != 'root'
```

### Loop with Conditions

```yaml
- name: "Install packages per OS"
  package:
    name: "{{ item }}"
    state: present
  loop: "{{ packages[ansible_os_family] }}"
  when: packages[ansible_os_family] is defined

vars:
  packages:
    Debian: ['nginx', 'postgresql', 'redis-server']
    RedHat: ['nginx', 'postgresql-server', 'redis']
```

### Nested Loops

```yaml
- name: "Create directory structure"
  file:
    path: "/var/www/{{ item.0.name }}/{{ item.1 }}"
    state: directory
  with_nested:
    - "{{ websites }}"
    - ['public', 'logs', 'backups']
```

---

## Error Handling

### Block/Rescue/Always

```yaml
- name: "Try to deploy app"
  block:
    - name: "Stop service"
      service:
        name: myapp
        state: stopped
    
    - name: "Deploy new version"
      copy:
        src: app-v2.0.tar.gz
        dest: /opt/myapp/
    
    - name: "Extract and configure"
      unarchive:
        src: /opt/myapp/app-v2.0.tar.gz
        dest: /opt/myapp/
  
  rescue:
    - name: "Rollback on failure"
      copy:
        src: /opt/myapp/backup/
        dest: /opt/myapp/
        remote_src: yes
    
    - name: "Notify failure"
      debug:
        msg: "Deployment failed! Rolled back to previous version."
  
  always:
    - name: "Start service"
      service:
        name: myapp
        state: started
```

### Retry Logic

```yaml
- name: "Wait for service to be healthy"
  uri:
    url: "http://localhost:8080/health"
    status_code: 200
  register: health_check
  until: health_check.status == 200
  retries: 10
  delay: 5
  failed_when: false  # Don't fail immediately
```

---

## Performance Optimization

### Async Tasks

```yaml
- name: "Long running backup (async)"
  command: /usr/local/bin/backup.sh
  async: 3600  # Timeout 1h
  poll: 0      # Fire and forget
  register: backup_job

- name: "Do other stuff while backup runs"
# ... other tasks ...

- name: "Check backup status"
  async_status:
    jid: "{{ backup_job.ansible_job_id }}"
  register: backup_result
  until: backup_result.finished
  retries: 60
  delay: 10
```

### Parallel Execution

```yaml
# ansible.cfg
[defaults]
forks = 20            # Run on 20 hosts simultaneously
gathering = smart     # Cache facts
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 3600
```

### Disable Fact Gathering

```yaml
- name: "Quick playbook"
  hosts: all
  gather_facts: no  # Saves 2-5 seconds per host!
  tasks:
    - name: "Quick task"
      command: echo "hello"
```

---

## Custom Facts

### Create Custom Fact

```yaml
- name: "Create custom fact"
  copy:
    dest: /etc/ansible/facts.d/myapp.fact
    content: |
      [deployment]
      version=2.1.0
      deployed_by=ansible
      deployed_at={{ ansible_date_time.iso8601 }}
    mode: '0755'

- name: "Reload facts"
  setup:

- name: "Use custom fact"
  debug:
    msg: "App version: {{ ansible_local.myapp.deployment.version }}"
```

### Dynamic Facts Script

```bash
#!/bin/bash
# /etc/ansible/facts.d/app_status.fact

echo "{
  \"status\": \"$(systemctl is-active myapp)\",
  \"uptime\": \"$(systemctl show -p ActiveEnterTimestamp myapp --value)\",
  \"memory\": \"$(ps aux | grep myapp | awk '{sum+=$6} END {print sum}')\"
}"
```

---

##  Challenge: Full Stack Deployment

**Ülesanne:** Loo täielik 3-tier deployment playbook

**Requirements:**
- [ ] Load balancer setup (nginx)
- [ ] Application servers (3x replicas)
- [ ] Database setup (PostgreSQL with replication)
- [ ] Redis cache
- [ ] SSL certificates (Let's Encrypt simulation)
- [ ] Monitoring agents (node_exporter)
- [ ] Backup cron jobs
- [ ] Health checks ja rolling updates
- [ ] Error handling ja rollback
- [ ] Custom facts for deployment info
- [ ] Performance optimized (async, parallelism)

**Bonus:**
- [ ] Zero-downtime deployment
- [ ] Blue-green deployment logic
- [ ] Automated testing after deployment
- [ ] Slack/email notifications

---

## Troubleshooting Tips

### Debug Output

```yaml
- name: "Debug complex variable"
  debug:
    var: my_complex_dict
    verbosity: 2  # Only with -vv

- name: "Debug with formatting"
  debug:
    msg: |
      Host: {{ inventory_hostname }}
      IP: {{ ansible_default_ipv4.address }}
      OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
```

### Dry Run

```bash
# Check mode (no changes)
ansible-playbook playbook.yml --check

# Diff mode (show what would change)
ansible-playbook playbook.yml --check --diff
```

### Step-by-Step Execution

```bash
# Ask before each task
ansible-playbook playbook.yml --step

# Start from specific task
ansible-playbook playbook.yml --start-at-task="Deploy application"
```

---

## Kasulikud Ressursid

- **Ansible Docs**: https://docs.ansible.com/
- **Jinja2 Docs**: https://jinja.palletsprojects.com/
- **Best Practices**: https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html
- **Module Index**: https://docs.ansible.com/ansible/latest/collections/index_module.html

---

**Edu advanced Ansible'iga!** 

