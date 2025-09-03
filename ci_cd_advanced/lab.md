# CI/CD Advanced Lab: Täielik Automatiseerimine
*ITS-24 DevOps Automatiseerimine | 3 tundi praktiline töö*

## 🎯 **Samm 1: Lab'i eesmärk**

**Täna teeme LÕPPPROJEKTI!** Kasutame KÕIKI oskusi, mida õppisime:

- **Git** (Nädal 9) → Version control ja collaboration
- **Ansible** (Nädal 11-15) → Server configuration
- **Docker** (Nädal 19-21) → Containerization
- **Terraform** (Nädal 23) → Infrastructure as Code
- **CI/CD** (Nädal 25) → Automated deployment
- **Monitoring** → Production visibility

## 🏢 **PROJEKT: "TechShop" E-commerce Automatiseerimine**

**Klient:** Väike e-commerce startup "TechShop"

**Probleem:** 
- Käsitsi deployment (2-3 tundi)
- Tihti vigu (30% failure rate)
- Aeglane rollback (1 tund)
- Arendajad stressis

**Lahendus:** Täielik automatiseerimine kõigi oskustega!

---

## 🛠️ **Vajalikud tööriistad**

**Kontrollige, et teil on:**
- Git
- Docker
- Python 3.9+
- Ansible
- Terraform
- GitLab konto (tasuta)
- VS Code

---

## 🚀 **Samm 2: Infrastructure as Code (Terraform) - 30 min**

### 2.1: Loo Terraform projekt

```bash
# 1. Loo projekt struktuur
mkdir techshop-automation
cd techshop-automation

# 2. Loo Terraform kaust
mkdir terraform
cd terraform

# 3. Loo Terraform failid
touch main.tf
touch variables.tf
touch outputs.tf
touch terraform.tfvars
```

### 2.2: Loo infrastruktuur

**`variables.tf`:**
```hcl
variable "project_name" {
  description = "Project name"
  type        = string
  default     = "techshop"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "instance_type" {
  description = "Local instance type"
  type        = string
  default     = "local"
}
```

**`main.tf`:**
```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# Local infrastructure setup
resource "local_file" "project_config" {
  content  = "Project: ${var.project_name}\nEnvironment: ${var.environment}\nInstance Type: ${var.instance_type}"
  filename = "${path.module}/config.txt"
}

resource "local_directory" "app_directory" {
  path = "${path.module}/app"
}

resource "local_file" "docker_compose" {
  content = templatefile("${path.module}/docker-compose.yml.tpl", {
    project_name = var.project_name
    environment  = var.environment
  })
  filename = "${path.module}/docker-compose.yml"
}

resource "local_file" "nginx_config" {
  content = templatefile("${path.module}/nginx.conf.tpl", {
    project_name = var.project_name
    server_name  = "localhost"
  })
  filename = "${path.module}/nginx.conf"
}

  tags = {
    Name = "${var.project_name}-web-server"
  }
}

# Web configuration
resource "local_file" "web_config" {
  content  = "Web server configuration for ${var.project_name}"
  filename = "web_config.txt"

  tags = {
    Name = "${var.project_name}-config"
  }
}
```

**`outputs.tf`:**
```hcl
output "project_config_path" {
  description = "Path to project configuration"
  value       = local_file.project_config.filename
}

output "app_directory_path" {
  description = "Path to application directory"
  value       = local_directory.app_directory.path
}
```

### 2.3: Deploy'i infrastruktuur

```bash
# 1. Initsialiseeri Terraform
terraform init

# 2. Vaata planeeritud muudatusi
terraform plan

# 3. Deploy'i infrastruktuur
terraform apply -auto-approve

# 4. Salvesta väljundid
terraform output > outputs.txt
```

---

## 🔧 **Samm 3: Server Configuration (Ansible) - 30 min**

### 3.1: Loo Ansible projekt

```bash
# 1. Mine tagasi projekti juurkausta
cd ..

# 2. Loo Ansible kaust
mkdir ansible
cd ansible

# 3. Loo Ansible failid
touch inventory.yml
touch playbook.yml
touch group_vars/all.yml
mkdir roles
mkdir roles/webserver
mkdir roles/webserver/tasks
mkdir roles/webserver/handlers
mkdir roles/webserver/templates
touch roles/webserver/tasks/main.yml
touch roles/webserver/handlers/main.yml
```

### 3.2: Seadista inventory

**`inventory.yml`:**
```yaml
all:
  children:
    webservers:
      hosts:
        localhost:
          ansible_connection: local
      vars:
        app_name: techshop
        app_port: 5000
```

### 3.3: Loo webserver role

