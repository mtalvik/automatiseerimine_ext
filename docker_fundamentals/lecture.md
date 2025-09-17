# 🐳 Docker Meisterlikkus: Nullist Tootmiseni
*Kaasaegne konteinerite tehnoloogia arendajatele*

---

## 📋 Course Overview

```mermaid
graph TD
    A[Why Containers?] --> B[Docker Installation & CLI]
    B --> C[Dockerfile Mastery]
    C --> D[Networking & Volumes]
    D --> E[Production Best Practices]
    E --> F[Podman Alternative]
    F --> G[Real-World Projects]
```

**Kestus:** 75 minutit | **Tase:** Keskmine | **Eeltingimused:** Linuxi põhialused

---

# Osa 1: Konteinerite Revolutsioon (10 min)
## Miks Docker vallutas maailma

### 1 Miljardi Dollari Probleem

**2010 scenario:** Netflix wants to deploy to 1000 servers
- Each server: Different OS versions, libraries, configurations  
- Result: "Works on my machine" syndrome
- Cost: Months of debugging, failed deployments

**2015 with Docker:** Same deployment
- Package once → Deploy everywhere
- Result: 99.9% consistency across environments
- Netflix saves millions in deployment time

### Evolution Timeline

```mermaid
timeline
    title Container Technology Evolution
    1979 : Unix chroot
         : Process isolation
    2000 : FreeBSD Jails
         : First "containers"
    2006 : Linux Containers (LXC)
         : Full OS virtualization
    2013 : Docker Release
         : Developer-friendly containers
    2014 : Kubernetes
         : Container orchestration
    2020 : 83% enterprises use containers
         : Industry standard
```

### Performance Comparison: VMs vs Containers

| Metric | Virtual Machines | Containers | Winner |
|--------|------------------|------------|--------|
| **Startup Time** | 30-120 seconds | 1-5 seconds | 🐳 24x faster |
| **Memory Overhead** | 1-8GB per VM | 10-100MB per container | 🐳 80x less |
| **Density** | 10-50 per server | 100-1000 per server | 🐳 20x more |
| **File Size** | 10-50GB | 100MB-1GB | 🐳 50x smaller |

### Real-World Impact

**Spotify case study:**
- Before Docker: 6-hour deployment cycles
- After Docker: 30-minute deployments
- Result: 12x faster iteration, $2M saved annually

**Airbnb case study:**
- Before: 1000+ AWS instances
- After: 500 instances with containers
- Result: 50% infrastructure cost reduction

---

# Part 2: Docker Fundamentaalid (15 min)
## Installation & Põhikäsud

### Installation Matrix

```bash
# Ubuntu/Debian (Production Ready)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version && docker run hello-world
```

**📚 Official Installation Guide:** https://docs.docker.com/engine/install/

### Architecture Deep Dive

```mermaid
graph TB
    subgraph "Docker Host"
        Client[Docker CLI]
        Daemon[Docker Daemon<br/>dockerd]
        Images[Images Storage]
        Containers[Running Containers]
        Registry[Local Registry Cache]
    end
    
    subgraph "External"
        Hub[Docker Hub<br/>registry.hub.docker.com]
        Private[Private Registry<br/>harbor/nexus]
    end
    
    Client -->|API calls| Daemon
    Daemon --> Images
    Daemon --> Containers
    Daemon <-->|Pull/Push| Hub
    Daemon <-->|Pull/Push| Private
```

### Kus Hoitakse Docker Image'sid? (Registry Deep Dive)

#### Registry vs Repository - Mis vahe?

```mermaid
graph TB
    subgraph "Registry (Pood)"
        subgraph "Docker Hub"
            A[nginx repository]
            B[mysql repository] 
            C[python repository]
        end
        
        subgraph "Private Registry"
            D[company/api repository]
            E[company/frontend repository]
        end
    end
    
    subgraph "Repository (Riiulid)"
        subgraph "nginx repository"
            F[nginx:latest]
            G[nginx:1.21]
            H[nginx:alpine]
        end
    end
```

