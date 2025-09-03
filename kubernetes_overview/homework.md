# Kubernetes Overview Kodutöö: Kohalik Container Orchestration

## 🎯 Ülesande Kirjeldus

**Projekt:** "TechShop" E-commerce Kubernetes Deployment

**Eesmärk:** Deploy'ida lihtne e-commerce rakendus Kubernetes'i kasutades kohalikku Minikube keskkonda.

**Aeg:** 2-3 tundi

---

## 📋 Ülesande Nõuded

### 1. Rakenduse Arhitektuur

**TechShop koosneb kolmest komponendist:**

```yaml
# Arhitektuur:
Frontend (React) → Backend (Node.js) → Database (PostgreSQL)
     ↓                    ↓                    ↓
  nginx:alpine      node:16-alpine      postgres:13
```

### 2. Vajalikud Ressursid

**Kubernetes ressursid:**
- **3 Deployment'i** - frontend, backend, database
- **3 Service'i** - frontend, backend, database
- **1 ConfigMap** - rakenduse konfiguratsioon
- **1 Secret** - andmebaasi parool
- **1 PersistentVolumeClaim** - andmebaasi andmete salvestamine

---

## 🚀 Samm 1: Projekti Struktuuri Loomine (30 min)

### 1.1: Loo projekt struktuur

```bash
# Loo projekt kaust
mkdir techshop-kubernetes
cd techshop-kubernetes

# Loo faili struktuur
mkdir -p {frontend,backend,database,config}
touch README.md
```

### 1.2: Loo README.md

```markdown
# TechShop Kubernetes Deployment

## Projekt kirjeldus
Lihtne e-commerce rakendus Kubernetes'i kasutades.

## Komponendid
- Frontend: React (nginx:alpine)
- Backend: Node.js API
- Database: PostgreSQL

## Kuidas kasutada
1. `kubectl apply -f config/`
2. `kubectl get all`
3. `minikube service frontend-service`
```

---

## 🔧 Samm 2: Database Setup (30 min)

### 2.1: Loo PostgreSQL Secret

**`database/postgres-secret.yaml`:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
type: Opaque
data:
  username: dGVjaHNob3A=  # techshop (base64)
  password: cGFzc3dvcmQxMjM=  # password123 (base64)
  database: dGVjaHNob3BkYg==  # techshopdb (base64)
```

### 2.2: Loo PostgreSQL ConfigMap

**`database/postgres-config.yaml`:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-config
data:
  POSTGRES_DB: techshopdb
  POSTGRES_USER: techshop
  POSTGRES_PASSWORD: password123
```

### 2.3: Loo PostgreSQL PersistentVolumeClaim

**`database/postgres-pvc.yaml`:**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

### 2.4: Loo PostgreSQL Deployment

**`database/postgres-deployment.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deployment
  labels:
    app: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        ports:
        - containerPort: 5432
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
            configMapKeyRef:
              name: postgres-config
              key: POSTGRES_PASSWORD
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
```

### 2.5: Loo PostgreSQL Service

**`database/postgres-service.yaml`:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
```

---

## 🔧 Samm 3: Backend Setup (45 min)

### 3.1: Loo Backend ConfigMap

**`backend/backend-config.yaml`:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
data:
  NODE_ENV: "development"
  PORT: "3000"
  DATABASE_URL: "postgresql://techshop:password123@postgres-service:5432/techshopdb"
  JWT_SECRET: "development-secret"
```

### 3.2: Loo Backend Deployment

**`backend/backend-deployment.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deployment
  labels:
    app: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: node:16-alpine
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          valueFrom:
            configMapKeyRef:
              name: backend-config
              key: NODE_ENV
        - name: PORT
          valueFrom:
            configMapKeyRef:
              name: backend-config
              key: PORT
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: backend-config
              key: DATABASE_URL
        - name: JWT_SECRET
          valueFrom:
            configMapKeyRef:
              name: backend-config
              key: JWT_SECRET
        command: ["sh", "-c"]
        args:
        - |
          echo "Starting backend server..."
          echo "Database URL: $DATABASE_URL"
          echo "Port: $PORT"
          echo "Environment: $NODE_ENV"
          sleep 3600
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 3.3: Loo Backend Service

**`backend/backend-service.yaml`:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
  - port: 3000
    targetPort: 3000
  type: ClusterIP
```

---

## 🎨 Samm 4: Frontend Setup (30 min)

### 4.1: Loo Frontend ConfigMap

**`frontend/frontend-config.yaml`:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-config
data:
  REACT_APP_API_URL: "http://backend-service:3000"
  REACT_APP_ENVIRONMENT: "development"
