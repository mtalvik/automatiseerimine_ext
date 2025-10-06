#  Docker: Konteinerite Põhitõed

**Teemad:** Container vs VM, Docker põhikäsud, Dockerfile, volumes, best practices

---

##  Õpiväljundid

Pärast seda moodulit oskate:
- Selgitada, mis probleemi Docker lahendab ja miks see on parem kui VM
- Käivitada ja hallata Docker container'eid (`run`, `ps`, `logs`, `exec`)
- Kirjutada Dockerfile'i ja ehitada image'e
- Kasutada volume'e andmete säilitamiseks ja port mapping'u
- Rakendada põhilisi best practices'eid (`.dockerignore`, cache, väiksemad image'd)

---

# BLOKK 1: Miks Docker?

## Probleem enne Dockerit

### "Works on My Machine" sündroom
```bash
Arendaja: "Mul töötab!"
Testija: "Mul crashib..."
DevOps: "Serveris error..."
Klient: "Miks ei tööta?!"
```

**Näide:** Python rakendus
- Arendaja: Python 3.8 + Ubuntu 20.04
- Server: Python 3.6 + CentOS 7  
- Tulemus:  Dependency conflict

### Kuidas lahendati varem?

#### 1. Virtuaalmasinad (2000-2010)
```
 Aeglased (30s+ käivitus)
 Ressursinõudlikud (GB RAM per VM)
 Keerulised haldada
```

#### 2. Configuration Management (2010-2015)
```bash
# Puppet/Ansible
- package: python3.8
- service: nginx
- config: /etc/nginx/nginx.conf
```
```
 Drift (serverid muutuvad aja jooksul)
 Keeruline debugida
 Snowflake serverid
```

## Docker'i revolutsioon (2013)

### Konteinerite idee

```mermaid
graph TB
    subgraph "Host OS (Linux)"
        Docker[Docker Engine]
        C1[ Container 1<br/>Python app]
        C2[ Container 2<br/>Node.js app]
        C3[ Container 3<br/>Database]
        C4[ Container 4<br/>Redis]
        
        Docker --> C1
        Docker --> C2
        Docker --> C3
        Docker --> C4
    end
    
    style Docker fill:#2496ed,color:#fff
    style C1 fill:#f0f0f0
    style C2 fill:#f0f0f0
    style C3 fill:#f0f0f0
    style C4 fill:#f0f0f0
```

### Peamised eelised
1. **Kiirus:** 1-2 sekundit käivituseks
2. **Ressursid:** MB mitte GB  
3. **Portability:** Töötab kõikjal
4. **Consistency:** Sama käitumine kõikjal

### Numbrites
```
Traditional VM    vs    Docker Container
├── 30-120s startup    ├── 1-5s startup
├── 1-8GB RAM         ├── 10-100MB RAM  
├── 10-50 per server  ├── 100-1000 per server
└── 10-50GB disk      └── 100MB-1GB disk
```

## Kasutusstatistika
- **87%** ettevõtetest kasutab konteinereid (2024)
- **Netflix:** 1 miljardit konteinerit nädalas
- **Google:** 2 miljardit konteinerit nädalas

---

# BLOKK 2: Docker Install ja Esimesed Käsud

## Docker'i arhitektuur

```mermaid
graph TB
    subgraph "Docker Host"
        Client[Docker CLI]
        Daemon[Docker Daemon]
        Images[Images]
        Containers[Containers]
    end
    
    subgraph "External"
        Registry[Docker Hub Registry]
    end
    
    Client -->|commands| Daemon
    Daemon --> Images
    Daemon --> Containers
    Daemon <-->|pull/push| Registry
```

### Komponendid
- **Docker CLI:** Kasutaja käsud
- **Docker Daemon:** Taustaprotsess (dockerd)  
- **Images:** Template'id rakenduste jaoks
- **Containers:** Töötavad instantsid
- **Registry:** Image'ide ladu (Docker Hub)

## Installation

### Ubuntu/Debian
```bash
# Automatic install script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker run hello-world
```

### Windows/Mac
- **Docker Desktop:** https://www.docker.com/products/docker-desktop/
- GUI + Linux VM taustal

## Põhimõisted

