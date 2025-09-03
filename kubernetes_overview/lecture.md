# Kubernetes Overview: Container Orchestration
*ITS-24 DevOps Automatiseerimine | 2 tundi (ülevaade)*

## 🎯 Õpiväljundid

Pärast loengut oskate:
- Mõista Kubernetes'i põhilisi kontseptsioone
- Kasutada kubectl käsklusi
- Deploy'ida lihtsaid rakendusi
- Mõista Kubernetes'i arhitektuuri

---

## 📖 Loeng 26.1: Mis on Kubernetes? (30 min)

### Miks vajame Container Orchestration?

**Docker probleemid suurel skaalal:**
```bash
# 1. Käsitsi container management
docker run -d --name web1 nginx:latest
docker run -d --name web2 nginx:latest
docker run -d --name web3 nginx:latest

# 2. Käsitsi networking
docker network create web-network
docker network connect web-network web1
docker network connect web-network web2

# 3. Käsitsi scaling
docker stop web1  # Kui üks container kukub
docker run -d --name web1-new nginx:latest

# 4. Käsitsi load balancing
# Peate ise seadistama reverse proxy
```

**Kubernetes lahendab:**
- **Automaatne scaling** - lisab/eemaldab container'eid vastavalt koormusele
- **Automaatne failover** - kui container kukub, taaskäivitub automaatselt
- **Load balancing** - jaotab liiklust container'ite vahel
- **Service discovery** - container'id leiavad üksteist automaatselt
- **Configuration management** - keskkonnamuutujad, secret'id, config map'id

---

## 🏗️ Kubernetes Arhitektuur

### Control Plane (Master Node)

**Kubernetes'i "aju" - teeb otsused:**

```yaml
# Control Plane komponendid:
- kube-apiserver      # API server - kõik käsud lähevad siia
- etcd                # Andmebaas - salvestab kõik andmed
- kube-scheduler      # Planeerija - otsustab, kuhu container'id panna
- kube-controller-manager  # Kontroller - jälgib ja parandab olukordi
```

### Worker Nodes

**Kus teie rakendused jooksevad:**

```yaml
# Worker Node komponendid:
- kubelet             # Agent - kommunikeerib Control Plane'iga
- kube-proxy          # Networking - teenuste vahelised ühendused
- Container Runtime   # Docker/containerd - container'ite käivitamine
```

---

## 📋 Loeng 26.2: Kubernetes Põhikontseptsioonid (40 min)

### 1. Pod - Väikseim üksus

**Pod on nagu "logistiline üksus" - võib sisaldada ühte või mitut container'it:**

```yaml
# Lihtne Pod
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
```

**Praktiline näide:**
```bash
# Loo Pod
kubectl run nginx-pod --image=nginx:latest --port=80

# Vaata Pod'i staatust
kubectl get pods

# Vaata Pod'i detaile
kubectl describe pod nginx-pod

# Kustuta Pod
kubectl delete pod nginx-pod
```

### 2. Deployment - Rakenduse juhtimine

**Deployment haldab Pod'e - scaling, updates, rollbacks:**

```yaml
# Nginx Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3  # Kolm koopiat
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
        ports:
        - containerPort: 80
```

**Praktiline näide:**
```bash
# Loo Deployment
kubectl create deployment nginx --image=nginx:latest --replicas=3

# Vaata Deployment'i
kubectl get deployments

# Skaleeri üles
kubectl scale deployment nginx --replicas=5

# Uuenda image'i
kubectl set image deployment/nginx nginx=nginx:1.20

# Vaata rollback ajalugu
kubectl rollout history deployment/nginx

# Tee rollback
kubectl rollout undo deployment/nginx
```

### 3. Service - Networking

**Service pakub stabiilset IP ja DNS nime Pod'idele:**

```yaml
# ClusterIP Service (vaikimisi)
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

**Service tüübid:**
- **ClusterIP** - sisemine ligipääs (vaikimisi)
- **NodePort** - ligipääs node'ide kaudu
- **LoadBalancer** - väline ligipääs (cloud provider'id)
- **ExternalName** - DNS alias

**Praktiline näide:**
```bash
# Loo Service
kubectl expose deployment nginx --port=80 --target-port=80

