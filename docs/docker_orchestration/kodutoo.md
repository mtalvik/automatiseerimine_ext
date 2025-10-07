# Docker Compose Kodutöö: Täienda Todo Rakendust

Selles kodutöös täiendad labori Todo rakendust uute teenustega ja konfigureeritud keskkondadega. Rakendad õpitud Docker Compose oskusi praktilises stsenaariumis. See ülesanne võtab umbes 1.5 tundi.

**Eeldused:** Lab "Docker Compose" läbitud, põhiline Todo rakendus töötab  
**Esitamine:** GitHub repository link + 3 screenshot'i + refleksioon  
**Tähtaeg:** Järgmise nädala algus

---

## Ülesande kirjeldus

Võta oma labori Todo rakendus ja täienda seda:
1. Lisa Redis cache teenus
2. Seadista development ja production keskkonnad
3. Lisa health checks kõigile teenustele
4. Loo deployment script
5. Dokumenteeri muudatused

---

## 1. Redis Cache lisamine

### 1.1 Miks Redis?

Todo rakendus pärib praegu alati andmebaasist. Lisa Redis cache et kiirendada `/api/todos` päringuid.

### 1.2 Muuda `docker-compose.yml`

Lisa Redis teenus:
```yaml
  redis:
    image: redis:7-alpine
    container_name: todo_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    restart: unless-stopped
    command: redis-server --appendonly yes

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

### 1.3 Muuda API koodi

Muuda `api/package.json` - lisa dependency:
```json
{
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.0",
    "cors": "^2.8.5",
    "redis": "^4.6.0"
  }
}
```

Muuda `api/server.js` - lisa Redis cache:
```javascript
const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const redis = require('redis');

const app = express();
const PORT = 3000;
const CACHE_TTL = 60; // 60 seconds

// Middleware
app.use(cors());
app.use(express.json());

console.log('Starting API server...');

// PostgreSQL connection
const pool = new Pool({
  host: 'database',
  port: 5432,
  database: 'tododb',
  user: 'todouser',
  password: 'mypassword',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

// Redis connection
let redisClient;
(async () => {
  redisClient = redis.createClient({
    socket: {
      host: 'redis',
      port: 6379
    }
  });

  redisClient.on('error', (err) => console.error('Redis Client Error', err));
  redisClient.on('connect', () => console.log('Connected to Redis'));

  await redisClient.connect();
})();

pool.on('connect', () => {
  console.log('Connected to PostgreSQL');
});

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    const dbResult = await pool.query('SELECT NOW()');
    const redisResult = await redisClient.ping();
    res.json({ 
      status: 'OK', 
      database: 'connected',
      redis: redisResult === 'PONG' ? 'connected' : 'disconnected',
      timestamp: dbResult.rows[0].now 
    });
  } catch (err) {
    console.error('Health check failed:', err);
    res.status(503).json({ 
      status: 'ERROR', 
      message: err.message 
    });
  }
});

// GET all todos - WITH CACHE
app.get('/api/todos', async (req, res) => {
  console.log('GET /api/todos');
  try {
    // Check cache first
    const cachedTodos = await redisClient.get('todos:all');
    if (cachedTodos) {
      console.log('Cache HIT');
      return res.json(JSON.parse(cachedTodos));
    }

    console.log('Cache MISS - fetching from DB');
    const result = await pool.query(
      'SELECT * FROM todos ORDER BY created_at DESC'
    );
    
    // Store in cache
    await redisClient.setEx('todos:all', CACHE_TTL, JSON.stringify(result.rows));
    
    console.log(`Found ${result.rows.length} todos`);
    res.json(result.rows);
  } catch (err) {
    console.error('Error fetching todos:', err);
    res.status(500).json({ error: err.message });
  }
});