**Registry** = Terve pood (Docker Hub, Nexus, Harbor)  
**Repository** = Üks toote riiuli (nginx, mysql, sinu-app)  
**Tag** = Konkreetne versioon (latest, v1.0, alpine)

#### 1. Docker Hub - Avalik Registry
```bash
# Avalikud image'id - TASUTA
docker pull nginx                    # docker.io/library/nginx:latest
docker pull ubuntu:20.04            # docker.io/library/ubuntu:20.04

# Kasutajate image'id  
docker pull username/myapp:latest    # docker.io/username/myapp:latest

# Organisatsioonide image'id
docker pull bitnami/postgresql       # docker.io/bitnami/postgresql:latest
```

**Miks Docker Hub populaarne?**
- ✅ 13+ miljardit allalaadimist kuus
- ✅ Automaatne build GitHub'ist
- ✅ Turvalisuse skannimine
- ✅ Tasuta avalikud repositooriumid

#### 2. Nexus Repository - Ettevõtte Registry
```bash
# Nexus server
docker pull nexus.company.com/myteam/api:v1.2.3

# Login vajalik
docker login nexus.company.com
Username: john.doe
Password: ****

# Edasi saad kasutada
docker pull nexus.company.com/private/secret-app:latest
```

**Miks Nexus?**
- 🔒 Privaatsed image'id (ei näe kõik)
- 🏢 Ettevõtte kontroll
- 📊 Kasutusstatistika  
- 🔧 LDAP/Active Directory integratsioon

#### 3. Harbor - Cloud Native Registry
```bash
# Harbor registry
docker pull harbor.k8s.company.com/production/frontend:v2.1.0

# Projektide kaupa organiseeritud
docker pull harbor.k8s.company.com/development/api:latest
docker pull harbor.k8s.company.com/staging/api:v1.5.0-rc1
```

**Miks Harbor?**
- 🚢 Kubernetes native
- 🔐 Role-based access control
- 🛡️ Turvalisuse skannimine
- 📝 Audit logging

### Versioonihaldus ja Git Integratsioon

**Probleem:** Kuidas hoida image'id sünkroonis koodiga?

```mermaid
graph LR
    A[Git Commit] --> B[CI/CD Pipeline]
    B --> C[Docker Build]
    C --> D[Image Tag = Git SHA]
    D --> E[Push Registry'sse]
    
    F[git commit abc123] --> G[docker build myapp:abc123]
    G --> H[docker push myapp:abc123]
```

**GitHub Actions näide:**
```yaml
name: Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build image
        run: |
          SHA=$(git rev-parse --short HEAD)
          docker build -t company/myapp:$SHA .
          docker build -t company/myapp:latest .
          
      - name: Push registry'sse
        run: |
          docker push company/myapp:$SHA
          docker push company/myapp:latest
```

**Tulemus:**
```bash
git log --oneline
abc123f Fix login bug        → myapp:abc123f
def456a Add user profile     → myapp:def456a  
789xyz1 Update dependencies  → myapp:789xyz1
```

### Registry Cleanup ja Lifecycle

**Probleem:** Registry täitub vanarde image'idega!

```bash
# Registry'is võib olla:
myapp:v1.0.0    # 500MB
myapp:v1.0.1    # 500MB  
myapp:v1.0.2    # 500MB
# ... 100 versiooni = 50GB!
```

**Harbor cleanup policy:**
```yaml
# Säilita ainult:
- Viimased 10 tagi per repository
- Tag'id uuemad kui 30 päeva  
- Production tag'id: v\d+\.\d+\.\d+
```

### Registry Võrdlus

