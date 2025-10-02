# Docker Compose Labor

**Kestus:** 2-3 tundi  
**Eesmärk:** Ehitada töötav multi-container rakendus VM-is

---

## ENNE ALUSTAMIST - Kontrolli Need!

### 1. Kas Docker on installitud VM-is?

```bash
docker --version
docker-compose --version
```

**Kui EI OLE installitud:**

```bash
# Ubuntu/Debian VM
sudo apt update
sudo apt install -y docker.io docker-compose

# Käivita Docker
sudo systemctl start docker
sudo systemctl enable docker

# Lisa oma kasutaja docker gruppi (OLULINE!)
sudo usermod -aG docker $USER

# RESTART VM või logi välja ja sisse
# Kontrolli et töötab ilma sudo'ta:
docker ps
```

### 2. Kas VSCode on installitud?

**Host masinas (Windows/Mac):**
- Lae alla: https://code.visualstudio.com/
- Installi "Remote - SSH" extension

**Või kasuta VM-is:**
```bash
# Kui tahad VSCode otse VM-is
sudo snap install code --classic
```

### 3. VM Port Forwarding (VirtualBox)

**Kui kasutad VirtualBox:**

1. Ava VirtualBox
2. Vali oma VM → Settings → Network
3. Adapter 1 → Advanced → Port Forwarding
4. Lisa uus reegel:
   - Name: `HTTP`
   - Protocol: `TCP`
   - Host Port: `8080`
   - Guest Port: `80`

**Nüüd saad HOST masinas avada:** `http://localhost:8080`

---

## SAMM 1: Projekti loomine VSCode'is (10 min)

### 1.1 Loo projekt kaust VM-is

```bash
# Ava terminal VM-is
cd ~
mkdir todo-app
cd todo-app
```

### 1.2 Ava VSCode

**Kui VSCode on VM-is:**
```bash
code .
```

**Kui VSCode on HOST masinas (Windows/Mac):**
1. VSCode → Remote-SSH
2. Ühenda VM-iga
3. File → Open Folder → vali `/home/kasutaja/todo-app`

### 1.3 Loo kaustad VSCode'is

VSCode'is vajuta **New Folder** ikooni ja loo:
- `api`
- `database`
- `frontend`
- `nginx`

**KONTROLLI** et su kausad näevad välja nii:
```
todo-app/
├── api/
├── database/
├── frontend/
└── nginx/
```

---

## SAMM 2: Andmebaas (5 min)

**Miks:** Andmebaas hoiab meie todos'e. PostgreSQL on eraldi konteineris, et saaksime seda uuendada ilma API-d puutumata.

### 2.1 Loo fail `database/init.sql`

VSCode'is: Right click `database` kaust → New File → `init.sql`

```sql
-- Lubame UUID-d kasutada
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Loome tabeli
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

---

## SAMM 3: API (Backend) - 20 min

**Miks:** API on vahendaja frontendi ja andmebaasi vahel. Node.js töötab eraldi konteineris.

### 3.1 Loo fail `api/.dockerignore`

**Miks:** Et Docker EI kopeeriks `node_modules` (see on SUUR ja AEGLANE).

```
node_modules
npm-debug.log
.env
.git
```

### 3.2 Loo fail `api/package.json`

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

### 3.3 Loo fail `api/server.js`

**Miks:** See on meie API loogika - see kuulab päringuid ja räägib andmebaasiga.

```javascript
const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

console.log('Starting API server...');

// PostgreSQL connection
// OLULINE: host='database' on Docker Compose DNS nimi
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

pool.on('connect', () => {
  console.log('✓ Connected to PostgreSQL');
});

pool.on('error', (err) => {
  console.error('PostgreSQL error:', err);
});

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({ 
      status: 'OK', 
      database: 'connected',
      timestamp: result.rows[0].now 
    });
  } catch (err) {
    console.error('Health check failed:', err);
    res.status(503).json({ 
      status: 'ERROR', 
      message: err.message 
    });
  }
});

// GET all todos
app.get('/api/todos', async (req, res) => {
  console.log('GET /api/todos');
  try {
    const result = await pool.query(
      'SELECT * FROM todos ORDER BY created_at DESC'
    );
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

// POST new todo
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
    console.log('Created todo:', result.rows[0].id);
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Error creating todo:', err);
    res.status(500).json({ error: err.message });
  }
});

