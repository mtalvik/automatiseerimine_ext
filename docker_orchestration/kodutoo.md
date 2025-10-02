# Docker Registry ja Production Deployment - Kodutöö

**Tähtaeg:** Järgmise nädala algus  
**Aeg:** 2-3 tundi

---

## Eesmärk

Õppida Docker registry workflow ja production deployment. Ehitate laboris tehtud Todo rakenduse production versiooni - seekord ei ehita image'id lokaalselt, vaid pushite registry'sse ja deployate sealt.

## Mida ehitame

```
Development → Build → Push Docker Hub → Pull Production → Deploy
```

Võtate oma laboritöö Todo rakenduse ja teete sellest registry-based deployment'i.

---

## Osa 1: Docker Hub Setup

### Konto loomine

1. Registreeru: https://hub.docker.com/signup
2. Logi sisse terminalis:

```bash
docker login
# Username: your_username
# Password: your_password
```

### Projekti ettevalmistus

```bash
# Mine oma labori kausta
cd labs/lab-docker-compose/mariatesttalvik

# Seadista muutuja
export DOCKER_USER="your_dockerhub_username"

# Genereeri package-lock.json failid (vajalik Dockerfile'i jaoks)
cd api && npm install && cd ..
cd frontend && npm install && cd ..
```

---

## Osa 2: Image'ide Build ja Push

### API image

```bash
cd api/

# Build
docker build -t $DOCKER_USER/todo-api:1.0.0 .

# Tag'i versioonid
docker tag $DOCKER_USER/todo-api:1.0.0 $DOCKER_USER/todo-api:1.0
docker tag $DOCKER_USER/todo-api:1.0.0 $DOCKER_USER/todo-api:1
docker tag $DOCKER_USER/todo-api:1.0.0 $DOCKER_USER/todo-api:latest

# Push
docker push $DOCKER_USER/todo-api:1.0.0
docker push $DOCKER_USER/todo-api:1.0
docker push $DOCKER_USER/todo-api:1
docker push $DOCKER_USER/todo-api:latest

cd ..
```

**Miks mitu tag'i?**
- `1.0.0` - täpne versioon (production)
- `1.0` - minor versioon (staging)
- `1` - major versioon (dev)
- `latest` - viimane versioon (testing)

### Frontend image

Sama protsess:

```bash
cd frontend/
docker build -t $DOCKER_USER/todo-frontend:1.0.0 .
docker tag $DOCKER_USER/todo-frontend:1.0.0 $DOCKER_USER/todo-frontend:1.0
docker tag $DOCKER_USER/todo-frontend:1.0.0 $DOCKER_USER/todo-frontend:1
docker tag $DOCKER_USER/todo-frontend:1.0.0 $DOCKER_USER/todo-frontend:latest

docker push $DOCKER_USER/todo-frontend:1.0.0
docker push $DOCKER_USER/todo-frontend:1.0
docker push $DOCKER_USER/todo-frontend:1
docker push $DOCKER_USER/todo-frontend:latest
cd ..
```

**Kontrolli:** Ava brauseris Docker Hub ja vaata oma repositories.

**📸 SCREENSHOT 1:** Docker Hub repositories koos tagidega

---

## Osa 3: Production Docker Compose

### Loo `docker-compose.prod.yml`

Põhiline erinevus laborist: **EI EHITA** image'id, vaid **KASUTAB** registry'st.

```yaml
version: '3.8'

services:
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

  frontend:
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

  api:
    image: ${DOCKER_USER}/todo-api:${VERSION:-1.0.0}
    container_name: todo_api_prod
    environment:
      NODE_ENV: production
      PORT: 3000
      DATABASE_URL: postgres://todouser:${DB_PASSWORD}@database:5432/tododb
      APP_VERSION: ${VERSION:-1.0.0}
    depends_on:
      database:
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

networks:
  frontend_network:
    name: todo_frontend_net
  backend_network:
    name: todo_backend_net
    internal: true

volumes:
  postgres_data:
    name: todo_postgres_data
```

