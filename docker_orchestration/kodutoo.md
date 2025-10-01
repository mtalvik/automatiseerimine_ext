# 📝 Docker Orkestreerimine Kodutöö: Registry ja Tootmise Juurutamine

**Tähtaeg:** Järgmise nädala alguseks  
**Eesmärk:** Õppida Docker registry workflow ja production deployment praktilisi oskusi  
**Aeg:** 2-3 tundi

---

## 🎯 Ülesande kirjeldus

Õpite Docker registry workflow ja production deployment praktilisi oskusi. Ehitame täieliku CI/CD pipeline'i Docker konteinerite jaoks.

---

## 📋 Mida ehitame?

Ehitate laboris tehtud Todo rakenduse production versiooni. Seekord ei ehita image'id lokaalselt, vaid pushite registry'sse ja deployate sealt - nagu päris projektides tehakse.

```mermaid
graph LR
    subgraph "Development"
        Code[Kirjuta kood]
        Build[Ehita image]
        Test[Testi lokaalselt]
    end
    
    subgraph "Registry"
        Push[Push Docker Hub'i]
        Tag[Versioonihaldus]
    end
    
    subgraph "Production"
        Pull[Pull image'd]
        Deploy[Deploy production'i]
    end
    
    Code --> Build
    Build --> Test
    Test --> Push
    Push --> Tag
    Tag --> Pull
    Pull --> Deploy
    
    style Code fill:#99ff99
    style Push fill:#99ccff
    style Deploy fill:#ffcc99
```

---

## Osa 1: Ettevalmistus

### Docker Hub konto

```bash
# 1. Registreeru (tasuta): https://hub.docker.com/signup
# 2. Logi sisse terminalis
docker login
# Username: your_username
# Password: your_password
```

### Projekti setup

```bash
# Mine oma labori kausta
cd labs/lab-docker-compose/mariatesttalvik

# Või loo uus kaust ja kopeeri failid
mkdir ~/docker-registry-homework && cd ~/docker-registry-homework
cp -r /path/to/your/mariatesttalvik/* .

# Git setup (kui pole veel)
git init
echo -e ".env\nnode_modules/\n*/node_modules/\n*.log\n*_data/\n.DS_Store" > .gitignore

# Genereeri package-lock.json failid (OLULINE!)
cd api && npm install && cd ..
cd frontend && npm install && cd ..
```

---

## Osa 2: Image'ide ehitamine ja Registry

### Seadista muutuja

```bash
# Asenda oma Docker Hub kasutajanimega!
export DOCKER_USER="your_dockerhub_username"
```

### API image ehitamine ja push

API jaoks ehitame mitu versiooni - see on production best practice.

```bash
cd api/

# Ehita production image
docker build -t $DOCKER_USER/todo-api:1.0.0 .

# Lisa täiendavad tagid
docker tag $DOCKER_USER/todo-api:1.0.0 $DOCKER_USER/todo-api:1.0
docker tag $DOCKER_USER/todo-api:1.0.0 $DOCKER_USER/todo-api:latest

# Push kõik tagid Docker Hub'i
docker push $DOCKER_USER/todo-api:1.0.0
docker push $DOCKER_USER/todo-api:1.0
docker push $DOCKER_USER/todo-api:latest

cd ..
```

### Frontend image ehitamine ja push

```bash
cd frontend/

# Ehita production image
docker build -t $DOCKER_USER/todo-frontend:1.0.0 .

# Lisa tagid
docker tag $DOCKER_USER/todo-frontend:1.0.0 $DOCKER_USER/todo-frontend:1.0
docker tag $DOCKER_USER/todo-frontend:1.0.0 $DOCKER_USER/todo-frontend:latest

# Push Docker Hub'i
docker push $DOCKER_USER/todo-frontend:1.0.0
docker push $DOCKER_USER/todo-frontend:1.0
docker push $DOCKER_USER/todo-frontend:latest

cd ..
```