```mermaid
graph LR
    Registry[ Registry<br/>Docker Hub]
    Image[ Image<br/>read-only template]
    Container[ Container<br/>running instance]
    
    Registry -->|docker pull| Image
    Image -->|docker run| Container
    Container -->|docker commit| Image
    Image -->|docker push| Registry
    
    style Registry fill:#0db7ed,color:#fff
    style Image fill:#384d54,color:#fff
    style Container fill:#2496ed,color:#fff
```

### 1. Image
- **Read-only template** 
- Sisaldab: OS + runtime + dependencies + rakendus
- **Immutable** (ei muutu)

### 2. Container  
- **Running instance** image'ist
- **Writable layer** image'i peal
- **Isolated process**

### 3. Registry
- **Repository** image'ide jaoks
- **Docker Hub:** avalik registry
- **Private registries:** ettevõtte sisesed

## DEMO: Esimesed käsud

### Image operations
```bash
# Search images
docker search nginx
docker search python --filter stars=100

# Pull image  
docker pull nginx
docker pull nginx:alpine  # specific tag

# List local images
docker images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Inspect image
docker image inspect nginx
docker image history nginx  # layer history
```

### Container operations
```bash
# Run container (foreground)
docker run nginx

# Run in background
docker run -d nginx

# Run with port mapping
docker run -d -p 8080:80 nginx

# Run with name
docker run -d -p 8080:80 --name minu-nginx nginx

# List running containers
docker ps

# List all containers
docker ps -a

# View logs
docker logs minu-nginx
docker logs -f minu-nginx  # follow

# Execute command in container
docker exec minu-nginx ls /etc/nginx
docker exec -it minu-nginx bash  # interactive

# Stop container
docker stop minu-nginx

# Remove container
docker rm minu-nginx

# Remove image
docker rmi nginx
```

### Cleanup commands
```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove everything unused
docker system prune

# See disk usage
docker system df
```

---

# BLOKK 3: Dockerfile ja Image'ide Loomine

## Dockerfile põhitõed

### Mis on Dockerfile?
- **Text file** mis kirjeldab kuidas image ehitada
- **Layer-based:** iga käsk = uus layer
- **Cached:** korduvad layerid kasutatakse uuesti

```mermaid
graph TD
    DF[ Dockerfile]
    Build[docker build]
    L1[Layer 1: FROM ubuntu]
    L2[Layer 2: RUN apt-get update]
    L3[Layer 3: COPY app.py]
    L4[Layer 4: CMD python app.py]
    Image[ Final Image]
    
    DF --> Build
    Build --> L1
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> Image
    
    style DF fill:#f9f9f9
    style Build fill:#2496ed,color:#fff
    style L1 fill:#e8f4f8
    style L2 fill:#e8f4f8
    style L3 fill:#e8f4f8
    style L4 fill:#e8f4f8
    style Image fill:#384d54,color:#fff
```

### Dockerfile süntaks
```dockerfile
# Comment
INSTRUCTION arguments
```

## Dockerfile instruction'id

### FROM - alus image
```dockerfile
FROM ubuntu:20.04          # specific version
FROM python:3.9-alpine     # smaller base  
FROM scratch               # empty base
```

### WORKDIR - töökaust
```dockerfile
WORKDIR /app
# Equivalent to: mkdir -p /app && cd /app
```

### COPY vs ADD
```dockerfile
# COPY - lihtne faili kopeerimine
COPY src/ /app/src/
COPY requirements.txt .

# ADD - extended features (avoid!)
ADD https://example.com/file.tar.gz /app/  # downloads
ADD archive.tar.gz /app/                   # auto-extracts
```

### RUN - käsu käivitamine
```dockerfile
# Separate commands (bad)
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y pip

# Combined (good)
RUN apt-get update && \
    apt-get install -y python3 pip && \
    rm -rf /var/lib/apt/lists/*
```

### ENV - environment variables
```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
ENV DATABASE_URL=postgresql://user:pass@db:5432/mydb
```

### EXPOSE - dokumentatsioon
```dockerfile
EXPOSE 8080
# Doesn't actually publish port - just documentation
```

### USER - security
```dockerfile
# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001

USER appuser
```

### CMD vs ENTRYPOINT
```dockerfile
# CMD - default command (can be overridden)
CMD ["python", "app.py"]

# ENTRYPOINT - always runs
ENTRYPOINT ["python", "app.py"]

# Combined usage
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]
```

## DEMO: Dockerfile loomine

### Lihtne Python app

**app.py:**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Docker!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**requirements.txt:**
```
Flask==2.3.3
```

