# Kubernetes Labor: E-Pood Mikroteenustega

---

# 📚 Sisukord

1. [Sissejuhatus](#sissejuhatus)
2. [Ettevalmistus](#ettevalmistus)
3. [Kubernetes Klaster](#kubernetes-klaster)
4. [PostgreSQL Andmebaas](#postgresql-andmebaas)
5. [Backend API](#backend-api)
6. [Frontend](#frontend)
7. [Ligipääs ja Testimine](#ligipääs-ja-testimine)
8. [Kubernetes Kontseptid](#kubernetes-kontseptid)
9. [Dokumentatsioon](#dokumentatsioon)

---

# 🎯 Sissejuhatus

## Mida Me Ehitame

E-pood kolme komponendiga: andmebaas (PostgreSQL), API server (Node.js), veebileht (Nginx). Kõik komponendid töötavad Kubernetes klastris eraldi pod'ides. Nad suhtlevad omavahel läbi Kubernetes Service'ite.

```
┌────────────────────────────────────────────────┐
│                   BRAUSER                      │
│                (Teie arvuti)                   │
└────────────────┬───────────────────────────────┘
                 │ HTTP :8080
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

## Failide Struktuur

Loome eraldi failid iga komponendi jaoks. See teeb debugging'u lihtsamaks. Kui midagi ei tööta, saate kontrollida konkreetset faili.

```
k8s-lab/
├── postgres/
│   ├── 1-configmap.yaml     # Avalikud seaded
│   ├── 2-secret.yaml        # Parool
│   ├── 3-pvc.yaml          # Kettaruum
│   ├── 4-statefulset.yaml  # Pod definitsioon
│   └── 5-service.yaml      # Võrgu ligipääs
├── backend/
│   ├── 1-configmap.yaml    # Node.js kood
│   ├── 2-deployment.yaml   # Pod definitsioon
│   └── 3-service.yaml      # Võrgu ligipääs
└── frontend/
    ├── 1-html.yaml         # HTML leht
    ├── 2-nginx.yaml        # Nginx config
    ├── 3-deployment.yaml   # Pod definitsioon
    └── 4-service.yaml      # Välise ligipääsu
```

---

# 💻 Ettevalmistus

## 1. VM Loomine

### 📍 **KOHALIK ARVUTI** - Windows + VirtualBox

```
1. Laadige Ubuntu Server 22.04 ISO
   https://ubuntu.com/download/server
   
2. VirtualBox'is:
   - New VM → Ubuntu 64-bit
   - 2 CPU, 4GB RAM, 15GB disk
   - Network: NAT
   
3. Installige Ubuntu:
   - Username: student
   - Password: oma valik
```

### 📍 **KOHALIK ARVUTI** - Mac + Multipass

```bash
# Looge VM
multipass launch --name k8s-lab --cpus 2 --memory 4G --disk 15G

# Sisenemine
multipass shell k8s-lab
```

## 2. Kubernetes Setup

### 📍 **VM SEES** - Kõik järgnevad käsud

```bash
# Kontrollige arhitektuuri
uname -m
# x86_64 = AMD64
# aarch64 = ARM64

# Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Kubectl (vali õige versioon)
# AMD64:
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
# ARM64:
# curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"

chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Minikube (vali õige versioon)  
# AMD64:
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
# ARM64:
# curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-arm64

chmod +x minikube-linux-*
sudo mv minikube-linux-* /usr/local/bin/minikube
```

---

# ☸️ Kubernetes Klaster

### 📍 **VM SEES**

```bash
# Käivita Minikube
minikube start --cpus=2 --memory=2000 --driver=docker

# Kontrolli
minikube status
kubectl get nodes

# Loo projekti kaustad
mkdir -p ~/k8s-lab/{postgres,backend,frontend}
cd ~/k8s-lab
```

---

# 🗄️ PostgreSQL Andmebaas

PostgreSQL vajab 5 eraldi faili. Iga fail teeb üht kindlat asja. ConfigMap hoiab avalikke seadeid nagu andmebaasi nimi. Secret hoiab parooli turvaliselt. PVC küsib kettaruumi, et andmed säiliksid. StatefulSet loob andmebaasi pod'i püsiva nimega. Service annab DNS nime, et teised komponendid leiaksid andmebaasi üles.

## FAIL 1: ConfigMap - Avalikud Seaded

ConfigMap on nagu .env fail, aga Kubernetes'is. Siia paneme info, mis pole salajane. Kui hiljem tahate andmebaasi nime muuta, muudate ainult seda faili. Pole vaja konteinerit uuesti ehitada.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/postgres/1-configmap.yaml
```

```yaml
# ConfigMap hoiab konfiguratsiooni, mis POLE salajane
# Saab muuta ilma konteinerit rebuild'imata
# Kõik pod'id näevad samu väärtusi
apiVersion: v1                    # Kubernetes API versioon
kind: ConfigMap                   # Ressursi tüüp
metadata:
  name: postgres-config           # Nimi, millega viidatakse
  namespace: default              # Namespace (vaikimisi default)
data:                            # Key-value paarid
  POSTGRES_DB: shopdb            # Andmebaasi nimi
  POSTGRES_USER: shopuser        # Kasutajanimi (pole salajane)
```

## FAIL 2: Secret - Paroolid

Secret on spetsiaalselt paroolide jaoks. Kubernetes salvestab Secret'id krüpteeritult etcd andmebaasis. Parool peab olema base64 formaadis. See pole krüpteering, lihtsalt encoding, aga Kubernetes nõuab seda.

### 📍 **VM SEES**

```bash
# Arvuta parool base64 formaadis
echo -n 'secretpassword' | base64
# Tulemus: c2VjcmV0cGFzc3dvcmQ=

nano ~/k8s-lab/postgres/2-secret.yaml
```

```yaml
# Secret hoiab tundlikku infot turvaliselt
# Kubernetes krüpteerib automaatselt
# Ainult volitatud pod'id saavad lugeda
apiVersion: v1
kind: Secret                      # Secret, mitte ConfigMap
metadata:
  name: postgres-secret           # Nimi viitamiseks
  namespace: default
type: Opaque                      # Tavaline secret (on teisi tüüpe)
data:
  # Parool PEAB olema base64 kodeeritud
  # secretpassword → c2VjcmV0cGFzc3dvcmQ=
  POSTGRES_PASSWORD: c2VjcmV0cGFzc3dvcmQ=
```

## FAIL 3: PVC - Püsiv Kettaruum

PVC (Persistent Volume Claim) on taotlus kettaruumi jaoks. Ilma selleta kaovad kõik andmebaasi andmed, kui pod taaskäivitub. PVC tagab, et PostgreSQL'i andmed salvestatakse kettale. See on nagu "external hard drive" konteinerile.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/postgres/3-pvc.yaml
```

```yaml
# PVC = Persistent Volume Claim
# "Ma tahan 500MB kettaruumi"
# Ilma: pod restart = kõik andmed kadunud
apiVersion: v1
kind: PersistentVolumeClaim       # Küsib salvestust
metadata:
  name: postgres-pvc              # Nimi, mida StatefulSet kasutab
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce               # Üks pod korraga
    # ReadWriteMany - mitu pod'i kirjutavad
    # ReadOnlyMany - mitu pod'i loevad
  resources:
    requests:
      storage: 500Mi              # 500 MB ruumi
      # Võimalikud: 1Gi, 10Gi, 100Gi
```

## FAIL 4: StatefulSet - Andmebaasi Pod

StatefulSet loob PostgreSQL pod'i. Miks mitte Deployment? StatefulSet annab püsiva nime (postgres-0), Deployment annaks suvalise (postgres-xyz-abc). Andmebaas vajab püsivat nime, et andmed leiaksid õige pod'i. StatefulSet garanteerib ka õige käivituse järjekorra.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/postgres/4-statefulset.yaml
```

```yaml
# StatefulSet annab püsiva identiteedi
# postgres-0 vs postgres-random-xyz
# Andmebaasid vajavad stabiilsust
apiVersion: apps/v1
kind: StatefulSet                 # MITTE Deployment!
metadata:
  name: postgres
  namespace: default
spec:
  serviceName: postgres-service   # Headless service nimi
  replicas: 1                     # ALATI 1 andmebaasi jaoks
  selector:
    matchLabels:
      app: postgres               # Peab klappima template labels
  
  template:                       # Pod'i mall
    metadata:
      labels:
        app: postgres             # Service leiab selle järgi
    spec:
      containers:
      - name: postgres
        image: postgres:14-alpine  # Alpine = 50MB vs 350MB
        
        ports:
        - containerPort: 5432      # PostgreSQL standard port
          name: postgres
        
        # Environment muutujad
        env:
        - name: POSTGRES_DB
          valueFrom:
            configMapKeyRef:      # Võta ConfigMap'ist
              name: postgres-config
              key: POSTGRES_DB
        
        - name: POSTGRES_USER
          valueFrom:
            configMapKeyRef:
              name: postgres-config
              key: POSTGRES_USER
        
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:         # Võta Secret'ist (turvaline)
              name: postgres-secret
              key: POSTGRES_PASSWORD
        
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
          # PostgreSQL vajab alamkausta
        
        # Kus hoiame andmeid
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
          # PostgreSQL vaikimisi andmete asukoht
        
        # Ressursi piirangud väikse VM jaoks
        resources:
          requests:
            memory: "128Mi"       # Garanteeritud RAM
            cpu: "100m"           # 0.1 CPU tuuma
          limits:
            memory: "256Mi"       # Maksimaalne RAM
            cpu: "200m"           # 0.2 CPU tuuma
      
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc # Viide PVC failile
```

## FAIL 5: Service - Võrgu Ligipääs

Service annab andmebaasile püsiva võrguaadressi. Ilma Service'ita peaks backend teadma pod'i IP aadressi, mis muutub iga restart'iga. Service annab DNS nime (postgres-service), mis ei muutu kunagi. See on nagu telefoni kontakt vs telefoninumber.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/postgres/5-service.yaml
```

```yaml
# Service = püsiv võrguaadress ja DNS nimi
# Teised pod'id: postgres-service:5432
apiVersion: v1
kind: Service
metadata:
  name: postgres-service          # DNS nimi!
  namespace: default
spec:
  selector:
    app: postgres                 # Leiab pod'id selle label'iga
  ports:
  - port: 5432                    # Service port
    targetPort: 5432              # Container port
    protocol: TCP
  type: ClusterIP                 # Ainult klastri sees
  # NodePort = väljast ligipääs
  # LoadBalancer = pilves (AWS, GCP)
```

## PostgreSQL Deploy ja Test

### 📍 **VM SEES**

```bash
# Deploy kõik PostgreSQL failid
kubectl apply -f ~/k8s-lab/postgres/

# Kontrolli mis loodi
kubectl get all
kubectl get pvc
kubectl get configmap
kubectl get secret

# Oota kuni pod töötab
kubectl wait --for=condition=ready pod postgres-0 --timeout=120s

# Initsialiseeri andmebaas
cat > ~/k8s-lab/init.sql << 'EOF'
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price DECIMAL(10,2),
    stock INTEGER
);

INSERT INTO products (name, description, price, stock) VALUES
('Dell XPS 13', 'Sülearvuti', 1299.99, 5),
('Logitech Hiir', 'Juhtmeta', 89.99, 15),
('Klaviatuur', 'Mehaaniline', 119.99, 8),
('Monitor LG', '4K 27 toll', 449.99, 3),
('Kõrvaklapid', 'Sony', 279.99, 12);
EOF

kubectl exec -i postgres-0 -- psql -U shopuser -d shopdb < ~/k8s-lab/init.sql

# Test
kubectl exec postgres-0 -- psql -U shopuser -d shopdb -c "SELECT * FROM products;"
```

### ✅ Kontrollpunkt
Peate nägema 5 toodet tabelis!

---

# 🔧 Backend API

Backend on Node.js API server. Ta ühendub PostgreSQL'iga ja serveerib JSON andmeid. Kasutame Deployment'i, sest backend on stateless - tal pole püsiandmeid. Saab skaleerida mitme koopiaga.

## FAIL 1: ConfigMap - Node.js Kood

Tavaliselt ehitatakse Docker image koodiga. Õppimise jaoks hoiame koodi ConfigMap'is. See lubab muuta koodi ilma Docker'it kasutamata. Produktsioonis ÄRGE tehke nii.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/backend/1-configmap.yaml
```

```yaml
# Backend kood ConfigMap'is
# Ebatavaline, aga õppimiseks mugav
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-code
  namespace: default
data:
  # package.json - Node.js sõltuvused
  package.json: |
    {
      "name": "shop-backend",
      "version": "1.0.0",
      "main": "server.js",
      "dependencies": {
        "express": "^4.18.2",
        "pg": "^8.11.0",
        "cors": "^2.8.5"
      }
    }
  
  # server.js - API kood
  server.js: |
    const express = require('express');
    const { Pool } = require('pg');
    const cors = require('cors');
    
    const app = express();
    
    // Middleware seadistus
    app.use(cors());              // Luba cross-origin
    app.use(express.json());      // Parse JSON body
    
    // PostgreSQL ühendus
    const pool = new Pool({
      host: 'postgres-service',   // Service DNS nimi!
      port: 5432,
      database: 'shopdb',
      user: 'shopuser',
      password: 'secretpassword',
      max: 5                       // Max 5 ühendust
    });
    
    // Health check Kubernetes'ile
    app.get('/health', (req, res) => {
      res.json({ 
        status: 'OK',
        timestamp: new Date()
      });
    });
    
    // Ready check - kas andmebaas töötab
    app.get('/ready', async (req, res) => {
      try {
        await pool.query('SELECT 1');
        res.json({ ready: true });
      } catch (err) {
        res.status(503).json({ ready: false });
      }
    });
    
    // API: kõik tooted
    app.get('/api/products', async (req, res) => {
      try {
        const result = await pool.query('SELECT * FROM products ORDER BY id');
        res.json({ 
          success: true,
          count: result.rows.length,
          data: result.rows 
        });
      } catch (err) {
        console.error('Database error:', err);
        res.status(500).json({ error: err.message });
      }
    });
    
    // API: üks toode
    app.get('/api/products/:id', async (req, res) => {
      try {
        const result = await pool.query(
          'SELECT * FROM products WHERE id = $1',
          [req.params.id]
        );
        
        if (result.rows.length === 0) {
          return res.status(404).json({ error: 'Product not found' });
        }
        
        res.json({ 
          success: true,
          data: result.rows[0] 
        });
      } catch (err) {
        res.status(500).json({ error: err.message });
      }
    });
    
    // Käivita server
    const PORT = 3000;
    app.listen(PORT, () => {
      console.log('Backend API running on port', PORT);
    });
```

## FAIL 2: Deployment

Deployment sobib stateless rakendustele. Backend ei salvesta midagi, ainult töötleb päringuid. Deployment lubab skaleerida (1→10 pod'i) ja teeb automaatse taaskäivituse kui pod kukub. Init container installib npm paketid enne põhikonteineri käivitust.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/backend/2-deployment.yaml
```

```yaml
# Deployment backend API jaoks
# Stateless, skaleeritav, self-healing
apiVersion: apps/v1
kind: Deployment                  # Mitte StatefulSet!
metadata:
  name: backend-api
  namespace: default
spec:
  replicas: 1                     # Alusta 1, saab skaleerida
  selector:
    matchLabels:
      app: backend                # Peab klappima pod labels
  
  template:                       # Pod'i mall
    metadata:
      labels:
        app: backend              # Service leiab selle järgi
    spec:
      # Init container - käivitub esimesena
      initContainers:
      - name: npm-install
        image: node:18-alpine
        command: ['sh', '-c']
        args:
        - |
          echo "Installing npm packages..."
          cp /code/* /app/        # Kopeeri kood
          cd /app
          npm install --production # Installi paketid
          echo "Dependencies installed!"
        volumeMounts:
        - name: code
          mountPath: /code        # ConfigMap siia
        - name: app
          mountPath: /app         # NPM paketid siia
        resources:
          limits:
            memory: "256Mi"
            cpu: "200m"
      
      # Põhikonteiner
      containers:
      - name: api
        image: node:18-alpine
        command: ['node', '/app/server.js']
        workingDir: /app
        
        ports:
        - containerPort: 3000
          name: http
        
        volumeMounts:
        - name: app
          mountPath: /app         # NPM + kood siin
        
        # Health checks
        livenessProbe:           # Kas pod töötab?
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30 # Oota 30s enne kontrolli
          periodSeconds: 30       # Kontrolli iga 30s
        
        readinessProbe:           # Kas valmis päringuteks?
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 10
        
        # Ressursid
        resources:
          requests:
            memory: "64Mi"        # Garanteeritud
            cpu: "50m"
          limits:
            memory: "128Mi"       # Maksimaalne
            cpu: "100m"
      
      volumes:
      - name: code
        configMap:
          name: backend-code      # Kood ConfigMap'ist
      - name: app
        emptyDir: {}             # Ajutine NPM jaoks
```

## FAIL 3: Service

Backend Service teeb load balancing'u kui on mitu pod'i. DNS nimi backend-service on kättesaadav kõigile pod'idele klastris. Frontend kasutab seda nime API päringuteks.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/backend/3-service.yaml
```

```yaml
# Service backend API jaoks
# Load balancer ja DNS
apiVersion: v1
kind: Service
metadata:
  name: backend-service           # DNS nimi
  namespace: default
spec:
  selector:
    app: backend                  # Leiab pod'id
  ports:
  - port: 3000                    # Service port
    targetPort: 3000              # Container port
    protocol: TCP
  type: ClusterIP                 # Sisene
```

## Backend Deploy ja Test

### 📍 **VM SEES**

```bash
# Deploy
kubectl apply -f ~/k8s-lab/backend/

# Oota kuni valmis (npm install võtab aega)
kubectl get pods -l app=backend -w

# Test API
kubectl port-forward service/backend-service 3000:3000 &
curl http://localhost:3000/health
curl http://localhost:3000/api/products
kill %1

# Vaata logisid
kubectl logs -l app=backend
```

### ✅ Kontrollpunkt
API peab tagastama 5 toodet JSON formaadis!

---

# 🎨 Frontend

Frontend on Nginx server, mis serveerib HTML lehte. Nginx teeb ka proxy API päringutele backend'i. Kasutame NodePort Service'i, et pääseda ligi väljast.

## FAIL 1: HTML ConfigMap

HTML ja JavaScript on ConfigMap'is. See lubab muuta kasutajaliidest ilma Docker image't ehitamata. JavaScript teeb AJAX päringuid backend API'sse.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/frontend/1-html.yaml
```

```yaml
# Frontend HTML ja JavaScript
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-html
  namespace: default
data:
  index.html: |
    <!DOCTYPE html>
    <html lang="et">
    <head>
        <meta charset="UTF-8">
        <title>Kubernetes E-Pood</title>
        <style>
            /* CSS stiilid */
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
            }
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
                background: #ffeeee;
                padding: 10px;
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
            // Näita pod'i hostname
            document.getElementById('podname').textContent = location.hostname;
            
            // Lae tooted API'st
            fetch('/api/products')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('API ei vasta');
                    }
                    return response.json();
                })
                .then(data => {
                    // Uuenda staatus
                    document.getElementById('status').textContent = '✅ Ühendatud';
                    
                    // Näita tooted
                    if (data.data && data.data.length > 0) {
                        let html = '';
                        data.data.forEach(product => {
                            html += `
                                <div class="product">
                                    <h3>${product.name}</h3>
                                    <p>${product.description || 'Toote kirjeldus'}</p>
                                    <p><strong>Hind:</strong> €${product.price}</p>
                                    <p class="stock">Laos: ${product.stock} tk</p>
                                </div>
                            `;
                        });
                        document.getElementById('products').innerHTML = html;
                    } else {
                        document.getElementById('products').innerHTML = 
                            '<p>Tooteid ei leitud</p>';
                    }
                })
                .catch(error => {
                    document.getElementById('status').textContent = '❌ Viga';
                    document.getElementById('products').innerHTML = 
                        `<div class="error">Viga: ${error.message}</div>`;
                });
        </script>
    </body>
    </html>
```

## FAIL 2: Nginx Config

Nginx konfiguratsioon määrab, kuidas käsitleda päringuid. Staatilised failid (HTML, CSS) serveeritakse otse. API päringud (/api/*) suunatakse backend-service'isse. See on reverse proxy.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/frontend/2-nginx.yaml
```

```yaml
# Nginx server konfiguratsioon
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: default
data:
  default.conf: |
    server {
        listen 80;                 # Kuula port 80
        server_name _;            # Kõik domeeninimed
        
        # Staatilised failid
        location / {
            root /usr/share/nginx/html;
            index index.html;
            try_files $uri $uri/ /index.html;
        }
        
        # API proxy backend'i
        location /api {
            proxy_pass http://backend-service:3000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
```

## FAIL 3: Deployment

Frontend Deployment loob Nginx pod'i. Volume mount'id ühendavad ConfigMap'id õigetesse kohtadesse. Nginx loeb automaatselt konfiguratsiooni /etc/nginx/conf.d kaustast.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/frontend/3-deployment.yaml
```

```yaml
# Frontend Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: default
spec:
  replicas: 1                     # Alusta 1 koopiaga
  selector:
    matchLabels:
      app: frontend
  
  template:
    metadata:
      labels:
        app: frontend              # Service label
    spec:
      containers:
      - name: nginx
        image: nginx:alpine        # Väike Nginx image
        
        ports:
        - containerPort: 80
          name: http
        
        # Mount ConfigMaps õigetesse kohtadesse
        volumeMounts:
        - name: html
          mountPath: /usr/share/nginx/html
          # Nginx otsib HTML'i siit
        - name: config
          mountPath: /etc/nginx/conf.d
          # Nginx loeb config'i siit
        
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
          name: frontend-html      # HTML ConfigMap
      - name: config
        configMap:
          name: nginx-config       # Nginx ConfigMap
```

## FAIL 4: Service - NodePort

NodePort Service teeb frontend'i kättesaadavaks väljast. Kubernetes valib automaatselt pordi vahemikus 30000-32767. See port on avatud kõigil node'idel. ClusterIP oleks ainult sisevõrgus.

### 📍 **VM SEES**

```bash
nano ~/k8s-lab/frontend/4-service.yaml
```

```yaml
# Frontend Service - väline ligipääs
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: default
spec:
  selector:
    app: frontend                  # Leiab frontend pod'id
  ports:
  - port: 80                       # Service port
    targetPort: 80                 # Container port
    protocol: TCP
  type: NodePort                   # Väline ligipääs!
  # Kubernetes valib pordi 30000-32767
```

## Frontend Deploy

### 📍 **VM SEES**

```bash
# Deploy
kubectl apply -f ~/k8s-lab/frontend/

# Vaata mis port määrati
kubectl get service frontend-service
# PORT(S): 80:30XXX/TCP

# Oota kuni valmis
kubectl get pods -l app=frontend -w
```

---

# 🌐 Ligipääs ja Testimine

## Port Forwarding

### 📍 **VM SEES - Terminal 1**

```bash
# Port forward kõigile IP'dele
kubectl port-forward --address 0.0.0.0 service/frontend-service 8080:80

# Jätke töötama!
```

### 📍 **KOHALIK ARVUTI - Brauser**

```bash
# Leidke VM IP
# Multipass: multipass info k8s-lab | grep IPv4
# VirtualBox: ip addr show

# Avage brauseris
http://<VM-IP>:8080
```

### ✅ Mida Peaksite Nägema

- Valge kast sinise taustaga
- "Kubernetes E-Pood" pealkiri
- Pod'i hostname
- 5 toodet andmebaasist
- Roheline "Ühendatud" staatus

---

# 🧪 Kubernetes Kontseptid

## Self-Healing Test

### 📍 **VM SEES**

```bash
# Kustuta pod
kubectl delete pod $(kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}')

# Vaata kuidas taastub
kubectl get pods -w
```

Kubernetes näeb, et Deployment tahab 1 pod'i, aga on 0. Loob automaatselt uue pod'i. See on self-healing.

## Skaleerimine

```bash
# Skalee 3 koopiaga
kubectl scale deployment backend-api --replicas=3

kubectl get pods -l app=backend
```

Service teeb automaatse load balancing'u 3 pod'i vahel.

## Rolling Update

```bash
# Muuda environment
kubectl set env deployment/frontend VERSION=v2.0

kubectl rollout status deployment/frontend
```

Kubernetes loob uue pod'i v2.0, ootab kuni valmis, siis kustutab vana. Zero downtime!

---

# 📚 Dokumentatsioon

## Kubernetes Ressursid
- **ConfigMap**: https://kubernetes.io/docs/concepts/configuration/configmap/
- **Secret**: https://kubernetes.io/docs/concepts/configuration/secret/
- **Deployment**: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- **StatefulSet**: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- **Service**: https://kubernetes.io/docs/concepts/services-networking/service/
- **PVC**: https://kubernetes.io/docs/concepts/storage/persistent-volumes/

## kubectl Käsud
- **Cheatsheet**: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- **Reference**: https://kubernetes.io/docs/reference/kubectl/

## Debugging
```bash
kubectl describe pod <name>       # Detailne info
kubectl logs <pod-name>           # Logid
kubectl exec -it <pod> -- bash    # Sisene pod'i
kubectl get events               # Klasteri sündmused
```

---

**Labor Lõppenud! 🎉**