### Kontrolli Docker Hub'is

Ava brauser ja vaata:
- `https://hub.docker.com/r/YOUR_USERNAME/todo-api/tags`
- `https://hub.docker.com/r/YOUR_USERNAME/todo-frontend/tags`

**📸 SCREENSHOT 1:** Tee screenshot Docker Hub'ist kus on näha sinu repositories ja tagid

---

## Osa 3: Production Docker Compose

### Loo production compose fail

See fail **ei ehita** image'id, vaid **kasutab registry'st**.

Loo `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  # Nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: todo_nginx_prod
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
      - frontend
    restart: unless-stopped
    networks:
      - frontend_network

  # Frontend teie registry'st
  frontend:
    # Kasuta oma Docker Hub image'i
    image: ${DOCKER_USER}/todo-frontend:${VERSION:-1.0.0}
    container_name: todo_frontend_prod
    restart: unless-stopped
    networks:
      - frontend_network
    healthcheck:
      test: ["CMD", "wget", "-q", "--tries=1", "--spider", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3

  # API teie registry'st
  api:
    # Kasuta oma Docker Hub image'i
    image: ${DOCKER_USER}/todo-api:${VERSION:-1.0.0}
    container_name: todo_api_prod
    environment:
      NODE_ENV: production
      PORT: 3000
      DATABASE_URL: postgres://todouser:${DB_PASSWORD}@database:5432/tododb
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
      APP_VERSION: ${VERSION:-1.0.0}
    depends_on:
      database:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - frontend_network
      - backend_network
    healthcheck:
      test: ["CMD", "wget", "-q", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Database - avalik image
  database:
    image: postgres:14-alpine
    container_name: todo_db_prod
    environment:
      POSTGRES_DB: tododb
      POSTGRES_USER: todouser
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    restart: unless-stopped
    networks:
      - backend_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todouser -d tododb"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis - avalik image
  redis:
    image: redis:7-alpine
    container_name: todo_redis_prod
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - backend_network
    healthcheck:
      test: ["CMD", "redis-cli", "--auth", "${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

networks:
  frontend_network:
    name: todo_frontend_net
    driver: bridge
  backend_network:
    name: todo_backend_net
    driver: bridge
    internal: true

volumes:
  postgres_data:
    name: todo_postgres_data
  redis_data:
    name: todo_redis_data
```

### Loo production environment fail

Loo `.env.prod`:

```bash
# Docker Hub kasutajanimi
DOCKER_USER=your_dockerhub_username

# Versioon
VERSION=1.0.0

# Andmebaasi paroolid
DB_PASSWORD=super_secret_password_123
REDIS_PASSWORD=redis_secret_456
```

### Deploy production

```bash
# Kustuta vanad konteinerid kui on
docker-compose down

# Pull image'd registry'st ja käivita
docker-compose -f docker-compose.prod.yml --env-file .env.prod pull
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

# Kontrolli staatust
docker-compose -f docker-compose.prod.yml ps

# Vaata logisid
docker-compose -f docker-compose.prod.yml logs -f
```

**📸 SCREENSHOT 2:** Tee screenshot `docker-compose ps` väljundist kus on näha running containers

### Testi rakendust

```bash
# Test API health
curl http://localhost/api/health

# Ava brauser
open http://localhost
```

---

## Osa 4: Versioonihaldus

### Lisa version endpoint API-sse (valikuline)

Muuda `api/server.js` ja lisa peale health endpoint'i:

```javascript
// Version endpoint
app.get('/api/version', (req, res) => {
  res.json({
    version: process.env.APP_VERSION || '1.0.0',
    environment: process.env.NODE_ENV,
    timestamp: new Date().toISOString()
  });
});
```

### Tee muudatus ja ehita uus versioon