| Registry | Kasutamine | Hind | Security |
|----------|------------|------|----------|
| **Docker Hub** | Avalikud projektid | Tasuta/tasulised | Avalik + privaatsed |
| **Nexus** | Ettevõtte sisene | Tasuta (self-hosted) | LDAP, RBAC |
| **Harbor** | Cloud-native | Tasuta (self-hosted) | Kubernetes RBAC |
| **AWS ECR** | AWS keskkond | $0.10/GB/kuu | IAM integration |

**Golden Rules:**
1. **Avalikud image'id** → Docker Hub
2. **Ettevõtte rakendused** → Nexus/Harbor  
3. **Git SHA = Image tag** (jälgitavus)
4. **Cleanup policy** (ruumi kokkuhoid)
5. **Security scanning** (turvalisus)

### Essential Commands Mastery

#### Image Operations
```bash
# Search and discover
docker search nginx --limit 5 --filter stars=100
docker search python --filter is-official=true

# Pull strategies  
docker pull nginx:alpine          # Small & secure
docker pull nginx:1.21.6          # Production pinning
docker pull nginx:1.21.6@sha256:... # Immutable digest

# Image inspection
docker image inspect nginx:alpine | jq '.Config.Env'
docker image history nginx:alpine  # Layer analysis
```

#### Container Lifecycle Management
```bash
# Advanced run options
docker run -d \
  --name production-web \
  --restart unless-stopped \
  --memory="512m" \
  --cpus="1.5" \
  --health-cmd="curl -f http://localhost || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  -p 80:80 \
  nginx:alpine

# Container introspection
docker stats production-web        # Live resource monitoring
docker top production-web          # Process tree
docker exec -it production-web sh  # Interactive debugging
```

#### Production Debugging
```bash
# Log analysis
docker logs --since=2h --tail=100 production-web
docker logs --follow --timestamps production-web

# Resource monitoring
docker system df                   # Disk usage breakdown
docker system events               # Real-time system events
```

### Docker Hub Mastery

**🌐 Docker Hub:** https://hub.docker.com

**Top Official Images to Know:**
- `alpine` (5MB) - Minimal Linux base
- `nginx` - Web server
- `postgres` - SQL database  
- `redis` - In-memory cache
- `node:alpine` - JavaScript runtime
- `python:slim` - Python runtime

**Security tip:** Always verify official images have the "Docker Official Image" badge

### 🚀 LIVE DEMO: Suur vs Väike Image (8 min)

**Challenge:** Kes teeb väiksema Docker image'i?

```bash
# Vaata milline on suurim image sinu arvutis
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | sort -k3 -h

# Pull mõned näited
docker pull python:3.9          # Ennusta: kui suur?
docker pull python:3.9-alpine   # Ennusta: kui suur?

# Tulemused:
# python:3.9        900MB  😱 (Ubuntu base)
# python:3.9-alpine  45MB  🎉 (Alpine base)
# Erinevus: 20x väiksem!
```

**Speed test:**
```bash
# Kumb laeb kiiremini?
time docker pull redis           # ~32MB
time docker pull ubuntu:20.04   # ~700MB

# Network impact:
# 10 serverit × 700MB = 7GB traffic
# 10 serverit × 32MB = 320MB traffic
```

### 🏗️ BUILD VÕISTLUS (7 min)

**Ülesanne:** Sama Flask app, kaks lähenemist

**app.py** (kopeeri kiiresti):
```python
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return '<h1>Docker Size Contest!</h1>'
app.run(host='0.0.0.0', port=5000)
```

**Meeskond 1 - "Big Boy" approach:**
```dockerfile
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install flask
COPY app.py .
CMD ["python3", "app.py"]
```

**Meeskond 2 - "Ninja" approach:**
```dockerfile
FROM python:3.9-alpine
RUN pip install flask
COPY app.py .
CMD ["python", "app.py"]
```

**Võistlus:**
```bash
# Build race!
docker build -t bigboy . &
docker build -t ninja . &

# Kes võitis?
docker images | grep -E "(bigboy|ninja)"
# bigboy    1.1GB  😭
# ninja     60MB   🏆

# Speed test
time docker run -p 5000:5000 ninja
# Result: Same app, 18x smaller!
```

