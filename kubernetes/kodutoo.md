#  Kubernetes Kodutöö: E-Pood → Tootmine

**Tähtaeg:** Järgmise nädala alguseks  


---

##  Ülesande kirjeldus

Laboris tegime e-poe kus kood oli ConfigMap'is. See on halb praktika. Nüüd teeme sama e-poe õigesti - kood Docker image'isse.

---

##  Mida Me Teeme

---

## Osa 1: Docker Images (50 punkti)

### 1.1 Backend Docker Image

#### Samm 1: Kopeeri kood laborist

```bash
# Loo kaustad
mkdir -p ~/kodutoo/docker/backend
cd ~/kodutoo/docker/backend

# Vaata mis laboris ConfigMap'is oli
kubectl get configmap backend-code -o yaml

# Kopeeri server.js sisu uude faili
nano server.js
# Kopeeri ConfigMap'ist ainult JavaScript kood (ilma YAML indent'ideta)
# Algab: const express = require('express');
# Lõppeb: app.listen(3000);

# Kopeeri package.json sisu
nano package.json
# Kopeeri ConfigMap'ist package.json sisu
# { "name": "shop-backend", ... }
```

#### Samm 2: Loo Dockerfile

```bash
nano Dockerfile
```

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --production
COPY server.js ./
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

#### Samm 3: Build ja Push

```bash
# Docker Hub konto vaja!
# Mine https://hub.docker.com → Sign Up
# Username: valixyz (jäta meelde!)

# Login
docker login
# Username: valixyz
# Password: teie-parool

# Build (asenda valixyz oma nimega!)
docker build -t valixyz/shop-backend:v1.0 .

# Test lokaalselt
docker run -p 3000:3000 valixyz/shop-backend:v1.0
# Ctrl+C stop

# Push Docker Hub'i
docker push valixyz/shop-backend:v1.0
```

### 1.2 Frontend Docker Image

#### Samm 1: Kopeeri kood

```bash
cd ~/kodutoo/docker/frontend

# Vaata ConfigMap
kubectl get configmap frontend-html -o yaml

# Kopeeri HTML
nano index.html
# Kopeeri ainult HTML osa (ilma YAML indent'ideta)

# Kopeeri nginx config
kubectl get configmap nginx-config -o yaml
nano nginx.conf
# Kopeeri server { ... } osa
```

#### Samm 2: Dockerfile

```bash
nano Dockerfile
```

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

#### Samm 3: Build ja Push

```bash
docker build -t valixyz/shop-frontend:v1.0 .
docker push valixyz/shop-frontend:v1.0
```

### 1.3 Uuenda Kubernetes Deployments

```bash
cd ~/kodutoo/kubernetes
```

**backend-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
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
        image: valixyz/shop-backend:v1.0  # SINU IMAGE!
        ports:
        - containerPort: 3000
        # POLE ENAM:
        # - volumeMounts
        # - initContainers
        # - volumes ConfigMap'iga
        resources:
          requests:
            cpu: "50m"
            memory: "64Mi"
          limits:
            cpu: "100m"
            memory: "128Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
  - port: 3000
```

**frontend-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 2
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
        image: valixyz/shop-frontend:v1.0  # SINU IMAGE!
        ports:
        - containerPort: 80
        # POLE ENAM volumeMounts ConfigMap'iga!
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
  ports:
  - port: 80
  type: NodePort
```

### 1.4 Deploy ja Test

```bash
# Deploy PostgreSQL (sama mis laboris)
kubectl apply -f ~/k8s-lab/postgres/

# Deploy uued images
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml

# Kontrolli
kubectl get pods
# Peavad kõik olema Running

# Test
kubectl port-forward service/frontend-service 8080:80
# Ava brauser: http://localhost:8080
# Peaksid nägema e-poodi!
```

---

## Osa 2: Kubernetes Dashboard (20 punkti)

Dashboard näitab mis klastris toimub. See on GUI kubectl'i asemel.

### Enable Dashboard

```bash
# Minikube'is lihtne
minikube dashboard

# VÕI käsitsi
kubectl proxy
# Ava brauser:
# http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
```

### Mida Vaadata (tee screenshots!)

1. **Workloads → Deployments**
   - Peaksid nägema: backend-api, frontend, postgres
   - Kõik rohelised

2. **Workloads → Pods**
   - 5-6 pod'i running
   - Kliki pod'ile → näed detaile

3. **Config → ConfigMaps**
   - POLE ENAM backend-code ega frontend-html!
   - Ainult postgres-config

---

## Osa 3: Üks Production Feature (30 punkti)

### Valik A: Auto-Scaling (HPA)

HPA skaleerib pod'e automaatselt kui koormus kasvab. Näiteks kui CPU > 50%, lisab pod'e. Kui koormus langeb, vähendab pod'e. See säästab ressursse ja hoiab app'i töös.

