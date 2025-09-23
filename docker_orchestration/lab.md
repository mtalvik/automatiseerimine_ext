# Lab: Docker Compose - Ehitame päris rakenduse

## 🎯 Mida ja miks me ehitame?

Täna ehitame **päris töötava rakenduse** - ülesannete halduse süsteemi (todo app). See on piisavalt lihtne mõistmiseks, aga samas piisavalt keeruline, et õppida kõiki olulisi Docker Compose kontsepte.

**Miks multi-container arhitektuur?**

Kujutage ette, et olete väike meeskond, kes ehitab startup'i. Alguses panete kõik ühte serverisse - andmebaas, API, frontend. Kõik töötab... kuni ei tööta. Mis juhtub kui:
- Andmebaas vajab rohkem mälu, aga frontend ei vaja?
- Tahate uuendada Node.js versiooni API jaoks, aga ei taha puutuda andmebaasi?
- Üks arendaja tahab töödata ainult frontend'iga?

Lahendus: **teenuste eraldamine**. Iga komponent oma konteineris, iga meeskonna liige saab arendada oma osa, iga teenust saab skaleerida iseseisvalt.

---

## 📁 Projekti struktuur

Meie rakendus koosneb järgmistest komponentidest:

```
mariatesttalvik/
├── api/
│   ├── .dockerignore      # Millised failid Docker ei peaks kopeerima
│   ├── Dockerfile          # Kuidas ehitada API konteiner
│   ├── package.json        # Node.js sõltuvused
│   └── server.js          # API loogika
├── database/
│   └── init.sql           # Andmebaasi algseadistus
├── frontend/
│   ├── .dockerignore      
│   ├── Dockerfile         # Multi-stage build React'i jaoks
│   ├── package.json       
│   ├── public/
│   │   └── index.html     # React'i HTML template
│   └── src/
│       ├── App.css        # Stiilid
│       ├── App.js         # Põhikomponent
│       └── index.js       # React'i sisendpunkt
├── nginx/
│   ├── .dockerignore
│   └── nginx.conf         # Reverse proxy konfiguratsioon
├── .dockerignore          # Projekti üldine dockerignore
├── .env.example           # Näidis keskkonnamuutujad
├── .gitignore            # Git'i jaoks ignoreeritavad failid
└── docker-compose.yml     # Orkestreerib kõiki teenuseid
```

---

## 🚀 Alustame ehitamist

### 1. Projekti juurkausta failid

#### .gitignore
```gitignore
# Dependencies
node_modules/
*/node_modules/

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Build outputs
dist/
build/
*.log
```

#### .dockerignore (juurkaustas)
```dockerignore
# Miks need failid?
# Docker kopeerib kogu konteksti konteinerisse
# See võib olla VÄGA aeglane kui node_modules kaasas
node_modules
*/node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.DS_Store
.vscode
.idea
```

#### .env.example
```bash
# Keskkonnamuutujad - ära kunagi pane paroole Git'i!
NODE_ENV=
DB_PASSWORD=
REDIS_PASSWORD=
```

#### .env (looge ise, see EI lähe Git'i)
```bash
NODE_ENV=development
DB_PASSWORD=secretpassword123
REDIS_PASSWORD=redispass123
```