**Oluline:**
- `image:` direktiiv, mitte `build:`
- `${VERSION:-1.0.0}` - default versioon kui muutuja puudub
- `healthcheck` - kontrollib kas teenus töötab
- `restart: unless-stopped` - auto-restart kui crashib
- `internal: true` backend network'il - DB ei ole väljast ligipääsetav

### Loo `.env.prod`

```bash
DOCKER_USER=your_dockerhub_username
VERSION=1.0.0
DB_PASSWORD=super_secret_password_123
```

### Deploy

```bash
# Pull image'd
docker-compose -f docker-compose.prod.yml --env-file .env.prod pull

# Käivita
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

# Kontrolli
docker-compose -f docker-compose.prod.yml ps
```

**Test:**
```bash
curl http://localhost/api/health
open http://localhost
```

**📸 SCREENSHOT 2:** `docker-compose ps` output kus on running containers

---

## Osa 4: Versioonihaldus

### Lisa version endpoint API'sse

Muuda `api/server.js`:

```javascript
// Lisa peale health endpoint'i
app.get('/api/version', (req, res) => {
  res.json({
    version: process.env.APP_VERSION || '1.0.0',
    environment: process.env.NODE_ENV,
    timestamp: new Date().toISOString()
  });
});
```

### Build ja push uus versioon

```bash
cd api/

# Build 1.1.0
docker build -t $DOCKER_USER/todo-api:1.1.0 .

# Tag'i
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
# Muuda .env.prod
sed -i 's/VERSION=1.0.0/VERSION=1.1.0/' .env.prod

# Deploy
docker-compose -f docker-compose.prod.yml --env-file .env.prod pull api
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d api

# Kontrolli
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
curl http://localhost/api/version
```

**📸 SCREENSHOT 3:** Version upgrade (containers with new version)

### Rollback

```bash
# Tagasi 1.0.0
sed -i 's/VERSION=1.1.0/VERSION=1.0.0/' .env.prod

# Deploy
docker-compose -f docker-compose.prod.yml --env-file .env.prod pull api
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d api

# Kontrolli
curl http://localhost/api/version
```

---

## Osa 5: Multi-Environment

### Loo environment failid

`.env.dev`:
```bash
DOCKER_USER=your_dockerhub_username
VERSION=latest
DB_PASSWORD=devpass
```

`.env.staging`:
```bash
DOCKER_USER=your_dockerhub_username
VERSION=1.1.0
DB_PASSWORD=stagingpass
```

`.env.prod`:
```bash
DOCKER_USER=your_dockerhub_username
VERSION=1.0.0
DB_PASSWORD=prodpass
```

### Deploy erinevad keskkonnad

```bash
# Development
docker-compose -f docker-compose.prod.yml --env-file .env.dev up -d

# Staging
docker-compose -f docker-compose.prod.yml --env-file .env.staging up -d

# Production
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

---

## Osa 6: Deployment Script

### Loo `deploy.sh`

```bash
#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.prod"

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

[ -f "$COMPOSE_FILE" ] || error "Compose file not found"
[ -f "$ENV_FILE" ] || error "Environment file not found"

ACTION=${1:-status}
VERSION=${2:-}

case $ACTION in
    deploy)
        log "Deploying version ${VERSION:-current}..."
        
        if [ -n "$VERSION" ]; then
            sed -i.bak "s/^VERSION=.*/VERSION=$VERSION/" "$ENV_FILE"
            log "Updated VERSION to $VERSION"
        fi
        
        log "Pulling images..."
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" pull
        
        log "Starting services..."
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d
        
        sleep 10
        docker-compose -f "$COMPOSE_FILE" ps
        
        log "Deployment complete!"
        ;;
        
    rollback)
        [ -n "$VERSION" ] || error "Version required: ./deploy.sh rollback 1.0.0"
        
        log "Rolling back to $VERSION..."
        sed -i.bak "s/^VERSION=.*/VERSION=$VERSION/" "$ENV_FILE"
        
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" pull
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d
        
        log "Rollback complete!"
        ;;
        
    status)
        docker-compose -f "$COMPOSE_FILE" ps
        ;;
        
    logs)
        docker-compose -f "$COMPOSE_FILE" logs -f "${2:-}"
        ;;
        
    stop)
        log "Stopping services..."
        docker-compose -f "$COMPOSE_FILE" down
        ;;
        
    *)
        echo "Usage: $0 {deploy|rollback|status|logs|stop} [version]"
        echo ""
        echo "Examples:"
        echo "  $0 deploy 1.1.0"
        echo "  $0 rollback 1.0.0"
        echo "  $0 status"
        echo "  $0 logs api"
        exit 1
        ;;
