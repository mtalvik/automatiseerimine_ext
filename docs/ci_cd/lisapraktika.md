# CI/CD Lisapraktika

Täiendavad ülesanded production-grade CI/CD pipeline'ide ehitamiseks.

**Eeldused:** Põhilabor läbitud, CI/CD pipeline põhitõed selged

---

## Enne alustamist

Need ülesanded on valikulised ja mõeldud neile, kes:

- Lõpetasid põhilabori ära
- Mõistavad CI/CD pipeline põhitõdesid
- Tahavad õppida advanced deployment strateegiaid
- Valmistuvad päris DevOps tööks

---

## Väljakutse 1: Multi-Stage Pipeline

**Eesmärk:** Loo täielik CI/CD pipeline mitme stage'iga

### Mida õpid?
- Pipeline stage'id ja dependencies
- Artifact management
- Conditional execution
- Pipeline optimization

### GitLab CI näide (.gitlab-ci.yml):
```yaml
stages:
  - build
  - test
  - security
  - deploy-staging
  - test-staging
  - deploy-production

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

# Build stage
build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  artifacts:
    reports:
      dotenv: build.env
  only:
    - main
    - develop

# Test stage - parallel jobs
test:unit:
  stage: test
  image: node:18
  script:
    - npm ci
    - npm run test:unit
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:integration:
  stage: test
  image: docker/compose:latest
  services:
    - docker:dind
  script:
    - docker-compose -f docker-compose.test.yml up --abort-on-container-exit
    - docker-compose -f docker-compose.test.yml down
  only:
    - main

# Security scanning
security:sast:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep --config=auto --json --output=sast-report.json .
  artifacts:
    reports:
      sast: sast-report.json

security:container:
  stage: security
  image: aquasec/trivy
  script:
    - trivy image --severity HIGH,CRITICAL --exit-code 1 $IMAGE_TAG
  allow_failure: true

# Deploy to staging
deploy:staging:
  stage: deploy-staging
  image: alpine/k8s:latest
  script:
    - kubectl config set-cluster staging --server=$K8S_STAGING_SERVER
    - kubectl config set-credentials deployer --token=$K8S_STAGING_TOKEN
    - kubectl set image deployment/myapp myapp=$IMAGE_TAG -n staging
    - kubectl rollout status deployment/myapp -n staging
  environment:
    name: staging
    url: https://staging.myapp.com
  only:
    - main

# Smoke tests on staging
test:smoke:
  stage: test-staging
  image: curlimages/curl
  script:
    - curl -f https://staging.myapp.com/health || exit 1
    - curl -f https://staging.myapp.com/api/v1/status || exit 1
  only:
    - main

# Deploy to production (manual)
deploy:production:
  stage: deploy-production
  image: alpine/k8s:latest
  script:
    - kubectl config set-cluster prod --server=$K8S_PROD_SERVER
    - kubectl config set-credentials deployer --token=$K8S_PROD_TOKEN
    - kubectl set image deployment/myapp myapp=$IMAGE_TAG -n production
    - kubectl rollout status deployment/myapp -n production
  environment:
    name: production
    url: https://myapp.com
  when: manual
  only:
    - main
```

### GitHub Actions näide (.github/workflows/ci-cd.yml):
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: myapp:${{ github.sha }}
          cache-from: type=registry,ref=myapp:latest
          cache-to: type=inline

  test:
    runs-on: ubuntu-latest
    needs: build
    strategy:
      matrix:
        test-type: [unit, integration, e2e]
    steps:
      - uses: actions/checkout@v3
      - name: Run ${{ matrix.test-type }} tests
        run: npm run test:${{ matrix.test-type }}

  deploy-staging:
    runs-on: ubuntu-latest
    needs: [build, test]
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v4
        with:
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
          images: myapp:${{ github.sha }}
          namespace: staging
```

###  Boonus:
- Lisa performance testing stage (k6, JMeter)
- Loo automated rollback on failure
- Implementeeri deployment approval workflow
- Lisa Slack/Discord notifications

---

## Väljakutse 2: Blue-Green Deployment

**Eesmärk:** Implementeeri zero-downtime deployment strategy

### Mida õpid?
- Blue-Green deployment pattern
- Traffic switching
- Automated rollback
- Health checks

### Kubernetes manifests:

```yaml
# deployment-blue.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  labels:
    app: myapp
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0.0
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080

---
# deployment-green.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
  labels:
    app: myapp
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: myapp
        image: myapp:v2.0.0
        ports:
        - containerPort: 8080

---
# service.yaml (switches between blue/green)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Change to "green" to switch
  ports:
  - port: 80
    targetPort: 8080
```

### Deployment script:
```bash
#!/bin/bash
# blue-green-deploy.sh

NEW_VERSION=$1
CURRENT_COLOR=$(kubectl get svc myapp -o jsonpath='{.spec.selector.version}')

if [ "$CURRENT_COLOR" == "blue" ]; then
  NEW_COLOR="green"
else
  NEW_COLOR="blue"
