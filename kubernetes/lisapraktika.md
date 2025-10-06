#  Kubernetes: Lisapraktika


**Eesmärk:** Süvenda Kubernetes teadmisi ja õpi production-ready patterns

---

##  Enne alustamist

Need ülesanded on **valikulised** ja mõeldud neile, kes:
-  Lõpetasid põhilabori ära
-  Mõistavad Pods, Deployments, Services
-  Tahavad õppida advanced Kubernetes
-  Valmistuvad päris cluster'i haldamiseks

**Vali üks või mitu väljakutset!**

---

##  Väljakutse 1: Horizontal Pod Autoscaler

**Eesmärk:** Loo automaatne scaling süsteem, mis reageerib CPU/RAM kasutusele

### Mida õpid?
- Horizontal Pod Autoscaler (HPA)
- Metrics Server
- Resource limits ja requests
- Load testing

### Sammud:

1. **Installi Metrics Server:**
   ```bash
   kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
   
   # Minikube'is:
   minikube addons enable metrics-server
   
   # Kontrolli:
   kubectl top nodes
   kubectl top pods
   ```

2. **Loo deployment koos resource limits:**
   ```yaml
   # deployment-with-resources.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: php-apache
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: php-apache
     template:
       metadata:
         labels:
           app: php-apache
       spec:
         containers:
         - name: php-apache
           image: registry.k8s.io/hpa-example
           ports:
           - containerPort: 80
           resources:
             requests:
               cpu: 200m
               memory: 128Mi
             limits:
               cpu: 500m
               memory: 256Mi
   ```

3. **Loo HPA:**
   ```yaml
   # hpa.yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: php-apache
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: php-apache
     minReplicas: 1
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 50
     - type: Resource
       resource:
         name: memory
         target:
           type: Utilization
           averageUtilization: 70
   ```

4. **Test load:**
   ```bash
   # Loo load generator
   kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
   
   # Container sees:
   while true; do wget -q -O- http://php-apache; done
   
   # Teises terminal'is vaata scaling'u:
   kubectl get hpa php-apache --watch
   kubectl get pods --watch
   ```

###  Boonus:
- Lisa custom metrics (application-specific)
- Kasuta KEDA (Kubernetes Event-Driven Autoscaling)
- Loo scaling based on external metrics (queue length)
- Implementeeri predictive autoscaling

---

##  Väljakutse 2: StatefulSets ja Persistent Storage

**Eesmärk:** Deploy database cluster Kubernetes'es kasutades StatefulSets

### Mida õpid?
- StatefulSets vs Deployments
- Persistent Volumes (PV) ja Claims (PVC)
- Headless Services
- Init Containers

### Ülesanne: MySQL Cluster

```yaml
# mysql-statefulset.yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  ports:
  - port: 3306
    name: mysql
  clusterIP: None  # Headless service
  selector:
    app: mysql
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      initContainers:
      - name: init-mysql
        image: mysql:8.0
        command:
        - bash
        - "-c"
        - |
          set -ex
          # Generate server-id from pod ordinal index
          [[ $(hostname) =~ -([0-9]+)$ ]] || exit 1
          ordinal=${BASH_REMATCH[1]}
          echo [mysqld] > /mnt/conf.d/server-id.cnf
          echo server-id=$((100 + $ordinal)) >> /mnt/conf.d/server-id.cnf
        volumeMounts:
        - name: conf
          mountPath: /mnt/conf.d
      containers:
      - name: mysql
        image: mysql:8.0
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: password
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
        - name: conf
          mountPath: /etc/mysql/conf.d
        livenessProbe:
          exec:
            command: ["mysqladmin", "ping"]
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command: ["mysql", "-h", "127.0.0.1", "-e", "SELECT 1"]
          initialDelaySeconds: 5
          periodSeconds: 2
      volumes:
      - name: conf
        emptyDir: {}
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

### Test StatefulSet:
```bash
# Deploy
kubectl apply -f mysql-statefulset.yaml

# Vaata pod'e
kubectl get pods -l app=mysql --watch

# Vaata PVCs
kubectl get pvc

# Connect to pod
kubectl exec -it mysql-0 -- mysql -u root -p