#### docker-compose.yml
```yaml
version: '3.8'

# Miks versioon 3.8? 
# - 3.x on production-ready
# - 3.8+ toetab kõiki vajalikke feature'id

services:
  # Andmebaas - kõige aluseks
  # Miks esimesena? Sest teised sõltuvad sellest
  database:
    image: postgres:14-alpine
    # Miks alpine? 10x väiksem kui tavaline image (150MB vs 1.5GB)
    container_name: todo_db
    environment:
      # Need muutujad PostgreSQL ootab
      POSTGRES_DB: tododb
      POSTGRES_USER: todouser
      POSTGRES_PASSWORD: ${DB_PASSWORD:-defaultpass}
      # ${VAR:-default} tähendab: võta .env failist või kasuta defaulti
    volumes:
      # Andmed peavad püsima ka peale konteineri restardi
      - postgres_data:/var/lib/postgresql/data
      # Init skript käivitub esimesel käivitusel
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - backend_network
    healthcheck:
      # Miks healthcheck? depends_on ei oota muidu kuni DB päriselt töötab
      test: ["CMD-SHELL", "pg_isready -U todouser -d tododb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  # Redis cache
  redis:
    image: redis:7-alpine
    container_name: todo_redis
    command: redis-server --appendonly yes --maxmemory 100mb --maxmemory-policy allkeys-lru
    # --appendonly yes: salvesta andmed kettale (persistence)
    # --maxmemory 100mb: ära kasuta üle 100MB RAM-i
    # --maxmemory-policy allkeys-lru: kui mälu täis, kustuta vähemkasutatud
    volumes:
      - redis_data:/data
    networks:
      - backend_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  # API server
  api:
    build: 
      context: ./api
      dockerfile: Dockerfile
    container_name: todo_api
    environment:
      NODE_ENV: ${NODE_ENV:-development}
      PORT: 3000
      DATABASE_URL: postgres://todouser:${DB_PASSWORD:-defaultpass}@database:5432/tododb
      # Miks @database, mitte @localhost? 
      # Docker Compose loob DNS kirje iga teenuse jaoks
      REDIS_URL: redis://redis:6379
    volumes:
      # Development jaoks - hot reload
      - ./api:/app
      - /app/node_modules  # Ära üle kirjuta node_modules
    depends_on:
      # Oota kuni need on "healthy", mitte lihtsalt käivitunud
      database:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend_network
      - frontend_network

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: todo_frontend
    environment:
      NODE_ENV: production
      REACT_APP_API_URL=  # OLULINE! Tühi = kasutab suhtelisi URL-e
    volumes:
      - ./frontend:/app
      - /app/node_modules
    networks:
      - frontend_network

  # Nginx - värav välismaailma
  nginx:
    image: nginx:alpine
    container_name: todo_nginx
    ports:
      - "80:80"      # HTTP
      - "443:443"    # HTTPS (tulevikuks)
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      # :ro tähendab read-only - turvalisuse jaoks
    depends_on:
      - api
      - frontend
    networks:
      - frontend_network
      - backend_network

networks:
  # Miks kaks võrku?
  # Turvalisus - andmebaas ei pea olema frontend võrgus
  backend_network:
    driver: bridge
  frontend_network:
    driver: bridge

volumes:
  # Named volumes - Docker haldab, püsivad restart'ide vahel
  postgres_data:
  redis_data:
```

---

## 🗄️ Andmebaasi seadistamine

#### database/init.sql
```sql
-- Miks UUID primary key, mitte serial?
-- 1. Turvalisem - ei saa ennustada järgmist ID-d
-- 2. Saab genereerida kliendi poolel
-- 3. Töötab hästi distributed süsteemides

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Todos tabel
CREATE TABLE IF NOT EXISTS todos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Miks indeksid?
-- Ilma indeksita peab DB iga päringu puhul kogu tabeli läbi vaatama
CREATE INDEX idx_todos_completed ON todos(completed);
CREATE INDEX idx_todos_created_at ON todos(created_at DESC);

-- Trigger updated_at välja uuendamiseks
-- Miks trigger? Garanteerib, et updated_at on alati õige
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_todos_updated_at 
    BEFORE UPDATE ON todos 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Lisa test andmed
INSERT INTO todos (title, description) VALUES 
    ('Õpi Docker Compose', 'Ehita multi-container rakendus'),
    ('Kirjuta dokumentatsioon', 'Lisa README ja kommentaarid'),
    ('Test rakendust', 'Kirjuta testid ja kontrolli kõik üle');
```

---

## 🔧 API teenus

#### api/.dockerignore
```dockerignore
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.DS_Store
.vscode
.idea
```

#### api/package.json
```json
{
  "name": "todo-api",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",      // Web framework
    "pg": "^8.11.0",           // PostgreSQL klient
    "redis": "^4.6.7",         // Redis klient cache jaoks
    "cors": "^2.8.5",          // Lubab frontend'il API-ga suhelda
    "helmet": "^7.0.0",        // Lisab turvalisuse headereid
    "morgan": "^1.10.0",       // Logib kõik päringud (debugging)
    "joi": "^17.9.2"           // Valideerib sisendeid - ÄRA KUNAGI usalda kasutaja sisendit!
  },
  "devDependencies": {
    "nodemon": "^2.0.22"       // Restardib serveri kui kood muutub
  }
}
```