### ⚡ Alpine Magic Explained

**Miks Alpine nii väike?**
- Ubuntu: Täispikk desktop OS (700MB)
- Alpine: Ainult vajalik (5MB base)
- Sama tulemused, vähem jama

**Real-world impact:**
- Netflix: 1000 serverit × 700MB = 700GB vs 50GB
- Deployment: 10 min → 30 sek
- AWS bill: $1000/month → $100/month

---

# Part 3: Dockerfile Meisterlikkus (20 min)
## Algajast Ekspertiks

### The Dockerfile Hierarchy

```mermaid
graph TD
    A[FROM: Base Image] --> B[WORKDIR: Set Directory]
    B --> C[COPY: Dependencies First]
    C --> D[RUN: Install Dependencies]
    D --> E[COPY: Application Code]
    E --> F[USER: Security]
    F --> G[EXPOSE: Documentation]
    G --> H[CMD/ENTRYPOINT: Startup]
```

### Best Practice Evolution

#### Beginner Dockerfile (⚠️ Problems)
```dockerfile
FROM ubuntu:latest                    # ❌ Latest is unpredictable
RUN apt-get update                    # ❌ Separate layers
RUN apt-get install -y python3       # ❌ Cache invalidation
RUN apt-get install -y pip           # ❌ Security issues
COPY . /app                          # ❌ Dependencies rebuild every time
WORKDIR /app
RUN pip install -r requirements.txt  # ❌ Cache miss on code change
CMD python app.py                    # ❌ Runs as root
```

#### Expert Dockerfile (✅ Optimized)
```dockerfile
# Multi-stage build for size optimization
FROM python:3.11-slim as builder
WORKDIR /app

# Install dependencies in separate layer (cache optimization)
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app

# Security: Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy only what's needed from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

# Security: Switch to non-root
USER appuser

# Add /home/appuser/.local/bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Health check for monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Documentation
EXPOSE 8000

# Startup
CMD ["python", "app.py"]
```

### Advanced Patterns

#### Pattern 1: Multi-Stage for Different Environments
```dockerfile
# Development stage
FROM node:16-alpine as development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

# Testing stage  
FROM development as testing
RUN npm run test
RUN npm run lint

# Production build stage
FROM node:16-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production runtime
FROM nginx:alpine as production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Pattern 2: Extreme Size Optimization
```dockerfile
# Build stage
FROM golang:1.19-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Runtime stage - FROM SCRATCH!
FROM scratch
COPY --from=builder /app/main /main
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 8080
USER 65534:65534
ENTRYPOINT ["/main"]

# Result: 15MB final image! (vs 800MB with full Go image)
```

### Security Hardening

```dockerfile
FROM node:16-alpine