# Test persistent storage
kubectl delete pod mysql-0
kubectl get pod mysql-0  # Uus pod, sama data!
```

###  Boonus:
- Loo automated backup system
- Implementeeri MySQL replication
- Lisa monitoring (Prometheus MySQL exporter)
- Loo database migration job

---

##  Väljakutse 3: ConfigMaps, Secrets ja Security

**Eesmärk:** Õpi turvalist configuration management'i

### Mida õpid?
- ConfigMaps best practices
- Secrets encryption at rest
- RBAC (Role-Based Access Control)
- Pod Security Standards

### Sammud:

1. **Loo ConfigMap erinevatel viisidel:**
   ```yaml
   # From literal
   kubectl create configmap app-config \
     --from-literal=APP_ENV=production \
     --from-literal=LOG_LEVEL=info
   
   # From file
   kubectl create configmap nginx-config \
     --from-file=nginx.conf
   
   # From YAML
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: app-config
   data:
     app.properties: |
       database.host=postgres
       database.port=5432
     config.json: |
       {
         "feature_flags": {
           "new_ui": true
         }
       }
   ```

2. **Kasuta ConfigMap deployment'is:**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: myapp
   spec:
     template:
       spec:
         containers:
         - name: app
           image: myapp
           # As environment variables
           envFrom:
           - configMapRef:
               name: app-config
           # As volume
           volumeMounts:
           - name: config
             mountPath: /etc/config
         volumes:
         - name: config
           configMap:
             name: app-config
   ```

3. **Loo ja kasuta Secrets:**
   ```yaml
   # Loo Secret
   kubectl create secret generic db-credentials \
     --from-literal=username=admin \
     --from-literal=password=super-secret
   
   # Use in Deployment
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: myapp
   spec:
     template:
       spec:
         containers:
         - name: app
           image: myapp
           env:
           - name: DB_USER
             valueFrom:
               secretKeyRef:
                 name: db-credentials
                 key: username
           - name: DB_PASS
             valueFrom:
               secretKeyRef:
                 name: db-credentials
                 key: password
   ```

4. **Implementeeri RBAC:**
   ```yaml
   # Service Account
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: app-reader
   ---
   # Role (namespace-specific)
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     name: pod-reader
   rules:
   - apiGroups: [""]
     resources: ["pods"]
     verbs: ["get", "watch", "list"]
   ---
   # RoleBinding
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: read-pods
   subjects:
   - kind: ServiceAccount
     name: app-reader
   roleRef:
     kind: Role
     name: pod-reader
     apiGroup: rbac.authorization.k8s.io
   ```

###  Boonus:
- Encrypt Secrets at rest (enable in cluster)
- Kasuta External Secrets Operator (AWS Secrets Manager)
- Implementeeri Pod Security Admission
- Loo Network Policies

---

##  Väljakutse 4: Helm Charts

**Eesmärk:** Package rakendust Helm chart'ina

### Mida õpid?
- Helm chart structure
- Templating
- Values files
- Chart dependencies

### Sammud:

1. **Loo chart:**
   ```bash
   helm create myapp
   cd myapp/
   ```

2. **Chart struktuuri:**
   ```
   myapp/
   ├── Chart.yaml          # Chart metadata
   ├── values.yaml         # Default values
   ├── templates/
   │   ├── deployment.yaml
   │   ├── service.yaml
   │   ├── ingress.yaml
   │   ├── _helpers.tpl    # Template helpers
   │   └── NOTES.txt       # Post-install notes
   └── charts/             # Dependencies
   ```

3. **values.yaml:**
   ```yaml
   replicaCount: 2
   
   image:
     repository: myapp
     tag: "1.0.0"
     pullPolicy: IfNotPresent
   
   service:
     type: ClusterIP
     port: 80
   
   resources:
     limits:
       cpu: 500m
       memory: 512Mi
     requests:
       cpu: 250m
       memory: 256Mi
   
   autoscaling:
     enabled: true
     minReplicas: 2
     maxReplicas: 10
     targetCPUUtilizationPercentage: 80
   ```

4. **Template with values:**
   ```yaml
   # templates/deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: {{ include "myapp.fullname" . }}
   spec:
     replicas: {{ .Values.replicaCount }}
     selector:
       matchLabels:
         {{- include "myapp.selectorLabels" . | nindent 8 }}
     template:
       metadata:
         labels:
           {{- include "myapp.selectorLabels" . | nindent 10 }}
       spec:
         containers:
         - name: {{ .Chart.Name }}
           image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
           ports:
           - containerPort: 80
           resources:
             {{- toYaml .Values.resources | nindent 12 }}
   ```

5. **Install ja upgrade:**
   ```bash
   # Install
   helm install myapp ./myapp
   
   # Upgrade
   helm upgrade myapp ./myapp --set replicaCount=5
   
   # Override with file
   helm upgrade myapp ./myapp -f values-prod.yaml
   
   # Rollback
   helm rollback myapp 1
   ```

###  Boonus:
- Loo multi-environment values (values-dev.yaml, values-prod.yaml)
- Lisa chart dependencies (PostgreSQL, Redis)
- Publish chart to Helm repository
- Loo automated chart testing (helm test)

---

##  Väljakutse 5: Service Mesh (Istio)

**Eesmärk:** Implementeeri service mesh advanced networking'u jaoks