// GET single todo
app.get('/api/todos/:id', async (req, res) => {
  const { id } = req.params;
  console.log(`GET /api/todos/${id}`);
  
  try {
    const result = await pool.query(
      'SELECT * FROM todos WHERE id = $1',
      [id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Todo not found' });
    }
    
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error fetching todo:', err);
    res.status(500).json({ error: err.message });
  }
});

// POST new todo - INVALIDATE CACHE
app.post('/api/todos', async (req, res) => {
  const { title, description } = req.body;
  console.log('POST /api/todos', { title, description });
  
  if (!title || title.trim() === '') {
    return res.status(400).json({ error: 'Title is required' });
  }

  try {
    const result = await pool.query(
      'INSERT INTO todos (title, description) VALUES ($1, $2) RETURNING *',
      [title.trim(), description || null]
    );
    
    // Invalidate cache
    await redisClient.del('todos:all');
    console.log('Cache invalidated');
    
    console.log('Created todo:', result.rows[0].id);
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Error creating todo:', err);
    res.status(500).json({ error: err.message });
  }
});

// PUT update todo - INVALIDATE CACHE
app.put('/api/todos/:id', async (req, res) => {
  const { id } = req.params;
  const { title, description, completed } = req.body;
  console.log(`PUT /api/todos/${id}`, { title, description, completed });

  if (!title || title.trim() === '') {
    return res.status(400).json({ error: 'Title is required' });
  }

  try {
    const result = await pool.query(
      'UPDATE todos SET title=$1, description=$2, completed=$3 WHERE id=$4 RETURNING *',
      [title.trim(), description || null, completed || false, id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Todo not found' });
    }

    // Invalidate cache
    await redisClient.del('todos:all');

    console.log('Updated todo:', id);
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error updating todo:', err);
    res.status(500).json({ error: err.message });
  }
});

// DELETE todo - INVALIDATE CACHE
app.delete('/api/todos/:id', async (req, res) => {
  const { id } = req.params;
  console.log(`DELETE /api/todos/${id}`);

  try {
    const result = await pool.query(
      'DELETE FROM todos WHERE id=$1 RETURNING id',
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Todo not found' });
    }

    // Invalidate cache
    await redisClient.del('todos:all');

    console.log('Deleted todo:', id);
    res.status(204).send();
  } catch (err) {
    console.error('Error deleting todo:', err);
    res.status(500).json({ error: err.message });
  }
});

// 404 handler
app.use((req, res) => {
  console.log('404:', req.method, req.url);
  res.status(404).json({ error: 'Endpoint not found' });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`API server running on port ${PORT}`);
  console.log(`  Health: http://localhost:${PORT}/health`);
  console.log(`  Todos:  http://localhost:${PORT}/api/todos`);
});
```

### 1.4 Rebuild ja test
```bash
# Rebuild API konteiner
docker-compose build api

# Käivita kõik
docker-compose up -d

# Kontrolli et Redis töötab
docker-compose ps
docker-compose logs redis

# Test cache
curl http://localhost/api/todos  # Cache MISS
curl http://localhost/api/todos  # Cache HIT
```

**SCREENSHOT 1:** API logid kus näha "Cache HIT" ja "Cache MISS"

---

## 2. Health Checks

### 2.1 Lisa health checks

Muuda `docker-compose.yml` - lisa health checks API'le ja frontend'ile:
```yaml
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: todo_api
    environment:
      NODE_ENV: production
    depends_on:
      database:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend
      - frontend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: todo_frontend
    networks:
      - frontend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 2.2 Test health checks
```bash
docker-compose up -d

# Oota 30 sekundit ja kontrolli
docker-compose ps

# Peaks näitama "healthy" staatust
docker inspect todo_api | grep -A 10 Health
```

**SCREENSHOT 2:** `docker-compose ps` kus kõik teenused on "healthy"

---

## 3. Development vs Production

### 3.1 Loo `docker-compose.dev.yml`

Development keskkond kus kood on bind-mounted (live reload):
```yaml
version: '3.8'

services:
  api:
    volumes:
      - ./api:/app
      - /app/node_modules
    environment:
      NODE_ENV: development
    command: sh -c "npm install && node server.js"

  frontend:
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
    environment:
      NODE_ENV: development
```

### 3.2 Loo `.env.dev` ja `.env.prod`

`.env.dev`:
```bash
COMPOSE_PROJECT_NAME=todo-dev
DB_PASSWORD=devpassword
```

`.env.prod`:
```bash
COMPOSE_PROJECT_NAME=todo-prod
DB_PASSWORD=prodpassword123
```

### 3.3 Test
```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up -d

# Production
docker-compose --env-file .env.prod up -d
```

---

## 4. Deployment Script

### 4.1 Loo `deploy.sh
`
```bash
#!/bin/bash

set -e

ENV=${1:-dev}

case $ENV in
  dev)
    echo "Deploying DEVELOPMENT..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up -d
    ;;
  prod)
    echo "Deploying PRODUCTION..."
    docker-compose --env-file .env.prod up -d --build
    ;;
  stop)
    echo "Stopping services..."
    docker-compose down
    ;;
  logs)
    docker-compose logs -f
    ;;
  status)
    docker-compose ps
    ;;
  *)
    echo "Usage: $0 {dev|prod|stop|logs|status}"
    exit 1
    ;;
esac

echo "Done!"
docker-compose ps
`
`
`
```bash
chmod +x deploy.sh
```

### 4.2 Kasuta
```bash
./deploy.sh dev     # Development
./deploy.sh prod    # Production
./deploy.sh status  # Vaata staatust
./deploy.sh logs    # Vaata logisid
./deploy.sh stop    # Peata
```

---

## 5. Dokumentatsioon

### 5.1 Uuenda `README.md
`
```markdown
# Todo App with Redis Cache

## Architecture
```
Nginx (80) → Frontend → API → Database
                        ↓
                      Redis
```

## Services