```bash
# Muuda midagi API koodis (näiteks lisa kommentaar)
cd api/
echo "// Version 1.1.0 - Added version endpoint" >> server.js

# Ehita uus versioon
docker build -t $DOCKER_USER/todo-api:1.1.0 .

# Lisa tagid
docker tag $DOCKER_USER/todo-api:1.1.0 $DOCKER_USER/todo-api:1.1
docker tag $DOCKER_USER/todo-api:1.1.0 $DOCKER_USER/todo-api:latest

# Push
docker push $DOCKER_USER/todo-api:1.1.0
docker push $DOCKER_USER/todo-api:1.1
docker push $DOCKER_USER/todo-api:latest

cd ..
```

### Deploy uus versioon

```bash
# Muuda versiooni .env.prod failis
sed -i 's/VERSION=1.0.0/VERSION=1.1.0/' .env.prod

# Või kasuta environment muutujat
export VERSION=1.1.0

# Pull uus versioon ja uuenda
docker-compose -f docker-compose.prod.yml --env-file .env.prod pull api
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d api

# Kontrolli
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"

# Test version endpoint (kui lisasid)
curl http://localhost/api/version
```

**📸 SCREENSHOT 3:** Tee screenshot kus on näha version upgrade (containers with new version)

### Rollback varasemale versioonile

Kui midagi läheb valesti:

```bash
# Rollback
export VERSION=1.0.0

# Või muuda .env.prod failis tagasi
sed -i 's/VERSION=1.1.0/VERSION=1.0.0/' .env.prod

# Deploy vana versioon
docker-compose -f docker-compose.prod.yml --env-file .env.prod pull api
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d api

# Kontrolli
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
```

---

## Osa 5: Multi-stage deployment

### Development vs Staging vs Production

Loo erinevad environment failid:

`.env.dev`:
```bash
DOCKER_USER=your_dockerhub_username
VERSION=latest
DB_PASSWORD=devpass
REDIS_PASSWORD=devredis
```

`.env.staging`:
```bash
DOCKER_USER=your_dockerhub_username
VERSION=1.1.0
DB_PASSWORD=stagingpass
REDIS_PASSWORD=stagingredis
```

`.env.prod`:
```bash
DOCKER_USER=your_dockerhub_username
VERSION=1.0.0
DB_PASSWORD=prodpass
REDIS_PASSWORD=prodredis
```

Deploy erinevad keskkonnad:

```bash
# Development
docker-compose -f docker-compose.prod.yml --env-file .env.dev up -d

# Staging (test new version)  
docker-compose -f docker-compose.prod.yml --env-file .env.staging up -d

# Production (stable)
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

---

## Osa 6: CI/CD Pipeline (Bonus)

### GitHub Actions workflow

Loo `.github/workflows/docker-build.yml`:

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main ]
    tags:
      - 'v*'
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Docker Hub
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract version
        id: version
        run: |
          if [[ "${{ github.ref }}" == refs/tags/v* ]]; then
            VERSION=${GITHUB_REF#refs/tags/v}
          elif [[ "${{ github.ref }}" == refs/heads/main ]]; then
            VERSION=latest
          else
            VERSION=pr-${{ github.event.pull_request.number }}
          fi
          echo "VERSION=$VERSION" >> $GITHUB_OUTPUT

      - name: Build and push API
        uses: docker/build-push-action@v4
        with:
          context: ./api
          push: ${{ github.event_name != 'pull_request' }}
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/todo-api:${{ steps.version.outputs.VERSION }}
            ${{ secrets.DOCKER_USERNAME }}/todo-api:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build and push Frontend
        uses: docker/build-push-action@v4
        with:
          context: ./frontend
          push: ${{ github.event_name != 'pull_request' }}
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/todo-frontend:${{ steps.version.outputs.VERSION }}
            ${{ secrets.DOCKER_USERNAME }}/todo-frontend:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### GitHub Secrets

GitHub repo Settings → Secrets → Actions:
- `DOCKER_USERNAME`: your_dockerhub_username
- `DOCKER_PASSWORD`: your_dockerhub_password_or_token

**📸 SCREENSHOT 4:** Tee screenshot GitHub Actions successful run'ist (kui teed CI/CD osa)

---

## Osa 7: Deployment Script

### Loo deployment script

Loo `deploy.sh`:

```bash
#!/bin/bash

