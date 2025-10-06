# Docker Orchestration Lisapraktika

Täiendavad ülesanded Docker Compose'i oskuste süvendamiseks.

**Eeldused:** Põhilabor läbitud, Docker Compose põhitõed selged

---

## Enne alustamist

Need ülesanded on valikulised ja mõeldud neile, kes:

- Lõpetasid põhilabori ära
- Mõistavad Docker Compose põhitõdesid
- Tahavad õppida advanced orchestration
- Valmistuvad päris production deployment'ideks

---

## Väljakutse 1: Multi-Stage Builds ja Optimization


### Mida õpid?
- Multi-stage builds
- Layer caching strategies
- Image optimization techniques
- Build arguments

### Ülesanne:
Loo Node.js rakendus, mis kasutab multi-stage build'i:

```dockerfile
# Halb näide (image: ~1GB)
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]

# Hea näide (image: ~150MB)
# Stage 1: Build
FROM node:18-alpine AS builder
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
COPY package*.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Sammud:
1. **Loo test projekt:**
   ```bash
   mkdir multi-stage-demo && cd multi-stage-demo
   npm init -y
   npm install express
   ```

2. **Lisa .dockerignore:**
   ```
   node_modules
   npm-debug.log
   .git
   .DS_Store
   *.md
   ```

3. **Build ja võrdle:**
   ```bash
# Enne
   docker build -t myapp:basic -f Dockerfile.basic .
   docker images myapp:basic
   
# Pärast
   docker build -t myapp:optimized -f Dockerfile.multistage .
   docker images myapp:optimized
   ```

###  Boonus:
- Lisa BuildKit cache mounts
- Kasuta distroless images
- Implementeeri security scanning (Trivy)
- Loo automated image optimization pipeline

---

## Väljakutse 2: Health Checks ja Self-Healing


### Mida õpid?
- Docker health checks
- Restart policies
- Dependency management
- Graceful shutdowns

### Ülesanne:
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    image: nginx:alpine
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 40s
    restart: unless-stopped
    depends_on:
      api:
        condition: service_healthy
  
  api:
    build: ./api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: on-failure:3
    environment:
      - DB_HOST=postgres
    depends_on:
      postgres:
        condition: service_healthy
  
  postgres:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Sammud:
1. **Loo health endpoint API'sse:**
   ```javascript
   // api/index.js
   app.get('/health', async (req, res) => {
     try {
       await db.query('SELECT 1');
       res.json({ status: 'healthy', timestamp: new Date() });
     } catch (error) {
       res.status(503).json({ status: 'unhealthy', error: error.message });
     }
   });
   ```

2. **Test health checks:**
   ```bash
   docker-compose up -d
   docker-compose ps  # Vaata health status
   docker inspect myapp_api_1 | grep -A 10 Health
   ```

3. **Simulee failure:**
   ```bash
# Tapa API protsess container sees
   docker-compose exec api kill 1
# Vaata, kuidas Docker automaatselt restartib
   ```

###  Boonus:
- Lisa monitoring (Prometheus health check metrics)
- Loo custom health check script
- Implementeeri circuit breaker pattern
- Lisa notification system (ebaõnnestumise korral Slack alert)

---

## Väljakutse 3: Multi-Environment Setup


### Mida õpid?
- Environment-specific configs
- Docker Compose extends
- Secret management
- Configuration best practices

### Projekt struktuur:
```
multi-env-app/
├── docker-compose.yml           # Base configuration
├── docker-compose.dev.yml       # Dev overrides
├── docker-compose.staging.yml   # Staging overrides
├── docker-compose.prod.yml      # Prod overrides
├── .env.dev                     # Dev environment variables
├── .env.staging                 # Staging environment variables
├── .env.prod                    # Prod environment variables (encrypted!)
└── scripts/
    ├── deploy-dev.sh
    ├── deploy-staging.sh
    └── deploy-prod.sh
```

### Base config (docker-compose.yml):
```yaml
version: '3.8'

services:
  app:
    image: myapp:${VERSION:-latest}
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - LOG_LEVEL=${LOG_LEVEL:-info}
    volumes:
      - ./app:/app
    ports:
      - "${APP_PORT:-3000}:3000"
```

### Dev override (docker-compose.dev.yml):
```yaml
version: '3.8'

services:
  app:
    build:
      context: ./app
      dockerfile: Dockerfile.dev
    volumes:
      - ./app:/app
      - /app/node_modules  # Don't override node_modules
    environment:
      - NODE_ENV=development
      - LOG_LEVEL=debug
      - HOT_RELOAD=true
    command: npm run dev
```

### Prod override (docker-compose.prod.yml):
```yaml
version: '3.8'

services:
  app:
    image: myapp:${VERSION}  # Must specify version
    restart: always
    environment:
      - NODE_ENV=production
      - LOG_LEVEL=error
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`myapp.com`)"
```

### Deploy scripts:
```bash
# scripts/deploy-dev.sh
#!/bin/bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml \
  --env-file .env.dev up -d

# scripts/deploy-prod.sh
#!/bin/bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml \
  --env-file .env.prod up -d --scale app=3
```

###  Boonus:
- Lisa secrets management (Docker secrets või AWS Secrets Manager)
- Loo automated deployment pipeline
- Implementeeri blue-green deployment
- Lisa rollback functionality

---

## Väljakutse 4: Logging ja Monitoring Stack


### Mida õpid?
- Centralized logging
- Metrics collection
- Log aggregation
- Visualization

### Stack komponendid:
```yaml
version: '3.8'

