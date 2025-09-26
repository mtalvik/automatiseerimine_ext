# Kubernetes Kodutöö: Mikroteenuste E-Kaubanduse Platvorm

## Kodutöö Ülevaade

**Eesmärk:** Laiendada laboris õpitut, luues täiustatud e-kaubanduse platvormi täiendavate funktsioonidega.

**Aeg:** 4-6 tundi
**Hindamine:** 100 punkti
**Tähtaeg:** 1 nädal

---

## Ülesanne 1: Redis Cache Lisamine (20 punkti)

### 1.1 Nõuded (10 punkti)

Lisage Redis cache backend API ja PostgreSQL vahele. Redis peaks cache'ima toodete päringuid, et vähendada andmebaasi koormust.

**Tehnilised nõuded:**
- Redis Deployment (1 pod on piisav)
- Redis Service
- TTL (Time To Live) 5 minutit cache'itud andmetele
- Cache invalidation kui toode ostetakse

**Dokumentatsioon:**
- Redis Docker Hub: https://hub.docker.com/_/redis
- Redis Kubernetes näited: https://kubernetes.io/docs/tutorials/configuration/configure-redis-using-configmap/
- Redis Node.js klient: https://github.com/redis/node-redis

### 1.2 Implementatsioon (10 punkti)

```yaml
# redis.yaml - TEIE ÜLESANNE: täitke lüngad
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cache
spec:
  replicas: 1  # Vihje: Redis on stateful, 1 on piisav
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis  # Peab vastama selector.matchLabels.app
    spec:
      containers:
      - name: redis
        image: redis:7-alpine  # Vihje: Alpine versioon on väiksem
        ports:
        - containerPort: 6379  # Redis vaikimisi port
        resources:
          requests:
            memory: "64Mi"   # Minimaalne mälu
            cpu: "50m"       # 0.05 CPU
          limits:
            memory: "128Mi"  # Maksimaalne mälu
            cpu: "100m"      # 0.1 CPU
        # Vihje: Lisage liveness ja readiness probes
        livenessProbe:
          tcpSocket:
            port: 6379
          initialDelaySeconds: 15
          periodSeconds: 20
        readinessProbe:
          exec:
            command:
            - redis-cli
            - ping
          initialDelaySeconds: 5
          periodSeconds: 10

---
apiVersion: v1
kind: Service
metadata:
  name: redis-service  # Backend kasutab seda nime
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
```

**Backend koodi muudatus:**
```javascript
// Lisage Redis tugi backend API-sse
const redis = require('redis');
const client = redis.createClient({
    host: 'redis-service',  // Kubernetes service nimi
    port: 6379
});

// Promisify Redis funktsioonid
const { promisify } = require('util');
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.setex).bind(client);
const delAsync = promisify(client.del).bind(client);

// Näide: Cache products endpoint
app.get('/api/products', async (req, res) => {
    try {
        // 1. Kontrolli Redis cache'i
        const cacheKey = 'products:all';
        const cachedData = await getAsync(cacheKey);
        
        if (cachedData) {
            console.log('Cache hit!');
            return res.json(JSON.parse(cachedData));
        }
        
        // 2. Kui pole cache'is, päri andmebaasist
        console.log('Cache miss, querying database...');
        const result = await pool.query('SELECT * FROM products');
        
        // 3. Salvesta Redis'esse 5 minutiks (300 sekundit)
        await setAsync(cacheKey, 300, JSON.stringify(result.rows));
        
        res.json(result.rows);
    } catch (err) {
        console.error('Error:', err);
        res.status(500).json({ error: err.message });
    }
});

// Cache invalidation kui toode ostetakse
app.post('/api/products/:id/buy', async (req, res) => {
    // ... ostmise loogika
    
    // Invalideeri cache
    await delAsync('products:all');
    await delAsync(`product:${req.params.id}`);
    
    // ...
});
```

### 1.3 Testimine

```bash
# 1. Deploy Redis
kubectl apply -f redis.yaml

# 2. Kontrolli kas Redis pod töötab
kubectl get pods -l app=redis
kubectl logs -l app=redis

# 3. Testi Redis'e otse
kubectl exec -it $(kubectl get pods -l app=redis -o jsonpath='{.items[0].metadata.name}') -- redis-cli
# Redis CLI sees:
> ping
# Peaks vastama: PONG
> set test "hello"
> get test
> exit

# 4. Testi backend -> Redis ühendust
kubectl exec -it $(kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}') -- sh
# Pod'i sees:
$ npm install redis-cli -g
$ redis-cli -h redis-service ping
$ exit

# 5. Monitoori cache hit/miss rate
kubectl logs -l app=backend -f | grep -E "Cache (hit|miss)"

# 6. Testi cache TTL
# Päri tooteid (cache miss)
curl http://localhost:3000/api/products
# Päri uuesti kohe (cache hit)
curl http://localhost:3000/api/products
# Oota 5+ minutit ja päri uuesti (cache miss)
sleep 310 && curl http://localhost:3000/api/products
```

**Dokumentatsioon lugemiseks:**
- Redis Commands: https://redis.io/commands
- Redis with Node.js: https://redis.io/docs/clients/nodejs/
- Kubernetes Probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

---

## Ülesanne 2: Horizontal Pod Autoscaler (20 punkti)

### 2.1 HPA Backend API jaoks (10 punkti)

Looge HorizontalPodAutoscaler, mis skaleerib backend pod'e automaatselt CPU kasutuse põhjal.

**Dokumentatsioon:**
- HPA Walkthrough: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/
- Metrics Server: https://github.com/kubernetes-sigs/metrics-server
- HPA Algorithm: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#algorithm-details

```yaml
# hpa-backend.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-api  # Teie backend deployment nimi
  minReplicas: 2      # Minimaalne pod'ide arv
  maxReplicas: 10     # Maksimaalne pod'ide arv
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50  # Skaleeri kui CPU > 50%
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 70  # Skaleeri kui Memory > 70%
  behavior:  # Valikuline: kontrolli skaleerimise kiirust
    scaleDown:
      stabilizationWindowSeconds: 300  # Oota 5 min enne alla skaleerimist
      policies:
      - type: Percent
        value: 50  # Ära skaleeri alla rohkem kui 50% korraga
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60  # Oota 1 min enne üles skaleerimist
      policies:
      - type: Percent
        value: 100  # Võib dubleerida pod'ide arvu
        periodSeconds: 60
```