# Deploy script for Todo application

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.prod"

# Functions
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check requirements
command -v docker >/dev/null 2>&1 || error "Docker is not installed"
command -v docker-compose >/dev/null 2>&1 || error "Docker Compose is not installed"

# Check environment file
if [ ! -f "$ENV_FILE" ]; then
    error "Environment file $ENV_FILE not found"
fi

# Parse arguments
ACTION=${1:-deploy}
VERSION=${2:-}

case $ACTION in
    deploy)
        log "Deploying application..."
        
        # Pull latest images
        log "Pulling images from registry..."
        docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE pull
        
        # Deploy
        log "Starting containers..."
        docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
        
        # Health check
        log "Waiting for services to be healthy..."
        sleep 10
        
        # Check status
        docker-compose -f $COMPOSE_FILE ps
        
        log "Deployment completed successfully!"
        ;;
        
    rollback)
        if [ -z "$VERSION" ]; then
            error "Version required for rollback. Usage: ./deploy.sh rollback 1.0.0"
        fi
        
        log "Rolling back to version $VERSION..."
        
        # Update version
        export VERSION=$VERSION
        
        # Pull specific version
        docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE pull
        
        # Restart services
        docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
        
        log "Rollback to version $VERSION completed!"
        ;;
        
    status)
        log "Checking application status..."
        docker-compose -f $COMPOSE_FILE ps
        ;;
        
    logs)
        log "Showing application logs..."
        docker-compose -f $COMPOSE_FILE logs -f
        ;;
        
    stop)
        log "Stopping application..."
        docker-compose -f $COMPOSE_FILE down
        log "Application stopped!"
        ;;
        
    *)
        echo "Usage: ./deploy.sh [deploy|rollback|status|logs|stop] [version]"
        exit 1
        ;;
esac
```

Tee script käivitatavaks:

```bash
chmod +x deploy.sh

# Kasuta
./deploy.sh deploy
./deploy.sh status
./deploy.sh rollback 1.0.0
```

---

## Osa 8: Dokumentatsioon

### Loo README.md

```markdown
# Todo App - Docker Registry Homework

## Overview

Production-ready Todo application deployed using Docker Hub registry workflow.

## Docker Hub Images

- API: https://hub.docker.com/r/USERNAME/todo-api
- Frontend: https://hub.docker.com/r/USERNAME/todo-frontend

## Quick Start

```bash
# Set your Docker Hub username
export DOCKER_USER=your_username

# Deploy
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

## Deployment

### Production Deployment

```bash
# Using deployment script
./deploy.sh deploy

# Manual deployment
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### Version Management

```bash
# Deploy specific version
export VERSION=1.1.0
./deploy.sh deploy

# Rollback to previous version
./deploy.sh rollback 1.0.0
```

### Monitoring

```bash
# Check status
./deploy.sh status

# View logs
./deploy.sh logs
```

## CI/CD

Automated builds via GitHub Actions on:
- Push to main branch → builds `latest`
- Tag push (v*) → builds version tag

## Environment Configuration

- `.env.dev` - Development environment
- `.env.staging` - Staging environment  
- `.env.prod` - Production environment

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│    Nginx    │────▶│   Frontend   │────▶│     API      │
│   Port 80   │     │   (React)    │     │  (Node.js)   │
└─────────────┘     └──────────────┘     └──────────────┘
                                                 │
                                          ┌──────┴──────┐
                                          │             │
                                    ┌─────▼───┐  ┌─────▼───┐
                                    │Postgres │  │  Redis  │
                                    └─────────┘  └─────────┘
```

## Testing

```bash
# API health
curl http://localhost/api/health

# Get todos
curl http://localhost/api/todos