services:
# Your application
  app:
    image: myapp
    logging:
      driver: "fluentd"
      options:
        fluentd-address: localhost:24224
        tag: "app"
    labels:
      - "prometheus-job=app"

# Log aggregation
  fluentd:
    image: fluent/fluentd:latest
    ports:
      - "24224:24224"
    volumes:
      - ./fluentd/conf:/fluentd/etc
      - fluentd-logs:/fluentd/log

# Log storage
  elasticsearch:
    image: elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es-data:/usr/share/elasticsearch/data

# Log visualization
  kibana:
    image: kibana:8.10.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

# Metrics collection
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus:/etc/prometheus
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

# Metrics visualization
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards

volumes:
  fluentd-logs:
  es-data:
  prometheus-data:
  grafana-data:
```

### Prometheus config:
```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:3000']
  
  - job_name: 'docker'
    static_configs:
      - targets: ['host.docker.internal:9323']
```

###  Boonus:
- Lisa alerting (Alertmanager)
- Loo custom Grafana dashboards
- Implementeeri log parsing rules
- Lisa APM (Application Performance Monitoring) - Jaeger

---

## Väljakutse 5: Service Mesh Pattern


### Mida õpid?
- Service mesh concepts
- Load balancing
- Service discovery
- Circuit breakers

### Ülesanne:
```yaml
version: '3.8'

services:
# Traefik reverse proxy
  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--metrics.prometheus=true"
    ports:
      - "80:80"
      - "8080:8080"  # Traefik dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro

# API Gateway
  gateway:
    image: myapp/gateway
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.gateway.rule=Host(`api.localhost`)"
      - "traefik.http.services.gateway.loadbalancer.server.port=3000"
      - "traefik.http.middlewares.gateway-ratelimit.ratelimit.average=100"
      - "traefik.http.routers.gateway.middlewares=gateway-ratelimit"

# Service A (scaled)
  service-a:
    image: myapp/service-a
    deploy:
      replicas: 3
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.service-a.rule=Host(`api.localhost`) && PathPrefix(`/api/a`)"
      - "traefik.http.services.service-a.loadbalancer.server.port=3000"
      - "traefik.http.services.service-a.loadbalancer.healthcheck.path=/health"
      - "traefik.http.services.service-a.loadbalancer.healthcheck.interval=10s"

# Service B (scaled)
  service-b:
    image: myapp/service-b
    deploy:
      replicas: 2
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.service-b.rule=Host(`api.localhost`) && PathPrefix(`/api/b`)"
```

### Test load balancing:
```bash
# Vaata Traefik dashboard
open http://localhost:8080

# Test round-robin load balancing
for i in {1..10}; do
  curl http://api.localhost/api/a/
done
```

###  Boonus:
- Lisa SSL/TLS (Let's Encrypt)
- Implementeeri sticky sessions
- Lisa circuit breaker (Traefik retry & circuit breaker middleware)
- Loo canary deployment strategy

---

## Väljakutse 6: CI/CD Integration


### Mida õpid?
- GitLab CI/Docker integration
- Automated testing
- Image versioning
- Automated deployment

### GitLab CI config (.gitlab-ci.yml):
```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker-compose build
    - docker-compose push
  only:
    - main

test:
  stage: test
  image: docker/compose:latest
  services:
    - docker:dind
  script:
    - docker-compose -f docker-compose.test.yml up --abort-on-container-exit
    - docker-compose -f docker-compose.test.yml down
  only:
    - main

deploy:
  stage: deploy
  image: docker/compose:latest
  script:
    - docker-compose -f docker-compose.prod.yml pull
    - docker-compose -f docker-compose.prod.yml up -d
  only:
    - main
  environment:
    name: production
    url: https://myapp.com
```

### Test compose (docker-compose.test.yml):
```yaml
version: '3.8'

services:
  app:
    build: ./app
    environment:
      - NODE_ENV=test
  
  test-runner:
    image: node:18-alpine
    volumes:
      - ./app:/app
    working_dir: /app
    command: npm test
    depends_on:
      - app
```

###  Boonus:
- Lisa integration tests
- Loo automated rollback on failure
- Implementeeri smoke tests pärast deployment'i
- Lisa deployment notifications (Slack/Discord)

---

## Täiendavad ressursid

### Dokumentatsioon:
- [Docker Compose Best Practices](https://docs.docker.com/compose/production/)
- [Docker Multi-Stage Builds](https://docs.docker.com/develop/develop-images/multistage-build/)
- [Docker Health Checks](https://docs.docker.com/engine/reference/builder/#healthcheck)

### Tööriistad:
- **Dive:** Docker image analyzer - `docker run --rm -it wagoodman/dive:latest <image>`
- **Hadolint:** Dockerfile linter
- **Trivy:** Container security scanner
- **ctop:** Container metrics viewer

### Näited:
- [Awesome Compose](https://github.com/docker/awesome-compose) - Community examples
- [Docker Samples](https://github.com/dockersamples) - Official samples

---

## Näpunäited

1. **Alusta väikesest:** Ära proovi kõike korraga. Lisa funktsionaalsust sammhaaval.
2. **Monitoring on kriit:** Production'is pead teadma, mis toimub.
3. **Security matters:** Ära kasuta `latest` tag'i production'is, scanni image'id.
4. **Test locally:** Kasuta sama compose file'i nii local'is kui production'is (overrides'idega).
5. **Document everything:** README should explain how to run everything.

---

**Edu ja head orkestreerimist!** 