fi

echo "Current: $CURRENT_COLOR, Deploying to: $NEW_COLOR"

# Deploy new version
kubectl set image deployment/myapp-$NEW_COLOR myapp=myapp:$NEW_VERSION

# Wait for rollout
kubectl rollout status deployment/myapp-$NEW_COLOR

# Run smoke tests
echo "Running smoke tests..."
kubectl run smoke-test --rm -i --restart=Never --image=curlimages/curl -- \
  curl -f http://myapp-$NEW_COLOR/health

if [ $? -eq 0 ]; then
  echo "Smoke tests passed! Switching traffic..."
  
# Switch traffic
  kubectl patch svc myapp -p "{\"spec\":{\"selector\":{\"version\":\"$NEW_COLOR\"}}}"
  
  echo "Deployment successful! Traffic switched to $NEW_COLOR"
  echo "Old version ($CURRENT_COLOR) still running for rollback"
else
  echo "Smoke tests failed! Keeping traffic on $CURRENT_COLOR"
  exit 1
fi
```

### GitLab CI integration:
```yaml
deploy:blue-green:
  stage: deploy
  image: bitnami/kubectl
  script:
    - ./scripts/blue-green-deploy.sh $CI_COMMIT_SHORT_SHA
  environment:
    name: production
    url: https://myapp.com
  when: manual
  only:
    - main
```

###  Boonus:
- Lisa automated smoke tests
- Loo gradual traffic shifting (10% → 50% → 100%)
- Implementeeri automated rollback on metrics degradation
- Lisa monitoring integration (Prometheus alerts)

---

## Väljakutse 3: Canary Deployment

**Eesmärk:** Implementeeri progressive delivery canary pattern'iga

### Mida õpid?
- Canary releases
- Traffic splitting
- A/B testing
- Progressive rollout

### Argo Rollouts manifest:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 5m}
      - setWeight: 40
      - pause: {duration: 5m}
      - setWeight: 60
      - pause: {duration: 5m}
      - setWeight: 80
      - pause: {duration: 5m}
      - setWeight: 100
      canaryService: myapp-canary
      stableService: myapp-stable
      trafficRouting:
        istio:
          virtualService:
            name: myapp
            routes:
            - primary
  revisionHistoryLimit: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 8080
```

### Istio VirtualService:
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp.com
  http:
  - name: primary
    route:
    - destination:
        host: myapp-stable
      weight: 100
    - destination:
        host: myapp-canary
      weight: 0
```

### Automated analysis:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  metrics:
  - name: success-rate
    interval: 1m
    successCondition: result[0] >= 0.95
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(rate(
            http_requests_total{status=~"2..",job="myapp-canary"}[1m]
          )) /
          sum(rate(
            http_requests_total{job="myapp-canary"}[1m]
          ))
```

###  Boonus:
- Lisa automated metric analysis (error rate, latency)
- Loo header-based routing (canary for specific users)
- Implementeeri flagger (automated canary with Prometheus)
- Lisa notification on rollback

---

## Väljakutse 4: GitOps with ArgoCD

**Eesmärk:** Implementeeri full GitOps workflow

### Mida õpid?
- GitOps principles
- Declarative deployments
- Git as single source of truth
- Automated sync

### Repository structure:
```
myapp-gitops/
├── apps/
│   ├── myapp/
│   │   ├── base/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   ├── configmap.yaml
│   │   │   └── kustomization.yaml
│   │   └── overlays/
│   │       ├── dev/
│   │       │   ├── kustomization.yaml
│   │       │   └── patch-replicas.yaml
│   │       ├── staging/
│   │       │   └── kustomization.yaml
│   │       └── prod/
│   │           ├── kustomization.yaml
│   │           └── patch-resources.yaml
├── argocd/
│   ├── projects/
│   │   └── myapp.yaml
│   └── applications/
│       ├── myapp-dev.yaml
│       ├── myapp-staging.yaml
│       └── myapp-prod.yaml
└── README.md
```

### ArgoCD Application:
```yaml
# argocd/applications/myapp-prod.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-prod
  namespace: argocd
spec:
  project: myapp
  source:
    repoURL: https://github.com/yourorg/myapp-gitops
    targetRevision: main
    path: apps/myapp/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### CI Pipeline (build only):
```yaml
# .gitlab-ci.yml
stages:
  - build
  - update-manifest

build:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHORT_SHA .
    - docker push myapp:$CI_COMMIT_SHORT_SHA

update-manifest:
  stage: update-manifest
  image: alpine/git
  script:
    - git clone https://github.com/yourorg/myapp-gitops
    - cd myapp-gitops
    - sed -i "s|image: myapp:.*|image: myapp:$CI_COMMIT_SHORT_SHA|" apps/myapp/base/deployment.yaml
    - git config user.email "ci@example.com"
    - git config user.name "CI Bot"
    - git add .
    - git commit -m "Update image to $CI_COMMIT_SHORT_SHA"
    - git push
  only:
    - main