### Mida õpid?
- Service mesh concepts
- Traffic management
- Observability
- Security (mTLS)

### Sammud:

1. **Installi Istio:**
   ```bash
   # Download Istio
   curl -L https://istio.io/downloadIstio | sh -
   cd istio-*
   export PATH=$PWD/bin:$PATH
   
   # Install
   istioctl install --set profile=demo -y
   
   # Enable sidecar injection
   kubectl label namespace default istio-injection=enabled
   ```

2. **Deploy app with Istio:**
   ```yaml
   # Istio automaatselt inject'ib sidecar proxy
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: myapp
   spec:
     template:
       spec:
         containers:
         - name: app
           image: myapp
   ---
   # Virtual Service for traffic routing
   apiVersion: networking.istio.io/v1beta1
   kind: VirtualService
   metadata:
     name: myapp
   spec:
     hosts:
     - myapp
     http:
     - match:
       - headers:
           user-agent:
             regex: ".*Chrome.*"
       route:
       - destination:
           host: myapp
           subset: v2
     - route:
       - destination:
           host: myapp
           subset: v1
   ```

3. **Canary deployment:**
   ```yaml
   apiVersion: networking.istio.io/v1beta1
   kind: VirtualService
   metadata:
     name: myapp-canary
   spec:
     hosts:
     - myapp
     http:
     - match:
       - headers:
           canary:
             exact: "true"
       route:
       - destination:
           host: myapp
           subset: v2
     - route:
       - destination:
           host: myapp
           subset: v1
         weight: 90
       - destination:
           host: myapp
           subset: v2
         weight: 10  # 10% traffic to v2
   ```

###  Boonus:
- Loo circuit breaker
- Implementeeri retry policies
- Lisa distributed tracing (Jaeger)
- Loo traffic mirroring (shadow deployment)

---

##  Väljakutse 6: CI/CD GitOps (ArgoCD)

**Eesmärk:** Implementeeri GitOps workflow ArgoCD'ga

### Mida õpid?
- GitOps principles
- ArgoCD
- Declarative deployments
- Automated sync

### Sammud:

1. **Installi ArgoCD:**
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   
   # Get admin password
   kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
   
   # Port forward
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```

2. **Loo Git repo struktuur:**
   ```
   myapp-k8s/
   ├── base/
   │   ├── deployment.yaml
   │   ├── service.yaml
   │   └── kustomization.yaml
   ├── overlays/
   │   ├── dev/
   │   │   └── kustomization.yaml
   │   └── prod/
   │       └── kustomization.yaml
   └── argocd/
       └── application.yaml
   ```

3. **ArgoCD Application:**
   ```yaml
   # argocd/application.yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: myapp
     namespace: argocd
   spec:
     project: default
     source:
       repoURL: https://github.com/yourusername/myapp-k8s
       targetRevision: HEAD
       path: overlays/prod
     destination:
       server: https://kubernetes.default.svc
       namespace: myapp
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
   ```

4. **Deploy via Git:**
   ```bash
   # Commit changes to Git
   git add .
   git commit -m "Update deployment"
   git push
   
   # ArgoCD automaatselt sync'ib!
   # Vaata ArgoCD UI's:
   open http://localhost:8080
   ```

###  Boonus:
- Loo multi-cluster setup
- Implementeeri progressive delivery (Argo Rollouts)
- Lisa automated testing (Argo Events)
- Loo notification system (Slack/Discord)

---

##  Täiendavad ressursid

### Dokumentatsioon:
- [Kubernetes Docs](https://kubernetes.io/docs/home/)
- [Helm Docs](https://helm.sh/docs/)
- [Istio Docs](https://istio.io/latest/docs/)
- [ArgoCD Docs](https://argo-cd.readthedocs.io/)

### Tööriistad:
- **k9s:** Terminal UI for Kubernetes
- **kubectx/kubens:** Context and namespace switching
- **stern:** Multi-pod log tailing
- **kube-ps1:** Kubernetes prompt info
- **popeye:** Cluster sanity checker

### Õppimisressursid:
- [Kubernetes By Example](https://kubernetesbyexample.com/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)
- [KillerCoda K8s Playground](https://killercoda.com/playgrounds/scenario/kubernetes)

---

##  Näpunäited

1. **Start small:** Alusta lihtsamatest väljakutsetest ja liikudes keerulisemate poole.
2. **Use namespaces:** Hoia oma eksperimendid eraldi namespace'ides.
3. **Clean up:** `kubectl delete namespace <name>` kustutab kõik ressursid.
4. **Learn kubectl:** Õpi lühendeid ja trikke - `kubectl get po`, `kubectl describe`, `kubectl logs -f`.
5. **Read errors carefully:** Kubernetes error messages on tavaliselt informatiivsed.

---

**Edu ja head orkestreerimist!** 

