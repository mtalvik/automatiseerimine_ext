# Docker Lisapraktika

**Eesmärk:** Süvendada Docker oskusi täiendavate praktiliste ülesannetega  
**Eeltingimused:** Docker põhiteadmised, Docker Hub konto

---

##  Ülevaade

See fail sisaldab lisapraktikaid ja boonusülesandeid Docker mooduli jaoks, sealhulgas multi-stage builds, Docker networking, ja advanced optimization techniques.

---

## Õpiväljundid

Pärast lisapraktikat oskate:

- Multi-stage Dockerfile'ide kirjutamine
- Docker networking'u süvitsi mõistmine
- Image'ide optimeerimist (size, layers, cache)
- Docker Compose advanced features
- Container security best practices

---

##  Multi-Stage Builds

### Praktiline Näide: Node.js Rakendus

**Probleem:** Build dependencies suurendavad image'i üle 1GB

**Lahendus:** Multi-stage build

```dockerfile
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Tulemus:** Image väheneb 1.2GB → 150MB!

### Ülesanne 1: Python Flask Multi-Stage

Loo multi-stage Dockerfile Python Flask app'ile:
- Stage 1: Install dependencies ja compile
- Stage 2: Ainult runtime + compiled files
- Eesmärk: <100MB final image

---

## Docker Networking Süvitsi

### Custom Networks

```bash
# Loo bridge network
docker network create --driver bridge my-network

# Loo subnet'iga
docker network create \
  --driver bridge \
  --subnet 172.20.0.0/16 \
  --gateway 172.20.0.1 \
  app-network

# Vaata detaile
docker network inspect app-network
```

### Container-to-Container Communication

```bash
# Network'is containers näevad teineteist DNS'i kaudu
docker run -d --name db --network app-network postgres
docker run -d --name api --network app-network \
  -e DB_HOST=db \
  my-api:latest

# API saab ühenduda: postgresql://db:5432
```

### Ülesanne 2: 3-Tier Network Setup

Loo 3 network'i:
- `frontend-net` (nginx ↔ api)
- `backend-net` (api ↔ db)
- `api` on mõlemas network'is (bridge)

---

##  Image Optimization

### Tehnikad

**1. Use .dockerignore**
```
node_modules/
.git/
*.log
.env
README.md
.vscode/
```

**2. Combine RUN commands**
```dockerfile
# Halb (3 layer'it)
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Hea (1 layer)
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

**3. Order matters (cache)**
```dockerfile
# Dependencies enne koodi (cache friendly)
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
```

**4. Use slim/alpine images**
```dockerfile
FROM python:3.11-slim  # 50MB vs python:3.11 (900MB)
```

### Ülesanne 3: Optimize Bloated Image

Antud image on 800MB. Optimeeri alla 100MB:
```dockerfile
FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip git curl wget vim
COPY . /app
WORKDIR /app
RUN pip3 install flask requests beautifulsoup4
CMD ["python3", "app.py"]
```

---

##  Docker Compose Advanced

### Health Checks

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    image: my-api:latest
    depends_on:
      db:
        condition: service_healthy  # Ootab kuni db healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Profiles (Different Environments)

```yaml
services:
  app:
    image: my-app:latest
    
  debug:
    image: my-app:debug
    profiles: ["debug"]  # Ainult kui: docker-compose --profile debug up
    
  test-db:
    image: postgres:15-alpine
    profiles: ["testing"]
```

### Ülesanne 4: Production-Ready Compose

Loo `docker-compose.yml` koos:
- Health checks kõigile services'tele
- Resource limits (CPU, memory)
- Restart policies
- Logging configuration
- Profiles (dev, prod)

---

##  Container Security

### 1. Non-Root User

```dockerfile
FROM python:3.11-slim

# Loo kasutaja
RUN useradd -m -u 1000 appuser

WORKDIR /app
COPY --chown=appuser:appuser . .

# Vaheta kasutajale
USER appuser

CMD ["python", "app.py"]
```

### 2. Read-Only Filesystem

```bash
docker run --read-only \
  --tmpfs /tmp:rw,noexec,nosuid \
  my-app:latest
```

### 3. Security Scanning

```bash
# Scan image vulnerabilities
docker scan my-app:latest

# Trivy scanner (better)
trivy image my-app:latest
```

### Ülesanne 5: Secure Your Container

Võta olemasolev Dockerfile ja:
- [ ] Lisa non-root user
- [ ] Eemalda SHELL access (`rm /bin/sh`)
- [ ] Kasuta read-only filesystem
- [ ] Scan vulnerabilities ja paranda

---

##  Advanced Scenarios

### Scenario 1: Zero-Downtime Deployment

**Blue-Green Deployment with Docker:**

```bash
# Blue (current)
docker run -d --name app-blue -p 8080:80 my-app:v1

# Green (new)
docker run -d --name app-green -p 8081:80 my-app:v2

# Test green
curl http://localhost:8081/health

# Switch traffic (update load balancer or port mapping)
docker stop app-blue
docker rm app-blue
docker rename app-green app-blue
docker port app-blue  # Update to port 8080
```

### Scenario 2: Multi-Architecture Build

```bash
# Build for ARM ja AMD64
docker buildx create --use
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t my-app:multiarch \
  --push .
```

### Scenario 3: Docker-in-Docker (CI/CD)

```yaml
# .github/workflows/docker.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t my-app:${{ github.sha }} .
      - name: Test in container
        run: docker run my-app:${{ github.sha }} npm test
```

---

## Monitoring ja Logging

### Container Stats

```bash
# Real-time stats
docker stats

# Specific container
docker stats my-app

# Export metrics
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Centralized Logging

```yaml
version: '3.8'

services:
  app:
    image: my-app:latest
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
  
# Või kasuta syslog
  api:
    image: my-api:latest
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://192.168.1.100:514"
```

---

##  Challenge: Fullstack Production Setup

**Ülesanne:** Loo production-ready fullstack app Docker'iga

**Nõuded:**
- [ ] Frontend (React/Vue) - multi-stage build, nginx
- [ ] Backend (Node/Python) - non-root, health checks
- [ ] Database (PostgreSQL) - volumes, backups
- [ ] Redis cache
- [ ] Nginx reverse proxy SSL'iga
- [ ] Docker Compose orchestration
- [ ] Monitoring (Prometheus + Grafana)
- [ ] Logging (ELK stack või Loki)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Security hardened (scanning, non-root, secrets)

---

## Kasulikud Ressursid

- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **Dockerfile Reference**: https://docs.docker.com/engine/reference/builder/
- **Multi-stage builds**: https://docs.docker.com/build/building/multi-stage/
- **Security**: https://docs.docker.com/engine/security/
- **Compose Spec**: https://compose-spec.io/

---

**Edu advanced Docker'iga!** 

