# Kubernetes Overview Lab: Container Orchestration
*ITS-24 DevOps Automatiseerimine | 2 tundi praktiline töö*

## 🎯 Samm 1: Lab'i eesmärgid

Pärast laborit oskate:
- Seadistada kohaliku Kubernetes keskkonna
- Deploy'ida lihtsaid rakendusi
- Kasutada kubectl käsklusi
- Mõista Kubernetes'i põhikontseptsioone

---

## 🛠️ Samm 2: Kohaliku Kubernetes Seadistamine (30 min)

### 2.1: Minikube Install

**Kontrollige, et teil on:**
- Docker (juba installitud)
- VirtualBox või Hyper-V (Windows)
- Vähemalt 2GB vaba RAM

**Install Minikube:**
```bash
# macOS
brew install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Windows (PowerShell)
choco install minikube
```

### 2.2: Käivita Minikube

```bash
# Käivita Minikube
minikube start

# Kontrolli staatust
minikube status

# Vaata cluster info
kubectl cluster-info

# Vaata node'id
kubectl get nodes
```

### 2.3: Install kubectl (kui vajalik)

```bash
# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Kontrolli versiooni
kubectl version --client
```

---

## 🚀 Samm 3: Esimene Kubernetes Rakendus (45 min)

### 3.1: Lihtne Nginx Pod

**Loo esimene Pod:**
```bash
# Loo Pod
kubectl run nginx-pod --image=nginx:latest --port=80

# Vaata Pod'i staatust
kubectl get pods

# Vaata Pod'i detaile
kubectl describe pod nginx-pod

# Vaata Pod'i log'e
kubectl logs nginx-pod
```

**Testi Pod'i:**
```bash
# Mine Pod'i sisse
kubectl exec -it nginx-pod -- /bin/bash

# Pod'i sees
curl localhost
exit

# Või testi väljast
kubectl port-forward nginx-pod 8080:80
# Avage brauser: http://localhost:8080
```

### 3.2: Nginx Deployment

**Loo Deployment fail:**
```yaml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
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
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

**Deploy'i rakendus:**
```bash
# Loo Deployment
kubectl apply -f nginx-deployment.yaml

# Vaata Deployment'i
kubectl get deployments

# Vaata Pod'e
kubectl get pods

# Vaata ReplicaSet'e
kubectl get replicasets
```

### 3.3: Nginx Service

**Loo Service fail:**
```yaml
# nginx-service.yaml
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
  type: NodePort
```

**Deploy'i Service:**
```bash
# Loo Service
kubectl apply -f nginx-service.yaml

# Vaata Service'e
kubectl get services

# Testi Service'i
kubectl run test-pod --image=busybox --rm -it --restart=Never -- wget -O- nginx-service

# Või kasuta Minikube
minikube service nginx-service
```

---

## 🔧 Samm 4: Scaling ja Updates (30 min)

### 4.1: Scaling

```bash
# Skaleeri üles
kubectl scale deployment nginx-deployment --replicas=5

# Vaata tulemust
kubectl get pods

# Skaleeri alla
kubectl scale deployment nginx-deployment --replicas=2

# Vaata tulemust
kubectl get pods
```

### 4.2: Rolling Update

```bash
# Uuenda image'i
kubectl set image deployment/nginx-deployment nginx=nginx:1.20

# Vaata update'i progressi
kubectl rollout status deployment/nginx-deployment

# Vaata rollback ajalugu
kubectl rollout history deployment/nginx-deployment

# Tee rollback
kubectl rollout undo deployment/nginx-deployment

# Vaata rollback'i progressi
kubectl rollout status deployment/nginx-deployment
```

### 4.3: Pod'i kustutamine ja taaskäivitumine

```bash
# Vaata Pod'e
kubectl get pods

# Kustuta üks Pod
kubectl delete pod <pod-name>

# Vaata, kuidas uus Pod tekib automaatselt
kubectl get pods -w
```

---

## 📊 Samm 5: Monitoring ja Debugging (30 min)

### 5.1: Põhilised kubectl käsud

```bash
# Vaata kõiki ressursse
kubectl get all

# Vaata Pod'e details
kubectl get pods -o wide

# Vaata Service'e details
kubectl get services -o wide

# Vaata Deployment'i details
kubectl describe deployment nginx-deployment

# Vaata Pod'i details
kubectl describe pod <pod-name>

