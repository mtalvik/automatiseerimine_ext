# Ansible Edasijõudnud Lisapraktika

Täiendavad ülesanded Ansible advanced patterns'i õppimiseks.

**Eeldused:** Põhilabor läbitud, templates/vault/variables selged

---

## Enne alustamist

Need ülesanded on valikulised ja mõeldud neile, kes:

- Lõpetasid põhilabori ära
- Mõistavad Ansible templates, vault, variables
- Tahavad õppida advanced Ansible patterns
- Valmistuvad päris production automation'iks

---

## Väljakutse 1: Complex Template Logic


### Mida õpid?
- Jinja2 filters ja tests
- Macros ja includes
- Template inheritance
- Complex conditionals

### Advanced Jinja2 näited:

```jinja2
{# templates/nginx-advanced.conf.j2 #}
{% set workers = ansible_processor_vcpus | default(2) %}

user nginx;
worker_processes {{ workers }};

events {
    worker_connections {{ (1024 * workers) | int }};
}

http {
    {# Loop over upstream servers #}
    {% for backend in backend_servers %}
    upstream {{ backend.name }} {
        {% for server in backend.servers %}
        server {{ server.host }}:{{ server.port }}{% if server.weight is defined %} weight={{ server.weight }}{% endif %};
        {% endfor %}
    }
    {% endfor %}

    {# Include SSL config only if enabled #}
    {% if ssl_enabled | default(false) %}
    ssl_protocols {{ ssl_protocols | join(' ') }};
    ssl_ciphers {{ ssl_ciphers }};
    ssl_prefer_server_ciphers on;
    {% endif %}

    {# Macro for location blocks #}
    {% macro location_block(path, proxy_pass) %}
    location {{ path }} {
        proxy_pass {{ proxy_pass }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    {% endmacro %}

    {# Use macros #}
    server {
        listen 80;
        server_name {{ server_name }};

        {{ location_block('/api/', 'http://api_backend') }}
        {{ location_block('/admin/', 'http://admin_backend') }}
    }

    {# Complex conditional with filters #}
    {% if environment == 'prod' %}
    access_log /var/log/nginx/access.log combined;
    error_log /var/log/nginx/error.log error;
    {% elif environment == 'staging' %}
    access_log /var/log/nginx/access.log combined;
    error_log /var/log/nginx/error.log warn;
    {% else %}
    access_log /var/log/nginx/access.log combined;
    error_log /var/log/nginx/error.log debug;
    {% endif %}

    {# Custom filters #}
    {% set disk_space_gb = (ansible_mounts[0].size_total / 1024 / 1024 / 1024) | round(2) %}
# Available disk space: {{ disk_space_gb }} GB
}
```

### Variables for template:
```yaml
# group_vars/webservers/nginx.yml
backend_servers:
  - name: api_backend
    servers:
      - host: 10.0.1.10
        port: 8080
        weight: 3
      - host: 10.0.1.11
        port: 8080
        weight: 2

ssl_enabled: true
ssl_protocols:
  - TLSv1.2
  - TLSv1.3
ssl_ciphers: "HIGH:!aNULL:!MD5"

environment: "{{ lookup('env', 'ENVIRONMENT') | default('dev') }}"
server_name: "{{ inventory_hostname }}.example.com"
```

###  Boonus:
- Loo custom Jinja2 filter plugins
- Implementeeri template testing
- Lisa template validation
- Loo template library

---

## Väljakutse 2: Dynamic Inventory


### Mida õpid?
- Dynamic inventory scripts
- AWS EC2 inventory
- Inventory caching
- Custom grouping

### AWS EC2 Dynamic Inventory:

```yaml
# aws_ec2.yml
plugin: aws_ec2

regions:
  - us-east-1
  - eu-west-1

filters:
  tag:Environment:
    - production
    - staging
  instance-state-name: running

keyed_groups:
# Group by tags
  - key: tags.Environment
    prefix: env
  - key: tags.Role
    prefix: role
  - key: placement.availability_zone
    prefix: az

hostnames:
  - tag:Name
  - dns-name

compose:
  ansible_host: public_ip_address
  ansible_user: "'ec2-user'"
```