### 2.2 Load Test ja Verifikatsioon (10 punkti)

```bash
#!/bin/bash
# loadtest.sh - Põhjalik load test skript

echo "=== Kubernetes HPA Load Test ==="
echo "Alustame: $(date)"

# Kontrolli eeltingimusi
echo "1. Kontrollin metrics-server..."
kubectl get deployment metrics-server -n kube-system > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Metrics server pole installitud!"
    echo "Palun käivitage: minikube addons enable metrics-server"
    exit 1
fi

# Näita algne olek
echo "2. Algne pod'ide arv:"
kubectl get pods -l app=backend --no-headers | wc -l

echo "3. HPA staatus enne testi:"
kubectl get hpa backend-hpa

# Loo load generator pod
echo "4. Loon load generator pod'i..."
kubectl run load-generator --image=busybox --restart=Never -- /bin/sh -c "
while true; do
  wget -q -O- http://backend-service:3000/api/products > /dev/null
done
"

# Jälgi HPA staatust
echo "5. Jälgin HPA skaleerimist (Ctrl+C lõpetamiseks)..."
echo "Oodake 2-3 minutit, et näha skaleerimist..."

# Salvesta tulemused faili
LOG_FILE="hpa-test-$(date +%Y%m%d-%H%M%S).log"
echo "Salvestan tulemused: $LOG_FILE"

# Jälgi 5 minutit
for i in {1..30}; do
    echo "=== Minut $i/5 ===" | tee -a $LOG_FILE
    kubectl get hpa backend-hpa | tee -a $LOG_FILE
    kubectl get pods -l app=backend --no-headers | wc -l | xargs echo "Pod count:" | tee -a $LOG_FILE
    sleep 10
done

# Cleanup
echo "6. Puhastame..."
kubectl delete pod load-generator

echo "7. Ootan stabiliseerumist (5 min)..."
sleep 300

echo "8. Lõplik pod'ide arv:"
kubectl get pods -l app=backend --no-headers | wc -l

echo "Test lõpetatud: $(date)"
echo "Tulemused salvestatud: $LOG_FILE"
```

### 2.3 Testimine

```bash
# 1. Kontrolli metrics-server
kubectl top nodes
kubectl top pods

# Kui ei tööta:
minikube addons enable metrics-server
# Oota 1-2 minutit

# 2. Deploy HPA
kubectl apply -f hpa-backend.yaml

# 3. Kontrolli HPA staatust
kubectl get hpa backend-hpa
kubectl describe hpa backend-hpa

# 4. Käivita load test
chmod +x loadtest.sh
./loadtest.sh

# 5. Jälgi reaalajas (teine terminal)
watch -n 2 'kubectl get hpa backend-hpa; echo "---"; kubectl get pods -l app=backend'

# 6. Genereeri stress ilma skriptita
# Terminal 1:
kubectl run -it load-test --image=busybox --restart=Never -- sh
# Busybox sees:
while true; do wget -q -O- http://backend-service:3000/api/products; done

# Terminal 2: Jälgi
kubectl get hpa backend-hpa --watch

# 7. Vaata graafikuid Grafanas
kubectl port-forward -n monitoring service/monitoring-grafana 3000:80
# Ava: http://localhost:3000
# Vaata "Kubernetes / Compute Resources / Deployment" dashboard
```

**Vihje HPA konfigureerimiseks:**
```yaml
# Backend deployment peab olema resource requests/limits
spec:
  containers:
  - name: backend
    resources:
      requests:
        cpu: "100m"     # OLULINE: Ilma selleta HPA ei tööta!
        memory: "128Mi"
      limits:
        cpu: "500m"
        memory: "256Mi"
```

---

## Ülesanne 3: Blue-Green Deployment (25 punkti)

### 3.1 Implementeerimine (15 punkti)

**Dokumentatsioon:**
- Blue-Green Deployment: https://kubernetes.io/blog/2018/04/30/zero-downtime-deployment-kubernetes-jenkins/
- Service Selectors: https://kubernetes.io/docs/concepts/services-networking/service/#services-without-selectors
- kubectl patch: https://kubernetes.io/docs/reference/kubectl/cheatsheet/#patching-resources

```yaml
# blue-green.yaml
# Blue deployment (praegune versioon)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-blue
  labels:
    app: frontend
    version: blue
spec:
  replicas: 3
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
        image: nginx:1.21-alpine
        ports:
        - containerPort: 80
        volumeMounts:
        - name: config
          mountPath: /usr/share/nginx/html
        resources:
          requests:
            cpu: "50m"
            memory: "64Mi"
          limits:
            cpu: "100m"
            memory: "128Mi"
      volumes:
      - name: config
        configMap:
          name: frontend-config-blue  # Erinev config

---
# Green deployment (uus versioon)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-green
  labels:
    app: frontend
    version: green
spec:
  replicas: 3
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
        image: nginx:1.22-alpine  # Uuem versioon
        ports:
        - containerPort: 80
        volumeMounts:
        - name: config
          mountPath: /usr/share/nginx/html
        resources:
          requests:
            cpu: "50m"
            memory: "64Mi"
          limits:
            cpu: "100m"
            memory: "128Mi"
      volumes:
      - name: config
        configMap:
          name: frontend-config-green  # Erinev config

---
# Service mis suunab liikluse
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
    version: blue  # Alguses blue
  ports:
  - port: 80
    targetPort: 80
  type: NodePort

---
# ConfigMaps erinevate versioonide jaoks
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-config-blue
data:
  index.html: |
    <html>
      <body style="background: blue; color: white;">
        <h1>BLUE Version 1.21</h1>
        <p>This is the stable blue version</p>
      </body>
    </html>

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-config-green
data:
  index.html: |
    <html>
      <body style="background: green; color: white;">
        <h1>GREEN Version 1.22</h1>
        <p>This is the new green version</p>
      </body>
    </html>
```

