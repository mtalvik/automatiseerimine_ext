# Kubernetes Labor: E-Pood Mikroteenustega

---

# 📚 Sisukord

1. [Sissejuhatus](#sissejuhatus)
2. [Ettevalmistus](#ettevalmistus)
3. [Kubernetes Klaster](#kubernetes-klaster)
4. [Andmebaas (PostgreSQL)](#andmebaas)
5. [Backend API](#backend-api)
6. [Frontend](#frontend)
7. [Dashboard](#dashboard)
8. [Kubernetes Kontseptid](#kubernetes-kontseptid)
9. [Lisaülesanded](#lisaülesanded)
10. [Puhastamine](#puhastamine)

---

# 🎯 Sissejuhatus

## Mida Me Ehitame

```
┌────────────────────────────────────────────────┐
│                   BRAUSER                      │
│                (Teie arvuti)                   │
└────────────────┬───────────────────────────────┘
                 │ HTTP
                 ▼
┌────────────────────────────────────────────────┐
│                    VM                          │
│  ┌──────────────────────────────────────────┐  │
│  │         KUBERNETES KLASTER                │  │
│  │                                           │  │
│  │  ┌─────────┐  ┌─────────┐  ┌──────────┐ │  │
│  │  │Frontend │──▶│Backend  │──▶│PostgreSQL│ │  │
│  │  │(Nginx)  │  │(Node.js)│  │(Database)│ │  │
│  │  └─────────┘  └─────────┘  └──────────┘ │  │
│  │                                           │  │
│  └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────┘
```

## Kubernetes Põhimõisted

| 🔵 **Kubernetes Termin** | 📝 **Selgitus** | 💡 **Näide Laboris** |
|--------------------------|-----------------|----------------------|
| **Pod** | Väikseim üksus, üks või mitu konteinerit | `backend-api-xyz` |
| **Deployment** | Haldab pod'ide koopiaid, skaleeritav | Backend API (1-3 koopiat) |
| **StatefulSet** | Nagu Deployment, aga püsiva identiteediga | PostgreSQL (postgres-0) |
| **Service** | Sisene load balancer, DNS nimi | `backend-service:3000` |
| **ConfigMap** | Konfiguratsioon (mitte-salajane) | HTML kood, package.json |
| **Secret** | Salajane info (base64 kodeeritud) | Andmebaasi parool |
| **PVC** | Persistent Volume Claim - kettaruumi taotlus | Andmebaasi failid |

---

# 💻 Ettevalmistus

## 1. VM Loomine

### 📍 **KOHALIK ARVUTI** - Windows + VirtualBox

```powershell
# 1. Laadige Ubuntu Server 22.04 ISO
# 2. VirtualBox'is:
#    - New VM → Ubuntu 64-bit
#    - 2 CPU, 4GB RAM, 15GB disk
#    - Network: NAT
# 3. Installige Ubuntu vaikesätetega
```

### 📍 **KOHALIK ARVUTI** - Mac + Multipass

```bash
# Terminal 1 - Looge VM
multipass launch --name k8s-lab --cpus 2 --memory 4G --disk 15G

# Sisenemine VM'i
multipass shell k8s-lab
```

## 2. Arhitektuuri Kontroll

### 📍 **VM SEES**

```bash
# Kontrollige arhitektuuri - OLULINE!
uname -m

# Tulemus määrab, millised versioonid laadida:
# x86_64 või amd64 → kasutage AMD64 versioone
# aarch64 või arm64 → kasutage ARM64 versioone
```

## 3. Tööriistade Paigaldus

### 📍 **VM SEES** - Kõik käsud käivad VM'is!

```bash
# Süsteemi uuendamine
sudo apt update && sudo apt upgrade -y

# Docker installimine (konteinerite käitamiseks)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker  # Aktiveerib grupi kohe

# Kontrollige Docker
docker --version
docker run hello-world  # Peab näitama "Hello from Docker!"
```

### Kubectl ja Minikube - Valige Õige Versioon!

```bash
# Määrake arhitektuur
ARCH=$(uname -m)

if [ "$ARCH" = "x86_64" ]; then
    echo "Installing AMD64 versions..."
    # kubectl AMD64
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    # minikube AMD64  
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    mv minikube-linux-amd64 minikube
    
elif [ "$ARCH" = "aarch64" ]; then
    echo "Installing ARM64 versions..."
    # kubectl ARM64
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
    # minikube ARM64
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-arm64
    mv minikube-linux-arm64 minikube
fi

# Installimine
sudo install kubectl /usr/local/bin/kubectl
sudo install minikube /usr/local/bin/minikube

# Puhastamine
rm kubectl minikube

# Kontrollimine
kubectl version --client
minikube version
```

---

# ☸️ Kubernetes Klaster

## Minikube Käivitamine

### 📍 **VM SEES**

```bash
# Käivitage Minikube minimaalsete ressurssidega
# --cpus=2       → 2 CPU tuuma (miinimum)
# --memory=2000  → 2GB RAM
# --driver=docker → kasutab Docker'it konteinerite jaoks
minikube start --cpus=2 --memory=2000 --driver=docker

# See võtab 5-10 minutit esimesel korral
# Laadib alla ~800MB komponente
```

### Kontrollimine

```bash
# Klasteri staatus
minikube status

# Oodatav väljund:
# minikube: Running    ← Klaster töötab
# kubelet: Running     ← Node agent töötab
# apiserver: Running   ← API server töötab

# Kubernetes node
kubectl get nodes

# Oodatav väljund:
# NAME       STATUS   ROLES           AGE   VERSION
# minikube   Ready    control-plane   2m    v1.28.0
```

## ⚠️ Levinud Probleemid

| Viga | Põhjus | Lahendus |
|------|--------|----------|
| `Insufficient cores` | Minikube vajab min 2 CPU | Kasutage `--cpus=2` |
| `Exec format error` | Vale arhitektuur | Laadige õige versioon (ARM64/AMD64) |
| `Cannot connect to Docker` | Docker ei tööta | `sudo systemctl restart docker` |

---

# 🗄️ Andmebaas (PostgreSQL)

## Mis on StatefulSet?

```yaml
# 🔵 KUBERNETES KONTSEPT: StatefulSet
# - Püsiv identiteet (postgres-0, mitte random nimi)
# - Andmed säilivad pod'i taaskäivitusel
# - Järjestatud käivitus ja sulgemine
# - Sobib andmebaasidele
```

## PostgreSQL Konfiguratsioon

### 📍 **VM SEES** - Looge fail

```bash
cat > postgres-minimal.yaml << 'EOF'
# ============================================
# 1. CONFIGMAP - Avalik konfiguratsioon
# ============================================
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-config
data:
  POSTGRES_DB: shopdb      # Andmebaasi nimi
  POSTGRES_USER: shopuser  # Kasutaja (pole salajane)

---
# ============================================
# 2. SECRET - Salajane info (paroolid)
# ============================================
apiVersion: v1  
kind: Secret
metadata:
  name: postgres-secret
type: Opaque
data:
  # Parool: secretpassword
  # Base64 kodeeritud: echo -n 'secretpassword' | base64
  POSTGRES_PASSWORD: c2VjcmV0cGFzc3dvcmQ=

---
# ============================================
# 3. PVC - Püsiv kettaruum (Persistent Volume Claim)
# ============================================
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce  # Üks pod korraga saab kirjutada
  resources:
    requests:
      storage: 500Mi  # Küsi 500MB kettaruumi

---
# ============================================
# 4. STATEFULSET - Andmebaasi pod
# ============================================
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres-service
  replicas: 1  # Ainult 1 koopia (ei skaleeri andmebaasi)
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres  # Label service'i jaoks
    spec:
      containers:
      - name: postgres
        image: postgres:14-alpine  # Alpine = väike image (50MB vs 350MB)
        ports:
        - containerPort: 5432  # PostgreSQL vaikeport
        
        # Keskkonna muutujad ConfigMap'ist ja Secret'ist
        env:
        - name: POSTGRES_DB
          valueFrom:
            configMapKeyRef:
              name: postgres-config
              key: POSTGRES_DB
        - name: POSTGRES_USER
          valueFrom:
            configMapKeyRef:
              name: postgres-config
              key: POSTGRES_USER
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: POSTGRES_PASSWORD
        - name: PGDATA  # Kus PostgreSQL hoiab andmeid
          value: /var/lib/postgresql/data/pgdata
        
        # Kettaruum
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        
        # Ressursi piirangud (väike VM)
        resources:
          requests:
            memory: "128Mi"  # Miinimum RAM
            cpu: "100m"      # 0.1 CPU tuuma
          limits:
            memory: "256Mi"  # Maksimaalne RAM
            cpu: "200m"      # 0.2 CPU tuuma
      
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc  # Kasuta PVC'd

---
# ============================================
# 5. SERVICE - Võrgu ligipääs
# ============================================
apiVersion: v1
kind: Service
metadata:
  name: postgres-service  # DNS nimi klasteri sees!
spec:
  selector:
    app: postgres  # Leiab pod'id selle label'iga
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP  # Ainult klasteri sees, mitte väljast
EOF
```

## Deploy ja Seadistamine

### 📍 **VM SEES**

```bash
# 1. Deploy PostgreSQL
kubectl apply -f postgres-minimal.yaml

# 2. Vaadake loodud ressursse
kubectl get all
kubectl get pvc  # Peaks näitama "Bound"
kubectl get secrets
kubectl get configmaps

# 3. Oodake kuni pod on valmis (30-60 sek)
kubectl wait --for=condition=ready pod postgres-0 --timeout=120s

# Või jälgige reaalajas
kubectl get pods -w
# Oodake: postgres-0  1/1  Running
# Ctrl+C väljumiseks
```

## Andmebaasi Initsialiseerimine

### 📍 **VM SEES**

```bash
# 1. Looge SQL fail tabelite ja andmetega
cat > init-db.sql << 'EOF'
-- Toodete tabel
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sisestame näidistooted
INSERT INTO products (name, description, price, stock, category) VALUES
('Dell XPS 13', 'Õhuke sülearvuti', 1299.99, 5, 'Arvutid'),
('Logitech Hiir', 'Juhtmeta hiir', 89.99, 15, 'Tarvikud'),
('Mehaaniline Klaviatuur', '65% klaviatuur', 119.99, 8, 'Tarvikud'),
('LG Monitor 27"', '4K IPS ekraan', 449.99, 3, 'Monitorid'),
('Sony Kõrvaklapid', 'Mürasummutusega', 279.99, 12, 'Audio');
EOF

# 2. Käivitage SQL pod'i sees
kubectl exec -i postgres-0 -- psql -U shopuser -d shopdb < init-db.sql

# 3. Kontrollige
kubectl exec postgres-0 -- psql -U shopuser -d shopdb -c "SELECT * FROM products;"
```

### ✅ Kontrollpunkt

```bash
kubectl exec postgres-0 -- psql -U shopuser -d shopdb -c "SELECT COUNT(*) FROM products;"
# Peab näitama: count = 5
```

---

# 🔧 Backend API

## Mis on Deployment?

```yaml
# 🔵 KUBERNETES KONTSEPT: Deployment
# - Skaleeritav (1-100 koopiat)
# - Self-healing (taastab kukkunud pod'id)
# - Rolling updates (järk-järguline uuendus)
# - Sobib stateless rakendustele
```

## Backend Konfiguratsioon

### 📍 **VM SEES** - Looge fail

```bash
cat > backend-minimal.yaml << 'EOF'
# ============================================
# 1. CONFIGMAP - Hoiab koodi (ebatavaline, aga õppimiseks hea)
# ============================================
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-code
data:
  # Node.js package.json
  package.json: |
    {
      "name": "shop-backend",
      "version": "1.0.0",
      "main": "server.js",
      "dependencies": {
        "express": "^4.18.2",    # Web framework
        "pg": "^8.11.0",         # PostgreSQL klient
        "cors": "^2.8.5"         # Cross-origin lubamine
      }
    }
  
  # Node.js API kood
  server.js: |
    const express = require('express');
    const { Pool } = require('pg');
    const cors = require('cors');
    
    const app = express();
    
    // Middleware
    app.use(cors());         // Luba kõik päringud (dev)
    app.use(express.json());  // Parse JSON body
    
    // PostgreSQL ühendus
    const pool = new Pool({
      host: 'postgres-service',  // Service DNS nimi!
      port: 5432,
      database: 'shopdb',
      user: 'shopuser',
      password: 'secretpassword',
      max: 5  // Max 5 ühendust
    });
    
    // Health check - Kubernetes kontrollib
    app.get('/health', (req, res) => {
      res.json({ status: 'OK' });
    });
    
    // Readiness check - Kas valmis päringuteks
    app.get('/ready', async (req, res) => {
      try {
        await pool.query('SELECT 1');
        res.json({ ready: true });
      } catch (err) {
        res.status(503).json({ ready: false });
      }
    });
    
    // API: Kõik tooted
    app.get('/api/products', async (req, res) => {
      try {
        const result = await pool.query('SELECT * FROM products ORDER BY id');
        res.json({ success: true, data: result.rows });
      } catch (err) {
        res.status(500).json({ error: err.message });
      }
    });
    
    // API: Üks toode
    app.get('/api/products/:id', async (req, res) => {
      try {
        const result = await pool.query(
          'SELECT * FROM products WHERE id = $1',
          [req.params.id]
        );
        res.json({ success: true, data: result.rows[0] });
      } catch (err) {
        res.status(500).json({ error: err.message });
      }
    });
    
    // Käivita server
    app.listen(3000, () => {
      console.log('Backend running on port 3000');
    });

---
# ============================================
# 2. DEPLOYMENT - API server
# ============================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
spec:
  replicas: 1  # Alustame 1 koopiaga (saab skaleerida)
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend  # Label service'i jaoks
    spec:
      # Init container - paigaldab npm paketid
      initContainers:
      - name: npm-install
        image: node:18-alpine
        command: ['sh', '-c']
        args:
        - |
          cp /code/* /app/           # Kopeeri kood
          cd /app
          npm install --production    # Installi paketid
          echo "NPM install complete!"
        volumeMounts:
        - name: code
          mountPath: /code
        - name: app
          mountPath: /app
        resources:
          limits:
            memory: "256Mi"
      
      # Põhikonteiner
      containers:
      - name: api
        image: node:18-alpine
        command: ['npm', 'start']
        workingDir: /app
        ports:
        - containerPort: 3000
        
        volumeMounts:
        - name: app
          mountPath: /app
        
        # Ressursi piirangud (väike)
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
        
        # Kubernetes health checks
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 30
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 10
      
      volumes:
      - name: code
        configMap:
          name: backend-code  # Kood ConfigMap'ist
      - name: app
        emptyDir: {}         # Temp kaust npm pakettidele

---
# ============================================
# 3. SERVICE - API võrgu ligipääs
# ============================================
apiVersion: v1
kind: Service
metadata:
  name: backend-service  # DNS nimi!
spec:
  selector:
    app: backend  # Leiab pod'id
  ports:
  - port: 3000
    targetPort: 3000
  type: ClusterIP
EOF
```

## Deploy ja Testimine

### 📍 **VM SEES**

```bash
# 1. Deploy backend
kubectl apply -f backend-minimal.yaml

# 2. Jälgige pod'i käivitumist
kubectl get pods -l app=backend -w
# Oodake: backend-api-xxx  1/1  Running
# Init võib võtta 30-60 sekundit (npm install)

# 3. Vaadake logisid
kubectl logs -l app=backend
```

### API Testimine

### 📍 **VM SEES - Terminal 1**

```bash
# Port forward localhost'i
kubectl port-forward service/backend-service 3000:3000
# Jääb töötama! ÄRA SULGE!
```

### 📍 **VM SEES - Terminal 2** (Uus terminal/tab)

```bash
# Testi health
curl http://localhost:3000/health
# Oodatav: {"status":"OK"}

# Testi products API
curl http://localhost:3000/api/products
# Oodatav: JSON 5 tootega

# Testi üksik toode
curl http://localhost:3000/api/products/1
# Oodatav: Dell XPS 13 info
```

### ✅ Kontrollpunkt

API peab tagastama 5 toodet PostgreSQL'ist!

---

# 🎨 Frontend

## Frontend Konfiguratsioon

### 📍 **VM SEES** - Looge fail

```bash
cat > frontend-simple.yaml << 'EOF'
# ============================================
# 1. CONFIGMAP - HTML leht
# ============================================
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-html
data:
  index.html: |
    <!DOCTYPE html>
    <html lang="et">
    <head>
        <meta charset="UTF-8">
        <title>Kubernetes E-Pood</title>
        <style>
            /* 🎨 MUUTKE VÄRVE SIIN! */
            body { 
                font-family: Arial, sans-serif; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: white; 
                padding: 20px; 
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            h1 { color: #333; }
            .info { 
                background: #e7f3ff; 
                padding: 15px; 
                margin: 20px 0; 
                border-radius: 5px;
            }
            .product { 
                border: 1px solid #ddd; 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 5px;
                transition: transform 0.2s;
            }
            .product:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .stock { 
                color: green; 
                font-weight: bold; 
            }
            .error { 
                color: red; 
                padding: 10px;
                background: #ffeeee;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Kubernetes E-Pood</h1>
            <div class="info">
                <p><strong>Pod:</strong> <span id="podname"></span></p>
                <p><strong>Versioon:</strong> <span style="color: blue;">v1.0</span></p>
                <p><strong>Staatus:</strong> <span id="status">Kontrollin...</span></p>
            </div>
            <h2>Tooted:</h2>
            <div id="products">Laadin tooteid...</div>
        </div>
        
        <script>
            // Näita pod'i nime
            document.getElementById('podname').textContent = location.hostname;
            
            // Lae tooted API'st
            fetch('/api/products')
                .then(response => {
                    if (!response.ok) throw new Error('API ei vasta');
                    return response.json();
                })
                .then(data => {
                    document.getElementById('status').textContent = '✅ Ühendatud';
                    
                    let html = '';
                    if (data.data && data.data.length > 0) {
                        data.data.forEach(product => {
                            html += `
                                <div class="product">
                                    <h3>${product.name}</h3>
                                    <p>${product.description || 'Kirjeldus puudub'}</p>
                                    <p><strong>Hind:</strong> €${product.price}</p>
                                    <p class="stock">Laos: ${product.stock} tk</p>
                                </div>
                            `;
                        });
                    } else {
                        html = '<p>Tooteid ei leitud</p>';
                    }
                    document.getElementById('products').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('status').textContent = '❌ Viga';
                    document.getElementById('products').innerHTML = 
                        `<div class="error">Viga: ${error.message}</div>`;
                });
        </script>
    </body>
    </html>

---
# ============================================
# 2. CONFIGMAP - Nginx konfiguratsioon
# ============================================
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  default.conf: |
    server {
        listen 80;
        
        # Staatilised failid
        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
        
        # API päringud → backend service'sse
        location /api {
            proxy_pass http://backend-service:3000;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
        }
    }

---
# ============================================
# 3. DEPLOYMENT - Nginx server
# ============================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
        
        volumeMounts:
        - name: html
          mountPath: /usr/share/nginx/html
        - name: config
          mountPath: /etc/nginx/conf.d
        
        resources:
          requests:
            memory: "32Mi"
            cpu: "25m"
          limits:
            memory: "64Mi"
            cpu: "50m"
      
      volumes:
      - name: html
        configMap:
          name: frontend-html
      - name: config
        configMap:
          name: nginx-config

---
# ============================================
# 4. SERVICE - NodePort väline ligipääs
# ============================================
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
  type: NodePort  # NodePort = ligipääs väljast!
  # Kubernetes määrab automaatselt pordi 30000-32767 vahel
EOF
```

## Deploy ja Ligipääs

### 📍 **VM SEES**

```bash
# 1. Deploy frontend
kubectl apply -f frontend-simple.yaml

# 2. Oodake kuni pod töötab
kubectl get pods -l app=frontend -w

# 3. Vaadake määratud NodePort
kubectl get service frontend-service
# Näide väljund:
# NAME               TYPE       PORT(S)        
# frontend-service   NodePort   80:30500/TCP
#                                  ^^^^^ See on teie port!
```

## Ligipääs Brauserist

### 📍 **VM SEES - Terminal 1**

```bash
# Port forward KÕIGILE võrguliidestele
kubectl port-forward --address 0.0.0.0 service/frontend-service 8080:80

# Jääb töötama! ÄRA SULGE!
# Näete: Forwarding from 0.0.0.0:8080 -> 80
```

### 📍 **KOHALIK ARVUTI** - Teie brauser

```bash
# 1. Leidke VM IP aadress
# Multipass kasutajad:
multipass info k8s-lab | grep IPv4
# Näide: 192.168.2.10

# VirtualBox kasutajad:
# VM'is: ip addr show | grep inet

# 2. Avage brauseris:
http://<VM-IP>:8080
# Näide: http://192.168.2.10:8080
```

### ✅ Mida Peaksite Nägema

- ✅ Valge konteiner sinise gradiendi taustal
- ✅ "Kubernetes E-Pood" pealkiri
- ✅ Pod'i nimi (IP aadress)
- ✅ Versioon: v1.0
- ✅ Staatus: ✅ Ühendatud
- ✅ 5 toodet koos hindade ja laoseisuga

---

# 📊 Dashboard

## Kubernetes Dashboard

### 📍 **VM SEES - Terminal 1**

```bash
# Kontrollige dashboard addon
minikube addons list | grep dashboard

# Kui disabled, siis luba
minikube addons enable dashboard

# Käivitage dashboard
minikube dashboard --url

# Näete URL'i:
# http://127.0.0.1:XXXXX/api/v1/namespaces/kubernetes-dashboard/...
# JÄTKE TÖÖTAMA!
```

### 📍 **VM SEES - Terminal 2** (Uus)

```bash
# Proxy kõigile liidestele
kubectl proxy --address='0.0.0.0' --accept-hosts='^.*$'

# JÄTKE TÖÖTAMA!
```

### 📍 **KOHALIK ARVUTI** - Brauser

```
http://<VM-IP>:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
```

## Mida Dashboard'is Vaadata

### 🔵 **Workloads**
- **Deployments**: 2 (backend-api, frontend)
- **Pods**: 3 running (roheline ring)
- **Replica Sets**: Automaatselt loodud
- **Stateful Sets**: 1 (postgres)

### 🔵 **Service**
- 3 service'i (postgres, backend, frontend)
- Igaüks näitab Endpoints (pod'ide IP'd)

### 🔵 **Config and Storage**
- **ConfigMaps**: 4 tk (kood ja konfig)
- **Secrets**: 1 (postgres parool)
- **PVC**: postgres-pvc (Bound staatuses)

---

# 🧪 Kubernetes Kontseptid

## 1. Self-Healing Test

### 📍 **VM SEES**

```bash
# "Tapa" backend pod
kubectl delete pod $(kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}')

# Vaadake reaalajas
kubectl get pods -w

# 🎯 TULEMUS: Uus pod tekib automaatselt 30 sekundi jooksul!
```

## 2. Skaleerimine

### 📍 **VM SEES**

```bash
# Skaleeri 3 koopiaga
kubectl scale deployment backend-api --replicas=3

# Vaata tulemust
kubectl get pods -l app=backend

# 🎯 TULEMUS: 3 backend pod'i töötavad paralleelselt!

# Skaleeri tagasi
kubectl scale deployment backend-api --replicas=1
```

## 3. Rolling Update

### 📍 **VM SEES**

```bash
# Muuda versiooni
kubectl set env deployment/frontend VERSION=v2.0

# Jälgi uuendust
kubectl rollout status deployment/frontend

# 🎯 TULEMUS: Brauser näitab v2.0 pärast värskendust!
```

---

# 🎨 Lisaülesanded

## Ülesanne 1: Muutke Värve

### 📍 **VM SEES**

```bash
# 1. Muutke ConfigMap
kubectl edit configmap frontend-html

# 2. Leidke style sektsioon
# Muutke:
# background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# Uueks:
# background: linear-gradient(135deg, #ff6b6b 0%, #ffd93d 100%);

# 3. Salvestage (ESC, :wq)

# 4. Taaskäivitage pod
kubectl rollout restart deployment/frontend

# 5. Värskendage brauser!
```

## Ülesanne 2: Lisage Toode

### 📍 **VM SEES**

```bash
# Lisa uus toode otse andmebaasi
kubectl exec -it postgres-0 -- psql -U shopuser -d shopdb

# SQL prompt'is:
INSERT INTO products (name, description, price, stock, category) 
VALUES ('iPhone 15', 'Uusim Apple telefon', 999.99, 10, 'Telefonid');

# Välju: \q

# Värskendage brauser - näete 6 toodet!
```

---

# 🧹 Puhastamine

## Kõige Kustutamine

### 📍 **VM SEES**

```bash
# 1. Kustuta rakendus
kubectl delete -f postgres-minimal.yaml
kubectl delete -f backend-minimal.yaml
kubectl delete -f frontend-simple.yaml

# 2. Kontrolli
kubectl get all
# Peaks olema tühi

# 3. Peata Minikube (säilitab andmed)
minikube stop

# VÕI

# 4. Kustuta kõik (täielik reset)
minikube delete
```

## Uuesti Alustamine

### 📍 **VM SEES**

```bash
# Kui tegite 'minikube delete'
minikube start --cpus=2 --memory=2000 --driver=docker

# Deploy kõik uuesti järjekorras:
kubectl apply -f postgres-minimal.yaml
kubectl wait --for=condition=ready pod postgres-0 --timeout=120s
kubectl exec -i postgres-0 -- psql -U shopuser -d shopdb < init-db.sql
kubectl apply -f backend-minimal.yaml
kubectl apply -f frontend-simple.yaml
```

---

# 📝 Kokkuvõte

## Mida Õppisite

### ✅ Kubernetes Arhitektuur
- **Pod**: Väikseim üksus (üks konteiner)
- **Deployment**: Skaleeritav, self-healing
- **StatefulSet**: Püsiv identiteet, andmebaasidele
- **Service**: Sisene load balancer, DNS

### ✅ Võrgundus
- **ClusterIP**: Ainult klasteri sees
- **NodePort**: Ligipääs väljast (30000-32767)
- **DNS**: backend-service:3000

### ✅ Konfiguratsioon
- **ConfigMap**: Avalik konfig ja kood
- **Secret**: Paroolid (base64)
- **PVC**: Püsiv salvestus

### ✅ Praktilised Oskused
- kubectl käsud
- Port forwarding
- Logimine ja debugging
- Dashboard kasutamine

## Järgmised Sammud

1. **Proovige Helm** - Kubernetes paketihaldur
2. **Õppige Ingress** - Domeeninimed
3. **CI/CD** - GitLab/GitHub Actions
4. **Monitoring** - Prometheus + Grafana
5. **Service Mesh** - Istio

---

**Labor Lõppenud! 🎉**

Küsimuste korral:
- Kubernetes Docs: https://kubernetes.io/docs/
- kubectl Cheat Sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