### Custom inventory script (Python):
```python
#!/usr/bin/env python3
# inventory/custom_inventory.py

import json
import boto3

def get_inventory():
    ec2 = boto3.client('ec2')
    
    inventory = {
        '_meta': {
            'hostvars': {}
        }
    }
    
    response = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            name = next((tag['Value'] for tag in instance.get('Tags', []) 
                        if tag['Key'] == 'Name'), instance['InstanceId'])
            
# Get tags
            tags = {tag['Key']: tag['Value'] 
                   for tag in instance.get('Tags', [])}
            
# Add to inventory
            env = tags.get('Environment', 'undefined')
            if env not in inventory:
                inventory[env] = {'hosts': []}
            
            inventory[env]['hosts'].append(name)
            
# Host vars
            inventory['_meta']['hostvars'][name] = {
                'ansible_host': instance.get('PublicIpAddress'),
                'ansible_user': 'ec2-user',
                'instance_id': instance['InstanceId'],
                'instance_type': instance['InstanceType'],
                'tags': tags
            }
    
    return inventory

if __name__ == '__main__':
    print(json.dumps(get_inventory(), indent=2))
```

### Use dynamic inventory:
```bash
# List inventory
ansible-inventory -i aws_ec2.yml --list

# Use in playbook
ansible-playbook -i aws_ec2.yml site.yml

# With caching
ansible-playbook -i aws_ec2.yml site.yml \
  --inventory-cache-plugin jsonfile \
  --inventory-cache-timeout 3600
```

###  Boonus:
- Loo multi-cloud inventory (AWS + Azure + GCP)
- Implementeeri inventory caching
- Lisa custom grouping logic
- Loo inventory validation

---

## Väljakutse 3: Ansible Tower/AWX Automation


### Mida õpid?
- AWX installation
- Job Templates
- Workflows
- RBAC

### AWX setup (Docker Compose):
```yaml
# docker-compose.yml
version: '3.8'

services:
  awx_web:
    image: ansible/awx:latest
    depends_on:
      - postgres
      - redis
    environment:
      - SECRET_KEY=awxsecret
      - DATABASE_USER=awx
      - DATABASE_PASSWORD=awxpass
      - DATABASE_NAME=awx
      - DATABASE_HOST=postgres
    ports:
      - "8080:8052"

  awx_task:
    image: ansible/awx:latest
    depends_on:
      - awx_web
    environment:
      - SECRET_KEY=awxsecret

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_USER=awx
      - POSTGRES_PASSWORD=awxpass
      - POSTGRES_DB=awx

  redis:
    image: redis:6
```

### AWX Configuration via API:
```python
#!/usr/bin/env python3
# configure_awx.py

import requests
import json

AWX_URL = "http://localhost:8080/api/v2"
USERNAME = "admin"
PASSWORD = "password"

def create_project(name, scm_url):
    response = requests.post(
        f"{AWX_URL}/projects/",
        auth=(USERNAME, PASSWORD),
        json={
            "name": name,
            "scm_type": "git",
            "scm_url": scm_url,
            "scm_update_on_launch": True
        }
    )
    return response.json()

def create_job_template(name, project_id, playbook):
    response = requests.post(
        f"{AWX_URL}/job_templates/",
        auth=(USERNAME, PASSWORD),
        json={
            "name": name,
            "job_type": "run",
            "inventory": 1,
            "project": project_id,
            "playbook": playbook,
            "credential": 1,
            "ask_variables_on_launch": True
        }
    )
    return response.json()

# Create project
project = create_project(
    "MyApp Infrastructure",
    "https://github.com/myorg/ansible-playbooks"
)

# Create job template
job_template = create_job_template(
    "Deploy Application",
    project['id'],
    "playbooks/deploy.yml"
)

print(f"Created job template: {job_template['id']}")
```

### Workflow setup:
```python
def create_workflow():
# Create workflow
    workflow = requests.post(
        f"{AWX_URL}/workflow_job_templates/",
        auth=(USERNAME, PASSWORD),
        json={
            "name": "Full Deployment Workflow",
            "description": "Deploy app with validation"
        }
    ).json()
    
# Add nodes
    nodes = [
        {"unified_job_template": 1, "success_nodes": [2]},  # Validate
        {"unified_job_template": 2, "success_nodes": [3], "failure_nodes": [4]},  # Deploy
        {"unified_job_template": 3},  # Test
        {"unified_job_template": 5}   # Rollback
    ]
    
    for node in nodes:
        requests.post(
            f"{AWX_URL}/workflow_job_templates/{workflow['id']}/workflow_nodes/",
            auth=(USERNAME, PASSWORD),
            json=node
        )
```