- **nginx**: Reverse proxy (port 80)
- **frontend**: React app (internal)
- **api**: Node.js REST API (internal)
- **database**: PostgreSQL 14 (internal)
- **redis**: Redis cache (internal)

## Quick Start

### Development
```bash
./deploy.sh dev
```

### Production
```bash
./deploy.sh prod
```

## Testing
```bash
curl http://localhost/health
curl http://localhost/api/todos
```

## Cache Testing
```bash
# First request - cache MISS
time curl http://localhost/api/todos

# Second request - cache HIT (faster)
time curl http://localhost/api/todos
```

## Environment Variables

Create `.env.dev` and `.env.prod`:
```bash
COMPOSE_PROJECT_NAME=todo-dev
DB_PASSWORD=yourpassword
```

## Health Checks

All services have health checks:
- Database: `pg_isready`
- Redis: `redis-cli ping`
- API: `GET /health`
- Frontend: HTTP check

Check status:
```bash
docker-compose ps
```
```

**SCREENSHOT 3:** Brauseris töötav rakendus + cache testimine terminalis

---

## Esitamine

### GitHub repository sisaldab:
```
docker-compose-homework/
├── api/
│   ├── Dockerfile
│   ├── package.json
│   └── server.js (MUUDETUD - Redis cache)
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── nginx/
│   └── nginx.conf
├── database/
│   └── init.sql
├── docker-compose.yml (MUUDETUD - Redis teenus)
├── docker-compose.dev.yml (UUS)
├── .env.dev (UUS)
├── .env.prod (UUS)
├── .env.example (UUS)
├── deploy.sh (UUS)
└── README.md (UUENDATUD)
```

### 3 Screenshot'i:

1. API logid kus näha cache HIT ja MISS
2. `docker-compose ps` kus kõik teenused "healthy"
3. Brauser - töötav rakendus + cache testimine terminalis

### GitHub link:
`https://github.com/username/docker-compose-homework`

---

## Refleksioon

Lisa oma README.md faili lõppu peatükk "Refleksioon" ja vasta järgmistele küsimustele (2-3 lausega igaühele):

### Küsimused:

1. **Mis oli selle kodutöö juures kõige raskem ja kuidas sa selle lahendasid?**

2. **Milline Docker Compose kontseptsioon oli sulle kõige suurem "ahaa!"-elamus ja miks?**

3. **Kuidas saaksid Docker Compose'i kasutada oma teistes projektides või tööl?**

4. **Kui peaksid oma sõbrale selgitama, mis on Docker Compose ja miks see on kasulik, siis mida ütleksid?**

5. **Mis oli selle projekti juures kõige lõbusam või huvitavam osa?**

---

## Kontrollnimekiri

Kontrolli need asjad enne esitamist:

- [ ] GitHubis on avalik repositoorium
- [ ] Redis teenus on lisatud ja töötab
- [ ] API kasutab Redis cache'i (näha logides)
- [ ] Kõigil teenustel on health checks
- [ ] docker-compose.dev.yml on loodud
- [ ] Environment failid on seadistatud (.env.example on repo's)
- [ ] deploy.sh script töötab
- [ ] 3 screenshot'i on tehtud
- [ ] README.md sisaldab:
  - [ ] Arhitektuuri diagramm
  - [ ] Quick start juhised (./deploy.sh)
  - [ ] Cache testimine
  - [ ] Refleksioon (5 küsimuse vastused)
- [ ] Kõik muudatused on GitHubi pushitud

---

## Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **Redis Cache** | 30% | Redis teenus lisatud, API kasutab cache'i, cache invalidation töötab |
| **Health Checks** | 20% | Kõigil teenustel on health checks, depends_on kasutab service_healthy |
| **Multi-Environment** | 20% | docker-compose.dev.yml ja .env failid, deploy script |
| **Dokumentatsioon** | 20% | README selge, screenshot'id tõestavad töötamist |
| **Refleksioon** | 10% | 5 küsimust vastatud, sisukas, näitab mõistmist |

**Kokku: 100%**

---

## Troubleshooting

### Redis connection error:
```bash
# Kontrolli kas Redis töötab
docker-compose logs redis

# Restart API
docker-compose restart api
```

### Cache ei tööta:
```bash
# Kontrolli API logisid
docker-compose logs api | grep -i cache

# Test Redis käsitsi
docker-compose exec redis redis-cli ping
```

### Health check fails:
```bash
# Vaata täpsemalt
docker inspect todo_api | grep -A 20 Health

# Kontrolli kas endpoint töötab
docker-compose exec api wget -O- http://localhost:3000/health
```

---

## Kasulikud lingid

- Redis Docker: https://hub.docker.com/_/redis
- Node Redis client: https://github.com/redis/node-redis
- Docker Compose health checks: https://docs.docker.com/compose/compose-file/05-services/#healthcheck
- Cache strategies: https://redis.io/docs/manual/patterns/