#### api/server.js
```javascript
const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const Joi = require('joi');

const app = express();
const port = process.env.PORT || 3000;

// Miks middleware'id selles järjekorras?
// 1. Turvalisus (helmet) - esimesena, kaitseb kõike
// 2. Logimine (morgan) - logib kõik päringud
// 3. CORS - lubab browser'il API-ga suhelda
// 4. JSON parser - parsib request body
app.use(helmet());
app.use(morgan('combined'));
app.use(cors());
app.use(express.json());

// PostgreSQL connection pool
// Miks pool, mitte üks connection?
// Pool hoiab mitut ühendust avatuna, kiirem
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,  // Max 20 ühendust
  idleTimeoutMillis: 30000,  // Sulge idle ühendused 30s pärast
  connectionTimeoutMillis: 2000,  // Timeout uue ühenduse loomisel
});

// Test database connection
pool.on('connect', () => {
  console.log('Connected to PostgreSQL');
});

pool.on('error', (err) => {
  console.error('PostgreSQL error:', err);
  process.exit(-1);  // Suri andmebaas, suri ka API
});

// Redis client
const redisClient = redis.createClient({
  url: process.env.REDIS_URL,
  socket: {
    reconnectStrategy: (retries) => {
      // Proovi uuesti üha harvemini
      if (retries > 10) return false;
      return Math.min(retries * 50, 500);
    }
  }
});

// Redis error handling
redisClient.on('error', (err) => console.log('Redis error:', err));
redisClient.on('connect', () => console.log('Connected to Redis'));

// Connect to Redis
(async () => {
  try {
    await redisClient.connect();
  } catch (err) {
    console.error('Failed to connect to Redis:', err);
    // Jätkame ilma cache'ita - better than crashing
  }
})();

// Input validation schemas
// Miks Joi? Valideerib ja puhastab sisendid
const todoSchema = Joi.object({
  title: Joi.string().min(1).max(255).required(),
  description: Joi.string().max(1000).allow('', null).optional(),
  completed: Joi.boolean().optional()
});

// Health check endpoint
// Kubernetes/Docker vajab seda
app.get('/health', async (req, res) => {
  const health = {
    uptime: process.uptime(),
    timestamp: Date.now(),
    status: 'OK',
    services: {}
  };

  try {
    // Check database
    const dbResult = await pool.query('SELECT NOW()');
    health.services.database = 'healthy';
  } catch (err) {
    health.services.database = 'unhealthy';
    health.status = 'DEGRADED';
  }

  try {
    // Check Redis
    await redisClient.ping();
    health.services.redis = 'healthy';
  } catch (err) {
    health.services.redis = 'unhealthy';
    // Redis pole kriitiline, jätkame
  }

  const statusCode = health.status === 'OK' ? 200 : 503;
  res.status(statusCode).json(health);
});

// GET all todos
app.get('/api/todos', async (req, res) => {
  try {
    // 1. Check cache first
    const cacheKey = 'todos:all';
    
    if (redisClient.isOpen) {
      const cached = await redisClient.get(cacheKey);
      if (cached) {
        console.log('Cache hit!');
        return res.json(JSON.parse(cached));
      }
    }

    // 2. Query database
    console.log('Cache miss, querying database');
    const result = await pool.query(`
      SELECT 
        id, 
        title, 
        description, 
        completed, 
        created_at, 
        updated_at 
      FROM todos 
      ORDER BY created_at DESC
    `);

    // 3. Cache result
    if (redisClient.isOpen) {
      await redisClient.setEx(
        cacheKey, 
        60,  // TTL 60 seconds
        JSON.stringify(result.rows)
      );
    }

    res.json(result.rows);
  } catch (err) {
    console.error('Error fetching todos:', err);
    res.status(500).json({ 
      error: 'Failed to fetch todos',
      details: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
  }
});

// GET single todo
app.get('/api/todos/:id', async (req, res) => {
  const { id } = req.params;

  // Validate UUID format
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  if (!uuidRegex.test(id)) {
    return res.status(400).json({ error: 'Invalid ID format' });
  }

  try {
    // Check cache
    const cacheKey = `todo:${id}`;
    if (redisClient.isOpen) {
      const cached = await redisClient.get(cacheKey);
      if (cached) {
        return res.json(JSON.parse(cached));
      }
    }

    const result = await pool.query(
      'SELECT * FROM todos WHERE id = $1',
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Todo not found' });
    }

    // Cache individual todo
    if (redisClient.isOpen) {
      await redisClient.setEx(
        cacheKey,
        300,  // 5 minutes
        JSON.stringify(result.rows[0])
      );
    }

    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error fetching todo:', err);
    res.status(500).json({ error: 'Failed to fetch todo' });
  }
});

// CREATE new todo
app.post('/api/todos', async (req, res) => {
  // Validate input
  const { error, value } = todoSchema.validate(req.body);
  if (error) {
    return res.status(400).json({ 
      error: 'Invalid input',
      details: error.details.map(d => d.message)
    });
  }

  const { title, description } = value;

  try {
    const result = await pool.query(
      `INSERT INTO todos (title, description) 
       VALUES ($1, $2) 
       RETURNING *`,
      [title, description || null]
    );

    // Invalidate cache
    if (redisClient.isOpen) {
      await redisClient.del('todos:all');
    }

    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Error creating todo:', err);
    res.status(500).json({ error: 'Failed to create todo' });
  }
});

// UPDATE todo
// NB! API vajab KÕIKI välju - see on oluline teadmine!
app.put('/api/todos/:id', async (req, res) => {
  const { id } = req.params;

  // Validate input
  const { error, value } = todoSchema.validate(req.body);
  if (error) {
    return res.status(400).json({ 
      error: 'Invalid input',
      details: error.details.map(d => d.message)
    });
  }

  const { title, description, completed } = value;

  try {
    const result = await pool.query(
      `UPDATE todos 
       SET title = $1,
           description = $2,
           completed = $3,
           updated_at = CURRENT_TIMESTAMP
       WHERE id = $4
       RETURNING *`,
      [title, description || null, completed, id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Todo not found' });
    }

    // Invalidate cache
    if (redisClient.isOpen) {
      await redisClient.del('todos:all');
      await redisClient.del(`todo:${id}`);
    }

    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error updating todo:', err);
    res.status(500).json({ error: 'Failed to update todo' });
  }
});

// DELETE todo
app.delete('/api/todos/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const result = await pool.query(
      'DELETE FROM todos WHERE id = $1 RETURNING id',
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Todo not found' });
    }

    // Invalidate cache
    if (redisClient.isOpen) {
      await redisClient.del('todos:all');
      await redisClient.del(`todo:${id}`);
    }

    res.status(204).send();
  } catch (err) {
    console.error('Error deleting todo:', err);
    res.status(500).json({ error: 'Failed to delete todo' });
  }
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ 
    error: 'Internal server error',
    details: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// Start server
const server = app.listen(port, () => {
  console.log(`API server running on port ${port}`);
  console.log(`Environment: ${process.env.NODE_ENV}`);
});

// Graceful shutdown
// Miks see oluline? Ootame kuni kõik päringud on lõpetatud
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully');
  
  // Stop accepting new requests
  server.close(() => {
    console.log('HTTP server closed');
  });

  // Close database pool
  await pool.end();
  console.log('Database pool closed');

  // Close Redis
  await redisClient.quit();
  console.log('Redis connection closed');

  process.exit(0);
});
```