```

### 4.2: Loo Frontend Deployment

**`frontend/frontend-deployment.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
  labels:
    app: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: nginx:alpine
        ports:
        - containerPort: 80
        env:
        - name: REACT_APP_API_URL
          valueFrom:
            configMapKeyRef:
              name: frontend-config
              key: REACT_APP_API_URL
        - name: REACT_APP_ENVIRONMENT
          valueFrom:
            configMapKeyRef:
              name: frontend-config
              key: REACT_APP_ENVIRONMENT
        command: ["sh", "-c"]
        args:
        - |
          echo "Starting frontend server..."
          echo "API URL: $REACT_APP_API_URL"
          echo "Environment: $REACT_APP_ENVIRONMENT"
          echo "<html><body><h1>TechShop Frontend</h1><p>API: $REACT_APP_API_URL</p></body></html>" > /usr/share/nginx/html/index.html
          nginx -g "daemon off;"
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 4.3: Loo Frontend Service

**`frontend/frontend-service.yaml`:**
```yaml
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
  type: NodePort
```

---

## 🚀 Samm 5: Deployment ja Testimine (30 min)

### 5.1: Deploy'i kõik ressursid

```bash
# Deploy'i database
kubectl apply -f database/

# Deploy'i backend
kubectl apply -f backend/

# Deploy'i frontend
kubectl apply -f frontend/

# Vaata kõiki ressursse
kubectl get all
```

### 5.2: Kontrolli deployment'i

```bash
# Vaata Pod'ide staatust
kubectl get pods

# Vaata Service'e
kubectl get services

# Vaata ConfigMap'e
kubectl get configmaps

# Vaata Secret'e
kubectl get secrets

# Vaata PVC'e
kubectl get pvc
```

### 5.3: Testi rakendust

```bash
# Testi frontend'i
minikube service frontend-service

# Testi backend'i
kubectl port-forward service/backend-service 3000:3000

# Testi database'i
kubectl exec -it $(kubectl get pods -l app=postgres -o jsonpath='{.items[0].metadata.name}') -- psql -U techshop -d techshopdb
```

---

## 📊 Samm 6: Monitoring ja Scaling (15 min)

### 6.1: Scaling

```bash
# Skaleeri frontend'i üles
kubectl scale deployment frontend-deployment --replicas=5

# Skaleeri backend'i üles
kubectl scale deployment backend-deployment --replicas=3

# Vaata tulemust
kubectl get pods
```

### 6.2: Monitoring

```bash
# Vaata Pod'ide log'e
kubectl logs -l app=frontend
kubectl logs -l app=backend
kubectl logs -l app=postgres

# Vaata ressursi kasutust
kubectl top pods

# Vaata event'e
kubectl get events
```

---

## 🧹 Samm 7: Cleanup (10 min)

```bash
# Kustuta kõik ressursid
kubectl delete -f frontend/
kubectl delete -f backend/
kubectl delete -f database/

# Kontrolli, et kõik on kustutatud
kubectl get all
kubectl get pvc
kubectl get configmaps
kubectl get secrets
```

---

## 📝 HARJUTUS 8: Bonus Ülesanded (15 min)

### 8.1: Ingress Setup

**Loo Ingress controller ja Ingress:**
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: techshop-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: techshop.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

### 8.2: Horizontal Pod Autoscaler

**Loo HPA backend'ile:**
```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 8.3: Job ja CronJob

**Loo backup Job:**
```yaml
# backup-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: database-backup
spec:
  template:
    spec:
      containers:
      - name: backup
        image: postgres:13
        command: ["pg_dump"]
        args: ["-h", "postgres-service", "-U", "techshop", "-d", "techshopdb"]
        env:
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
      restartPolicy: Never
  backoffLimit: 3
```

---

## 🎯 Kodutöö Kokkuvõte

### **Õpitud kontseptsioonid:**
1. **Multi-tier application** - frontend, backend, database
2. **Service discovery** - teenuste vahelised ühendused
3. **Configuration management** - ConfigMap ja Secret'id
4. **Persistent storage** - PVC ja PV
5. **Scaling** - horizontal scaling
6. **Health checks** - liveness ja readiness probe'id

### **Järgmised sammud:**
- Lisa Ingress controller
- Seadista monitoring (Prometheus/Grafana)
- Lisa CI/CD pipeline
- Optimeeri resource kasutust
- Lisa security policies

**🎉 Palju õnne! Oled nüüd valmis keerukate rakenduste deploy'imiseks Kubernetes'i!**