```

###  Boonus:
- Lisa multi-cluster deployment
- Loo promotion workflow (dev → staging → prod)
- Implementeeri ArgoCD notifications
- Lisa Image Updater (automated image updates)

---

## Väljakutse 5: Infrastructure as Code Pipeline

**Eesmärk:** Automatiseeri infrastructure provisioning CI/CD'ga

### Mida õpid?
- Terraform in CI/CD
- State management
- Plan/Apply automation
- Drift detection

### GitLab CI Terraform pipeline:
```yaml
stages:
  - validate
  - plan
  - apply
  - destroy

variables:
  TF_ROOT: ${CI_PROJECT_DIR}/terraform
  TF_STATE_NAME: ${CI_PROJECT_NAME}

cache:
  paths:
    - ${TF_ROOT}/.terraform

before_script:
  - cd ${TF_ROOT}
  - terraform init -backend-config="key=${TF_STATE_NAME}"

validate:
  stage: validate
  script:
    - terraform fmt -check
    - terraform validate

plan:
  stage: plan
  script:
    - terraform plan -out=plan.cache
  artifacts:
    paths:
      - ${TF_ROOT}/plan.cache
  only:
    - merge_requests

apply:
  stage: apply
  script:
    - terraform apply -auto-approve
  dependencies:
    - plan
  only:
    - main
  when: manual

destroy:
  stage: destroy
  script:
    - terraform destroy -auto-approve
  only:
    - main
  when: manual
```

### Terraform with drift detection:
```yaml
# .github/workflows/terraform-drift.yml
name: Terraform Drift Detection

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  drift-detection:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
      
      - name: Terraform Init
        run: terraform init
      
      - name: Terraform Plan
        id: plan
        run: terraform plan -detailed-exitcode
        continue-on-error: true
      
      - name: Check for drift
        if: steps.plan.outputs.exitcode == 2
        run: |
          echo "Infrastructure drift detected!"
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{"text":"Terraform drift detected in production!"}'
```

###  Boonus:
- Lisa Terraform Cloud integration
- Loo multi-environment Terraform workspaces
- Implementeeri policy as code (Sentinel/OPA)
- Lisa cost estimation (Infracost)

---

## Väljakutse 6: Full DevOps Platform (Meister)

**Eesmärk:** Ehita täielik end-to-end DevOps platform

### Komponendid:
1. **Source Control:** GitLab/GitHub
2. **CI/CD:** GitLab CI/GitHub Actions
3. **Container Registry:** Harbor/GitLab Registry
4. **Orchestration:** Kubernetes
5. **GitOps:** ArgoCD
6. **Monitoring:** Prometheus + Grafana
7. **Logging:** ELK/Loki
8. **Security:** Trivy, Snyk
9. **Secrets:** Vault/Sealed Secrets
10. **Service Mesh:** Istio

### Architecture diagram:
```
Developer → Git Push
    ↓
CI Pipeline
    ├── Build (Docker)
    ├── Test (Unit, Integration)
    ├── Security Scan (Trivy, SAST)
    ├── Push to Registry (Harbor)
    └── Update GitOps Repo
         ↓
    ArgoCD (Watches Git)
         ↓
    Deploy to Kubernetes
         ├── Dev (auto)
         ├── Staging (auto + tests)
         └── Prod (manual approval)
              ↓
         Monitoring & Alerts
              ├── Prometheus (metrics)
              ├── Grafana (dashboards)
              ├── Loki (logs)
              └── Jaeger (traces)
```

### Kickstart project:
```bash
# Clone template
git clone https://github.com/yourorg/devops-platform-template
cd devops-platform-template

# Install platform
./scripts/install-platform.sh

# Deploy sample app
./scripts/deploy-sample-app.sh
```

###  Final Boss Challenges:
- Loo multi-cluster setup (3+ clusters)
- Implementeeri disaster recovery
- Lisa compliance scanning (CIS benchmarks)
- Loo developer self-service portal
- Implementeeri cost optimization automation

---

## Täiendavad ressursid

### Dokumentatsioon:
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
- [ArgoCD](https://argo-cd.readthedocs.io/)
- [Terraform Cloud](https://www.terraform.io/cloud)

### Tööriistad:
- **Telepresence:** Local development with remote Kubernetes
- **Skaffold:** Local Kubernetes development
- **Tilt:** Multi-service development
- **k6:** Load testing
- **Octant:** Kubernetes dashboard

### Õppimisressursid:
- [DevOps Roadmap](https://roadmap.sh/devops)
- [CNCF Landscape](https://landscape.cncf.io/)
- [GitOps Working Group](https://opengitops.dev/)

---

## Näpunäited

1. **Start with simple pipeline:** Lisa features sammhaaval.
2. **Security first:** Scan images, check secrets, validate configs.
3. **Monitor everything:** Kui ei näe, siis ei saa parandada.
4. **Document pipeline:** README should explain every stage.
5. **Practice rollbacks:** Testi rollback strategy enne production'i.

---

**Edu ja head automatiseerimist!** 

