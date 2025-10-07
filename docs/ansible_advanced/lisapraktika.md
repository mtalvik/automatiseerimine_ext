# Ansible Advanced Lisapraktika

Süvendavad harjutused Ansible edasijõudnud funktsioonidega. Need harjutused on mõeldud neile, kes soovivad õppida production-level tehnikaid ja automatiseerida keerukamaid stsenaariume.

**Eeldused:** Ansible põhiteadmised, templates, vault, handlers

---

## 1. Complex Template Logic

### 1.1 Probleem

Põhi Jinja2 template'id kasutavad lihtsaid muutujaid ja `{% if %}` tingimusi, kuid production keskkonnas on vaja keerulisemat loogikat. Kuidas luua template, mis:

- Arvutab dünaamiliselt väärtusi mitme muutuja põhjal
- Itereerib komplekssete andmestruktuuride üle
- Kasutab makrosid korduvate koodiplokkide jaoks
- Rakendab advanced filtreid andmete töötlemiseks

Näiteks Nginx konfiguratsioon, kus on mitu backend serverit, SSL seadistused sõltuvad keskkonnast, ja worker protsesside arv arvutatakse serveri ressursside põhjal.

### 1.2 Lahendus

Jinja2 pakub advanced funktsionaalsust, mis võimaldab kirjutada keerukaid template'eid:

**Filters ja arvutused:**
```jinja2
{% set workers = ansible_processor_vcpus | default(2) %}
worker_processes {{ workers }};
worker_connections {{ (1024 * workers) | int }};

{% set disk_space_gb = (ansible_mounts[0].size_total / 1024 / 1024 / 1024) | round(2) %}
# Available disk: {{ disk_space_gb }} GB
```

**Loops ja complex data:**
```jinja2
{% for backend in backend_servers %}
upstream {{ backend.name }} {
    {% for server in backend.servers %}
    server {{ server.host }}:{{ server.port }}{% if server.weight is defined %} weight={{ server.weight }}{% endif %};
    {% endfor %}
}
{% endfor %}
```

**Macros korduvate plokkide jaoks:**
```jinja2
{% macro location_block(path, proxy_pass) %}
location {{ path }} {
    proxy_pass {{ proxy_pass }};
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
{% endmacro %}

server {
    {{ location_block('/api/', 'http://api_backend') }}
    {{ location_block('/admin/', 'http://admin_backend') }}
}
```

**Advanced conditionals:**
```jinja2
{% if environment == 'prod' %}
error_log /var/log/nginx/error.log error;
{% elif environment == 'staging' %}
error_log /var/log/nginx/error.log warn;
{% else %}
error_log /var/log/nginx/error.log debug;
{% endif %}
```

Täielik näide (templates/nginx-advanced.conf.j2):
```jinja2
{% set workers = ansible_processor_vcpus | default(2) %}
user nginx;
worker_processes {{ workers }};

events {
    worker_connections {{ (1024 * workers) | int }};
}

http {
    {% for backend in backend_servers %}
    upstream {{ backend.name }} {
        {% for server in backend.servers %}
        server {{ server.host }}:{{ server.port }}{% if server.weight is defined %} weight={{ server.weight }}{% endif %};
        {% endfor %}
    }
    {% endfor %}

    {% if ssl_enabled | default(false) %}
    ssl_protocols {{ ssl_protocols | join(' ') }};
    ssl_ciphers {{ ssl_ciphers }};
    ssl_prefer_server_ciphers on;
    {% endif %}

    {% macro location_block(path, proxy_pass) %}
    location {{ path }} {
        proxy_pass {{ proxy_pass }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    {% endmacro %}

    server {
        listen 80;
        server_name {{ server_name }};

        {{ location_block('/api/', 'http://api_backend') }}
        {{ location_block('/admin/', 'http://admin_backend') }}
    }
}
```

### 1.3 Harjutus: Nginx Load Balancer Template

Loo advanced Nginx template, mis konfigreerib load balancer'i dünaamiliselt.

**Nõuded:**