// PUT update todo
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

    console.log('Updated todo:', id);
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error updating todo:', err);
    res.status(500).json({ error: err.message });
  }
});

// DELETE todo
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
  console.log(`✓ API server running on port ${PORT}`);
  console.log(`  Health: http://localhost:${PORT}/health`);
  console.log(`  Todos:  http://localhost:${PORT}/api/todos`);
});
```

### 3.4 Loo fail `api/Dockerfile`

**Miks:** See ütleb Docker'ile kuidas ehitada meie API konteiner.

```dockerfile
FROM node:16-alpine

WORKDIR /app

# Kopeerime package.json
COPY package*.json ./

# Installime dependencies
RUN npm install

# Kopeerime kogu koodi
COPY . .

# Avame port
EXPOSE 3000

# Käivitame
CMD ["node", "server.js"]
```

---

## SAMM 4: Frontend (React) - 25 min

**Miks:** Frontend on kasutajaliides brauseris. See on eraldi konteineris, et frontend arendajad saaksid töötada ilma backend'i puutumata.

### 4.1 Loo fail `frontend/.dockerignore`

```
node_modules
npm-debug.log
.env
.git
build
```

### 4.2 Loo fail `frontend/package.json`

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
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": ["react-app"]
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  }
}
```

### 4.3 Loo kaustad ja failid

VSCode'is loo:
- `frontend/public/` kaust
- `frontend/src/` kaust

### 4.4 Loo fail `frontend/public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Todo app with Docker Compose" />
    <title>Todo App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
```

### 4.5 Loo fail `frontend/src/index.js`

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### 4.6 Loo fail `frontend/src/index.css`

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New', monospace;
}
```

### 4.7 Loo fail `frontend/src/App.js`

**Miks:** See on peamine React komponent mis näitab todos'e ja suhtleb API-ga.

```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');

  // Lae todos kui komponent laetakse
  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      console.log('Fetching todos from /api/todos');
      const response = await axios.get('/api/todos');
      console.log('Received todos:', response.data);
      setTodos(response.data);
      setError(null);
    } catch (err) {
      console.error('Fetch error:', err);
      setError('Failed to fetch todos: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (e) => {
    e.preventDefault();
    
    if (!newTitle.trim()) {
      setError('Title cannot be empty');
      return;
    }

    try {
      console.log('Creating todo:', { title: newTitle, description: newDescription });
      const response = await axios.post('/api/todos', {
        title: newTitle,
        description: newDescription
      });
      console.log('Created todo:', response.data);
      
      setTodos([response.data, ...todos]);
      setNewTitle('');
      setNewDescription('');
      setError(null);
    } catch (err) {
      console.error('Create error:', err);
      setError('Failed to add todo: ' + (err.response?.data?.error || err.message));
    }
  };

  const toggleTodo = async (todo) => {
    try {
      console.log('Toggling todo:', todo.id);
      const response = await axios.put(`/api/todos/${todo.id}`, {
        title: todo.title,
        description: todo.description,
        completed: !todo.completed
      });
      console.log('Updated todo:', response.data);
      
      setTodos(todos.map(t => t.id === todo.id ? response.data : t));
      setError(null);
    } catch (err) {
      console.error('Update error:', err);
      setError('Failed to update todo: ' + (err.response?.data?.error || err.message));
    }
  };

  const deleteTodo = async (id) => {
    if (!window.confirm('Are you sure you want to delete this todo?')) {
      return;
    }

    try {
      console.log('Deleting todo:', id);
      await axios.delete(`/api/todos/${id}`);
      console.log('Deleted todo:', id);
      
      setTodos(todos.filter(t => t.id !== id));
      setError(null);
    } catch (err) {
      console.error('Delete error:', err);
      setError('Failed to delete todo: ' + (err.response?.data?.error || err.message));
    }
  };

  if (loading) {
    return (
      <div className="App">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="header">
        <h1>📝 Todo App</h1>
        <p>Built with Docker Compose</p>
      </header>
      
      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}
      
      <div className="container">
        <form onSubmit={addTodo} className="todo-form">
          <h2>Add New Todo</h2>
          <input
            type="text"
            placeholder="What needs to be done?"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            className="input"
            required
          />
          <textarea
            placeholder="Description (optional)"
            value={newDescription}
            onChange={(e) => setNewDescription(e.target.value)}
            className="textarea"
            rows="3"
          />
          <button type="submit" className="btn btn-primary">
            Add Todo
          </button>
        </form>

        <div className="todos-section">
          <h2>My Todos ({todos.length})</h2>
          
          {todos.length === 0 ? (
            <div className="no-todos">
              <p>🎉 No todos yet!</p>
              <p>Create your first todo above</p>
            </div>
          ) : (
            <div className="todos-list">
              {todos.map(todo => (
                <div key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                  <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={() => toggleTodo(todo)}
                    className="checkbox"
                  />
                  <div className="todo-content">
                    <h3>{todo.title}</h3>
                    {todo.description && <p>{todo.description}</p>}
                    <small>
                      Created: {new Date(todo.created_at).toLocaleDateString('en-GB')} at{' '}
                      {new Date(todo.created_at).toLocaleTimeString('en-GB')}
                    </small>
                  </div>
                  <button
                    onClick={() => deleteTodo(todo.id)}
                    className="btn-delete"
                    title="Delete todo"
                  >
                    🗑️
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <footer className="footer">
        <p>Docker Compose Lab | Multi-container Application</p>
      </footer>
    </div>
  );
}

export default App;
```

