# Docker Compose Lisapraktika

**Eeldused:** Loeng ja labor läbitud, Docker Hub konto

See fail sisaldab lisaharjutusi ja edasijõudnud teemasid Docker Compose mooduli jaoks. Materjal on valikuline ja mõeldud neile, kes soovivad süvendada oma oskusi.

---

## 1. Multi-Stage Builds Optimeerimiseks

### 1.1 Probleem

Build dependencies suurendavad image'i mahtu. Node.js rakenduse image võib olla 1.2GB, kuigi runtime vajab ainult 150MB.

### 1.2 Lahendus: Multi-Stage Build```dockerfile
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
CMD ["node", "dist/index.js"]```

Image väheneb 1.2GB → 150MB.

### 1.3 Harjutus: Python Flask Multi-Stage

Looge multi-stage Dockerfile Python Flask rakendusele:

**Nõuded:**
- [ ] Stage 1: Install dependencies ja compile
- [ ] Stage 2: Ainult runtime + compiled files
- [ ] Eesmärk: alla 100MB final image
- [ ] Kasutage `python:3.11` builder'is
- [ ] Kasutage `python:3.11-alpine` runtime'is

**Näpunäiteid:**
- Kompileerige `.pyc` failid: `python -m compileall`
- Kopeerige ainult vajalikud failid
- Lisage .dockerignore fail

**Boonus:**
- Kasutage distroless image't lõpptulemuses
- Skannige Trivy'ga: `trivy image your-image:latest`
- Optimeerige alla 50MB

---

## 2. Health Checks ja Self-Healing

### 2.1 Probleem

Container jookseb aga rakendus sees on hangund või ei vasta enam. Docker arvab et kõik on OK, sest protsess töötab.

### 2.2 Lahendus: Health Checks```yaml
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
    restart: unless-stopped```

### 2.3 Harjutus: Production-Ready Compose

Looge `docker-compose.yml` mis sisaldab:

**Nõuded:**
- [ ] Vähemalt 3 teenust (frontend, backend, database)
- [ ] Health checks kõigile teenustele
- [ ] Resource limits (CPU: 0.5, Memory: 512M)
- [ ] Restart policies
- [ ] `depends_on` koos `condition: service_healthy`

**Näpunäiteid:**
- `start_period` annab aega bootimiseks
- `wget --spider` ei lae sisu, ainult kontrollib HTTP status
- `pg_isready` on PostgreSQL'i built-in health check

**Testimine:**```bash
docker compose up -d
docker compose ps  # peaks näitama "(healthy)"

# Simuleerige crash
docker exec -it <container> pkill node

# Docker peaks 30 sek jooksul taaskäivitama
watch docker compose ps```

**Boonus:**
- Lisage logging configuration (max-size, max-file)
- Looge `/health` endpoint mis tagastab süsteemi seisundi
- Integreerige Prometheus metrics

---

## 3. Multi-Environment Setup

### 3.1 Probleem

Development vajab hot reload ja debug mode. Production vajab resource limits, turvalisust ja optimeerimist. Üks `docker-compose.yml` ei sobi mõlemale.

### 3.2 Lahendus: Override Files```
project/
├── docker-compose.yml          # Base config
├── docker-compose.dev.yml      # Development overrides
├── docker-compose.prod.yml     # Production overrides
├── .env.example
├── .env.dev                    # NOT in git
└── .env.prod                   # NOT in git```

**Base docker-compose.yml:**```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "${PORT}:3000"
    env_file:
      - .env```

**docker-compose.dev.yml:**```yaml
version: '3.8'

services:
  api:
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=*```

**docker-compose.prod.yml:**```yaml
version: '3.8'

services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    environment:
      - NODE_ENV=production
    restart: always```

**Käivitamine:**```bash
# Development
docker compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up -d

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d```

### 3.3 Harjutus: Kolme Keskkonna Setup

Looge projekti struktuur koos deployment script'iga:

**Nõuded:**
- [ ] Base `docker-compose.yml` + 2 override faili (dev, prod)
- [ ] Development mount'ib koodi (hot reload)
- [ ] Production seab resource limits ja restart: always
- [ ] `deploy.sh` script mis käivitab õige keskkonna
- [ ] `.env.example` on git'is, `.env.*` on `.gitignore`'s

**deploy.sh näide:**```bash
#!/bin/bash

ENV=${1:-dev}

case $ENV in
  dev)
    docker compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up -d
    ;;
  prod)
    docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d
    ;;
  stop)
    docker compose down
    ;;
  *)
    echo "Usage: $0 {dev|prod|stop}"
    exit 1
    ;;
esac```

**Testimine:**```bash
chmod +x deploy.sh

./deploy.sh dev
curl http://localhost:3000/health

./deploy.sh stop

./deploy.sh prod
curl http://localhost:3000/health```

**Näpunäiteid:**
- `-f` flag laseb override'ida config'e
- `--env-file` valib õige environment
- Production'is ALATI sea memory limits
- Ära pane saladusi git'i - kasuta `.env.example` placeholder'itega

**Boonus:**
- Lisage staging environment (docker-compose.staging.yml)
- Implementeerige Docker secrets
- Looge smoke test script mis kontrollib deployment'i
- Lisage blue-green deployment strategy

---

## Kasulikud Ressursid

**Dokumentatsioon:**
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Compose Healthcheck](https://docs.docker.com/compose/compose-file/compose-file-v3/#healthcheck)
- [Compose Override](https://docs.docker.com/compose/extends/)

**Tööriistad:**
- **Dive** - image layer analüüs: `docker run --rm -it wagoodman/dive:latest <image>`
- **Trivy** - security scanning: `trivy image <image>`
- **Hadolint** - Dockerfile linter: https://github.com/hadolint/hadolint

**Näited:**
- Awesome Compose: https://github.com/docker/awesome-compose
- Docker Samples: https://github.com/dockersamples

---

Need harjutused on mõeldud süvendama teie Docker Compose oskusi. Alustage esimesest ja liikuge järk-järgult keerulisemate poole.