#### api/Dockerfile
```dockerfile
# Multi-stage build - miks?
# 1. Väiksem lõplik image (pole build tööriistu)
# 2. Turvalisem (pole source koodi)
# 3. Kiirem deployment

# Build stage
FROM node:16-alpine AS builder
WORKDIR /app

# Miks package*.json eraldi?
# Docker cache - kui package.json ei muutu, 
# siis npm install tulemust ei pea uuesti tegema
COPY package*.json ./

# ci vs install?
# ci on kiirem ja deterministlik (kasutab package-lock.json)
RUN npm ci --production

# Production stage
FROM node:16-alpine

# Turvalisus - ära jooksuta root kasutajana
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Kopeeri ainult vajalik
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs . .

# Vaheta kasutaja
USER nodejs

EXPOSE 3000

# Health check Dockerfile'is või Compose'is?
# Dockerfile'is = image'i osa, töötab igal pool
# Compose'is = ainult selle deploymentiga
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => {if(r.statusCode !== 200) throw new Error()})"

CMD ["node", "server.js"]
```

---

## 🌐 Frontend

#### frontend/.dockerignore
```dockerignore
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.DS_Store
.vscode
.idea
```

#### frontend/package.json
```json
{
  "name": "todo-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.4.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

#### frontend/public/index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#000000" />
  <meta name="description" content="Todo app built with Docker Compose" />
  <title>Todo App</title>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
</body>
</html>
```