```bash
# 1. Enable metrics
minikube addons enable metrics-server
# Oota 2 min

# 2. Loo HPA
nano hpa.yaml
```

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-api
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

```bash
# 3. Apply
kubectl apply -f hpa.yaml

# 4. Test - tekita koormust
kubectl run -it loadtest --image=busybox --restart=Never -- sh
# Busybox'is:
while true; do wget -q -O- http://backend-service:3000/api/products; done

# 5. Vaata Dashboard'is
# Workloads → Replica Sets
# Peaksid nägema pod'ide arvu kasvamas
```

### Valik B: Blue-Green Deployment

Blue-Green tähendab 2 versiooni korraga. Blue töötab, Green on uuendus. Saad vahetada ilma katkestuseta. Kui Green on katki, vaheta tagasi Blue.

```bash
# 1. Tee 2 erinevat frontend versiooni
cd ~/kodutoo/docker/frontend

# Muuda index.html
nano index.html
# Muuda: <h1>E-Pood v1.0 BLUE</h1>

# Build blue
docker build -t valixyz/shop-frontend:blue .
docker push valixyz/shop-frontend:blue

# Muuda uuesti
nano index.html  
# Muuda: <h1>E-Pood v2.0 GREEN</h1>

# Build green
docker build -t valixyz/shop-frontend:green .
docker push valixyz/shop-frontend:green
```

```yaml
# 2. blue-green.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-blue
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
      version: blue
  template:
    metadata:
      labels:
        app: frontend
        version: blue
    spec:
      containers:
      - name: frontend
        image: valixyz/shop-frontend:blue
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-green
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
      version: green
  template:
    metadata:
      labels:
        app: frontend
        version: green
    spec:
      containers:
      - name: frontend
        image: valixyz/shop-frontend:green
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
    version: blue  # SIIN VAHETAD!
  ports:
  - port: 80
  type: NodePort
```

```bash
# 3. Deploy mõlemad
kubectl apply -f blue-green.yaml

# 4. Test blue
kubectl port-forward service/frontend-service 8080:80
# Näed: v1.0 BLUE

# 5. Vaheta green'ile
kubectl patch service frontend-service -p '{"spec":{"selector":{"version":"green"}}}'

# 6. Värskenda brauser
# Näed: v2.0 GREEN

# 7. Tagasi blue'le kui vaja
kubectl patch service frontend-service -p '{"spec":{"selector":{"version":"blue"}}}'
```

### Valik C: Helm Chart

Helm on nagu package manager. Ühe käsuga saad installida/uuendada/kustutada kogu app'i. Values.yaml's saad muuta seadeid. Hea kui on dev/test/prod environment'id.

```bash
# 1. Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 2. Loo chart
cd ~/kodutoo
helm create eshop

# 3. Muuda values
nano eshop/values.yaml
```

```yaml
backend:
  image: valixyz/shop-backend:v1.0
  replicas: 2

frontend:
  image: valixyz/shop-frontend:v1.0
  replicas: 2
  service:
    type: NodePort

postgres:
  enabled: true
```

```yaml
# 4. Muuda template
nano eshop/templates/backend.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-backend
spec:
  replicas: {{ .Values.backend.replicas }}
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
        image: {{ .Values.backend.image }}
        ports:
        - containerPort: 3000
```

```bash
# 5. Install
helm install myshop ./eshop

# 6. Upgrade (muuda replicas)
helm upgrade myshop ./eshop --set backend.replicas=5

# 7. Vaata Dashboard'is
# Peaks nägema 5 backend pod'i

# 8. Uninstall
helm uninstall myshop
```

---

## README.md Mall

```markdown
# Kubernetes E-Shop Production

## Autor: [Sinu Nimi]

## Tehtud Muudatused

### 1. Docker Images
- Laboris: Kood oli ConfigMap'is (halb)
- Nüüd: Kood on Docker image'is (hea)
- Backend: valixyz/shop-backend:v1.0
- Frontend: valixyz/shop-frontend:v1.0

### 2. Miks Docker Images Paremad
- Versioonihaldus (v1.0, v1.1, v2.0)
- Rollback võimalus
- CI/CD pipeline võimalik
- Ei pea pod'is npm install tegema

### 3. Production Feature: [HPA/Blue-Green/Helm]
[Kirjelda mida tegid ja miks kasulik]

## Testimine
1. Deploy PostgreSQL
2. Deploy Backend & Frontend (uued image'd)
3. Port forward ja test brauseris
4. [Kirjelda feature testimist]

## Dashboard Screenshots
1. Deployments view
2. Pods running
3. [Feature töötamas]

## Probleemid ja Lahendused
- Docker build error → lahendus: ...
- Image pull error → lahendus: tegi typo image nimes
- [Sinu probleemid]

## Õpitu
- ConfigMap koodile on ainult õppimiseks
- Production = Docker images
- Dashboard on kasulik monitoring'uks
- [Feature] aitab production'is sest...
```

---