# Vaata Service'e
kubectl get services

# Testi Service'i
kubectl run test-pod --image=busybox --rm -it --restart=Never -- wget -O- nginx-service
```

### 4. ConfigMap ja Secret - Konfiguratsioon

**ConfigMap - mittekrüpteeritud konfiguratsioon:**

```yaml
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "localhost:5432"
  api_key: "development-key"
  log_level: "INFO"
```

**Secret - krüpteeritud andmed:**

```yaml
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded
  password: cGFzc3dvcmQ=  # base64 encoded
```

**Kasutamine Pod'is:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: DB_URL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database_url
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: password
```

---

## 🛠️ Loeng 26.3: Praktiline Kubernetes (30 min)

### Kohalik Kubernetes Setup

**Minikube - kohalik Kubernetes keskkond:**

```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Käivita Minikube
minikube start

# Kontrolli staatust
kubectl cluster-info
kubectl get nodes
```

### Lihtne Web Application

**1. Loo Deployment:**
```yaml
# web-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: nginx:latest
        ports:
        - containerPort: 80
        env:
        - name: ENVIRONMENT
          value: "development"
```

**2. Loo Service:**
```yaml
# web-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
  type: NodePort
```

**3. Deploy'i rakendus:**
```bash
# Loo ressursid
kubectl apply -f web-app.yaml
kubectl apply -f web-service.yaml

# Vaata staatust
kubectl get pods
kubectl get services

# Testi rakendust
minikube service web-service
```

### Monitoring ja Debugging

**Põhilised kubectl käsud:**
```bash
# Pod'ide vaatamine
kubectl get pods
kubectl get pods -o wide
kubectl describe pod <pod-name>

# Log'ide vaatamine
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # järgi reaalajas

# Container'i sisse minemine
kubectl exec -it <pod-name> -- /bin/bash

# Ressursside kasutamine
kubectl top pods
kubectl top nodes

# Event'ide vaatamine
kubectl get events
```

---

## 📊 Loeng 26.4: Kubernetes vs Docker (20 min)

### Võrdlus

| Aspekt | Docker | Kubernetes |
|--------|--------|------------|
| **Skope** | Üksik container | Container orchestration |
| **Scaling** | Käsitsi | Automaatne |
| **Failover** | Käsitsi | Automaatne |
| **Load Balancing** | Käsitsi | Sisseehitatud |
| **Service Discovery** | Käsitsi | Automaatne |
| **Configuration** | Environment variables | ConfigMap/Secret |
| **Updates** | Käsitsi | Rolling updates |
| **Monitoring** | Basic | Comprehensive |

### Millal kasutada mida?

**Docker sobib:**
- Arenduskeskkond
- Lihtsad rakendused
- Prototüübid
- Üksikud serverid

**Kubernetes sobib:**
- Production keskkonnad
- Suured rakendused
- Microservices
- High availability

---

## 🎯 Kokkuvõte

### Kubernetes'i eelised:
✅ **Automaatne scaling** - vastavalt koormusele  
✅ **High availability** - automaatne failover  
✅ **Service discovery** - container'id leiavad üksteist  
✅ **Configuration management** - keskkonnamuutujad ja secret'id  
✅ **Rolling updates** - null downtime deployment'id  
✅ **Resource management** - CPU ja mälu piirangud  

### Järgmised sammud:
- Õppige Helm (package manager)
- Uurige Ingress (väline ligipääs)
- Õppige Persistent Volumes
- Uurige Kubernetes Dashboard
- Õppige monitoring (Prometheus/Grafana)

### Praktiline soovitus:
**Alustage Docker'iga, siis liikuge Kubernetes'i juurde!**

---

**Järgmises osas:** Praktiline lab - deploy'ime tervikliku rakenduse Kubernetes'i!
