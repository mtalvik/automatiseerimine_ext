# Docker Lisapraktika

**Eeldused:** Loeng ja labor läbitud, Docker Hub konto

See fail sisaldab lisaharjutusi ja edasijõudnud teemasid Docker mooduli jaoks. Materjal on valikuline ja mõeldud neile, kes soovivad süvendada oma oskusi.

---

## 1. Multi-Stage Builds Optimeerimiseks

### 1.1 Probleem

Build dependencies suurendavad image'i mahtu. Node.js rakenduse image võib olla 1.2GB, kuigi runtime vajab ainult 150MB.

### 1.2 Lahendus: Multi-Stage Build
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runtime stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

Image väheneb 1.2GB → 150MB.

### 1.3 Harjutus: Python Flask Multi-Stage

Looge multi-stage Dockerfile Python Flask rakendusele:

**Nõuded:**
- Stage 1: Install dependencies ja compile
- Stage 2: Ainult runtime + compiled files
- Eesmärk: alla 100MB final image

**Näpunäiteid:**
- Kasutage `python:3.11` builder'is
- Kasutage `python:3.11-alpine` runtime'is
- Kompileerige `.pyc` failid: `python -m compileall`
- Kopeerige ainult vajalikud failid

---

## 2. Docker Networking Süvitsi

### 2.1 Custom Networks
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

### 2.2 Container-to-Container DNS

Network'is container'id näevad teineteist DNS'i kaudu:
```bash
docker run -d --name db --network app-network postgres
docker run -d --name api --network app-network \
  -e DB_HOST=db \
  my-api:latest

# API saab ühenduda: postgresql://db:5432
```

### 2.3 Harjutus: 3-Tier Network Setup

Looge 3 network'i:

**Nõuded:**
- `frontend-net` - nginx ↔ api
- `backend-net` - api ↔ db
- `api` container on mõlemas network'is (bridge)

**Validatsioon:**
- nginx ei näe db'd
- api näeb mõlemat
- db ei näe nginx'i

---

## 3. Image Optimeerimise Tehnikad

### 3.1 .dockerignore Kasutamine
```
node_modules/
.git/
*.log
.DS_Store
.env
coverage/
.pytest_cache/
__pycache__/
```

### 3.2 RUN Käskude Kombineerimine

**Halb:**```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean
```

Kolm layer'it, apt cache jääb.

**Hea:**```dockerfile
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

Üks layer, cache kustutatud.

### 3.3 Layer Order Matters
```dockerfile
# Dependencies enne koodi (cache friendly)
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
```

### 3.4 Kasutage Slim/Alpine Image'e
```dockerfile
FROM python:3.11-slim  # 50MB vs python:3.11 (900MB)
```

### 3.5 Harjutus: Optimize Bloated Image

Antud image on 800MB. Optimeerige alla 100MB:
```dockerfile
FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip git curl wget vim
COPY . /app
WORKDIR /app
RUN pip3 install flask requests beautifulsoup4
CMD ["python3", "app.py"]
```

**Näpunäiteid:**
- Kasutage alpine base'd
- Eemaldage ebavajalikud tools (vim, wget)
- Kombineerige RUN käsud
- Lisage .dockerignore

---

## 4. Docker Compose Edasijõudnud

### 4.1 Health Checks
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
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 4.2 Profiles (Erinevad Keskkonnad)
```yaml
services:
  app:
    image: my-app:latest
    
  debug:
    image: my-app:debug
    profiles: ["debug"]
    
  test-db:
    image: postgres:15-alpine
    profiles: ["testing"]
```

Käivitamine:```bash
docker-compose up  # ainult app
docker-compose --profile debug up  # app + debug
```

### 4.3 Harjutus: Production-Ready Compose

Looge `docker-compose.yml` koos:

**Nõuded:**
- Health checks kõigile teenustele
- Resource limits (CPU, memory)
- Restart policies
- Logging configuration
- Profiles (dev, prod)

---

## 5. Container Turvalisus

### 5.1 Non-Root User
```dockerfile
FROM python:3.11-alpine

RUN adduser -D -s /bin/sh appuser

WORKDIR /app
COPY --chown=appuser:appuser . .

USER appuser

CMD ["python", "app.py"]
```

### 5.2 Read-Only Filesystem
```bash
docker run --read-only \
  --tmpfs /tmp:rw,noexec,nosuid \
  my-app:latest
```

### 5.3 Security Scanning
```bash
# Docker scan
docker scan my-app:latest

# Trivy (parem)
trivy image my-app:latest

# Filtreeri ainult HIGH ja CRITICAL
trivy image --severity HIGH,CRITICAL my-app:latest
```

### 5.4 Harjutus: Secure Container

Võtke olemasolev Dockerfile ja:

**Nõuded:**
- [ ] Lisa non-root user
- [ ] Eemalda shell access (`rm /bin/sh`)
- [ ] Kasuta read-only filesystem
- [ ] Skanni haavatavusi
- [ ] Paranda leitud probleemid

---

## 6. Advanced Scenarios

### 6.1 Zero-Downtime Deployment (Blue-Green)
```bash
# Blue (current)
docker run -d --name app-blue -p 8080:80 my-app:v1

