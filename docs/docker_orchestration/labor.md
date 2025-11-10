# Docker Compose Labor: Multi-container Rakendus

**Eeldused:** Docker + Docker Compose installitud ([vt seadistus.md](seadistus.md))  
**Platvorm:** Ubuntu 22.04 VM, Docker Engine 20.10+, Docker Compose v2  
**Aeg:** 90-120 min

## Õpiväljundid

Pärast seda lab'i oskad:

- Kirjutada `docker-compose.yml` faile
- Käivitada multi-container rakendusi
- Ühendada konteinereid võrkude kaudu
- Kasutada volumes andmete säilitamiseks
- Debugida Docker Compose projekte

---

## Ülevaade

Ehitame TODO rakenduse mis koosneb neljast konteinerist:

```
┌─────────────┐
│   Nginx     │ ← Port 80 (brauser)
│ (Proxy)     │
└──────┬──────┘
       │
   ┌───┴────┬──────────┐
   ▼        ▼          ▼
┌──────┐ ┌─────┐  ┌────────┐
│React │ │ API │  │Postgres│
│(UI)  │ │Node │  │  (DB)  │
└──────┘ └─────┘  └────────┘
```

**Mikr

oteenused:**
- **nginx** - reverse proxy, suunab päringuid
- **frontend** - React UI
- **api** - Node.js REST API
- **database** - PostgreSQL andmebaas

---

## 1. Ettevalmistus (5 min)

### Kontrolli keskkonda

```bash
# Kontrolli Docker
docker --version        # 20.10+
docker compose version  # v2.x

# Test
docker run --rm hello-world
```

❌ **Kui ei tööta** → [seadistus.md](seadistus.md)

### VSCode (optional)