- [ ] Template loob upstream blokke backend_servers listist
- [ ] Iga backend server saab weight väärtuse (kui defineeritud)
- [ ] SSL konfiguratsioon lisatakse ainult kui ssl_enabled == true
- [ ] Worker processes arvutatakse CPU tuumade põhjal
- [ ] Location blokid luuakse macro abil (vähemalt 2 location'i)
- [ ] Log level sõltub environment muutujast (prod/staging/dev)

**Näpunäiteid:**

- Kasuta `{% for %}` loopimiseks üle backend serverite
- `| default(value)` annab vaikeväärtuse kui muutuja puudub
- `| int` konverteerib stringi numbriks
- `{% if variable is defined %}` kontrollib muutuja olemasolu
- Macro defineeritakse `{% macro name(params) %}...{% endmacro %}`

**Testimine:**
```bash
# Genereeri template
ansible-playbook -i inventory/hosts.yml playbooks/site.yml --tags nginx

# Kontrolli genereeritud faili
cat /etc/nginx/nginx.conf

# Testi Nginx konfiguratsiooni
nginx -t
```

**Muutujad (group_vars/webservers/nginx.yml):**
```yaml
backend_servers:
  - name: api_backend
    servers:
      - host: 10.0.1.10
        port: 8080
        weight: 3
      - host: 10.0.1.11
        port: 8080
        weight: 2
  - name: admin_backend
    servers:
      - host: 10.0.2.10
        port: 9090

ssl_enabled: true
ssl_protocols:
  - TLSv1.2
  - TLSv1.3
ssl_ciphers: "HIGH:!aNULL:!MD5"

environment: "{{ app_env }}"
server_name: "{{ inventory_hostname }}.example.com"
```

**Boonus:**

- Lisa health check konfiguratsioon igale upstream serverile
- Implementeeri rate limiting erinevate location'ide jaoks
- Loo separate template fail includes jaoks ja kasuta `{% include %}`
- Lisa custom error pages konfiguratsioon

---

## 2. Dynamic Inventory AWS

### 2.1 Probleem

Static inventory failid ei skaleeru cloud keskkonnas, kus servereid luuakse ja kustutatakse dünaamiliselt. Kui AWS-is on 50 EC2 instance't ja need muutuvad iga päev, on käsitsi inventory uuendamine võimatu. Kuidas:

- Automaatselt avastada servereid AWS-ist
- Grupeerida neid tagide järgi
- Uuendada inventory't real-time
- Kasutada AWS metaandmeid Ansible muutujatena

### 2.2 Lahendus

Ansible toetab AWS EC2 dynamic inventory plugin'it, mis pärib instance'id otse AWS API-st. Plugin kasutab boto3 library't ja AWS credentials'eid.

**AWS EC2 inventory plugin (aws_ec2.yml):**
```yaml
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
  # Group by Environment tag
  - key: tags.Environment
    prefix: env
  # Group by Role tag
  - key: tags.Role
    prefix: role
  # Group by availability zone
  - key: placement.availability_zone
    prefix: az

hostnames:
  - tag:Name
  - dns-name

compose:
  ansible_host: public_ip_address
  ansible_user: "'ec2-user'"
```

See konfiguratsioon:

- Otsib instance'id US-East-1 ja EU-West-1 regioonidest
- Filtreerib ainult running instance'id Environment tagiga
- Loob gruppe tagide ja availability zone'ide järgi
- Kasutab Name tag'i või DNS nime hostname'ina
- Seadistab ansible_host ja ansible_user automaatselt

**Custom inventory script alternatiiv (inventory/custom_inventory.py):**
```python
#!/usr/bin/env python3

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
            
            tags = {tag['Key']: tag['Value'] 
                   for tag in instance.get('Tags', [])}
            
            env = tags.get('Environment', 'undefined')
            if env not in inventory:
                inventory[env] = {'hosts': []}
            
            inventory[env]['hosts'].append(name)
            
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

### 2.3 Harjutus: AWS Dynamic Inventory Setup

Seadista AWS EC2 dynamic inventory ja kasuta seda playbook'ides.

**Nõuded:**

- [ ] AWS credentials konfigureeritud (~/.aws/credentials või env vars)
- [ ] aws_ec2.yml inventory fail loodud
- [ ] Plugin pärib instance'id vähemalt ühest regioonist
- [ ] Instance'id on grupeeritud Environment tag järgi
- [ ] Playbook kasutab dynamic inventory't
- [ ] Inventory cache konfiguratsioon lisatud

**Näpunäiteid:**

- Installi boto3: `pip install boto3`
- AWS credentials: `aws configure` või seadista AWS_ACCESS_KEY_ID ja AWS_SECRET_ACCESS_KEY
- Testi inventory't: `ansible-inventory -i aws_ec2.yml --list`
- Kasuta `--graph` inventory struktuuri vaatamiseks
- Cache'imine kiirendab suuri inventory'sid

**Testimine:**
```bash
# Installi dependencies
pip install boto3 botocore

# Testi AWS ühendust
aws ec2 describe-instances --region us-east-1

# Vaata inventory't
ansible-inventory -i aws_ec2.yml --list

# Vaata grupeerimist
ansible-inventory -i aws_ec2.yml --graph

# Kasuta playbook'iga
ansible-playbook -i aws_ec2.yml site.yml

# Cache'imisega
ansible-playbook -i aws_ec2.yml site.yml \
  --inventory-cache-plugin jsonfile \
  --inventory-cache-timeout 3600
```

**AWS IAM õigused (minimum):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeTags"
      ],
      "Resource": "*"
    }
  ]
}
```

**Boonus:**

- Lisa multi-region support (kõik AWS regions)
- Implementeeri custom grouping logic (instance type, VPC, subnet)
- Loo inventory cache invalidation strategy
- Lisa DigitalOcean või Azure inventory samale projektile

---

## 3. Zero-Downtime Deployment

### 3.1 Probleem

Tavaline deployment peatab rakenduse, uuendab koodi ja käivitab uuesti. See tekitab downtime - kasutajad näevad vigu deployment'i ajal. Production keskkonnas pole downtime vastuvõetav. Kuidas:

- Deployida uus versioon ilma teenust peatamata
- Eemaldada servereid load balancer'ist enne uuendamist
- Kontrollida deployment'i õnnestumist enne järgmise serveri uuendamist
- Rollback automaatselt kui deployment ebaõnnestub

### 3.2 Lahendus

Rolling deployment strateegia uuendab servereid ühekaupa, kontrollides iga serveri tervise enne järgmise juurde liikumist. Ansible `serial` direktiiv võimaldab kontrollida mitu serverit korraga töödeldakse.

**Rolling deployment pattern:**
```yaml
---
- name: Rolling deployment
  hosts: webservers
  serial: 1  # Üks server korraga
  max_fail_percentage: 0  # Peata kui üks ebaõnnestub

  pre_tasks:
    - name: Health check enne deployment'i
      uri:
        url: "http://{{ inventory_hostname }}/health"
        status_code: 200
      delegate_to: localhost

    - name: Eemalda load balancer'ist
      haproxy:
        state: disabled
        host: "{{ inventory_hostname }}"
        socket: /var/run/haproxy.sock
      delegate_to: "{{ groups['loadbalancers'][0] }}"

  tasks:
    - name: Peata rakendus
      systemd:
        name: myapp
        state: stopped

    - name: Backup current version
      copy:
        src: /opt/myapp/app.jar
        dest: /opt/myapp/app.jar.backup
        remote_src: true

    - name: Deploy uus versioon
      copy:
        src: "myapp-{{ version }}.jar"
        dest: /opt/myapp/app.jar
      notify: restart myapp

    - name: Käivita rakendus
      systemd:
        name: myapp
        state: started

    - name: Oota kuni rakendus valmis
      uri:
        url: "http://{{ inventory_hostname }}:8080/health"
        status_code: 200
      register: result
      until: result.status == 200
      retries: 30
      delay: 2

  post_tasks:
    - name: Lisa tagasi load balancer'isse
      haproxy:
        state: enabled
        host: "{{ inventory_hostname }}"
        socket: /var/run/haproxy.sock
      delegate_to: "{{ groups['loadbalancers'][0] }}"

    - name: Smoke test
      uri:
        url: "http://{{ inventory_hostname }}/api/test"
        status_code: 200
      delegate_to: localhost

  handlers:
    - name: restart myapp
      systemd:
        name: myapp
        state: restarted
```

**Rollback playbook (rollback.yml):**
```yaml
---
- name: Rollback deployment
  hosts: "{{ failed_host }}"
  tasks:
    - name: Peata current version
      systemd:
        name: myapp
        state: stopped

    - name: Restore backup
      copy:
        src: /opt/myapp/app.jar.backup
        dest: /opt/myapp/app.jar
        remote_src: true

    - name: Käivita rakendus
      systemd:
        name: myapp
        state: started

    - name: Verify rollback
      uri:
        url: "http://{{ inventory_hostname }}:8080/health"
        status_code: 200
      register: result
      until: result.status == 200
      retries: 10
      delay: 2
```

### 3.3 Harjutus: Rolling Deployment Implementeerimine

Loo rolling deployment strategy veebirakendusele koos health check'ide ja rollback'iga.

**Nõuded:**

- [ ] Serial deployment - üks server korraga
- [ ] Pre-deployment health check kontrollib serveri tervise
- [ ] Server eemaldatakse load balancer'ist enne deployment'i
- [ ] Post-deployment health check verifitseerib rakenduse
- [ ] Server lisatakse tagasi load balancer'isse peale õnnestumist
- [ ] Deployment peatub kui üks server ebaõnnestub
- [ ] Backup luuakse enne uue versiooni deploy'mist

**Näpunäiteid:**

- `serial: 1` deployib üks server korraga, `serial: 2` kaks korraga
- `max_fail_percentage: 0` peatab kohe kui üks ebaõnnestub
- `delegate_to: localhost` käivitab task'i Ansible control node'is
- `until` ja `retries` ootavad kuni tingimus täidetud
- `pre_tasks` käivituvad enne `tasks`, `post_tasks` pärast

**Testimine:**
```bash
# Deploy uus versioon
ansible-playbook -i inventory/hosts.yml rolling-deploy.yml -e "version=2.0.0"

# Kontrolli deployment progressi
# (peaks nägema servereid ükshaaval)

# Testi rollback
ansible-playbook -i inventory/hosts.yml rollback.yml -e "failed_host=web1"
```

**Load balancer konfiguratsioon (HAProxy):**
```cfg
# /etc/haproxy/haproxy.cfg
global
    stats socket /var/run/haproxy.sock mode 600 level admin

backend webservers
    balance roundrobin
    option httpchk GET /health
    server web1 10.0.1.10:8080 check
    server web2 10.0.1.11:8080 check
    server web3 10.0.1.12:8080 check
```

**Boonus:**

- Implementeeri canary deployment (5% trafficu uuele versioonile esimesena)
- Lisa automated rollback kui health check ebaõnnestub
- Loo Slack notification deployment'i edusammudest
- Implementeeri blue-green deployment alternatiivina

---

## Kasulikud Ressursid

**Dokumentatsioon:**

- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Jinja2 Template Designer](https://jinja.palletsprojects.com/en/3.0.x/templates/)
- [AWS EC2 Inventory Plugin](https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html)
- [Rolling Updates](https://docs.ansible.com/ansible/latest/user_guide/playbooks_delegation.html)

**Tööriistad:**

- **ansible-lint**
- Playbook'ide linter ja best practices checker: `pip install ansible-lint`
- **ansible-doctor**
- Automaatne dokumentatsiooni genereerimine: `pip install ansible-doctor`
- **ara**
- Ansible run analysis ja visualiseerimine: `pip install ara`
- **mitogen**
- Ansible performance parandamine (kuni 7x kiirem): `pip install mitogen`

**Näited:**
- [Ansible Examples Repository](https://github.com/ansible/ansible-examples)
- [Jeff Geerling's Ansible Roles](https://github.com/geerlingguy) - kvaliteetsed production-ready rollid
- [Debops](https://debops.org/) - täielik datacenter automatiseerimine

---

Need harjutused on mõeldud sügvendama teie Ansible advanced oskusi. Alustage esimesest ja liikuge järk-järgult keerulisemate poole. Iga harjutus õpetab tehnikaid, mida kasutatakse pärisettevõtetes production keskkonnas.