###  Boonus:
- Loo automated workflow creation
- Implementeeri job scheduling
- Lisa notification integrations (Slack/Email)
- Loo custom credential types

---

## Väljakutse 4: Testing with Molecule


### Mida õpid?
- Molecule framework
- Test scenarios
- Multiple platforms
- CI/CD integration

### Molecule setup:
```bash
# Install
pip install molecule molecule-docker

# Initialize
cd roles/myapp
molecule init scenario --driver-name docker

# Test
molecule test
```

### Molecule config (molecule/default/molecule.yml):
```yaml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: ubuntu-20
    image: ubuntu:20.04
    pre_build_image: true
  - name: ubuntu-22
    image: ubuntu:22.04
    pre_build_image: true
  - name: centos-8
    image: centos:8
    pre_build_image: true

provisioner:
  name: ansible
  playbooks:
    converge: converge.yml
    verify: verify.yml
  inventory:
    group_vars:
      all:
        myapp_version: "1.0.0"

verifier:
  name: ansible

scenario:
  test_sequence:
    - dependency
    - lint
    - cleanup
    - destroy
    - syntax
    - create
    - prepare
    - converge
    - idempotence
    - side_effect
    - verify
    - cleanup
    - destroy
```

### Test playbook (molecule/default/verify.yml):
```yaml
---
- name: Verify
  hosts: all
  gather_facts: false
  tasks:
    - name: Check service is running
      command: systemctl is-active myapp
      register: result
      failed_when: result.rc != 0

    - name: Check port is listening
      wait_for:
        port: 8080
        timeout: 5

    - name: Test HTTP endpoint
      uri:
        url: http://localhost:8080/health
        status_code: 200
```

### GitLab CI integration:
```yaml
# .gitlab-ci.yml
test:molecule:
  stage: test
  image: python:3.9
  services:
    - docker:dind
  before_script:
    - pip install molecule molecule-docker
  script:
    - cd roles/myapp
    - molecule test
```

###  Boonus:
- Loo multi-platform tests
- Lisa performance testing
- Implementeeri security scanning
- Loo test coverage reports

---

## Väljakutse 5: Custom Modules


### Mida õpid?
- Module development
- AnsibleModule API
- Return values
- Error handling

### Custom module (library/custom_user.py):
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: custom_user
short_description: Manage users with custom logic
description:
    - Create, modify, or delete users with custom validation
options:
    name:
        description: Username
        required: true
        type: str
    state:
        description: User state
        choices: ['present', 'absent']
        default: present
        type: str
    email:
        description: User email
        type: str
'''

EXAMPLES = '''
- name: Create user
  custom_user:
    name: john
    email: john@example.com
    state: present