# Green (new)
docker run -d --name app-green -p 8081:80 my-app:v2

# Test v2.0 on port 8081
curl http://localhost:8081/health

# Switch traffic (update load balancer)
# Remove blue
docker stop app-blue && docker rm app-blue
```

### 6.2 Multi-Architecture Build
```bash
# Setup buildx
docker buildx create --use

# Build for ARM ja AMD64
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t my-app:multiarch \
  --push .
```

### 6.3 Docker-in-Docker (CI/CD)
```yaml
# .github/workflows/docker.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build image
        run: docker build -t my-app:${{ github.sha }} .
      - name: Test
        run: docker run my-app:${{ github.sha }} npm test
```

---

## 7. Monitoring ja Logging

### 7.1 Container Stats
```bash
# Real-time stats
docker stats

# Export metrics
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### 7.2 Centralized Logging
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
  
  api:
    image: my-api:latest
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://192.168.1.100:514"
```

### 7.3 Prometheus Metrics
```dockerfile
FROM prom/prometheus

COPY prometheus.yml /etc/prometheus/

CMD ["--config.file=/etc/prometheus/prometheus.yml"]
```
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'docker'
    static_configs:
      - targets: ['cadvisor:8080']
```

---

## 8. Fullstack Production Setup Challenge

Looge production-ready fullstack rakendus Docker'iga.

### 8.1 Nõuded

**Frontend:**
- [ ] React/Vue rakendus
- [ ] Multi-stage build
- [ ] Nginx serveerib
- [ ] Alla 50MB

**Backend:**
- [ ] Node/Python API
- [ ] Non-root user
- [ ] Health checks
- [ ] Environment variables

**Database:**
- [ ] PostgreSQL
- [ ] Named volume
- [ ] Backup strategy

**Infra:**
- [ ] Redis cache
- [ ] Nginx reverse proxy
- [ ] SSL sertifikaat
- [ ] Docker Compose orkestratsioon

**CI/CD:**
- [ ] GitHub Actions pipeline
- [ ] Image build ja test
- [ ] Push Docker Hub'i
- [ ] Auto-deploy

**Monitoring:**
- [ ] Prometheus metrics
- [ ] Grafana dashboard
- [ ] Centralized logging

**Turvalisus:**
- [ ] Security scanning
- [ ] Non-root users
- [ ] Secrets management
- [ ] Network isolation

### 8.2 Arhitektuur
```
Internet
    ↓
[Nginx Reverse Proxy] :80/:443
    ↓
[Frontend] :3000 ←→ [Backend API] :8000
                         ↓
                    [Redis] :6379
                         ↓
                    [PostgreSQL] :5432
```

### 8.3 Hindamine

**Põhi (60%):**
- Kõik teenused töötavad
- Docker Compose setup
- Volume'id säilitavad andmeid

**Täiendav (20%):**
- Health checks
- Non-root users
- Nginx reverse proxy

**Boonus (20%):**
- CI/CD pipeline
- Monitoring
- SSL sertifikaat
- Security scanning

---

## 9. Kasulikud Ressursid

**Dokumentatsioon:**
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Compose Specification](https://compose-spec.io/)

**Tööriistad:**
- Trivy - security scanning
- Dive - image layer analysis
- Hadolint - Dockerfile linter
- Container Structure Tests - Google'i test framework

**Platvormid:**
- Docker Hub - public registry
- GitHub Container Registry - private images
- AWS ECR - enterprise registry
- Harbor - self-hosted registry

---

## 10. Troubleshooting Guide

### 10.1 Build Ebaõnnestub
```bash
# Vaata build cache'i
docker builder prune

# Build ilma cache'ita
docker build --no-cache -t myapp .

# Vaata layer'eid
docker history myapp
```

### 10.2 Container Crashib
```bash
# Vaata exit code
docker ps -a

# Vaata logisid
docker logs container-name

# Käivita interaktiivselt
docker run -it --entrypoint sh myapp
```

### 10.3 Networking Probleemid
```bash
# Vaata network'e
docker network ls
docker network inspect network-name

# Test connectivity
docker run --rm --network mynet alpine ping -c 2 service-name

# DNS debug
docker run --rm --network mynet alpine nslookup service-name
```

### 10.4 Volume Probleemid
```bash
# Vaata volume'eid
docker volume ls
docker volume inspect volume-name

# Vaata sisu
docker run --rm -v volume-name:/data alpine ls -la /data

# Backup
docker run --rm -v volume-name:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz /data
```

---

Need harjutused on mõeldud süvendama teie Docker oskusi. Alustage lihtsatest ja liikuge järk-järgult keerulisemate poole.