#### frontend/src/index.js
```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

#### frontend/src/App.js
```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// API URL tuleb environment muutujast
// OLULINE: Tühi string = kasutab suhtelisi URL-e
// Miks? Sest browser ei tea midagi Docker'i sisemistest hostnimedes
const API_URL = '';

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });

  // Fetch todos on mount
  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/todos`);
      setTodos(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch todos');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const createTodo = async (e) => {
    e.preventDefault();
    if (!newTodo.title.trim()) return;
    
    try {
      // OLULINE õppetund: API ei aktsepteeri tühja stringi description'iks
      // Peame saatma ainult need väljad, mis pole tühjad
      const todoData = {
        title: newTodo.title
      };
      
      if (newTodo.description.trim()) {
        todoData.description = newTodo.description;
      }
      
      const response = await axios.post(`${API_URL}/api/todos`, todoData);
      setTodos([response.data, ...todos]);
      setNewTodo({ title: '', description: '' });
      setError(null);
    } catch (err) {
      setError('Failed to create todo');
      console.error('Create error:', err.response?.data || err);
    }
  };

  const toggleTodo = async (id, completed) => {
    try {
      // OLULINE õppetund: API vajab PUT päringu jaoks KÕIKI välju
      // See on tavaline REST API pattern - PUT asendab kogu objekti
      const todo = todos.find(t => t.id === id);
      
      await axios.put(`${API_URL}/api/todos/${id}`, {
        title: todo.title,
        description: todo.description,
        completed: !completed
      });
      
      setTodos(todos.map(todo =>
        todo.id === id ? { ...todo, completed: !completed } : todo
      ));
      setError(null);
    } catch (err) {
      setError('Failed to update todo');
      console.error('Update error:', err);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await axios.delete(`${API_URL}/api/todos/${id}`);
      setTodos(todos.filter(todo => todo.id !== id));
      setError(null);
    } catch (err) {
      setError('Failed to delete todo');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="App">
      <header>
        <h1>📝 Todo App</h1>
        <p>Built with Docker Compose</p>
      </header>
      
      {error && <div className="error">{error}</div>}
      
      <form onSubmit={createTodo} className="todo-form">
        <input
          type="text"
          placeholder="What needs to be done?"
          value={newTodo.title}
          onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
        />
        <textarea
          placeholder="Description (optional)"
          value={newTodo.description}
          onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
        />
        <button type="submit">Add Todo</button>
      </form>

      <div className="todos-list">
        {todos.length === 0 ? (
          <p className="no-todos">No todos yet. Create one!</p>
        ) : (
          todos.map(todo => (
            <div key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => toggleTodo(todo.id, todo.completed)}
              />
              <div className="todo-content">
                <h3>{todo.title}</h3>
                {todo.description && <p>{todo.description}</p>}
                <small>
                  Created: {new Date(todo.created_at).toLocaleDateString()}
                </small>
              </div>
              <button onClick={() => deleteTodo(todo.id)} className="delete-btn">
                🗑️
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
```

#### frontend/src/App.css
```css
/* Lihtne ja puhas disain */
.App {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
  text-align: center;
}

.todo-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.todo-form input,
.todo-form textarea {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.todo-form button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.todo-form button:hover {
  background-color: #45a049;
}

.todo-list {
  list-style: none;
  padding: 0;
}

.todo-item {
  padding: 15px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
  display: flex;
  gap: 10px;
  align-items: start;
}

.todo-item.completed {
  opacity: 0.6;
}

.todo-item.completed .todo-content h3 {
  text-decoration: line-through;
}

.todo-content {
  flex: 1;
}

.todo-content h3 {
  margin: 0 0 5px 0;
}

.todo-content p {
  margin: 0 0 10px 0;
  color: #666;
}

.todo-content small {
  color: #999;
}

.delete-btn {
  padding: 5px 10px;
  font-size: 14px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.delete-btn:hover {
  background-color: #da190b;
}

.loading,
.error,
.no-todos {
  text-align: center;
  padding: 20px;
}

.error {
  color: #f44336;
  background-color: #ffebee;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
}
```

#### frontend/Dockerfile
```dockerfile
# Build stage - ehitame React rakenduse
FROM node:16-alpine AS builder
WORKDIR /app

# Kopeeri package failid ja installi
COPY package*.json ./
RUN npm install

# Kopeeri kogu kood ja ehita
COPY . .
RUN npm run build

# Production stage - servime nginx'iga
# Miks nginx? 
# 1. Kiire staatiliste failide servimine
# 2. Gzip compression
# 3. Browser caching headers
FROM nginx:alpine

# Kopeeri ehitatud React app
COPY --from=builder /app/build /usr/share/nginx/html

# Custom nginx config React router'i jaoks
# try_files on oluline - ilma selleta ei tööta React Router
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 🔧 Nginx konfiguratsioon

#### nginx/.dockerignore
```dockerignore
*.log
.DS_Store
```

#### nginx/nginx.conf
```nginx
# Miks see number? Tavaliselt = CPU tuumade arv
events {
    worker_connections 1024;
}