esac
```

Tee käivitatavaks:
```bash
chmod +x deploy.sh
```

Kasuta:
```bash
./deploy.sh deploy 1.1.0
./deploy.sh rollback 1.0.0
./deploy.sh status
./deploy.sh logs api
```

---

## Osa 7: README

Loo `README.md`:

```markdown
# Todo App - Production Deployment

## Docker Hub Images

- API: https://hub.docker.com/r/USERNAME/todo-api
- Frontend: https://hub.docker.com/r/USERNAME/todo-frontend

## Quick Start

```bash
export DOCKER_USER=your_username
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

## Deployment

```bash
# Deploy version
./deploy.sh deploy 1.1.0

# Rollback
./deploy.sh rollback 1.0.0

# Status
./deploy.sh status
```

## Testing

```bash
curl http://localhost/api/health
curl http://localhost/api/version
```

## Architecture

```
Nginx (80) → Frontend → API → Database
                             → Redis
```
```

**📸 SCREENSHOT 4:** Brauseris töötav rakendus

---

## Esitamine

### GitHub repository sisaldab:

```
docker-registry-homework/
├── api/
│   ├── Dockerfile
│   ├── package.json
│   └── server.js
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── (muud failid)
├── nginx/
│   └── nginx.conf
├── database/
│   └── init.sql
├── docker-compose.yml (laborist)
├── docker-compose.prod.yml
├── .env.example
├── deploy.sh
└── README.md
```

### 4 Screenshot'i:

1. Docker Hub repositories ja tagid
2. Running containers (`docker-compose ps`)
3. Version upgrade (uue versiooniga containers)
4. Brauser - töötav rakendus

### Docker Hub lingid:

- `https://hub.docker.com/r/username/todo-api`
- `https://hub.docker.com/r/username/todo-frontend`

---

## Hindamine

**Docker Registry (40%)**
- ✓ Image'd Docker Hub'is
- ✓ Korrektsed tagid (1.0.0, 1.1.0, 1.0, 1, latest)
- ✓ Pull/push workflow töötab

**Production Deployment (30%)**
- ✓ `docker-compose.prod.yml` kasutab registry image'id
- ✓ Environment muutujad korrektselt
- ✓ Health checks ja restart policies

**Version Management (20%)**
- ✓ Deploy erinevaid versioone
- ✓ Rollback töötab
- ✓ Deploy script

**Dokumentatsioon (10%)**
- ✓ README kirjeldab deployment'i
- ✓ Screenshot'id tõestavad töötamist
- ✓ Kood GitHub'is

---

## Troubleshooting

**Login probleem:**
```bash
docker logout
docker login
```

**Rate limit:**
```bash
# Docker Hub authenticated users have higher limits
docker login
```

**Container ei käivitu:**
```bash
docker-compose -f docker-compose.prod.yml logs api
```

**Port already in use:**
```yaml
# docker-compose.prod.yml
ports:
  - "8080:80"  # Kasuta teist porti
```

---

## Bonus (+lisapunktid)

1. **GitHub Actions CI/CD** - automaatne build ja push
2. **Multi-architecture** - ARM64 + AMD64
3. **Image scanning** - turvaaukude kontroll
4. **Monitoring** - Prometheus + Grafana

---

## Kasulikud lingid

- Docker Hub: https://docs.docker.com/docker-hub/
- Docker Compose production: https://docs.docker.com/compose/production/
- Semantic Versioning: https://semver.org/
- GitHub Actions: https://docs.github.com/en/actions/publishing-packages/publishing-docker-images