## Esitamine

```
kodutoo/
├── README.md           (kirjeldus)
├── docker/
│   ├── backend/
│   │   ├── Dockerfile
│   │   ├── server.js
│   │   └── package.json
│   └── frontend/
│       ├── Dockerfile
│       ├── index.html
│       └── nginx.conf
├── kubernetes/
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── [hpa.yaml/blue-green.yaml/eshop-chart/]
└── screenshots/
    ├── dashboard-deployments.png
    ├── dashboard-pods.png
    └── feature-working.png
```

**Tähtaeg:** 1 nädal

---

##  Refleksioon (kirjuta README.md lõppu)

Lisa oma README.md faili lõppu peatükk **"## Refleksioon"** ja vasta järgmistele küsimustele:

### Küsimused (vasta 2-3 lausega igaühele):

1. **Mis oli selle kodutöö juures kõige raskem ja kuidas sa selle lahendasid?**
   - Näide: "Kõige raskem oli mõista, kuidas Kubernetes Services töötavad. Lugesin dokumentatsiooni ja kasutasin `kubectl describe` debugging'uks."

2. **Milline Kubernetes kontseptsioon oli sulle kõige suurem "ahaa!"-elamus ja miks?**
   - Näide: "Deployments ja Pods! Nüüd saan aru, kuidas Kubernetes automaatselt pod'e taastab kui need crashivad."

3. **Kuidas saaksid Kubernetes'i kasutada oma teistes projektides või töös?**
   - Näide: "Võiksin Kubernetes'iga käivitada oma mikroteenuste projekti ja skaleerida neid automaatselt."

4. **Kui peaksid oma sõbrale selgitama, mis on Kubernetes ja miks see on kasulik, siis mida ütleksid?**
   - Näide: "Kubernetes on nagu lennujuht – haldab tuhandeid container'eid ja tagab, et kõik töötab!"

5. **Mis oli selle projekti juures kõige lõbusam või huvitavam osa?**
   - Näide: "Mulle meeldis scaling - `kubectl scale --replicas=10` ja BAM, mul on 10 pod'i!"

---

##  Kontrollnimekiri (enne esitamist)

**Kontrolli need asjad:**

- [ ] GitHubis on avalik repositoorium
- [ ] Kubernetes manifests töötavad (`kubectl apply`)
- [ ] Kõik pod'id on RUNNING staadiumis
- [ ] Services suunavad liiklust õigesti
- [ ] Rakendus on ligipääsetav (browser test)
- [ ] README.md sisaldab:
  - [ ] Projekti kirjeldus (mis see on?)
  - [ ] Kuidas seadistada (minikube/kind)
  - [ ] Kuidas käivitada (`kubectl apply` käsud)
  - [ ] Kuidas testida (URL'id, käsud)
  - [ ] Refleksioon (5 küsimuse vastused)
- [ ] Screenshots on lisatud (pods, services, browser)
- [ ] Kõik muudatused on GitHubi push'itud

---

##  Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **Deployments** | 20% | Backend + Frontend deployments korrektsed |
| **Services** | 15% | Services suunavad liiklust õigesti |
| **ConfigMaps/Secrets** | 10% | Environment variables korrektsed |
| **Ingress** | 10% | Ingress seadistatud (kui kasutatud) |
| **Funktsionaalsus** | 20% | Rakendus töötab browser'is |
| **README** | 10% | Projekti kirjeldus, käivitamisjuhend, selge |
| **Refleksioon** | 15% | 5 küsimust vastatud, sisukas, näitab mõistmist |

**Kokku: 100%**

---

##  Abimaterjalid ja lugemine

**Kiirviited:**
- [Kubernetes Docs - Concepts](https://kubernetes.io/docs/concepts/)
- [Kubernetes Docs - kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/) - tasuta online playground
- [Kubernetes By Example](https://kubernetesbyexample.com/)

**Kui abi vaja:**
1. Vaata `lisapraktika.md` faili täiendavate näidete jaoks
2. Kasuta `kubectl describe` debugging'uks
3. Kasuta `kubectl logs` logide vaatamiseks
4. Küsi klassikaaslaselt või õpetajalt

---

##  Boonus (valikuline, +10%)

**Kui tahad ekstra punkte, tee üks või mitu neist:**

1. **Horizontal Pod Autoscaler:** Automaatne scaling CPU kasutuse põhjal
   ```bash
   kubectl autoscale deployment backend --cpu-percent=50 --min=2 --max=10
   ```

2. **Helm Chart:** Pakenda rakendus Helm chart'iks
   ```bash
   helm create myapp
   helm install myapp ./myapp
   ```

3. **Monitoring:** Lisa Prometheus + Grafana monitoring
4. **Persistent Volumes:** Kasuta PV ja PVC andmete säilitamiseks
5. **Network Policies:** Lisa network policies turvalisuse jaoks

---

**Edu ja head orkestreerimist!** 