'''

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            email=dict(type='str'),
        ),
        supports_check_mode=True
    )

    name = module.params['name']
    state = module.params['state']
    email = module.params['email']

    result = dict(
        changed=False,
        name=name,
        state=state
    )

# Check if user exists
    try:
        import pwd
        user_exists = True
        pwd.getpwnam(name)
    except KeyError:
        user_exists = False

    if state == 'present':
        if not user_exists:
            if not module.check_mode:
# Create user logic here
                import subprocess
                cmd = ['useradd', name]
                rc = subprocess.call(cmd)
                if rc != 0:
                    module.fail_json(msg=f"Failed to create user {name}")
            
            result['changed'] = True
            result['msg'] = f"User {name} created"
        else:
            result['msg'] = f"User {name} already exists"

    elif state == 'absent':
        if user_exists:
            if not module.check_mode:
# Delete user logic here
                import subprocess
                cmd = ['userdel', name]
                rc = subprocess.call(cmd)
                if rc != 0:
                    module.fail_json(msg=f"Failed to delete user {name}")
            
            result['changed'] = True
            result['msg'] = f"User {name} deleted"
        else:
            result['msg'] = f"User {name} does not exist"

    module.exit_json(**result)

if __name__ == '__main__':
    main()
```

### Use custom module:
```yaml
# playbook.yml
- hosts: all
  tasks:
    - name: Create user with custom module
      custom_user:
        name: john
        email: john@example.com
        state: present
```

###  Boonus:
- Loo module with complex logic
- Lisa comprehensive error handling
- Implementeeri module testing
- Publish module to Ansible Galaxy

---

## Väljakutse 6: Zero-Downtime Deployment


### Mida õpid?
- Serial execution
- Health checks
- Rollback strategies
- Load balancer integration

### Rolling deployment playbook:
```yaml
---
- name: Rolling deployment
  hosts: webservers
  serial: 1  # One server at a time
  max_fail_percentage: 0  # Stop if any fails

  pre_tasks:
    - name: Check server health before deployment
      uri:
        url: "http://{{ inventory_hostname }}/health"
        status_code: 200
      delegate_to: localhost

    - name: Remove from load balancer
      haproxy:
        state: disabled
        host: "{{ inventory_hostname }}"
        socket: /var/run/haproxy.sock
      delegate_to: "{{ groups['loadbalancers'][0] }}"

  tasks:
    - name: Stop application
      systemd:
        name: myapp
        state: stopped

    - name: Deploy new version
      copy:
        src: "myapp-{{ version }}.jar"
        dest: /opt/myapp/app.jar
      notify: restart myapp

    - name: Start application
      systemd:
        name: myapp
        state: started

    - name: Wait for application to be ready
      uri:
        url: "http://{{ inventory_hostname }}:8080/health"
        status_code: 200
      register: result
      until: result.status == 200
      retries: 30
      delay: 2

  post_tasks:
    - name: Add back to load balancer
      haproxy:
        state: enabled
        host: "{{ inventory_hostname }}"
        socket: /var/run/haproxy.sock
      delegate_to: "{{ groups['loadbalancers'][0] }}"

    - name: Run smoke tests
      uri:
        url: "http://{{ inventory_hostname }}/api/test"
        status_code: 200
      delegate_to: localhost

  handlers:
    - name: restart myapp
      systemd:
        name: myapp
        state: restarted

  rescue:
    - name: Rollback on failure
      include_tasks: rollback.yml
```

### Rollback playbook:
```yaml
# rollback.yml
---
- name: Stop current version
  systemd:
    name: myapp
    state: stopped

- name: Restore previous version
  copy:
    src: /opt/myapp/app.jar.backup
    dest: /opt/myapp/app.jar
    remote_src: true

- name: Start application
  systemd:
    name: myapp
    state: started

- name: Notify team
  slack:
    token: "{{ slack_token }}"
    channel: "#deployments"
    msg: "Rollback executed on {{ inventory_hostname }}"
```

###  Boonus:
- Lisa canary deployment strategy
- Loo automated rollback triggers
- Implementeeri health check validation
- Lisa deployment metrics collection

---

## Täiendavad ressursid

### Dokumentatsioon:
- [Ansible Docs](https://docs.ansible.com/)
- [Molecule Docs](https://molecule.readthedocs.io/)
- [AWX Docs](https://docs.ansible.com/ansible-tower/)
- [Jinja2 Docs](https://jinja.palletsprojects.com/)

### Tööriistad:
- **ansible-lint:** Playbook linter
- **ansible-doctor:** Documentation generator
- **ara:** Ansible run analysis
- **mitogen:** Performance boost for Ansible

### Näited:
- [Ansible Examples](https://github.com/ansible/ansible-examples)
- [Jeff Geerling's Roles](https://github.com/geerlingguy)
- [Debops](https://debops.org/) - Complete datacenter automation

---

## Näpunäited

1. **Test in dev first:** Ära kunagi testi production'is esimest korda
2. **Use check mode:** `--check` on sinu sõber
3. **Version control:** Kõik playbook'id peaks olema Git'is
4. **Document plays:** Kommentaarid on tulevase sina jaoks
5. **Monitor execution:** Kasuta ara või AWX logi analüüsiks

---

**Edu ja head automatiseerimist!** 