### 3.2 Switching Script (10 punkti)

```bash
#!/bin/bash
# switch-deployment.sh - Blue-Green deployment switch

set -e  # Exit on error

# Värvid output'ile
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Blue-Green Deployment Switcher ===${NC}"

# Funktsioon versiooni kontrollimiseks
check_deployment_ready() {
    local deployment=$1
    local ready=$(kubectl get deployment $deployment -o jsonpath='{.status.readyReplicas}')
    local desired=$(kubectl get deployment $deployment -o jsonpath='{.spec.replicas}')
    
    if [ "$ready" == "$desired" ]; then
        return 0
    else
        return 1
    fi
}

# Kontrolli praegust versiooni
CURRENT=$(kubectl get service frontend-service -o jsonpath='{.spec.selector.version}')
echo -e "Praegune versioon: ${BLUE}$CURRENT${NC}"

# Määra sihtversioon
if [ "$CURRENT" == "blue" ]; then
    TARGET="green"
    COLOR=$GREEN
else
    TARGET="blue"
    COLOR=$BLUE
fi

echo -e "Sihtversioon: ${COLOR}$TARGET${NC}"

# Kontrolli kas sihtversioon on valmis
echo "Kontrollin $TARGET deployment staatust..."
if ! check_deployment_ready "frontend-$TARGET"; then
    echo -e "${RED}ERROR: $TARGET deployment pole valmis!${NC}"
    kubectl get deployment frontend-$TARGET
    exit 1
fi

# Salvesta rollback info
echo "Salvestan rollback info..."
kubectl get service frontend-service -o yaml > /tmp/frontend-service-backup.yaml

# Tee smoke test enne switchimist
echo "Teen smoke testi $TARGET versioonil..."
POD=$(kubectl get pods -l version=$TARGET -o jsonpath='{.items[0].metadata.name}')
kubectl exec $POD -- curl -s localhost > /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Smoke test ebaõnnestus!${NC}"
    exit 1
fi

# Switch traffic
echo -e "${COLOR}Vahetame liikluse $TARGET versioonile...${NC}"
kubectl patch service frontend-service -p '{"spec":{"selector":{"version":"'$TARGET'"}}}'

# Oota natuke
sleep 2

# Kontrolli
NEW_VERSION=$(kubectl get service frontend-service -o jsonpath='{.spec.selector.version}')
if [ "$NEW_VERSION" == "$TARGET" ]; then
    echo -e "${GREEN}✓ Liiklus edukalt vahetatud!${NC}"
else
    echo -e "${RED}✗ Viga liikluse vahetamisel!${NC}"
    exit 1
fi

# Näita URL
NODEPORT=$(kubectl get service frontend-service -o jsonpath='{.spec.ports[0].nodePort}')
echo -e "Testi: ${COLOR}http://$(minikube ip):$NODEPORT${NC}"

# Küsi kas kustutada vana versioon
echo -e "\nKas kustutada $CURRENT deployment? (y/n)"
read -r response
if [[ "$response" == "y" ]]; then
    echo "Kustutan $CURRENT deployment..."
    kubectl delete deployment frontend-$CURRENT
    echo -e "${GREEN}Vana versioon kustutatud${NC}"
else
    echo "Hoidame mõlemad versioonid"
fi

echo -e "${GREEN}Blue-Green deployment lõpetatud!${NC}"
```

### 3.3 Testimine

```bash
# 1. Deploy mõlemad versioonid
kubectl apply -f blue-green.yaml

# 2. Kontrolli mõlemad deployment'd
kubectl get deployments -l app=frontend
kubectl get pods -l app=frontend

# 3. Testi blue versioon
minikube service frontend-service
# Peaksite nägema sinist lehte

# 4. Käivita switch script
chmod +x switch-deployment.sh
./switch-deployment.sh

# 5. Testi green versioon (sama URL)
# Peaksite nägema rohelist lehte

# 6. Testi zero-downtime
# Terminal 1: Pidev pärimine
while true; do 
    curl -s http://$(minikube ip):$(kubectl get svc frontend-service -o jsonpath='{.spec.ports[0].nodePort}') | grep -o "BLUE\|GREEN"
    sleep 0.5
done

# Terminal 2: Switch deployment
./switch-deployment.sh
# Terminal 1 ei tohiks näidata katkestusi

# 7. Rollback test
kubectl apply -f /tmp/frontend-service-backup.yaml
```

---

## Ülesanne 4: Security Hardening (20 punkti)

### 4.1 Network Policies (10 punkti)

**Dokumentatsioon:**
- Network Policies: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Network Policy Recipes: https://github.com/ahmetb/kubernetes-network-policy-recipes
- Cilium Network Policy: https://docs.cilium.io/en/stable/security/policy/

```yaml
# network-policy.yaml
# 1. Default deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: default
spec:
  podSelector: {}  # Kehtib kõigile pod'idele
  policyTypes:
  - Ingress
  - Egress
  egress:
  # Luba DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53

---
# 2. Allow frontend -> backend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 3000

---
# 3. Allow backend -> database
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-to-database
spec:
  podSelector:
    matchLabels:
      app: postgres
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 5432

---
# 4. Allow backend -> redis
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-to-redis
spec:
  podSelector:
    matchLabels:
      app: redis
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 6379

---
# 5. Allow ingress -> frontend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-frontend
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 80
```

### 4.2 Pod Security Context (10 punkti)

**Dokumentatsioon:**
- Pod Security Context: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
- Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/
- Linux Capabilities: https://man7.org/linux/man-pages/man7/capabilities.7.html