Kui kasutad VSCode Remote SSH → [seadistus.md - VSCode Setup](seadistus.md#vscode-setup)

---

## 2. Projekti Loomine (5 min)

```bash
# Loo projekt
mkdir ~/todo-app && cd ~/todo-app

# Loo struktuur
mkdir -p api database frontend nginx

# Kontrolli
tree -L 1
# .
# ├── api/
# ├── database/
# ├── frontend/
# └── nginx/
```

**Järgnevalt loome failid igas kaustas.**

---

## 3. Andmebaas (10 min)

PostgreSQL hoiab meie TODO'sid. Eraldi konteiner võimaldab andmebaasi uuendada ilma API'd puutumata.

### database/init.sql

```sql
-- UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabel
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test andmed
INSERT INTO todos (title, description) VALUES 
    ('Õpi Docker Compose', 'Multi-container rakendus'),
    ('Tee kodutöö', 'Labori ülesanded'),
    ('Test rakendust', 'Kontrolli et kõik töötab');
```

**Mis see teeb:**
- Loob `todos` tabeli UUID primary key'ga
- Lisab 3 test TODO'd
- Käivitub automaatselt kui PostgreSQL konteiner esimest korda käivitub

---

## 4. API (Backend) (15 min)

Node.js REST API mis ühendab frontendi ja andmebaasi.

### api/.dockerignore

```
node_modules
npm-debug.log
.env
.git
```

### api/package.json

```json
{
  "name": "todo-api",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.0",
    "cors": "^2.8.5"
  }
}
```

### api/server.js

```javascript
const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

console.log('Starting API server...');

// PostgreSQL connection
// OLULINE: host='database' on Docker Compose DNS nimi!
const pool = new Pool({
  host: 'database',      // ← teenuse nimi docker-compose.yml'is
  port: 5432,
  database: 'tododb',
  user: 'todouser',
  password: 'mypassword',
});

pool.on('connect', () => console.log('Connected to PostgreSQL'));
pool.on('error', (err) => console.error('PostgreSQL error:', err));

// Health check
app.get('/health', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({ status: 'OK', database: 'connected', timestamp: result.rows[0].now });
  } catch (err) {
    res.status(503).json({ status: 'ERROR', message: err.message });
  }
});

// GET all todos
app.get('/api/todos', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM todos ORDER BY created_at DESC');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST new todo
app.post('/api/todos', async (req, res) => {
  const { title, description } = req.body;
  if (!title?.trim()) return res.status(400).json({ error: 'Title required' });
  
  try {
    const result = await pool.query(
      'INSERT INTO todos (title, description) VALUES ($1, $2) RETURNING *',
      [title.trim(), description || null]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// PUT update todo
app.put('/api/todos/:id', async (req, res) => {
  const { id } = req.params;
  const { title, description, completed } = req.body;
  if (!title?.trim()) return res.status(400).json({ error: 'Title required' });

  try {
    const result = await pool.query(
      'UPDATE todos SET title=$1, description=$2, completed=$3 WHERE id=$4 RETURNING *',
      [title.trim(), description || null, completed || false, id]
    );
    if (result.rows.length === 0) return res.status(404).json({ error: 'Not found' });
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE todo
app.delete('/api/todos/:id', async (req, res) => {
  try {
    const result = await pool.query('DELETE FROM todos WHERE id=$1 RETURNING id', [req.params.id]);
    if (result.rows.length === 0) return res.status(404).json({ error: 'Not found' });
    res.status(204).send();
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`API server running on port ${PORT}`);
});
```

**Tähtis mõista:**
- `host: 'database'` - kasutab Docker Compose DNS'i, mitte IP aadressi
- API kuulab port 3000, aga see ei ole väljast nähtav (Nginx proxib)

### api/Dockerfile

```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

---

## 5. Frontend (React) (15 min)

React UI mis suhtleb API'ga.

### frontend/.dockerignore

```
node_modules
npm-debug.log
.env
.git
build
```

### frontend/package.json

```json
{
  "name": "todo-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.4.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}
```

### frontend/public/index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Todo App</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
```

### frontend/src/index.js

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<React.StrictMode><App /></React.StrictMode>);
```

### frontend/src/index.css

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background-color: #f5f5f5;
}
```

### frontend/src/App.js

```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/todos');
      setTodos(response.data);
    } catch (err) {
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (e) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    try {
      const response = await axios.post('/api/todos', {
        title: newTitle,
        description: newDescription
      });
      setTodos([response.data, ...todos]);
      setNewTitle('');
      setNewDescription('');
    } catch (err) {
      console.error('Create error:', err);
    }
  };

  const toggleTodo = async (todo) => {
    try {
      const response = await axios.put(`/api/todos/${todo.id}`, {
        ...todo,
        completed: !todo.completed
      });
      setTodos(todos.map(t => t.id === todo.id ? response.data : t));
    } catch (err) {
      console.error('Update error:', err);
    }
  };

  const deleteTodo = async (id) => {
    if (!window.confirm('Delete this todo?')) return;
    try {
      await axios.delete(`/api/todos/${id}`);
      setTodos(todos.filter(t => t.id !== id));
    } catch (err) {
      console.error('Delete error:', err);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="App">
      <header>
        <h1>Todo App</h1>
        <p>Docker Compose Lab</p>
      </header>
      
      <div className="container">
        <form onSubmit={addTodo} className="todo-form">
          <h2>Add New Todo</h2>
          <input
            type="text"
            placeholder="What needs to be done?"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            required
          />
          <textarea
            placeholder="Description (optional)"
            value={newDescription}
            onChange={(e) => setNewDescription(e.target.value)}
            rows="3"
          />
          <button type="submit">Add Todo</button>
        </form>

        <div className="todos-section">
          <h2>My Todos ({todos.length})</h2>
          {todos.length === 0 ? (
            <p className="no-todos">No todos yet!</p>
          ) : (
            <div className="todos-list">
              {todos.map(todo => (
                <div key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                  <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={() => toggleTodo(todo)}
                  />
                  <div className="todo-content">
                    <h3>{todo.title}</h3>
                    {todo.description && <p>{todo.description}</p>}
                  </div>
                  <button onClick={() => deleteTodo(todo.id)}>×</button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
```

### frontend/src/App.css

```css
.App {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
}

header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
}

.container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
  width: 100%;
}

.todo-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.todo-form input,
.todo-form textarea {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
}

.todo-form button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.todos-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.no-todos {
  text-align: center;
  color: #999;
  padding: 2rem;
}

.todos-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.todo-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
}

.todo-item.completed .todo-content h3 {
  text-decoration: line-through;
  color: #999;
}

.todo-content {
  flex: 1;
}

.todo-content h3 {
  margin: 0 0 0.5rem 0;
}

.todo-content p {
  color: #666;
  margin: 0;
}

.todo-item button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  opacity: 0.6;
}

.todo-item button:hover {
  opacity: 1;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  font-size: 1.5rem;
}
```

### frontend/Dockerfile

```dockerfile
# Multi-stage build
FROM node:16-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Serve with nginx
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html

# React Router support
RUN echo 'server { \
    listen 80; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Multi-stage build:**
1. Stage 1: Build React app (npm run build)
2. Stage 2: Serve static files nginx'iga
3. Tulemus: väike image (~25MB vs ~400MB)

---

## 6. Nginx (Reverse Proxy) (5 min)

Nginx on värav mis suunab päringuid õigetesse konteineritesse.

### nginx/nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:80;
    }

    upstream api {
        server api:3000;
    }

    server {
        listen 80;

        # API - kõik mis algab /api
        location /api {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Health check
        location /health {
            proxy_pass http://api/health;
        }

        # Frontend - kõik ülejäänud
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
        }
    }
}
```

**Kuidas see töötab:**
- `http://localhost/` → frontend konteiner
- `http://localhost/api/todos` → api konteiner
- `http://localhost/health` → api konteiner

---

## 7. Docker Compose (15 min)

Nüüd liidame kõik kokku! See on labori **kõige olulisem osa**.

### docker-compose.yml

```yaml
version: '3.8'

services:
  # PostgreSQL andmebaas
  database:
    image: postgres:14-alpine
    container_name: todo_db
    environment:
      POSTGRES_DB: tododb
      POSTGRES_USER: todouser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todouser -d tododb"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Node.js API
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: todo_api
    depends_on:
      database:
        condition: service_healthy
    networks:
      - backend
      - frontend
    restart: unless-stopped

  # React Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: todo_frontend
    networks:
      - frontend
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: todo_nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
      - frontend
    networks:
      - frontend
      - backend
    restart: unless-stopped

networks:
  backend:
    driver: bridge
  frontend:
    driver: bridge

volumes:
  postgres_data:
    driver: local
```

**Selgitus:**

**services** - 4 konteinerit:
- `database` - kasutab valmis image't `postgres:14-alpine`
- `api`, `frontend` - ehitavad custom image'id Dockerfile'idest
- `nginx` - kasutab valmis image't + custom config

**networks** - 2 võrku:
- `backend` - database + api (frontend ei näe DB'd otse)
- `frontend` - api + frontend + nginx

**volumes** - 1 named volume:
- `postgres_data` - andmebaasi andmed jäävad alles

**depends_on + healthcheck:**
- API ootab kuni DB on `healthy` (mitte ainult käivitunud!)
- Nginx ootab kuni API ja frontend käivitunud

**restart: unless-stopped:**
- Kui konteiner crashib, käivitab automaatselt uuesti

---

## 8. Käivitamine (10 min)

```bash
cd ~/todo-app

# Kontrolli et kõik failid on olemas
find . -name "*.yml" -o -name "Dockerfile" -o -name "*.js" -o -name "*.sql" -o -name "*.conf"

# Build ja käivita
docker compose up --build

# OOTAD:
# [+] Building...
# [+] Running 4/4
#  ✔ Container todo_db        Started
#  ✔ Container todo_api       Started  
#  ✔ Container todo_frontend  Started
#  ✔ Container todo_nginx     Started
```

**Esimene kord võtab 5-10 min** - Docker ehitab image'id.

### Vaata logisid

Uus terminal (jäta esimene jooksma):

```bash
# Staatus
docker compose ps

# Kõik logid
docker compose logs

# Ainult API
docker compose logs api

# Live logid
docker compose logs -f
```

---

## 9. Testimine (10 min)

### VM-ist

```bash
# Health check
curl http://localhost/health
# {"status":"OK","database":"connected",...}

# API
curl http://localhost/api/todos
# [{"id":"...","title":"Õpi Docker Compose",...},...]

# HTML
curl http://localhost/
# <!DOCTYPE html>...
```

### Brauserist

**Kui VM IP on teada:**

```bash
# VM-is
ip addr show | grep "inet " | grep -v 127.0.0.1
# inet 192.168.1.100/24
```

HOST masinas ava: `http://192.168.1.100`

**Kui VirtualBox port forwarding:**

HOST masinas ava: `http://localhost:8080`

([Port forwarding setup](seadistus.md#port-forwarding-virtualbox))

### Funktsionaalsus

1. ✅ Lisa uus TODO
2. ✅ Märgi completed (checkbox)
3. ✅ Kustuta TODO
4. ✅ Refresh lehte (F5) - andmed püsivad!

---

## 10. Docker Compose Käsud (5 min)

```bash
# KÄIVITAMINE
docker compose up              # foreground
docker compose up -d           # background (detached)
docker compose up --build      # rebuild image'd

# VAATAMINE
docker compose ps              # konteinerid
docker compose logs            # logid
docker compose logs -f api     # API logid live
docker compose top             # protsessid

# PEATAMINE
docker compose stop            # peata (jäta konteinerid alles)
docker compose start           # käivita uuesti
docker compose restart api     # restart üks teenus

# EEMALDAMINE
docker compose down            # peata + eemalda konteinerid
docker compose down -v         # + kustuta volumes (ANDMED KAOVAD!)

# DEBUGGING
docker compose exec api sh     # shell API konteineris
docker compose config          # valideeri YAML

# SKALEER IMINE
docker compose up --scale api=3  # käivita 3 API instantsi
```

---

## 11. Troubleshooting (10 min)

### Probleem: API crashib

```bash
# Vaata logisid
docker compose logs api

# Kui näed: "Cannot connect to database"
# Põhjus: DB pole veel valmis

# Lahendus 1: Oota ja restart
docker compose restart api

# Lahendus 2: Kontrolli healthcheck
docker compose ps
# database peaks olema (healthy)
```

### Probleem: Frontend blank page

```bash
# Browser console (F12) → Network tab
# Kas API päringud fail'ivad?

# Kontrolli nginx config
docker compose logs nginx

# Restart nginx
docker compose restart nginx
```

### Probleem: Port 80 busy

```bash
# Kontrolli mis kasutab
sudo lsof -i :80

# Muuda porti docker-compose.yml's
ports:
  - "8080:80"

# Siis: http://localhost:8080
```

### Probleem: Permission denied

```bash
# Lisa end docker gruppi
sudo usermod -aG docker $USER

# Logi välja ja sisse
# VÕI restart VM
```

Rohkem troubleshooting'ut: [seadistus.md - Troubleshooting](seadistus.md#troubleshooting)

---

## 12. Harjutused (20 min)

### Harjutus 1: Lisa Redis cache

Muuda `docker-compose.yml`:

```yaml
services:
  # ... existing services ...
  
  redis:
    image: redis:alpine
    container_name: todo_redis
    networks:
      - backend
    restart: unless-stopped
```

```bash
docker compose up -d redis

# Test
docker compose exec redis redis-cli ping
# PONG
```

### Harjutus 2: Environment failid

Loo `.env` fail:

```bash
# .env
DB_NAME=tododb
DB_USER=todouser
DB_PASS=mypassword
```

Muuda `docker-compose.yml`:

```yaml
database:
  environment:
    POSTGRES_DB: ${DB_NAME}
    POSTGRES_USER: ${DB_USER}
    POSTGRES_PASSWORD: ${DB_PASS}
```

```bash
docker compose config  # vaata parsed config'i
docker compose up -d
```

### Harjutus 3: Development mode

API live reload:

```yaml
api:
  volumes:
    - ./api:/app
    - /app/node_modules
  command: npm run dev  # kui lisad package.json'i
```

### Harjutus 4: Skaleerime API

```bash
# Käivita 3 API instantsi
docker compose up -d --scale api=3

# Vaata
docker compose ps
# todo_api_1, todo_api_2, todo_api_3

# Nginx teeb automaatselt load balancing'u!
```

---

## 13. Cleanup

```bash
# Peata kõik
docker compose down

# Kustuta ka andmed
docker compose down -v

# Täielik puhastus
docker system prune -a --volumes
# HOIATUS: Kustutab KÕIK Docker ressursid!
```

---

## Kokkuvõte

### Mida õppisime

**Docker Compose kontseptsioonid:**
- ✅ **services** - rakenduse komponendid
- ✅ **networks** - konteinerite suhtlus
- ✅ **volumes** - andmete püsimine
- ✅ **depends_on** - teenuste järjekord
- ✅ **healthcheck** - teenuse valmidus

**Praktiline:**
- ✅ Multi-container rakenduse ehitamine
- ✅ Service discovery (DNS)
- ✅ Debugging ja troubleshooting
- ✅ Compose käsud

**Arhitektuur:**
- ✅ Multi-tier: Database → API → Frontend → Proxy
- ✅ Mikroteenused isolatsioon
- ✅ Võrkude eraldamine (backend/frontend)

### Järgmised sammud

1. ✅ Mõistad Docker Compose põhimõtteid
2. → **Kodutöö:** Ehita oma multi-container rakendus
3. → **Järgmine teema:** Kubernetes orkestreerimiseks

---

## Kasulikud Lingid

- [Docker Compose dokumentatsioon](https://docs.docker.com/compose/)
- [Compose file reference](https://docs.docker.com/compose/compose-file/)
- [Docker Hub](https://hub.docker.com) - image'id
- [Awesome Compose](https://github.com/docker/awesome-compose) - näited

---

**Küsimused?** Küsi õpetajalt või õpilaskaaslastelt!