### Algaja Dockerfile (kehv)
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python app.py
```

**Probleemid:**
-  Ei kasuta cache'i optimaalselt
-  Suur base image
-  Runs as root
-  No health check

### Optimeeritud Dockerfile (hea)
```dockerfile
FROM python:3.9-alpine

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001

WORKDIR /app

# Copy dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

EXPOSE 5000

CMD ["python", "app.py"]
```

### Build ja käivitamine
```bash
# Build image
docker build -t minu-python-app .

# Run container
docker run -d -p 5000:5000 --name python-app minu-python-app

# Test
curl http://localhost:5000

# View health status
docker ps  # shows health status
```

### Multi-stage build näide

```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runtime stage  
FROM nginx:alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Eelised:**
-  Väiksem final image (ainult runtime)
-  Turvalisem (no build tools)
-  Kiirem deployment

---

# BLOKK 4: Volumes, Networks ja Docker Compose

## Volumes - andmete säilitamine

### Probleem
```bash
docker run -d --name db postgres
docker exec db createdb myapp
docker stop db
docker rm db

#  Kõik andmed kadunud!
```

### Volume tüübid

#### 1. Anonymous volumes
```bash
docker run -d -v /var/lib/postgresql/data postgres
# Docker loob automaatselt volume'i
```

#### 2. Named volumes  
```bash
# Create volume
docker volume create postgres_data

# Use volume
docker run -d -v postgres_data:/var/lib/postgresql/data postgres

# List volumes
docker volume ls

# Inspect volume
docker volume inspect postgres_data
```

#### 3. Bind mounts
```bash
# Mount host directory
docker run -d -v /host/path:/container/path nginx

# Development example
docker run -d -v $(pwd):/app -p 3000:3000 node:16-alpine
```

#### 4. tmpfs mounts (memory)
```bash
docker run -d --tmpfs /tmp nginx
# Data stored in RAM, lost on container stop
```

### Volume'ide võrdlus

| Type | Performance | Portability | Use Case |
|------|-------------|-------------|----------|
| **Named Volume** | ⭐⭐⭐ | ⭐⭐⭐ | Production data |
| **Bind Mount** | ⭐⭐ | ⭐ | Development |  
| **tmpfs** | ⭐⭐⭐ | ⭐⭐⭐ | Temporary cache |

## Networks - konteinerite suhtlus

### Default behavior
```bash
# Containers can't communicate by default
docker run -d --name web nginx
docker run -d --name app python:3.9-alpine

docker exec app ping web  #  Fails!
```

### Custom networks
```bash
# Create network
docker network create myapp-network

# Run containers in same network
docker run -d --name web --network myapp-network nginx
docker run -d --name app --network myapp-network python:3.9-alpine

# Now they can communicate!
docker exec app ping web  #  Works!
docker exec app nslookup web  # DNS resolution
```

### Network types

#### 1. Bridge (default)
```bash
docker network create --driver bridge mybridge
# Isolated network with internet access
```

#### 2. Host  
```bash
docker run --network host nginx
# Uses host networking directly
```

#### 3. None
```bash
docker run --network none alpine
# No networking
```

### Port publishing vs network
```bash
# Port publishing (external access)
docker run -p 8080:80 nginx

# Internal communication (no ports needed)
docker network create app-net
docker run --network app-net --name web nginx
docker run --network app-net --name app alpine
# app can reach web:80 directly
```

## DEMO: Multi-container rakendus

### Architecture
```
Frontend (nginx) → Backend (Flask) → Database (PostgreSQL)
```

### Manual setup
```bash
# 1. Create network
docker network create webapp-net

# 2. Database
docker run -d \
  --name postgres \
  --network webapp-net \
  -e POSTGRES_DB=webapp \
  -e POSTGRES_USER=app \
  -e POSTGRES_PASSWORD=secret \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:13-alpine

# 3. Backend
docker run -d \
  --name backend \
  --network webapp-net \
  -e DATABASE_URL=postgresql://app:secret@postgres:5432/webapp \
  python:3.9-alpine

# 4. Frontend  
docker run -d \
  --name frontend \
  --network webapp-net \
  -p 80:80 \
  nginx:alpine
```

**Probleem:** Palju käske, keeruline hallata!

## Docker Compose

### Mis on Docker Compose?
- **Tool** mitme konteineri haldamiseks
- **YAML file** konfiguratsiooniks
- **Single command** kogu stack'i haldamiseks