```yaml
# secure-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-backend
  labels:
    app: backend-secure
spec:
  # Pod-level security context
  securityContext:
    runAsNonRoot: true      # Keela root kasutaja
    runAsUser: 1000         # Kasuta UID 1000 (node user)
    runAsGroup: 3000        # Kasuta GID 3000
    fsGroup: 2000           # Failisüsteemi grupp
    seccompProfile:         # Seccomp profiil
      type: RuntimeDefault
  
  containers:
  - name: app
    image: node:18-alpine
    command: ["node", "server.js"]
    
    # Container-level security context
    securityContext:
      allowPrivilegeEscalation: false  # Keela privilege escalation
      readOnlyRootFilesystem: true     # Read-only failisüsteem
      capabilities:
        drop:
        - ALL           # Drop kõik capabilities
        add:
        - NET_BIND_SERVICE  # Lisa ainult vajalikud
      
    volumeMounts:
    - name: tmp
      mountPath: /tmp
      readOnly: false  # Ajutine kirjutatav kaust
    - name: cache
      mountPath: /app/.cache
      readOnly: false
    
    resources:
      limits:
        cpu: "200m"
        memory: "256Mi"
      requests:
        cpu: "100m"
        memory: "128Mi"
  
  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

### 4.3 Testimine

```bash
# 1. Network Policies testimine
# Deploy policies
kubectl apply -f network-policy.yaml

# Loo test pod
kubectl run test-pod --image=nicolaka/netshoot -it --rm -- bash

# Test pod'i sees:
# Proovi ühenduda backend'i (peaks ebaõnnestuma)
curl http://backend-service:3000
# timeout

# Proovi frontend pod'ist (peaks töötama)
kubectl exec -it $(kubectl get pods -l app=frontend -o jsonpath='{.items[0].metadata.name}') -- curl http://backend-service:3000/health

# Kontrolli policy'sid
kubectl get networkpolicies
kubectl describe networkpolicy allow-frontend-to-backend

# 2. Security Context testimine
# Deploy secure pod
kubectl apply -f secure-pod.yaml

# Kontrolli security context
kubectl get pod secure-backend -o jsonpath='{.spec.securityContext}' | jq

# Proovi saada root õigusi (peaks ebaõnnestuma)
kubectl exec -it secure-backend -- sh
$ whoami
# node (mitte root)
$ id
# uid=1000(node) gid=3000 groups=3000,2000
$ su root
# su: must be suid to work properly
$ touch /etc/test
# touch: /etc/test: Read-only file system

# 3. Skaneeri security probleeme
# Installi kubesec
wget https://github.com/controlplaneio/kubesec/releases/download/v2.11.5/kubesec_linux_amd64.tar.gz
tar -xzf kubesec_linux_amd64.tar.gz
sudo mv kubesec /usr/local/bin/

# Skaneeri pod
kubectl get pod secure-backend -o yaml | kubesec scan -

# 4. Kontrolli Pod Security Standards
kubectl label namespace default pod-security.kubernetes.io/enforce=restricted
kubectl apply -f secure-pod.yaml
# Kontrolli kas pod vastab "restricted" standardile
```

---

## Ülesanne 5: Monitoring Dashboard (15 punkti)

### 5.1 Custom Grafana Dashboard (10 punkti)

**Dokumentatsioon:**
- Grafana Dashboards: https://grafana.com/docs/grafana/latest/dashboards/
- PromQL Basics: https://prometheus.io/docs/prometheus/latest/querying/basics/
- Grafana JSON Model: https://grafana.com/docs/grafana/latest/dashboards/json-model/

```json
{
  "dashboard": {
    "title": "E-Shop Monitoring",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(nginx_ingress_controller_requests[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ],
        "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 }
      },
      {
        "id": 2,
        "title": "Error Rate %",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(nginx_ingress_controller_requests{status=~\"5..\"}[5m])) / sum(rate(nginx_ingress_controller_requests[5m])) * 100"
          }
        ],
        "gridPos": { "h": 8, "w": 12, "x": 12, "y": 0 }
      },
      {
        "id": 3,
        "title": "Response Time P95",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(nginx_ingress_controller_response_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "95th percentile"
          }
        ],
        "gridPos": { "h": 8, "w": 12, "x": 0, "y": 8 }
      },
      {
        "id": 4,
        "title": "Pod Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "container_memory_usage_bytes{pod=~\"backend-.*|frontend-.*\"}",
            "legendFormat": "{{pod}}"
          }
        ],
        "gridPos": { "h": 8, "w": 12, "x": 12, "y": 8 }
      },
      {
        "id": 5,
        "title": "Database Connections",
        "type": "stat",
        "targets": [
          {
            "expr": "pg_stat_database_numbackends{datname=\"shopdb\"}"
          }
        ],
        "gridPos": { "h": 8, "w": 12, "x": 0, "y": 16 }
      }
    ],
    "refresh": "10s",
    "time": { "from": "now-1h", "to": "now" }
  }
}
```

### 5.2 Alert Rules (5 punkti)

```yaml
# alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: shop-alerts
  namespace: monitoring
spec:
  groups:
  - name: shop.rules
    interval: 30s
    rules:
    # High Error Rate
    - alert: HighErrorRate
      expr: |
        sum(rate(nginx_ingress_controller_requests{status=~"5.."}[5m])) 
        / 
        sum(rate(nginx_ingress_controller_requests[5m])) 
        > 0.05
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High error rate detected ({{ $value | humanizePercentage }})"
        description: "Error rate is above 5% for 5 minutes"
    
    # Pod Memory High
    - alert: PodMemoryHigh
      expr: |
        container_memory_usage_bytes{pod=~"backend-.*|frontend-.*"} 
        / 
        container_spec_memory_limit_bytes{pod=~"backend-.*|frontend-.*"} 
        > 0.8
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Pod {{ $labels.pod }} memory usage high"
        description: "Memory usage is above 80% ({{ $value | humanizePercentage }})"
    
    # Pod Restarts
    - alert: PodRestartingTooOften
      expr: |
        rate(kube_pod_container_status_restarts_total[15m]) > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Pod {{ $labels.pod }} is restarting frequently"
        description: "Pod has restarted {{ $value }} times in the last 15 minutes"
    
    # Database Down
    - alert: PostgresDown
      expr: up{job="postgres"} == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "PostgreSQL database is down"
        description: "PostgreSQL has been down for more than 1 minute"
    
    # High Response Time
    - alert: HighResponseTime
      expr: |
        histogram_quantile(0.95,
          sum(rate(nginx_ingress_controller_response_duration_seconds_bucket[5m])) by (le)
        ) > 2
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "High response time detected"
        description: "95th percentile response time is above 2 seconds ({{ $value }}s)"