**`roles/webserver/tasks/main.yml`:**
```yaml
---
- name: Update package cache
  apt:
    update_cache: yes
    cache_valid_time: 3600

- name: Install required packages
  apt:
    name:
      - python3
      - python3-pip
      - nginx
      - docker.io
      - docker-compose
    state: present

- name: Start and enable Docker
  systemd:
    name: docker
    state: started
    enabled: yes

- name: Add ubuntu user to docker group
  user:
    name: ubuntu
    groups: docker
    append: yes

- name: Create application directory
  file:
    path: /opt/{{ app_name }}
    state: directory
    owner: ubuntu
    group: ubuntu
    mode: '0755'

- name: Copy nginx configuration
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/sites-available/{{ app_name }}
    owner: root
    group: root
    mode: '0644'
  notify: restart nginx

- name: Enable nginx site
  file:
    src: /etc/nginx/sites-available/{{ app_name }}
    dest: /etc/nginx/sites-enabled/{{ app_name }}
    state: link
  notify: restart nginx

- name: Remove default nginx site
  file:
    path: /etc/nginx/sites-enabled/default
    state: absent
  notify: restart nginx
```

**`roles/webserver/handlers/main.yml`:**
```yaml
---
- name: restart nginx
  systemd:
    name: nginx
    state: restarted
```

**`roles/webserver/templates/nginx.conf.j2`:**
```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:{{ app_port }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://localhost:{{ app_port }}/health;
        access_log off;
    }
}
```

### 3.4: Loo playbook

**`playbook.yml`:**
```yaml
---
- name: Configure web server
  hosts: webservers
  become: yes
  roles:
    - webserver
```

### 3.5: Käivita Ansible

```bash
# 1. Seadista keskkonna muutuja
export WEB_SERVER_IP=$(terraform -chdir=../terraform output -raw web_server_public_ip)

# 2. Käivita Ansible playbook
ansible-playbook -i inventory.yml playbook.yml

# 3. Kontrolli tulemus
ansible webservers -i inventory.yml -m ping
```

---

## 🐳 **Samm 4: Application Development (Docker) - 30 min**

### 4.1: Loo rakendus

```bash
# 1. Mine tagasi projekti juurkausta
cd ..

# 2. Loo rakenduse kaust
mkdir app
cd app

# 3. Loo rakenduse failid
touch app.py
touch requirements.txt
touch Dockerfile
touch docker-compose.yml
```

### 4.2: Loo Flask rakendus

**`app.py`:**
```python
from flask import Flask, jsonify, request
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    logger.info(f"Home page accessed at {datetime.now()}")
    return jsonify({
        'message': 'TechShop E-commerce API',
        'version': '1.0.0',
        'status': 'running',
        'timestamp': str(datetime.now()),
        'hostname': os.uname().nodename
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': str(datetime.now())
    })

@app.route('/products')
def products():
    products = [
        {'id': 1, 'name': 'Laptop', 'price': 999.99},
        {'id': 2, 'name': 'Phone', 'price': 599.99},
        {'id': 3, 'name': 'Tablet', 'price': 399.99}
    ]
    return jsonify(products)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    logger.info(f"New order created: {data}")
    return jsonify({
        'message': 'Order created successfully',
        'order_id': 12345,
        'timestamp': str(datetime.now())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**`requirements.txt`:**
```
Flask==2.3.3
gunicorn==21.2.0
psutil==5.9.5
requests==2.31.0
```

### 4.3: Loo Dockerfile

**`Dockerfile`:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

### 4.4: Loo docker-compose

**`docker-compose.yml`:**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 4.5: Testi kohalikult

```bash
# 1. Ehita ja käivita
docker-compose up --build -d

# 2. Testi rakendust
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/products

# 3. Peata
docker-compose down
```

---

## 🚀 **HARJUTUS 4: CI/CD Pipeline (GitLab CI) - 45 min**

### Samm 1: Loo Git repository

```bash
# 1. Mine tagasi projekti juurkausta
cd ..

# 2. Initsialiseeri Git
git init

# 3. Lisa .gitignore
echo "*.tfstate" > .gitignore
echo "*.tfstate.backup" >> .gitignore
echo "*.tfvars" >> .gitignore
echo ".terraform/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore

# 4. Lisa failid
git add .

# 5. Esimene commit
git commit -m "Initial commit - TechShop automation project"

# 6. Lisa remote (asenda oma GitLab URL'iga)
git remote add origin https://gitlab.com/teie-kasutajanimi/techshop-automation.git

# 7. Push'i kood
git push -u origin main
```

### Samm 2: Loo CI/CD pipeline

**`.gitlab-ci.yml`:**
```yaml
stages:
  - validate
  - test
  - build
  - deploy-infrastructure
  - configure-servers
  - deploy-application