# Security: Update packages & remove package manager
RUN apk update && apk upgrade && \
    apk add --no-cache dumb-init && \
    rm -rf /var/cache/apk/*

# Security: Non-root user with specific UID
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Security: Specific ownership
COPY --chown=nodejs:nodejs package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY --chown=nodejs:nodejs . .

# Security: Switch user
USER nodejs

# Security: Signal handling
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
```

### Dockerfile Linting & Security

```bash
# Install Hadolint (Dockerfile linter)
docker run --rm -i hadolint/hadolint < Dockerfile

# Install Trivy (security scanner)
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image nginx:alpine

# Build with security scan
docker build -t myapp . && \
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image myapp
```

**📚 Security Resources:**
- Docker Security Best Practices: https://docs.docker.com/develop/security-best-practices/
- OWASP Container Security: https://owasp.org/www-project-container-security/

---

# Part 4: Networking & Storage (15 min)
## Konteinerite Suhtlus ja Andmete Säilitamine

### Network Architecture Deep Dive

```mermaid
graph TB
    subgraph "Host Network Stack"
        subgraph "Custom Networks"
            FrontEnd[frontend<br/>172.20.0.0/16]
            BackEnd[backend<br/>172.21.0.0/16]
            Database[database<br/>172.22.0.0/16]
        end
        
        subgraph "Default Bridge"
            Bridge[bridge<br/>172.17.0.0/16]
        end
        
        subgraph "Host Network"
            Host[host<br/>Use host networking]
        end
    end
    
    Internet[Internet] --> HostPort[Host:80]
    HostPort --> FrontEnd
    FrontEnd -.-> BackEnd
    BackEnd -.-> Database
```

### Networking Strategies

#### Strategy 1: 3-Tier Architecture
```bash
# Create isolated networks
docker network create --driver bridge \
  --subnet=172.20.0.0/16 \
  --ip-range=172.20.240.0/20 \
  frontend

docker network create --driver bridge \
  --subnet=172.21.0.0/16 \
  --internal \
  backend

# Web tier (internet-facing)
docker run -d --name nginx \
  --network frontend \
  -p 80:80 \
  nginx:alpine

# API tier (bridge networks)
docker run -d --name api \
  --network backend \
  python:3.9-alpine
docker network connect frontend api

# Database tier (internal only)
docker run -d --name postgres \
  --network backend \
  -e POSTGRES_PASSWORD=secret \
  postgres:13-alpine
```

#### Strategy 2: Service Discovery
```bash
# DNS resolution in custom networks
docker exec nginx ping api          # ✅ Works by hostname
docker exec api ping postgres       # ✅ Internal communication

# Service discovery with aliases
docker run -d --name cache \
  --network backend \
  --network-alias redis-master \
  redis:alpine

docker exec api ping redis-master   # ✅ Works via alias
```

### Volume Strategies for Production

```mermaid
graph LR
    subgraph "Volume Types"
        A[Named Volumes<br/>Managed by Docker]
        B[Bind Mounts<br/>Host filesystem]
        C[tmpfs Mounts<br/>Memory only]
    end
    
    subgraph "Use Cases"
        D[Database Storage]
        E[Development Code]
        F[Temporary Cache]
    end
    
    A --> D
    B --> E
    C --> F
```

#### Production Database with Backup Strategy
```bash
# Named volume for production
docker volume create --driver local \
  --opt type=ext4 \
  --opt device=/dev/sdb1 \
  postgres_data

# PostgreSQL with optimized settings
docker run -d --name postgres-prod \
  --restart unless-stopped \
  -v postgres_data:/var/lib/postgresql/data \
  -v $(pwd)/postgres.conf:/etc/postgresql/postgresql.conf:ro \
  -e POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password \
  -e POSTGRES_DB=production \
  --memory=2g \
  --cpus=2 \
  postgres:13-alpine \
  -c config_file=/etc/postgresql/postgresql.conf

# Backup strategy
docker run --rm \
  -v postgres_data:/data:ro \
  -v $(pwd)/backups:/backup \
  alpine:latest \
  tar czf /backup/postgres_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

#### Development with Live Reload
```bash
# Bind mount for development
docker run -d --name dev-env \
  -v $(pwd):/workspace \
  -v /workspace/node_modules \
  -w /workspace \
  -p 3000:3000 \
  node:16-alpine \
  npm run dev

# Anonymous volume for node_modules prevents host override
```

### Monitoring & Observability

```bash
# Real-time container monitoring
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Network traffic analysis
docker exec nginx ss -tulpn
docker exec api netstat -i

# Volume usage monitoring
docker system df -v
docker volume ls --filter dangling=true
```

**📊 Monitoring Tools:**
- cAdvisor: https://github.com/google/cadvisor
- Portainer: https://www.portainer.io/
- Docker Desktop: Built-in dashboard

---

# Part 5: Podman - The Daemonless Future (10 min)
## Docker's Rootless Alternative

### Why Podman Matters

**The Daemon Problem:**
```bash
# Docker security model
$ docker run -v /:/host -it alpine chroot /host bash
root@container:/# rm -rf /usr/bin/*  # 😱 Can destroy host!
```

**Podman's Solution:**
```bash
# Rootless by design
$ podman run -v /:/host -it alpine chroot /host bash
Error: cannot mount /: permission denied  # ✅ Protected!
```

### Architecture Comparison

```mermaid
graph TB
    subgraph "Docker Architecture"
        DC[Docker CLI] --> DD[Docker Daemon<br/>Always running as root]
        DD --> DCont[Containers]
    end
    
    subgraph "Podman Architecture"  
        PC[Podman CLI] --> PCont[Containers<br/>Direct execution]
    end
    
    subgraph "Security Model"
        DR[Docker: Root required]
        PR[Podman: User namespaces]
    end
```

### Podman Unique Features

#### 1. Kubernetes Integration
```bash
# Generate Kubernetes YAML
podman run -d --name web nginx:alpine
podman generate kube web > pod.yaml

# pod.yaml is ready for kubectl!
kubectl apply -f pod.yaml

# Or run locally with Podman
podman play kube pod.yaml
```

#### 2. Pod Management (Like Kubernetes)
```bash
# Create pod with shared resources
podman pod create --name webapp --publish 8080:80

# Add containers to pod
podman run -d --pod webapp --name frontend nginx:alpine
podman run -d --pod webapp --name backend python:3.9-alpine

# Containers in pod share:
# - Network (localhost communication)
# - Storage volumes
# - Process namespace
```

#### 3. Systemd Integration (No Docker Daemon!)
```bash
# Generate systemd service
podman run -d --name myapp nginx:alpine
podman generate systemd --new --files --name myapp

# Install as user service (no sudo!)
mkdir -p ~/.config/systemd/user
cp container-myapp.service ~/.config/systemd/user/
systemctl --user enable container-myapp.service
systemctl --user start container-myapp.service

# Auto-start on boot (no Docker daemon needed!)
loginctl enable-linger $USER
```

### Migration Strategy

```bash
# 1. Install Podman alongside Docker
sudo apt install podman podman-compose

# 2. Create alias for gradual migration
echo "alias docker=podman" >> ~/.bashrc

# 3. Test existing workflows
docker run hello-world  # Actually runs: podman run hello-world

# 4. Migrate docker-compose projects
podman-compose up -d    # Drop-in replacement!
```

### Performance Comparison

| Feature | Docker | Podman | Winner |
|---------|---------|---------|---------|
| **Memory Usage** | ~50-100MB daemon | 0MB daemon | 🟢 Podman |
| **Startup Time** | 2-3 seconds | 1-2 seconds | 🟢 Podman |
| **Security** | Root daemon | User namespaces | 🟢 Podman |
| **Ecosystem** | Massive | Growing | 🔴 Docker |

**📚 Podman Resources:**
- Official Documentation: https://docs.podman.io/
- Migration Guide: https://podman.io/getting-started/

---

# Part 6: Production Näited (10 min)
## Töötavad Projektid

### Kiire Stack Demo

**3-tier arhitektuur:**
```bash
# Frontend
docker run -d --name web -p 80:80 nginx:alpine

# Backend API  
docker run -d --name api python:3.9-alpine

# Database
docker run -d --name db -e POSTGRES_PASSWORD=secret postgres:alpine

# Network them together
docker network create myapp
docker network connect myapp web
docker network connect myapp api  
docker network connect myapp db
```

### Production Tips

1. **Always use specific tags:** `nginx:1.21-alpine` not `nginx:latest`
2. **Health checks:** `HEALTHCHECK --interval=30s CMD curl -f http://localhost`
3. **Non-root users:** `USER 1001:1001`
4. **Multi-stage builds:** Build stage + Runtime stage
5. **Secret management:** Environment variables, not hardcoded

### Monitoring Stack
```bash
# Quick monitoring setup
docker run -d -p 9090:9090 prom/prometheus     # Metrics
docker run -d -p 3000:3000 grafana/grafana     # Dashboards
docker run -d -p 8080:8080 gcr.io/cadvisor/cadvisor  # Container stats
```

---

### Project 1: High-Performance Web Stack

**Architecture:**
```
Internet → CloudFlare → nginx → Node.js API → Redis → PostgreSQL
```

**docker-compose.production.yml:**
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - static_files:/usr/share/nginx/html/static
    depends_on:
      - api
    restart: unless-stopped
    
  api:
    build: 
      context: ./api
      target: production
    environment:
      - NODE_ENV=production
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://api:${DB_PASSWORD}@postgres:5432/production
    volumes:
      - static_files:/app/public
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      
  postgres:
    image: postgres:13-alpine
    environment:
      - POSTGRES_DB=production
      - POSTGRES_USER=api
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres.conf:/etc/postgresql/postgresql.conf
    restart: unless-stopped
    
  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    
volumes:
  postgres_data:
  redis_data:
  static_files:
```

### Project 2: Microservices with Service Mesh

```mermaid
graph TB
    subgraph "External"
        Users[Users] --> LB[Load Balancer]
    end
    
    subgraph "Frontend Network"
        LB --> Web[Web UI]
        LB --> API[API Gateway]
    end
    
    subgraph "Backend Network"
        API --> Auth[Auth Service]
        API --> User[User Service] 
        API --> Order[Order Service]
        API --> Payment[Payment Service]
    end
    
    subgraph "Data Network"
        Auth --> AuthDB[(Auth DB)]
        User --> UserDB[(User DB)]
        Order --> OrderDB[(Order DB)]
        Payment --> PaymentDB[(Payment DB)]
    end
```

### Project 3: CI/CD Pipeline Integration

**Dockerfile.multistage:**
```dockerfile
# Development stage
FROM node:16-alpine as development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Testing stage
FROM development as testing  
RUN npm run test:coverage
RUN npm run lint
RUN npm audit

# Security scan stage
FROM testing as security
RUN npm audit --audit-level high

# Production build
FROM node:16-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runtime optimized
FROM nginx:alpine as production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.prod.conf /etc/nginx/nginx.conf
HEALTHCHECK --interval=30s CMD curl -f http://localhost || exit 1
EXPOSE 80
```

**GitHub Actions Integration:**
```yaml
name: Docker Build & Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          docker build --target testing .
          
  security:
    runs-on: ubuntu-latest  
    steps:
      - uses: actions/checkout@v3
      - name: Security scan
        run: |
          docker build -t myapp .
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
            aquasec/trivy image myapp
            
  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker push registry.company.com/myapp:${{ github.sha }}
```

### Production Monitoring Stack

```yaml
version: '3.8'

services:
  # Application monitoring
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      
  # Log aggregation  
  loki:
    image: grafana/loki
    ports:
      - "3100:3100"
      
  # Container metrics
  cadvisor:
    image: gcr.io/cadvisor/cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
```

---

## 📚 Advanced Resources

### Essential Reading
- **Docker Best Practices:** https://docs.docker.com/develop/dev-best-practices/
- **Container Security Guide:** https://kubernetes.io/docs/concepts/security/
- **Production Patterns:** https://12factor.net/

### Tools & Extensions
- **Docker Desktop:** https://www.docker.com/products/docker-desktop/
- **Portainer:** https://www.portainer.io/
- **Hadolint:** https://github.com/hadolint/hadolint
- **Trivy Security Scanner:** https://github.com/aquasecurity/trivy

### Community
- **Docker Community Forum:** https://forums.docker.com/
- **Reddit r/docker:** https://reddit.com/r/docker
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/docker
---

*"Docker is not just a tool, it's a paradigm shift that enables modern software delivery at scale."*