### docker-compose.yml
```yaml
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: webapp
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  # Backend API
  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://app:secret@postgres:5432/webapp
    depends_on:
      - postgres
    networks:
      - backend
      - frontend

  # Frontend  
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
    networks:
      - frontend

# Define networks
networks:
  frontend:
  backend:

# Define volumes  
volumes:
  postgres_data:
```

### Compose käsud
```bash
# Start all services
docker-compose up -d

# View running services
docker-compose ps

# View logs
docker-compose logs
docker-compose logs backend

# Scale service
docker-compose up -d --scale backend=3

# Stop all
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Environment files
**.env:**
```bash
POSTGRES_PASSWORD=supersecret
DATABASE_URL=postgresql://app:${POSTGRES_PASSWORD}@postgres:5432/webapp
NODE_ENV=production
```

**docker-compose.yml:**
```yaml
services:
  postgres:
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

---

# BLOKK 5: Produktsiooni Parimad Praktikad

## Security Best Practices

### 1. Non-root user
```dockerfile
# BAD
USER root
CMD ["python", "app.py"]

# GOOD  
RUN adduser -D -s /bin/sh appuser
USER appuser
CMD ["python", "app.py"]
```

### 2. Minimal base images
```dockerfile
# BAD - 1GB
FROM ubuntu:latest

# GOOD - 50MB
FROM python:3.9-alpine

# BETTER - 15MB (multi-stage)
FROM python:3.9-alpine AS builder
# ... build steps
FROM alpine:latest
COPY --from=builder /app /app
```

### 3. No secrets in images
```dockerfile
# BAD
ENV API_KEY=secret123

# GOOD
ENV API_KEY_FILE=/run/secrets/api_key
```

### 4. Specific versions
```dockerfile
# BAD
FROM python:latest

# GOOD
FROM python:3.9.18-alpine3.18
```

### 5. Security Scanning (Trivy)

**Security scanning** leiab haavatavused (vulnerabilities) image'itest.

**Trivy** on populaarne, tasuta security scanner Docker image'itele:

```bash
# Installi Trivy
sudo apt install wget
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt update
sudo apt install trivy

# Skanni image
trivy image nginx:latest

# Näita ainult HIGH ja CRITICAL
trivy image --severity HIGH,CRITICAL python:3.9

# Skanni kohaliku Dockerfile
docker build -t myapp:test .
trivy image myapp:test
```

**Näide väljund:**
```
Total: 45 (HIGH: 8, CRITICAL: 2)

┌────────────┬──────────────┬──────────┬────────┬─────────────────┐
│  Library   │ Vulnerability│ Severity │ Status │    Title        │
├────────────┼──────────────┼──────────┼────────┼─────────────────┤
│ openssl    │ CVE-2023-123 │ CRITICAL │  fixed │ Buffer overflow │
│ curl       │ CVE-2023-456 │ HIGH     │  fixed │ Auth bypass     │
└────────────┴──────────────┴──────────┴────────┴─────────────────┘
```

**Mida teha tulemustega?**

1. **Update base image:**
   ```dockerfile
   FROM python:3.9.18-alpine3.18  # vanem versioon, haavatavused
   ↓
   FROM python:3.11.7-alpine3.19  # uuem, turvalisem
   ```

2. **Update dependencies:**
   ```dockerfile
   RUN pip install requests==2.28.0  # vanem, haavatav
   ↓
   RUN pip install requests==2.31.0  # uuem, parandatud
   ```

3. **Accept risk** (kui ei saa parandada):
   - Dokumenteeri, miks ei saa uuendada
   - Lisa `.trivyignore` fail

**CI/CD integration:**
```yaml
# GitLab CI
security_scan:
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity CRITICAL myapp:latest
  # Failib kui CRITICAL haavatavusi leitakse
```

