# Kodutöö: Docker Registry ja Production Deployment

**Eesmärk:** Õppida Docker registry workflow ja production deployment praktilisi oskusi  
**Aeg:** 2-3 tundi  
**Nõuded:** Docker, Docker Compose, Docker Hub konto (tasuta)

---

## Mida ehitame?

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
# Loo uus kaust kodutöö jaoks
mkdir ~/docker-registry-homework && cd ~/docker-registry-homework

# Kopeeri labori kood või kasuta oma
cp -r ~/todo-app/* . # või kirjuta ise

# Git setup
git init
echo -e ".env\nnode_modules/\n*.log\n*_data/\n.DS_Store" > .gitignore
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
# Test health endpoints
curl http://localhost/health
curl http://localhost/api/health

# Ava brauser
open http://localhost
```

---

## Osa 4: Versioonihaldus

### Tee muudatus ja ehita uus versioon

```bash
# Muuda midagi API koodis
echo "// Version 1.1.0 - Added new feature" >> api/server.js

# Ehita uus versioon
cd api/
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

## Osa 6: CI/CD Pipeline

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
- `DOCKER_PASSWORD`: your_dockerhub_password

**📸 SCREENSHOT 4:** Tee screenshot GitHub Actions successful run'ist

---

## Osa 7: Deployment script

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
docker-compose -f docker-compose.prod.yml up -d
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
# Health check
curl http://localhost/health

# API health
curl http://localhost/api/health

# Get todos
curl http://localhost/api/todos
```
```

---

## Esitamine

### Nõutud materjalid

1. **GitHub repository** sisuga:
   - `/api` - API kood Dockerfile'iga
   - `/frontend` - Frontend kood Dockerfile'iga
   - `/nginx` - Nginx konfiguratsioon
   - `/database` - Init SQL skriptid
   - `docker-compose.prod.yml` - Production compose fail
   - `.env.example` - Environment näidis
   - `deploy.sh` - Deployment script
   - `.github/workflows/` - CI/CD pipeline
   - `README.md` - Dokumentatsioon

2. **Screenshots** (5 tk):
   - Docker Hub repositories ja tagid
   - Running containers (`docker-compose ps`)
   - Version upgrade (containers with new version)
   - GitHub Actions successful run
   - Brauser kus töötav rakendus

3. **Docker Hub lingid**:
   - Link API repository'le
   - Link Frontend repository'le

### Hindamiskriteeriumid

- **Docker Registry workflow** (40%)
  - Image'd pushed Docker Hub'i
  - Korrektsed tagid (mitte ainult latest)
  - Versiooni haldus
  
- **Production deployment** (30%)
  - docker-compose.prod.yml töötab
  - Kasutab registry image'id
  - Environment muutujate haldus
  
- **CI/CD Pipeline** (20%)
  - GitHub Actions workflow
  - Automaatne build ja push
  
- **Dokumentatsioon** (10%)
  - README.md
  - Screenshots
  - Deploy script

---

## Troubleshooting

### Docker Hub login probleem
```bash
docker logout
docker login
```

### Rate limit error
Docker Hub tasuta plaanil on 200 pulls/6h. Lahendus:
- Oota 6 tundi
- Või logi sisse: `docker login`

### Version conflict
```bash
# Force pull
docker-compose -f docker-compose.prod.yml pull --ignore-pull-failures
```

### Container ei käivitu
```bash
# Vaata logisid
docker-compose -f docker-compose.prod.yml logs api
```