# Version info (if implemented)
curl http://localhost/api/version
```

## Troubleshooting

- **Login issues**: `docker logout && docker login`
- **Rate limits**: Wait 6h or authenticate
- **Port conflicts**: Change port in docker-compose.prod.yml
```

**📸 SCREENSHOT 5:** Tee screenshot brauserist kus on näha töötav rakendus

---

## Esitamine

### Nõutud materjalid

1. **GitHub repository** sisuga:
   - `/api` - API kood Dockerfile'iga
   - `/frontend` - Frontend kood Dockerfile'iga
   - `/nginx` - Nginx konfiguratsioon
   - `/database` - Init SQL skriptid
   - `docker-compose.yml` - Development compose (laborist)
   - `docker-compose.prod.yml` - Production compose fail
   - `.env.example` - Environment näidis
   - `.env.prod`, `.env.staging`, `.env.dev` - Environment failid
   - `deploy.sh` - Deployment script
   - `.github/workflows/` - CI/CD pipeline (bonus)
   - `README.md` - Dokumentatsioon

2. **Screenshots** (5 tk):
   - Docker Hub repositories ja tagid
   - Running containers (`docker-compose ps`)
   - Version upgrade (containers with new version)
   - GitHub Actions successful run (kui teed CI/CD)
   - Brauser kus töötav rakendus

3. **Docker Hub lingid**:
   - Link API repository'le (nt: https://hub.docker.com/r/username/todo-api)
   - Link Frontend repository'le (nt: https://hub.docker.com/r/username/todo-frontend)

### Hindamiskriteeriumid

- **Docker Registry workflow** (40%)
  - Image'd pushed Docker Hub'i ✓
  - Korrektsed tagid (versioonid, mitte ainult latest) ✓
  - Toimiv pull/push workflow ✓
  
- **Production deployment** (30%)
  - docker-compose.prod.yml töötab registry image'dega ✓
  - Environment muutujate korrektne haldus ✓
  - Health checks ja restart policies ✓
  
- **Version management** (20%)
  - Deploy erinevate versioonidega ✓
  - Rollback funktsioon töötab ✓
  - Deploy script või manual workflow ✓
  
- **Dokumentatsioon ja esitamine** (10%)
  - README.md kirjeldab deployment'i ✓
  - Screenshots tõestavad töötamist ✓
  - Kood on GitHub'is ✓

---

## Troubleshooting

### Docker Hub login probleem
```bash
# Proovi uuesti
docker logout
docker login
```

### Rate limit error
```bash
# Docker Hub tasuta plaanil on limiidid
# Lahendus 1: Oota 6 tundi
# Lahendus 2: Logi sisse (authenticated users have higher limits)
docker login
```

### Permission denied error
```bash
# Build käigus
sudo docker build ...

# Deploy script
chmod +x deploy.sh
```

### Container ei käivitu
```bash
# Vaata logisid
docker-compose -f docker-compose.prod.yml logs api
docker-compose -f docker-compose.prod.yml logs frontend
```

### Port already in use
```bash
# Muuda port docker-compose.prod.yml failis
ports:
  - "8080:80"  # Kasuta teist porti
```

### npm ci error Dockerfile'is
```bash
# Genereeri package-lock.json failid enne build'i
cd api && npm install && cd ..
cd frontend && npm install && cd ..
```

---

## Bonus ülesanded (lisapunktid)

1. **Multi-architecture build** (arm64 + amd64)
2. **Docker image scanning** turvaaukude jaoks
3. **Kubernetes deployment YAML** failid
4. **Monitoring stack** (Prometheus + Grafana)
5. **Backup script** andmebaasi jaoks

---

## Kasulikud lingid

- [Docker Hub dokumentatsioon](https://docs.docker.com/docker-hub/)
- [Docker Compose production guide](https://docs.docker.com/compose/production/)
- [GitHub Actions Docker guide](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)
- [Docker security best practices](https://docs.docker.com/develop/security-best-practices/)