```

### 5.3 Testimine

```bash
# 1. Import dashboard Grafanasse
# Port-forward Grafana
kubectl port-forward -n monitoring service/monitoring-grafana 3000:80

# Ava: http://localhost:3000 (admin/admin123)
# Create -> Import -> Upload JSON file

# 2. Deploy alert rules
kubectl apply -f alerts.yaml

# Kontrolli et reeglid laeti
kubectl get prometheusrules -n monitoring
kubectl describe prometheusrule shop-alerts -n monitoring

# 3. Testi alert'e
# High Error Rate - genereeri 500 vigu
for i in {1..100}; do 
    curl http://backend-service:3000/nonexistent
done

# Pod Memory - loo memory pressure
kubectl run memory-test --image=progrium/stress --rm -it -- --vm 1 --vm-bytes 250M --timeout 30s

# 4. Vaata alert'e Prometheuses
kubectl port-forward -n monitoring service/monitoring-kube-prometheus-prometheus 9090:9090
# Ava: http://localhost:9090/alerts

# 5. Testi Grafana paneelid
# Genereeri liiklust
kubectl run traffic-gen --image=busybox --rm -it -- sh -c "
while true; do
  wget -q -O- http://frontend-service > /dev/null
  wget -q -O- http://backend-service:3000/api/products > /dev/null
  sleep 1
done"

# Vaata Grafana dashboard'i - peaks nägema andmeid

# 6. PromQL päringute testimine
# Prometheus UI-s (http://localhost:9090)
# Proovi päringuid:
rate(container_cpu_usage_seconds_total{pod=~"backend-.*"}[5m])
container_memory_usage_bytes{pod=~"frontend-.*"}
up{job="kubernetes-pods"}
```

---

## Boonusülesanded (10 lisapunkti)

## Ülesanne 1: Redis Cache Lisamine (20 punkti)

### 1.1 Nõuded (10 punkti)

Lisage Redis cache backend API ja PostgreSQL vahele. Redis peaks cache'ima toodete päringuid, et vähendada andmebaasi koormust.

**Tehnilised nõuded:**
- Redis Deployment (1 pod on piisav)
- Redis Service
- TTL (Time To Live) 5 minutit cache'itud andmetele
- Cache invalidation kui toode ostetakse

**Dokumentatsioon:**
- Redis Docker Hub: https://hub.docker.com/_/redis
- Redis Kubernetes näited: https://kubernetes.io/docs/tutorials/configuration/configure-redis-using-configmap/
- Redis Node.js klient: https://github.com/redis/node-redis

### 1.2 Implementatsioon (10 punkti)

```yaml
# redis.yaml - TEIE ÜLESANNE: täitke lüngad
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cache
spec:
  replicas: ???  # Vihje: Redis on stateful, 1 on piisav
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: ???  # Peab vastama selector.matchLabels.app
    spec:
      containers:
      - name: redis
        image: ???  # Vihje: redis:7-alpine (väike ja kiire)
        ports:
        - containerPort: ???  # Vihje: Redis vaikimisi port on 6379
        resources:
          requests:
            memory: "???"  # Vihje: 64Mi on hea algus
            cpu: "???"     # Vihje: 50m (0.05 CPU)
          limits:
            memory: "???"  # Vihje: 128Mi
            cpu: "???"     # Vihje: 100m

---
apiVersion: v1
kind: Service
metadata:
  name: ???
spec:
  selector:
    app: ???
  ports:
  - port: ???
    targetPort: ???
```

**Backend koodi muudatus:**
```javascript
// Lisage Redis tugi backend API-sse
const redis = require('redis');
const client = redis.createClient({
    host: 'redis-service',
    port: 6379
});

// TEIE ÜLESANNE: Implementeerige cache loogika
app.get('/api/products', async (req, res) => {
    // 1. Kontrolli Redis cache'i
    // 2. Kui on cache'is, tagasta sealt
    // 3. Kui pole, päri andmebaasist
    // 4. Salvesta Redis'esse 5 minutiks
    // 5. Tagasta tulemus
});
```

**Kontroll:**
- Redis pod töötab: 5 punkti
- Service õigesti konfigureeritud: 5 punkti
- Cache loogika töötab backend'is: 10 punkti

---

## Ülesanne 2: Horizontal Pod Autoscaler (20 punkti)

### 2.1 HPA Backend API jaoks (10 punkti)

Looge HorizontalPodAutoscaler, mis skaleerib backend pod'e automaatselt CPU kasutuse põhjal.

```yaml
# hpa-backend.yaml - TEIE ÜLESANNE
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: ???
    kind: ???
    name: ???
  minReplicas: ???  # Minimaalne pod'ide arv
  maxReplicas: ???  # Maksimaalne pod'ide arv
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: ???  # CPU % mis käivitab skaleerimise
```

### 2.2 Load Test ja Verifikatsioon (10 punkti)

```bash
# TEIE ÜLESANNE: Kirjutage skript, mis:
# 1. Tekitab koormust backend API-le
# 2. Jälgib pod'ide arvu muutumist
# 3. Salvestab tulemused faili

#!/bin/bash
# loadtest.sh
echo "Alustame load testi..."

# Genereeri koormust
for i in {1..100}; do
    curl http://backend-service:3000/api/products &
done

# Jälgi HPA staatust
kubectl get hpa backend-hpa --watch
```

**Kontroll:**
- HPA õigesti konfigureeritud: 5 punkti
- Skaleerimine töötab (2→5 pod'i): 10 punkti
- Load test skript töötab: 5 punkti

---

## Ülesanne 3: Blue-Green Deployment - Turvaline Uuendamine (25 punkti)

### Mis on Blue-Green Deployment?

Kujutage ette, et teil on pood, mis töötab 24/7. Kuidas uuendada kassasüsteemi ilma poodi sulgemata? Blue-Green deployment on nagu kahe identse poe omamine - üks töötab (Blue) samal ajal kui teise (Green) uuendate. Kui Green on valmis, suunate kõik kliendid sinna. Kui midagi läheb valesti, suunate tagasi Blue poodi.

**Analoogia:** See on nagu teatris, kus on kaks lava. Samal ajal kui publik vaatab etendust Blue laval, valmistate Green laval uut etendust. Kui valmis, suunate publiku Green lavale ilma pausita.

```
Algus:       Kliendid → [Blue v1.0] ✓
                        [Green ----] (pole kasutusel)