### 4.8 Loo fail `frontend/src/App.css`

```css
.App {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
}

.header p {
  margin: 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.container {
  flex: 1;
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
  width: 100%;
}

.error {
  background-color: #fee;
  border: 1px solid #fcc;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error button {
  background: none;
  border: none;
  color: #c33;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0 0.5rem;
}

.todo-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.todo-form h2 {
  margin: 0 0 1rem 0;
  color: #333;
}

.input,
.textarea {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.3s;
}

.input:focus,
.textarea:focus {
  outline: none;
  border-color: #667eea;
}

.textarea {
  resize: vertical;
  min-height: 80px;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  width: 100%;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.todos-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.todos-section h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
}

.no-todos {
  text-align: center;
  padding: 3rem 1rem;
  color: #999;
}

.no-todos p:first-child {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.no-todos p:last-child {
  font-size: 1.1rem;
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
  transition: all 0.3s;
}

.todo-item:hover {
  border-color: #667eea;
  transform: translateX(4px);
}

.todo-item.completed {
  opacity: 0.6;
}

.todo-item.completed .todo-content h3 {
  text-decoration: line-through;
  color: #999;
}

.checkbox {
  width: 24px;
  height: 24px;
  cursor: pointer;
  margin-top: 0.25rem;
}

.todo-content {
  flex: 1;
}

.todo-content h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.1rem;
}

.todo-content p {
  margin: 0 0 0.5rem 0;
  color: #666;
  line-height: 1.5;
}

.todo-content small {
  color: #999;
  font-size: 0.85rem;
}

.btn-delete {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  opacity: 0.6;
  transition: all 0.3s;
}

.btn-delete:hover {
  opacity: 1;
  transform: scale(1.2);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  color: #667eea;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.footer {
  background: #333;
  color: white;
  text-align: center;
  padding: 1.5rem;
  margin-top: 2rem;
}

.footer p {
  margin: 0;
  opacity: 0.8;
}

@media (max-width: 600px) {
  .header h1 {
    font-size: 2rem;
  }
  
  .container {
    margin: 1rem auto;
  }
  
  .todo-form,
  .todos-section {
    padding: 1rem;
  }
}
```

### 4.9 Loo fail `frontend/Dockerfile`

**Miks:** Multi-stage build - ehitame React app'i ja servime nginxiga. See on kiire ja väike.

```dockerfile
# Stage 1: Build React app
FROM node:16-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Kopeerime ehitatud failid
COPY --from=builder /app/build /usr/share/nginx/html

# Custom nginx config React Router jaoks
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

## SAMM 5: Nginx (Reverse Proxy) - 10 min

**Miks:** Nginx on värav mis suunab päringuid. `/api` läheb API konteinerisse, ülejäänud frontend konteinerisse. Nii töötab kõik ühest portist.

### 5.1 Loo fail `nginx/nginx.conf`

```nginx
events {
    worker_connections 1024;
}