http {
    # Upstream servers - kui tahad lisada load balancing
    upstream frontend {
        server frontend:80;
        # Tulevikus saab lisada:
        # server frontend2:80;
        # server frontend3:80;
    }

    upstream api {
        server api:3000;
    }

    server {
        listen 80;
        
        # Frontend päringud
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        
        # API päringud
        # Kõik mis algab /api läheb API konteinerisse
        location /api {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

---

## 🚀 Käivitamise juhised

### 1. Eeldused
- Docker ja Docker Compose peavad olema installitud
- Internetiühendus Docker image'ite allalaadimiseks

### 2. Setup sammud

```bash
# 1. Mine projekti kausta
cd labs/lab-docker-compose/mariatesttalvik

# 2. Loo environment fail
cp .env.example .env
# Muuda .env failis paroolid

# 3. OLULINE! Genereeri package-lock.json failid
# See samm on KRIITILINE - ilma selleta ei tööta npm ci käsk Dockerfile'ides
cd api && npm install && cd ..
cd frontend && npm install && cd ..

# 4. Käivita kõik konteinerid
docker-compose up --build
```

### 3. Testimine

1. Ava brauser: http://localhost
2. API health check: http://localhost/api/health

---

## 🛠️ Kasulikud käsud

```bash
# Logide vaatamine
docker-compose logs -f
docker-compose logs -f api  # Ainult API logid

# Konteinerite staatus
docker-compose ps

# Peatamine
docker-compose down

# Peatamine koos andmete kustutamisega
docker-compose down -v

# Taaskäivitus
docker-compose restart

# Ühe teenuse taaskäivitus
docker-compose restart api

# Konteinerisse sisenemine debugging'uks
docker-compose exec api sh
docker-compose exec database psql -U todouser -d tododb
```

---

## 🔍 Troubleshooting

### "Port already in use"
```bash
# Mac/Linux
lsof -i :80
# Windows
netstat -ano | findstr :80

# Lahendus: muuda porti docker-compose.yml failis
ports:
  - "8080:80"
```

### "npm ci error - missing package-lock.json"
```bash
# See on kõige sagedasem viga!
# Genereeri puuduvad failid
cd api && npm install && cd ..
cd frontend && npm install && cd ..
```

### "Failed to fetch todos"
- Kontrolli et REACT_APP_API_URL on tühi string docker-compose.yml failis
- Kontrolli nginx.conf - peab olema events ja http blokid

### "Failed to update todo"
- API vajab PUT päringus KÕIKI välju (title, description, completed)
- See on tavaline REST API pattern

### "nginx: [emerg] "upstream" directive is not allowed here"
- nginx.conf vajab events {} ja http {} blokke
- Kõik server ja upstream direktiivid peavad olema http bloki sees

### Windows path probleem
```yaml
# Kasuta absolute path
volumes:
  - C:/Users/YourName/mariatesttalvik/api:/app
```

---

## 📚 Kokkuvõte

Õppisime:
1. **Multi-container arhitektuur** - iga teenus eraldi konteineris
2. **Container networking** - kuidas konteinerid omavahel suhtlevad
3. **Volume persistence** - andmete püsimine restartide vahel
4. **Environment configuration** - konfiguratsioon läbi muutujate
5. **Health checks** - teenuste tervise kontroll
6. **Production patterns** - multi-stage builds, security
7. **Debugging oskused** - kuidas vigu leida ja parandada

---

## 🎯 Edasised sammud

1. **Lisa autentimine** (JWT tokens)
2. **Lisa testid** (Jest, React Testing Library)
3. **Lisa CI/CD pipeline** (GitHub Actions)
4. **Lisa SSL sertifikaat** (Let's Encrypt)
5. **Lisa monitoring** (Prometheus, Grafana)
6. **Optimeeri** (väiksemad Docker images, cache strategia)

---

## 💡 Õppetunnid

1. **package-lock.json on kriitiline** - ilma selleta ei tööta npm ci
2. **nginx vajab õiget struktuuri** - events ja http blokid
3. **API URL peab olema õige** - Docker sisemised hostinimed ei tööta browseris
4. **Validation on oluline** - API peab kontrollima sisendeid
5. **Health checks aitavad** - depends_on üksi ei piisa
6. **Logid on sõbrad** - docker-compose logs aitab vigu leida