Uuendamine:  Kliendid → [Blue v1.0] ✓
                        [Green v2.0] (valmistame)

Vahetus:     Kliendid → [Green v2.0] ✓
                        [Blue v1.0] (backup)

Probleem?    Kliendid → [Blue v1.0] ✓ (tagasi vana juurde!)
                        [Green v2.0] (parandame)
```

### 3.1 Implementeerimine (15 punkti)

**Dokumentatsioon algajatele:**
- Mis on Blue-Green: https://www.redhat.com/en/topics/devops/what-is-blue-green-deployment
- Kubernetes Services selgitus: https://kubernetes.io/docs/tutorials/kubernetes-basics/expose/expose-intro/

```yaml
# blue-green.yaml
# See fail loob KAKS identset rakendust - Blue ja Green

# === BLUE VERSIOON (praegu töötav) ===
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-blue
  labels:
    version: blue  # Märgistame et see on blue
spec:
  replicas: 3  # 3 koopiat töökindluse jaoks
  selector:
    matchLabels:
      app: frontend
      version: blue  # Oluline: version peab olema blue
  template:
    metadata:
      labels:
        app: frontend
        version: blue  # Pod'id saavad blue märgistuse
    spec:
      containers:
      - name: nginx
        image: nginx:1.21-alpine
        ports:
        - containerPort: 80
        # Lisame lihtsa HTML faili et eristada versioone
        volumeMounts:
        - name: html
          mountPath: /usr/share/nginx/html
      volumes:
      - name: html
        configMap:
          name: blue-html