# Vaata Service'i details
kubectl describe service nginx-service
```

### 5.2: Log'ide vaatamine

```bash
# Vaata Pod'i log'e
kubectl logs <pod-name>

# Järgi log'e reaalajas
kubectl logs -f <pod-name>

# Vaata kõigi Pod'ide log'e
kubectl logs -l app=nginx

# Vaata eelmisi log'e
kubectl logs <pod-name> --previous
```

### 5.3: Container'i sisse minemine

```bash
# Mine Pod'i sisse
kubectl exec -it <pod-name> -- /bin/bash

# Pod'i sees
ls -la
ps aux
env
exit

# Käivita ühekordne käsk
kubectl exec <pod-name> -- ls -la
kubectl exec <pod-name> -- env
```

### 5.4: Event'ide vaatamine

```bash
# Vaata kõiki event'e
kubectl get events

# Vaata event'e cronoloogilises järjekorras
kubectl get events --sort-by='.lastTimestamp'

# Vaata ainult viimaseid event'e
kubectl get events --field-selector involvedObject.name=nginx-deployment
```

---

## 🎯 Samm 6: Konfiguratsioon ja Secret'id (15 min)

### 6.1: ConfigMap

**Loo ConfigMap:**
```yaml
# app-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "localhost:5432"
  api_key: "development-key"
  log_level: "INFO"
  environment: "development"
```

**Loo Pod ConfigMap'iga:**
```yaml
# app-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: config-pod
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "echo $DATABASE_URL && echo $LOG_LEVEL && sleep 3600"]
    env:
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database_url
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: log_level
```

**Deploy'i:**
```bash
kubectl apply -f app-config.yaml
kubectl apply -f app-pod.yaml

# Vaata Pod'i log'e
kubectl logs config-pod
```

### 6.2: Secret

**Loo Secret:**
```bash
# Loo Secret käsurealt
kubectl create secret generic app-secret \
  --from-literal=username=admin \
  --from-literal=password=secret123

# Vaata Secret'i
kubectl get secrets
kubectl describe secret app-secret
```

---

## 🧹 Samm 7: Cleanup (10 min)

**Kustuta kõik ressursid:**
```bash
# Kustuta Deployment ja Service
kubectl delete -f nginx-deployment.yaml
kubectl delete -f nginx-service.yaml

# Kustuta ConfigMap ja Pod
kubectl delete -f app-config.yaml
kubectl delete -f app-pod.yaml

# Kustuta Secret
kubectl delete secret app-secret

# Kustuta test Pod
kubectl delete pod nginx-pod

# Vaata, et kõik on kustutatud
kubectl get all

# Peata Minikube
minikube stop
```

---

## 📝 HARJUTUS 8: Bonus Ülesanded (15 min)

### 8.1: Multi-container Pod

**Loo Pod kahe container'iga:**
```yaml
# multi-container-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
  - name: sidecar
    image: busybox
    command: ["sh", "-c", "while true; do echo 'Sidecar running'; sleep 30; done"]
```

### 8.2: Resource Limits

**Lisa resource piirangud:**
```yaml
# resource-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-pod
spec:
  containers:
  - name: app
    image: nginx:latest
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### 8.3: Health Checks

**Lisa health check:**
```yaml
# health-check-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: health-check-pod
spec:
  containers:
  - name: app
    image: nginx:latest
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

---

## 🎯 Lab Kokkuvõte

### **Õpitud kontseptsioonid:**
1. **Pod** - väikseim Kubernetes üksus
2. **Deployment** - rakenduse juhtimine ja scaling
3. **Service** - networking ja load balancing
4. **ConfigMap** - konfiguratsiooni haldamine
5. **Secret** - krüpteeritud andmete haldamine

### **Õpitud kubectl käsud:**
- `kubectl get` - ressurside vaatamine
- `kubectl describe` - detailide vaatamine
- `kubectl logs` - log'ide vaatamine
- `kubectl exec` - container'i sisse minemine
- `kubectl scale` - scaling
- `kubectl rollout` - update'id ja rollback'id

### **Järgmised sammud:**
- Õppige Helm (package manager)
- Uurige Ingress (väline ligipääs)
- Õppige Persistent Volumes
- Uurige Kubernetes Dashboard
- Õppige monitoring (Prometheus/Grafana)

**🎉 Palju õnne! Oled nüüd valmis Kubernetes'i kasutamiseks!**