**Hea tava:**
-  Skanni image'd enne production'i
-  Automaatne scanning CI/CD's
-  Blokeeri CRITICAL vulnerabilities
-  Fix regulaarselt (mitte ainult release'i ajal)

## Performance Optimization

### 1. Layer caching
```dockerfile
# BAD - cache miss on code change
COPY . /app
RUN pip install -r requirements.txt

# GOOD - dependencies cached
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
```

### 2. .dockerignore
```
# .dockerignore
node_modules/
.git/
*.log
.DS_Store
```

### 3. Multi-stage builds

Multi-stage build võimaldab:
- Ehitada rakendust ühes stage'is (build tools)
- Käivitada teises stage'is (ainult runtime)
- Väiksemad image'id (100MB+ → 10MB)

**Praktiline näide:**
 Vaata [labor.md - Samm 6: Multi-stage build](labor.md#-samm-6-multi-stage-build)

**Kontseptsioon:**
```dockerfile
FROM builder-image AS build  # 1. stage
# ... compile, build ...

FROM runtime-image           # 2. stage
COPY --from=build /app/dist  # Kopeeri ainult build result
```

## Monitoring ja Logging

### Health checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Structured logging
```python
import logging
import json

def json_log(message, level="info", **kwargs):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
        **kwargs
    }
    print(json.dumps(log_entry))
```

### Resource limits
```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          memory: 256M
```

## Production deployment patterns

### 1. Blue-Green deployment
```bash
# Current: myapp-blue (v1.0)
# Deploy: myapp-green (v2.0)

docker run -d --name myapp-green -p 8081:8080 myapp:v2.0

# Test v2.0 on port 8081
# Switch load balancer: 8080 → 8081  
# Remove blue: docker stop myapp-blue
```

### 2. Rolling updates
```yaml
# docker-compose.yml
services:
  app:
    image: myapp:v2.0
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
```

### 3. Configuration management
```yaml
# docker-compose.prod.yml
services:
  app:
    image: myapp:${VERSION}
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    secrets:
      - db_password
      - api_keys

secrets:
  db_password:
    external: true
  api_keys:
    external: true
```

## Container orchestration tutvustus

### Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml myapp

# Scale service  
docker service scale myapp_web=5
```

### Kubernetes alternative
```bash
# Generate Kubernetes YAML from Compose
kompose convert docker-compose.yml

# Or use Podman
podman generate kube mycontainer > pod.yaml
kubectl apply -f pod.yaml
```

## Kokkuvõte

### Mis me õppisime?

1. **Docker basics:** Images, containers, registry
2. **Dockerfile:** Optimized image building
3. **Storage:** Volumes for data persistence
4. **Networking:** Container communication
5. **Compose:** Multi-container applications
6. **Production:** Security, performance, deployment

### Järgmised sammud

1. **Praktiline projekt:** Tee 3-tier web app
2. **CI/CD integratsioon:** GitHub Actions + Docker
3. **Orchestration:** Kubernetes või Docker Swarm
4. **Monitoring:** Prometheus + Grafana + logs

---

##  Kokkuvõte ja Refleksioon

### Põhiline töövoog

```bash
# Iga päev:
docker pull image-nimi          # võta uusim image
docker run -d -p 8080:80 image  # käivita container
docker ps                       # vaata, mis töötab
docker logs container-nimi      # debugi
docker stop container-nimi      # peata

# Arendus:
# 1. Kirjuta Dockerfile
# 2. docker build -t minu-app .
# 3. docker run minu-app
# 4. Testi ja paranda
# 5. Korda 2-4
```

###  Refleksioonküsimused (mõtle läbi)

1. **Kuidas Docker lahendab "Works on My Machine" probleemi?**
2. **Millal kasutada volume'e ja millal mitte?**
3. **Miks on cache oluline Dockerfile build'imisel?**
4. **Kuidas container erineb VM'ist? Mis on peamised eelised?**
5. **Mida MITTE panna Dockerfile'i või image'isse?** (paroolid, logid, cache)

###  Järgmised sammud

- **Labor:** Harjuta kõiki neid käske praktikas!
- **Kodutöö:** Loo oma rakendus Docker container'is
- **Edasijõudnud:** Docker Compose, Docker Swarm, Kubernetes

###  Ressursid ja lugemine

- **Docker dokumentatsioon:** https://docs.docker.com/
- **Docker Hub:** https://hub.docker.com/
- **Best practices guide:** https://docs.docker.com/develop/dev-best-practices/
- **Play with Docker** (brauseris): https://labs.play-with-docker.com/
- **Docker Cheat Sheet:** https://docs.docker.com/get-started/docker_cheatsheet.pdf

---

**Küsimus enne lab'i alustamist:** Kui Docker oleks superjõud, siis milline see oleks ja miks? ‍

---

*"Container technology is not the future - it's the present of software development!"* 