---
# Blue versiooni HTML (et visuaalselt eristada)
apiVersion: v1
kind: ConfigMap
metadata:
  name: blue-html
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blue Version</title>
        <style>
            body { 
                background: #3498db; 
                color: white; 
                font-family: Arial;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
            }
            h1 { font-size: 4em; }
            p { font-size: 2em; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔵 BLUE VERSION</h1>
            <p>Version 1.21 - Stable</p>
            <p>See on praegu töötav versioon</p>
        </div>
    </body>
    </html>

---
# === GREEN VERSIOON (uus versioon) ===
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-green
  labels:
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
      version: green  # Oluline: version peab olema green
  template:
    metadata:
      labels:
        app: frontend
        version: green  # Pod'id saavad green märgistuse
    spec:
      containers:
      - name: nginx
        image: nginx:1.22-alpine  # Uuem versioon!
        ports:
        - containerPort: 80
        volumeMounts:
        - name: html
          mountPath: /usr/share/nginx/html
      volumes:
      - name: html
        configMap:
          name: green-html

---
# Green versiooni HTML
apiVersion: v1
kind: ConfigMap
metadata:
  name: green-html
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head>
        <title>Green Version</title>
        <style>
            body { 
                background: #2ecc71; 
                color: white; 
                font-family: Arial;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
            }
            h1 { font-size: 4em; }
            p { font-size: 2em; }
            .new { 
                background: #f39c12; 
                padding: 10px; 
                border-radius: 5px;
                display: inline-block;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🟢 GREEN VERSION</h1>
            <p>Version 1.22 - New Features!</p>
            <div class="new">✨ UUS VERSIOON ✨</div>
        </div>
    </body>
    </html>

---
# === SERVICE - "Uksehoidja" ===
# Service otsustab, kumma versiooni juurde kasutajad suunata
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
    version: blue  # <-- SEE RIDA MÄÄRAB VERSIOONI!
                  # Muutes seda blue->green suuname kasutajad
  ports:
  - port: 80
    targetPort: 80
  type: NodePort
```

### 3.2 Lihtne Switching Script (10 punkti)

```bash
#!/bin/bash
# switch.sh - Lihtne script versiooni vahetamiseks

echo "======================================"
echo "   Blue-Green Deployment Switcher    "
echo "======================================"

# 1. Vaata mis versioon praegu töötab
echo "📍 Kontrollin praegust versiooni..."
CURRENT=$(kubectl get service frontend-service -o jsonpath='{.spec.selector.version}')
echo "   Praegu töötab: $CURRENT versioon"

# 2. Otsusta kuhu lülitada
if [ "$CURRENT" == "blue" ]; then
    NEW="green"
    echo "🟢 Lülitan GREEN versioonile"
else
    NEW="blue"
    echo "🔵 Lülitan BLUE versioonile"
fi

# 3. Kontrolli kas uus versioon töötab
echo "🔍 Kontrollin kas $NEW versioon on valmis..."
READY=$(kubectl get deployment frontend-$NEW -o jsonpath='{.status.readyReplicas}')
DESIRED=$(kubectl get deployment frontend-$NEW -o jsonpath='{.spec.replicas}')

if [ "$READY" != "$DESIRED" ]; then
    echo "❌ VIGA: $NEW versioon pole valmis!"
    echo "   Valmis: $READY / Vaja: $DESIRED"
    exit 1
fi

echo "✅ $NEW versioon on valmis!"

# 4. Tee backup praegusest seadistusest
echo "💾 Teen backup..."
kubectl get service frontend-service -o yaml > backup-service.yaml

# 5. Vaheta versioon
echo "🔄 Vahetan versiooni..."
kubectl patch service frontend-service -p '{"spec":{"selector":{"version":"'$NEW'"}}}'

# 6. Kontrolli kas õnnestus
sleep 2
FINAL=$(kubectl get service frontend-service -o jsonpath='{.spec.selector.version}')
if [ "$FINAL" == "$NEW" ]; then
    echo "✅ ÕNNESTUS! Nüüd töötab $NEW versioon"
    
    # Näita URL
    NODE_IP=$(minikube ip)
    NODE_PORT=$(kubectl get service frontend-service -o jsonpath='{.spec.ports[0].nodePort}')
    echo ""
    echo "🌐 Testi brauseris:"
    echo "   http://$NODE_IP:$NODE_PORT"
    echo ""
    echo "💡 Vihje: Kui midagi on valesti, taasta vana:"
    echo "   kubectl apply -f backup-service.yaml"
else
    echo "❌ Midagi läks valesti!"
fi
```

### 3.3 Testimine ja Selgitus

```bash
# === SAMM 1: Deploy mõlemad versioonid ===
kubectl apply -f blue-green.yaml

# Oota kuni kõik pod'id käivituvad (30-60 sekundit)
kubectl get pods -w
# Peaksite nägema:
# frontend-blue-xxxxx    Running
# frontend-green-xxxxx   Running
# (Kokku 6 pod'i - 3 blue, 3 green)

# === SAMM 2: Vaata praegust versiooni ===
minikube service frontend-service
# Avaneb brauser - näete SINIST lehte

# === SAMM 3: Testi switching ===
chmod +x switch.sh
./switch.sh
# Värskendage brauserit - näete ROHELIST lehte!

# === SAMM 4: Mis tegelikult juhtus? ===
# Service muutis oma "selector" välja:
# Enne: version: blue → Kõik liiklus läks blue pod'idele
# Nüüd: version: green → Kõik liiklus läheb green pod'idele

# === SAMM 5: Zero-downtime test ===
# Avage 2 terminali

# Terminal 1: Pidev testimine
while true; do
    curl -s http://$(minikube ip):$(kubectl get svc frontend-service -o jsonpath='{.spec.ports[0].nodePort}') | grep -o "BLUE\|GREEN"
    sleep 0.5
done
# See näitab: BLUE BLUE BLUE BLUE...

# Terminal 2: Vaheta versioon
./switch.sh
# Terminal 1 näitab nüüd: GREEN GREEN GREEN...
# Märkate et pole katkestust!

# === SAMM 6: Probleem? Rollback! ===
kubectl apply -f backup-service.yaml
# Tagasi vana versiooni juurde!
```

### Miks See On Kasulik?

1. **Null Downtime** - Kasutajad ei märka uuendust
2. **Kiire Rollback** - Kui uus versioon on vigane, saate sekundiga tagasi
3. **Testimine** - Saate testida uut versiooni enne kõigi kasutajate suunamist
4. **Turvaline** - Vana versioon jääb alles backup'iks

**Päris Elus:**
- Netflix kasutab seda filmide soovituste uuendamiseks
- Amazon kasutab seda e-poe uuendamiseks
- Facebook testib uusi funktsioone osale kasutajatest

---

## Ülesanne 4: Security - Turvalisus (20 punkti)

### Mis On Kubernetes Security?

Kujutage ette, et teie maja on Kubernetes klaster. Iga tuba on pod. Tavaliselt saavad kõik toad üksteisega suhelda - köögi (backend) saab minna magamistuppa (database). Aga kas see on turvaline? Network Policy on nagu uksed ja lukud - määrate, kes tohib kuhu minna.

**Analoogia:** See on nagu ülikooli turvareegel - tudengid pääsevad raamatukokku, aga mitte serveriruumi. Professorid pääsevad mõlemasse. Külalised pääsevad ainult fuajeesse.

### 4.1 Network Policies - "Tulemüürid" (10 punkti)

**Dokumentatsioon algajatele:**
- Mis on Network Policy: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Lihtne selgitus videoga: https://www.youtube.com/watch?v=3gGpMmYeEO8

```yaml
# network-policy.yaml
# Loome "Zero Trust" - keegi ei saa kellegagi rääkida, v.a lubatud

# === REEGEL 1: Keela kõik ===
# See on nagu lukustada kõik uksed majas
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: default
spec:
  podSelector: {}  # Kehtib KÕIGILE pod'idele
  policyTypes:
  - Ingress  # Sissetulevad ühendused
  - Egress   # Väljaminevad ühendused
  egress:
  # Lubame ainult DNS (et nimed töötaksid)
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53

---
# === REEGEL 2: Frontend tohib Backend'iga rääkida ===
# See on nagu: "Kassapidaja tohib laoga rääkida"
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend  # See policy kaitseb backend'i
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend  # Ainult frontend tohib siseneda
    ports:
    - protocol: TCP
      port: 3000  # Ainult port 3000 (API port)

---
# === REEGEL 3: Backend tohib Database'iga rääkida ===
# See on nagu: "Ladu tohib inventuurisüsteemiga rääkida"
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-to-database
spec:
  podSelector:
    matchLabels:
      app: postgres  # See policy kaitseb andmebaasi
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: backend  # Ainult backend tohib siseneda
    ports:
    - protocol: TCP
      port: 5432  # PostgreSQL port
```

### 4.2 Pod Security - "Kasutaja Õigused" (10 punkti)

Kui Network Policy on uksed ja lukud, siis Pod Security on kasutajaõigused. Näiteks: külalised ei tohi faile muuta, praktikandid ei tohi administraatori õigusi saada.

**Dokumentatsioon:**
- Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/

```yaml
# secure-pod.yaml
# Turvaline pod - töötab tavalise kasutajana, mitte root'ina

apiVersion: v1
kind: Pod
metadata:
  name: secure-backend
spec:
  # Pod'i turvaseaded
  securityContext:
    runAsNonRoot: true     # EI TOHI olla root (admin)
    runAsUser: 1000        # Tavaline kasutaja ID
    runAsGroup: 3000       # Grupi ID
    fsGroup: 2000          # Failide grupp
  
  containers:
  - name: app
    image: node:18-alpine
    
    # Konteineri turvaseaded
    securityContext:
      allowPrivilegeEscalation: false  # Ei tohi saada admin õigusi
      readOnlyRootFilesystem: true     # Failisüsteem on kirjutuskaitstud
      capabilities:
        drop:
        - ALL  # Eemalda KÕIK eriõigused
    
    # Need kaustad on kirjutatavad
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/cache
    
    resources:
      limits:
        cpu: "200m"
        memory: "256Mi"
  
  volumes:
  - name: tmp
    emptyDir: {}  # Ajutine kaust
  - name: cache
    emptyDir: {}  # Cache kaust
```

### 4.3 Testimine

```bash
# === Network Policy Testimine ===

# 1. Deploy policies
kubectl apply -f network-policy.yaml

# 2. Loo test pod
kubectl run test --image=nicolaka/netshoot -it --rm -- bash

# Test pod'is:
# Proovi ühenduda backend'i (ei tööta, sest pole lubatud)
curl backend-service:3000
# Timeout - ühendus blokeeritud!

exit

# 3. Proovi frontend pod'ist (peaks töötama)
kubectl exec -it $(kubectl get pods -l app=frontend -o jsonpath='{.items[0].metadata.name}') -- sh
curl backend-service:3000/health
# Töötab!
exit

# === Security Context Testimine ===

# 1. Deploy secure pod
kubectl apply -f secure-pod.yaml

# 2. Kontrolli, et EI ole root
kubectl exec -it secure-backend -- sh
whoami
# Vastus: node (MITTE root)

# Proovi luua fail süsteemi kausta
touch /etc/test.txt
# Permission denied - ei saa kirjutada!

# Proovi /tmp kausta (lubatud)
touch /tmp/test.txt
ls /tmp
# Töötab!
exit
```

### Miks See On Oluline?

1. **Network Policies** = Vähenda rünnaku pinda
   - Kui hacker pääseb frontend'i, ei saa ta andmebaasi
   
2. **Security Context** = Vähenda kahju ulatust
   - Kui hacker pääseb pod'i, ei saa ta admin õigusi

**Päris Näide:**
2017. aastal häkkis keegi Equifax'i, sest neil polnud network segmentation'i. Hacker pääses ühest serverist kogu võrku. Kubernetes Network Policies oleks selle ära hoidnud!

---

## Ülesanne 5: Monitoring Dashboard (15 punkti)

### 5.1 Custom Grafana Dashboard (10 punkti)

Looge Grafana dashboard järgmiste panelidega:

1. **Request Rate** - päringute arv sekundis
2. **Error Rate** - vigade %
3. **Response Time** - 95th percentile
4. **Pod Memory Usage** - kõik pod'id
5. **Database Connections** - aktiivsed ühendused

```json
{
  "dashboard": {
    "title": "E-Shop Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "???"  // TEIE ÜLESANNE: Prometheus query
          }
        ]
      }
      // ... ülejäänud panelid
    ]
  }
}
```

### 5.2 Alert Rules (5 punkti)

```yaml
# alerts.yaml - TEIE ÜLESANNE
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: shop-alerts
spec:
  groups:
  - name: shop
    rules:
    - alert: HighErrorRate
      expr: ???  # Error rate > 5%
      for: 5m
      annotations:
        summary: "High error rate detected"
    
    - alert: PodMemoryHigh
      expr: ???  # Memory > 80%
      for: 10m
      annotations:
        summary: "Pod memory usage high"