http {
    # Upstream definitions
    upstream frontend {
        server frontend:80;
    }

    upstream api {
        server api:3000;
    }

    server {
        listen 80;
        server_name localhost;

        # Logging
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        # API requests - kõik mis algab /api
        location /api {
            proxy_pass http://api;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }

        # Health check
        location /health {
            proxy_pass http://api/health;
            proxy_set_header Host $host;
        }

        # Frontend - kõik ülejäänud
        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

---

## SAMM 6: Docker Compose - Orkestratsioon (15 min)

**Miks:** See fail ütleb Docker'ile kuidas kõik konteinerid koos töötavad - võrgud, sõltuvused, portid.

### 6.1 Loo fail `docker-compose.yml` (juurkaustas!)

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
      # Andmed püsivad siin
      - postgres_data:/var/lib/postgresql/data
      # Init skript
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todouser -d tododb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    restart: unless-stopped

  # Node.js API
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
    networks:
      - backend
      - frontend
    restart: unless-stopped
    # Logid stdout'i
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

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
      # OLULINE: See port on kust pääsed ligi
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
  # Backend võrk - andmebaas ja API
  backend:
    driver: bridge
  # Frontend võrk - API, frontend, nginx
  frontend:
    driver: bridge

volumes:
  # PostgreSQL andmed
  postgres_data:
    driver: local
```

---

## SAMM 7: Kontrollime faile (5 min)

**OLULINE:** Enne käivitamist kontrolli et KÕIK failid on olemas!

```bash
# VM terminalis
cd ~/todo-app

# Näita failistruktuur
find . -type f -name "*.js" -o -name "*.json" -o -name "*.sql" -o -name "*.yml" -o -name "Dockerfile" -o -name "*.conf" -o -name "*.html" -o -name "*.css" | sort

# Peaksid nägema:
# ./api/Dockerfile
# ./api/package.json
# ./api/server.js
# ./database/init.sql
# ./docker-compose.yml
# ./frontend/Dockerfile
# ./frontend/package.json
# ./frontend/public/index.html
# ./frontend/src/App.css
# ./frontend/src/App.js
# ./frontend/src/index.css
# ./frontend/src/index.js
# ./nginx/nginx.conf
```

**Kui mõni fail puudub - LOO SEE!**

---

## SAMM 8: Ehitame ja käivitame (10 min)

**Miks:** Nüüd ehitame kõik Docker image'd ja käivitame konteinerid.

### 8.1 Ehita ja käivita

```bash
cd ~/todo-app

# OLULINE: Esimene kord võtab 5-10 minutit!
# Docker laeb alla image'd ja ehitab konteinerid

docker-compose up --build

# SA PEAKSID NÄGEMA:
# Creating network "todo-app_backend" ... done
# Creating network "todo-app_frontend" ... done
# Creating volume "todo-app_postgres_data" ... done
# Building api...
# Building frontend...
# Creating todo_db ... done
# Creating todo_api ... done
# Creating todo_frontend ... done
# Creating todo_nginx ... done
```

**OOTA kuni näed:**
```
todo_db       | PostgreSQL init process complete; ready for start up.
todo_api      | ✓ Connected to PostgreSQL
todo_api      | ✓ API server running on port 3000
todo_frontend | (nginx startup logs)
todo_nginx    | (nginx startup logs)
```

### 8.2 AGA LOGI FAILID ON PIKAD! Kuidas teada et töötab?

Ava **uus terminal** (ära sulge esimest!) ja kontrolli:

```bash
# Kontrolli konteinerite staatust
docker-compose ps

# Peaksid nägema 4 konteinerit "Up" staatuses:
# NAME            STATE              PORTS
# todo_db         Up (healthy)       5432/tcp
# todo_api        Up                 3000/tcp
# todo_frontend   Up                 80/tcp
# todo_nginx      Up                 0.0.0.0:80->80/tcp
```

---

## SAMM 9: TESTIMINE - Kas see töötab? (10 min)

### 9.1 Test VM-ist (sees)

```bash
# Test health check
curl http://localhost/health

# Peaks näitama:
# {"status":"OK","database":"connected","timestamp":"..."}

# Test API
curl http://localhost/api/todos

# Peaks näitama JSON array todos'ega
```

### 9.2 Test HOST masinast (Windows/Mac)

**Kui kasutad VirtualBox port forwarding:**

1. Ava brauser HOST masinas
2. Mine: **http://localhost:8080** (või mis port sa seadistasid)
3. Peaksid nägema Todo rakendust!

**Kui kasutad Bridged network:**

```bash
# VM-is saa IP aadressi
ip addr show

# Otsi inet 192.168.x.x
# Siis HOST masinas ava: http://192.168.x.x
```

### 9.3 Test funktsionaalsust

1. **Lisa uus todo** - Kirjuta tekst ja vajuta "Add Todo"
2. **Märgi tehtud** - Click checkbox
3. **Kustuta** - Click prügikasti ikoon
4. **Refresh leht** - F5 - andmed peaksid püsima!

---

## SAMM 10: Logide vaatamine (5 min)

**Miks:** Kui midagi ei tööta, logid ütlevad sulle MIKS.

```bash
# Vaata kõiki logisid
docker-compose logs

# Vaata ainult API logisid
docker-compose logs api

# Vaata logisid reaalajas (live)
docker-compose logs -f

# Vaata ainult viimased 50 rida
docker-compose logs --tail=50

# Vaata andmebaasi logisid
docker-compose logs database
```

---

## KUI MIDAGI EI TÖÖTA - Troubleshooting

### Probleem 1: "Cannot connect from HOST machine"

**Diagnoos:**
```bash
# VM-is
curl http://localhost/health
# Kas töötab? JA

# HOST-is
# Ei tööta? Port forwarding probleem
```

**Lahendus:**

1. **VirtualBox Port Forwarding:**
   - VirtualBox → VM Settings → Network → Port Forwarding
   - Host Port: 8080
   - Guest Port: 80
   - Siis HOST-is: http://localhost:8080

2. **Või kasuta VM IP:**
```bash
# VM-is
ip addr show | grep "inet "
# Otsi 192.168.x.x

# HOST-is kasuta seda IP'd
http://192.168.1.100
```

### Probleem 2: "API konteiner crashib"

**Diagnoos:**
```bash
docker-compose logs api
```

**Kui näed:** "Cannot connect to database"

**Lahendus:**
```bash
# Restart API (andmebaas võtab kauem käivituda)
docker-compose restart api

# Või oota 30 sekundit ja käivita uuesti
```

### Probleem 3: "Frontend shows blank page"

**Diagnoos:**
```bash
# Ava browser console (F12)
# Vaata Network tab
# Kas API päringud ebaõnnestuvad?
```

**Lahendus 1:** nginx konfiguratsioon on vale
```bash
# Kontrolli nginx.conf
cat nginx/nginx.conf

# Restart nginx
docker-compose restart nginx
```

**Lahendus 2:** Frontend build failed
```bash
# Vaata frontend logisid
docker-compose logs frontend

# Rebuild
docker-compose up --build frontend
```

### Probleem 4: "Permission denied"

```bash
# Kui näed: permission denied on docker socket
# Lisa ennast docker gruppi

sudo usermod -aG docker $USER

# RESTART VM
sudo reboot

# Kontrolli
groups
# Peaksid nägema "docker" listis
```

### Probleem 5: "Port 80 already in use"

```bash
# Kontrolli mis kasutab porti
sudo lsof -i :80
# VÕI
sudo netstat -tulpn | grep :80

# Sulge see programm või muuda docker-compose.yml
ports:
  - "8080:80"
```

### Probleem 6: "Cannot build - out of disk space"

```bash
# Kontrolli ruumi
df -h

# Puhasta vanad Docker andmed
docker system prune -a --volumes

# HOIATUS: See kustutab KÕIK kasutamata image'd ja volume'd
```

### Probleem 7: "npm install fails in container"

```bash
# Kontrolli internet ühendust VM-is
ping google.com

# Kui ei tööta, kontrolli VM network settings
# NAT või Bridged peab olema seadistatud
```

---

## Debugimise käsud

```bash
# Sisene konteinerisse
docker-compose exec api sh
docker-compose exec database psql -U todouser -d tododb

# Kontrolli võrke
docker network ls
docker network inspect todo-app_backend

# Kontrolli volume'id
docker volume ls
docker volume inspect todo-app_postgres_data

# Restart üks teenus
docker-compose restart api

# Stop ja remove kõik
docker-compose down

# Remove ka volumes (KUSTUTAB ANDMED!)
docker-compose down -v

# Rebuild image'd
docker-compose build --no-cache
```

---

## Peatamine ja cleanup

```bash
# Peata konteinerid (andmed jäävad)
docker-compose down

# Peata JA kustuta andmed
docker-compose down -v

# Kustuta ka image'd
docker-compose down -v --rmi all

# Täielik cleanup
docker system prune -a --volumes
```

---

## Mida me õppisime?

### 1. Containerization põhitõed
- **Isolatsioon**: Iga teenus eraldi konteineris
- **Portsööd**: Kuidas portid kaardistuvad (80:80)
- **Võrgud**: Kuidas konteinerid omavahel räägivad

### 2. Docker Compose
- **Orkestreerimine**: Mitme konteineri haldamine koos
- **Sõltuvused**: `depends_on` ja `healthcheck`
- **Volumes**: Andmete püsimine

### 3. Multi-tier arhitektuur
- **Database tier**: PostgreSQL
- **Application tier**: Node.js API
- **Presentation tier**: React frontend
- **Proxy tier**: Nginx

### 4. Praktilised oskused
- Dockerfile'ide kirjutamine
- docker-compose.yml konfigureerimine
- Debugging ja troubleshooting
- Logide lugemine

---

## Järgmised sammud

Kui see töötab, proovi:

1. **Lisa Redis** cache'iks:
```yaml
redis:
  image: redis:alpine
  networks:
    - backend
```

2. **Lisa environment file** (.env):
```yaml
env_file:
  - .env
```

3. **Development mode** - hot reload:
```yaml
api:
  volumes:
    - ./api:/app
    - /app/node_modules
  command: npm run dev
```

4. **Scaling** - mitme API instantsi:
```bash
docker-compose up --scale api=3
```

5. **Monitoring** - lisa Prometheus ja Grafana

---

## Kokkuvõte

✅ Ehitasime töötava multi-container rakenduse  
✅ Õppisime Docker Compose põhitõdesid  
✅ Mõistame kuidas konteinerid suhtlevad  
✅ Oskame debugida ja probleeme lahendada  

**Palju õnne! Sa oled nüüd Docker Compose ekspert! 🎉**

---

## Viited

- Docker dokumentatsioon: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- PostgreSQL Docker: https://hub.docker.com/_/postgres
- Node.js Docker: https://hub.docker.com/_/node
- Nginx Docker: https://hub.docker.com/_/nginx

---

## Lisa: Kasulikud käsud kokkuvõte

```bash
# EHITAMINE JA KÄIVITAMINE
docker-compose up                 # Käivita foreground
docker-compose up -d              # Käivita background
docker-compose up --build         # Rebuild ja käivita
docker-compose up --force-recreate # Sunni uuesti loomine

# PEATAMINE
docker-compose down               # Peata ja eemalda
docker-compose down -v            # + kustuta volumes
docker-compose stop               # Peata (ära eemalda)
docker-compose start              # Käivita peatatud

# VAATAMINE
docker-compose ps                 # Konteinerite staatus
docker-compose logs               # Kõik logid
docker-compose logs -f api        # API logid live
docker-compose logs --tail=100    # Viimased 100 rida
docker-compose top                # Protsessid

# DEBUGGING
docker-compose exec api sh        # Sisene API konteinerisse
docker-compose exec database psql # Sisene DB konteinerisse
docker-compose restart api        # Restart API
docker-compose build api          # Rebuild API

# CLEANUP
docker system prune               # Puhasta kõik
docker volume prune               # Puhasta volumes
docker network prune              # Puhasta networks
docker image prune -a             # Puhasta images
```