variables:
  DOCKER_IMAGE: registry.gitlab.com/teie-kasutajanimi/techshop-app
  TF_ADDRESS: ${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/terraform/state/techshop

# Validate Terraform
validate-terraform:
  stage: validate
  image: hashicorp/terraform:latest
  script:
    - cd terraform
    - terraform init
    - terraform validate
    - terraform plan -out=plan.tfplan
  artifacts:
    paths:
      - terraform/plan.tfplan
    expire_in: 1 hour
  only:
    - main

# Test application
test-app:
  stage: test
  image: python:3.9
  script:
    - cd app
    - pip install -r requirements.txt
    - python -c "import app; print('✅ App import successful')"
    - echo "Application tests passed!"
  only:
    - main

# Build Docker image
build-app:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - cd app
    - docker build -t $DOCKER_IMAGE:$CI_COMMIT_SHA .
    - docker push $DOCKER_IMAGE:$CI_COMMIT_SHA
    - echo "✅ Docker image built and pushed!"
  only:
    - main

# Deploy infrastructure
deploy-infrastructure:
  stage: deploy-infrastructure
  image: hashicorp/terraform:latest
  before_script:
    - cd terraform
    - terraform init
  script:
    - terraform apply -auto-approve
    - terraform output -json > outputs.json
  artifacts:
    paths:
      - terraform/outputs.json
    expire_in: 1 week
  only:
    - main
  when: manual

# Configure servers with Ansible
configure-servers:
  stage: configure-servers
  image: alpine:latest
  before_script:
    - apk add --no-cache ansible openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - chmod 700 ~/.ssh
  script:
    - cd ansible
    - ansible-playbook -i inventory.yml playbook.yml
    - echo "✅ Local environment configured!"
  dependencies:
    - deploy-infrastructure
  only:
    - main
  when: manual

# Deploy application
deploy-application:
  stage: deploy-application
  image: alpine:latest
  before_script:
    - apk add --no-cache docker-cli curl
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - echo "🚀 Deploying application locally..."
    - docker pull $DOCKER_IMAGE:$CI_COMMIT_SHA
    - docker stop techshop-app || true
    - docker rm techshop-app || true
    - docker run -d --name techshop-app -p 5000:5000 $DOCKER_IMAGE:$CI_COMMIT_SHA
    - sleep 10
    - curl -f http://localhost:5000/health || exit 1
    - echo "✅ Application deployed successfully!"
  dependencies:
    - configure-servers
  only:
    - main
  when: manual
```

### Samm 3: Seadista GitLab CI/CD

1. **Mine GitLab'i** → oma projekt
2. **Settings** → **CI/CD** → **Variables**
3. **Lisa muutujad:**
   - `DOCKER_IMAGE`: teie Docker image nimi
   - `CI_REGISTRY_USER`: GitLab registry kasutajanimi
   - `CI_REGISTRY_PASSWORD`: GitLab registry parool

---

## 📊 **HARJUTUS 5: Monitoring ja Troubleshooting - 30 min**

### Samm 1: Lisa monitoring

**Lisa `app.py` faili:**
```python
# Lisa import'id
import psutil
import requests

@app.route('/metrics')
def metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return jsonify({
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'disk_percent': disk.percent,
        'timestamp': str(datetime.now())
    })

@app.route('/status')
def status():
    # Check database connection (if exists)
    db_status = "healthy"  # Placeholder
    
    # Check external services
    try:
        response = requests.get('https://httpbin.org/status/200', timeout=5)
        external_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        external_status = "unhealthy"
    
    return jsonify({
        'database': db_status,
        'external_services': external_status,
        'application': 'healthy',
        'timestamp': str(datetime.now())
    })
```

### Samm 2: Lisa health check CI/CD pipeline'i

**Lisa `.gitlab-ci.yml` faili:**
```yaml
# Lisa uus stage
health-check:
  stage: deploy-application
  image: alpine:latest
  script:
    - apk add --no-cache curl
    - python3 -c "import json; data=json.load(open('terraform/outputs.json')); print(f'export WEB_SERVER_IP={data[\"web_server_public_ip\"][\"value\"]}')" > set_ip.sh
    - source set_ip.sh
    - echo "🏥 Running health checks..."
    - curl -f http://$WEB_SERVER_IP/health || exit 1
    - curl -f http://$WEB_SERVER_IP/metrics || exit 1
    - curl -f http://$WEB_SERVER_IP/status || exit 1
    - echo "✅ All health checks passed!"
  dependencies:
    - deploy-application
  only:
    - main
```

### Samm 3: Troubleshooting harjutused

**Probleem 1: Application ei käivitu**
```bash
# Kontrolli Docker container'i
ssh ubuntu@$WEB_SERVER_IP "docker ps -a"
ssh ubuntu@$WEB_SERVER_IP "docker logs techshop-app"

# Kontrolli port'i
ssh ubuntu@$WEB_SERVER_IP "netstat -tlnp | grep 5000"

# Kontrolli nginx
ssh ubuntu@$WEB_SERVER_IP "sudo systemctl status nginx"
```

**Probleem 2: Infrastructure deployment ebaõnnestub**
```bash
# Kontrolli Terraform state
cd terraform
terraform show
terraform plan

# Kontrolli kohalikke seadeid
ls -la
```

**Probleem 3: Ansible connection ebaõnnestub**
```bash
# Kontrolli SSH connection
ssh -i ~/.ssh/techshop-key.pem ubuntu@$WEB_SERVER_IP

# Kontrolli Ansible inventory
ansible webservers -i inventory.yml -m ping -vvv
```

---

## 📝 **HARJUTUS 6: Dokumenteerimine ja Demo - 15 min**

### Samm 1: Loo README.md

```markdown
# TechShop E-commerce Automation Project

## Projekt kirjeldus
Täielik automatiseeritud e-commerce lahendus, mis kasutab kõiki DevOps oskusi.

## Arhitektuur
- **Infrastructure**: Local (Terraform)
- **Configuration**: Ansible
- **Application**: Python Flask (Docker)
- **CI/CD**: GitLab CI
- **Monitoring**: Custom metrics

## Komponendid

### 1. Infrastructure (Terraform)
- Kohalikud seaded
- Konfiguratsioonifailid
- Security groups
- Elastic IP

### 2. Server Configuration (Ansible)
- Nginx reverse proxy
- Docker installation
- Application directory setup

### 3. Application (Docker)
- Flask REST API
- Health checks
- Metrics endpoint
- Product catalog

### 4. CI/CD Pipeline (GitLab CI)
- Infrastructure deployment
- Server configuration
- Application deployment
- Health monitoring

## Kuidas kasutada

### Kohalik arendus
```bash
# 1. Klooni projekt
git clone https://gitlab.com/teie-kasutajanimi/techshop-automation.git

# 2. Käivita kohalikult
cd app
docker-compose up --build

# 3. Testi
curl http://localhost:5000/
```

### Production deployment
1. Push'i kood GitLab'i
2. Käivita "deploy-infrastructure" job
3. Käivita "configure-servers" job
4. Käivita "deploy-application" job

## API Endpoints
- `GET /` - Home page
- `GET /health` - Health check
- `GET /metrics` - System metrics
- `GET /status` - Service status
- `GET /products` - Product catalog
- `POST /orders` - Create order

## Monitoring
- Health checks: `/health`
- System metrics: `/metrics`
- Service status: `/status`
- CI/CD pipeline monitoring

## Troubleshooting
- Application logs: `docker logs techshop-app`
- Nginx logs: `sudo tail -f /var/log/nginx/access.log`
- System logs: `journalctl -u docker`

## Tehnoloogiad
- **Infrastructure**: Terraform, Local
- **Configuration**: Ansible
- **Containerization**: Docker
- **CI/CD**: GitLab CI
- **Application**: Python Flask
- **Web Server**: Nginx

## Järgmised sammud
- [ ] Lisa PostgreSQL andmebaas
- [ ] Lisa Redis cache
- [ ] Lisa Prometheus monitoring
- [ ] Lisa SSL sertifikaadid
- [ ] Lisa backup automatiseerimine
```

### Samm 2: Demo ettevalmistus

**Valmista ette demo:**
1. **Infrastructure**: Näita Terraform koodi ja kohalikke ressursse
2. **Configuration**: Näita Ansible playbook'i ja kohalikku seadistust
3. **Application**: Näita Flask rakendust ja Docker container'it
4. **CI/CD**: Käivita pipeline ja näita deployment'i
5. **Monitoring**: Näita health checks ja metrics

---

## 🎯 **Samm 2: Lab Kokkuvõte**

### **Kõik oskused kasutatud:**
1. **Git** → Version control ja collaboration
2. **Terraform** → Infrastructure as Code
3. **Ansible** → Server configuration
4. **Docker** → Application containerization
5. **CI/CD** → Automated deployment
6. **Monitoring** → Production visibility
7. **Troubleshooting** → Probleemide lahendamine

### 🚀 **Real-world projekt:**
- **Production-ready** e-commerce lahendus
- **Täielik automatiseerimine** - nullist kuni deployment'ini
- **Kõik DevOps praktikad** ühes projektis

### 📊 **Tulemused:**
- **Deployment aeg**: 2-3 tundi → 5 minutit
- **Vigade arv**: 30% → 2%
- **Rollback aeg**: 1 tund → 2 minutit
- **Arendaja stress**: Kõrge → Madal

### 📚 **Järgmised sammud:**
- Lisa andmebaas automatiseerimine
- Lisa monitoring ja alerting
- Lisa security scanning
- Lisa backup ja disaster recovery

**🎉 Palju õnne! Oled nüüd valmis automatiseerimise projektideks!**