```

**Kontroll:**
- Dashboard panelid töötavad: 10 punkti
- Alert'id käivituvad õigesti: 5 punkti

---

## Boonusülesanded (10 lisapunkti)

### B1: Helm Chart (5 punkti)

Pakendage kogu rakendus Helm chart'iks.

```yaml
# Chart.yaml
apiVersion: v2
name: eshop
description: E-Shop Kubernetes Application
type: application
version: 1.0.0

# values.yaml
backend:
  replicas: ???
  image: ???
  
frontend:
  replicas: ???
  
database:
  password: ???
```

### B2: CI/CD Pipeline (5 punkti)

Looge GitHub Actions workflow, mis:
1. Ehitab Docker image'd
2. Push'ib Docker Hub'i
3. Deploy'ib Kubernetes'isse

```yaml
# .github/workflows/deploy.yml
name: Deploy to Kubernetes
on:
  push:
    branches: [main]
    
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    # TEIE ÜLESANNE: Lisa sammud
```

---

## Esitamine

### Nõutud failid:

```
kodutoo/
├── README.md           # Dokumentatsioon
├── redis/
│   └── redis.yaml
├── hpa/
│   └── hpa-backend.yaml
├── blue-green/
│   ├── deployments.yaml
│   └── switch.sh
├── security/
│   ├── network-policy.yaml
│   └── secure-pod.yaml
├── monitoring/
│   ├── dashboard.json
│   └── alerts.yaml
├── scripts/
│   └── loadtest.sh
└── screenshots/
    ├── redis-working.png
    ├── hpa-scaling.png
    ├── blue-green-switch.png
    └── grafana-dashboard.png
```

### README.md struktuur:

```markdown
# Kubernetes Kodutöö - [Teie Nimi]

## Ülesanne 1: Redis Cache
- Kirjeldus, kuidas implementeerisite
- Probleemid ja lahendused
- Screenshot Redis'e töötamisest

## Ülesanne 2: HPA
- Scaling poliitika selgitus
- Load test tulemused
- Screenshot HPA töötamisest

## Ülesanne 3: Blue-Green Deployment
- Strateegia kirjeldus
- Switching protsess
- Zero-downtime tõestus

## Ülesanne 4: Security
- Network policies selgitus
- Security context põhjendused

## Ülesanne 5: Monitoring
- Dashboard kirjeldus
- Alert'ide loogika

## Õpitud Teadmised
- Mis oli kõige raskem?
- Mis oli kõige huvitavam?
- Mida teeksite teisiti?
```

---

## Hindamiskriteeriumid

| Kriteerium | Punktid |
|------------|---------|
| Redis Cache töötab | 20 |
| HPA skaleerib automaatselt | 20 |
| Blue-Green deployment | 25 |
| Security implementeeritud | 20 |
| Monitoring dashboard | 15 |
| **Kokku** | **100** |

**Hindamisskaala:**
- 90-100 punkti: A (Suurepärane)
- 80-89 punkti: B (Väga hea)
- 70-79 punkti: C (Hea)
- 60-69 punkti: D (Rahuldav)
- <60 punkti: F (Mitte rahuldav)

---

## Vihjed

1. **Redis:** Kasutage `redis:alpine` image'it (väiksem)
2. **HPA:** Metrics Server peab olema enabled (`minikube addons enable metrics-server`)
3. **Blue-Green:** Service selector on võti
4. **Network Policy:** Alustage "deny all" policy'st
5. **Monitoring:** Kasutage `rate()` funktsiooni Prometheus'is

**Edu!** 🚀
