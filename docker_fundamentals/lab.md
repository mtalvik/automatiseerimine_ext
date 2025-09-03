# Docker Fundamentals Lab: Docker & Podman Põhilised Kogemused
## Eesmärk: "Feel the difference" - Container fundamentals hands-on (2h)

Täna õpite konteinerite alused **praktikas**. Fookus on **mõistmisel**, mitte süntaksil.

---

## 🎯 **Lab'i eesmärgid**

**Pärast seda lab'i teate:**
- **Miks konteinerid on kiired** (kogesite ise)
- **Kuidas ehitada lihtsat rakendust** (käed-küljes)
- **Docker vs Podman erinevusi** (side-by-side)
- **Põhilisi troubleshooting'u oskusi** (õppinud vigadest)

---

## 📋 **Samm 1: Container Speed Experience (30 min)**

### Ülesanne 1.1: "Feel the Speed" (10 min)

**Võrdle VM vs Container startup aegu:**

```bash
# 1. Testi container kiirus
time docker run hello-world
# Märkige aeg: _____ sekundit

# 2. Testi teist container'it  
time docker run alpine echo "Hello from container"
# Märkige aeg: _____ sekundit

# 3. Võrdle VM'iga (kui teil on access)
# Käivitage VM - märkige aeg: _____ minutit
```

**🔍 Mida märkasite?**
- Container startup: ___ sekundit
- VM startup: ___ minutit  
- Erinevus: ___x kiirem

### Ülesanne 1.2: Resource Usage Comparison (10 min)

```bash
# 1. Vaadake Docker daemon resource kasutust
ps aux | grep docker
# Märkige RAM kasutus: _____ MB

# 2. Käivitage lihtne web server
docker run -d --name test-web -p 8080:80 nginx

# 3. Kontrollige container'i resource kasutust
docker stats test-web --no-stream
# Märkige CPU ja RAM: CPU: ___% RAM: ___MB

# 4. Testiga ühendust
curl http://localhost:8080
# Kas töötab? ✅/❌
```

**🧹 Cleanup:**
```bash
docker stop test-web && docker rm test-web
```

### Ülesanne 1.3: Basic Commands Discovery (10 min)

**Avastage käske ja vaadake, mis juhtub:**

```bash
# Millised image'id teil on?
docker images

# Millised containers töötavad?
docker ps
docker ps -a  # Mis erinevus?

# Palju ruumi võtab Docker?
docker system df

# Küsimus: Miks "hello-world" image on endiselt olemas?
# Vastus: _______________________
```

---

## 📦 **Samm 2: Build Your First App (45 min)**

### 2.1: Prepare Simple Web App (10 min)

**Looge töökaust:**
```bash
mkdir ~/docker-fundamentals-lab && cd ~/docker-fundamentals-lab
```

**Looge lihtne HTML fail:**
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>My Container App</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 100px; }
        .container { background: #f0f0f0; padding: 20px; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳 My First Container App!</h1>
        <p>Server: <span id="hostname">Loading...</span></p>
        <p>Time: <span id="time"></span></p>
        <script>
            document.getElementById('time').innerText = new Date();
            fetch('/hostname').then(r => r.text()).then(h => 
                document.getElementById('hostname').innerText = h
            ).catch(() => 
                document.getElementById('hostname').innerText = 'Container ID: Unknown'
            );
        </script>
    </div>
</body>
</html>
```

### 2.2: Write Your First Dockerfile (15 min)

**Template (täitke lüngad):**
```dockerfile
# TODO: Vali base image (nginx:alpine)
FROM ______

# TODO: Kopeeri HTML fail õigesse kohta 
# Nginx serveerib faile kaustast: /usr/share/nginx/html/
COPY ______ ______

# TODO: Avage port 80
EXPOSE ______

# CMD juba defined base image'is!
```

**Vastused (pärast katsetamist):**
```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
```

### 2.3: Build and Test (10 min)

```bash
# 1. Build image
docker build -t my-web-app .

# Kas build õnnestus? ✅/❌
# Kui ei, siis vaadake error message'i ja parandage

# 2. Run container
docker run -d --name my-app -p 8080:80 my-web-app

# 3. Test
curl http://localhost:8080
# Või avage brauseris: http://localhost:8080

# Kas näete oma HTML'i? ✅/❌
```

### 2.4: Modify and Rebuild (10 min)

**Muutke HTML faili:**
```html
<!-- Lisa midagi uut, näiteks: -->
<p>Version: 2.0 - Updated!</p>
<p>Student: [Your Name]</p>
```

**Rebuild ja test:**
```bash
# Build uus versioon
docker build -t my-web-app:v2 .

# Stop vana container
docker stop my-app && docker rm my-app

# Start uus container
docker run -d --name my-app-v2 -p 8080:80 my-web-app:v2

# Test
curl http://localhost:8080
# Kas näete muudatusi? ✅/❌
```

**🧹 Cleanup:**
```bash
docker stop my-app-v2 && docker rm my-app-v2
```

---

## 🔧 **Samm 3: Docker vs Podman Side-by-Side (30 min)**

### 3.1: Install Podman (if needed) (5 min)

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y podman

# Test installation
podman --version
```

### 3.2: Same Commands, Different Tools (15 min)

**Käivitage SAMA rakendus mõlemas süsteemis:**

**Docker versio:**
```bash
# Terminal 1: Docker
docker run -d --name web-docker -p 8081:80 my-web-app:v2
```

**Podman versio:**
```bash
# Terminal 2: Podman  
podman run -d --name web-podman -p 8082:80 my-web-app:v2
```

**Teste mõlemat:**
```bash
# Docker test
curl http://localhost:8081

# Podman test  
curl http://localhost:8082

# Mõlemad töötavad? ✅/❌
```

### 3.3: Observe the Differences (10 min)

**Resource usage:**
```bash
# Docker daemon
ps aux | grep dockerd
# Märkige RAM kasutus: _____ MB

# Podman (no daemon!)
ps aux | grep podman
# Märkige RAM kasutus: _____ MB
```

**User permissions:**
```bash
# Docker (check groups)
groups $USER
# Kas "docker" on listis? ✅/❌

# Podman (no special groups needed)
podman run --rm alpine id
# Container sees: uid=0 (root)

whoami
# Host sees: [your username]
```

**Commands:**
```bash
# Proovige sama käsku
docker ps
podman ps

# Kas output on sarnane? ✅/❌
```

**🧹 Cleanup:**
```bash
docker stop web-docker && docker rm web-docker
podman stop web-podman && podman rm web-podman
```

---

## 🐛 **Samm 4: Troubleshooting & Networks (15 min)**

### 4.1: Fix Broken Container (10 min)

**Antakse teile "broken" Dockerfile:**
```dockerfile
FROM nginx:alpine
COPY index.html /wrong/path/
EXPOSE 80
```

**Proovige ehitada:**
```bash
docker build -t broken-app .
docker run -d --name broken -p 8083:80 broken-app
curl http://localhost:8083
```

**Diagnoosimine:**
```bash
# Vaadake loge
docker logs broken

# Minge sisse ja uurige
docker exec -it broken sh
ls /usr/share/nginx/html/  # Kas index.html on siin?
exit
```

**🔍 Küsimus:** Miks ei tööta?  
**Vastus:** ________________

**Parandage ja teste uuesti:**
```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
```

### Ülesanne 4.2: Simple Network Test (5 min)

```bash
# Käivitage 2 container'it custom network'is
docker network create test-network

docker run -d --name app1 --network test-network nginx:alpine
docker run -d --name app2 --network test-network nginx:alpine

# Test connectivity
docker exec app1 ping app2
# Kas töötab? ✅/❌

# Cleanup
docker stop app1 app2 && docker rm app1 app2
docker network rm test-network
```

---

## 🎯 **Samm 3: Volume Persistence Test (20 min)**

### Ülesanne 5.1: Data Persistence Challenge (15 min)

**Create persistent web content:**
```bash
# 1. Create volume
docker volume create web-content

# 2. Run container with volume
docker run -d --name web-persistent \
    -p 8084:80 \
    -v web-content:/usr/share/nginx/html \
    nginx:alpine

# 3. Add custom content
docker exec web-persistent sh -c 'echo "<h1>Persistent Data!</h1>" > /usr/share/nginx/html/index.html'

# 4. Test
curl http://localhost:8084
# Kas näete custom content'i? ✅/❌

# 5. Destroy container (but keep volume!)
docker stop web-persistent && docker rm web-persistent

# 6. Create NEW container with SAME volume
docker run -d --name web-new \
    -p 8084:80 \
    -v web-content:/usr/share/nginx/html \
    nginx:alpine

# 7. Test again
curl http://localhost:8084
# Kas andmed on alles? ✅/❌
```

**🔍 Küsimus:** Miks andmed jäid alles?  
**Vastus:** ________________

### Ülesanne 5.2: Development Workflow (5 min)

```bash
# Mount current directory
docker run -it --rm \
    -v $(pwd):/workspace \
    -w /workspace \
    alpine sh

# Inside container:
echo "Container can modify host files" > test.txt
exit

# Check on host:
cat test.txt
# Kas fail on host'is? ✅/❌

# Cleanup
rm test.txt
```

---

## 🎓 **Samm 5: Lab Summary & Reflection**

### Mida te kogesite:

**Container Speed:**
- Container startup: ___ sekundit vs VM: ___ minutit
- Resource efficiency: Vähem overhead

**Building Apps:**
- Dockerfile = retsept rakenduse loomiseks
- Layer caching optimiseerib rebuild kiirust

**Docker vs Podman:**
- Docker: Daemon architecture, vajab special group
- Podman: Daemonless, rootless security

**Troubleshooting:**
- `docker logs` - esimene debug samm
- `docker exec` - konteiner investigation
- Volume'id säilitavad andmeid

 

### 🚀 **Järgmised sammud:**

**Kodutöö:** Süvauurige Docker vs Podman võrdlust  
**Järgmine lab:** Docker Compose multi-container applications

---

## 🚀 **BOONUSÜLESANDED** (Docker'i oskajatele)

### B1: Multi-stage Docker Builds (20 min)

```dockerfile
# Optimized Node.js build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "start"]

# Build: docker build -t optimized-app .
```

### B2: Docker Security ja Best Practices (25 min)

```bash
# Non-root user
FROM alpine:latest
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -s /bin/sh -D appuser
USER appuser

# Security scanning
docker scout cves myapp:latest
docker security scan myapp:latest

# Read-only filesystem
docker run --read-only --tmpfs /tmp myapp:latest

# Resource limits
docker run --memory=512m --cpus=1.5 myapp:latest
```

### B3: Advanced Networking ja Storage (20 min)

```bash
# Custom networks
docker network create --driver bridge \
  --subnet=172.20.0.0/16 \
  --gateway=172.20.0.1 \
  custom-network

# Named volumes with options
docker volume create --driver local \
  --opt type=bind \
  --opt device=/host/path \
  --opt o=bind \
  custom-volume

# Network debugging
docker exec container-name netstat -tulpn
docker exec container-name ss -tulpn
```

### B4: Docker Performance Monitoring (15 min)

```bash
# Container stats
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# System events
docker events --filter container=myapp

# Detailed inspection
docker inspect myapp | jq '.[].[0].State'

# Health checks
docker run --health-cmd='curl -f http://localhost:3000/health' \
           --health-interval=30s \
           --health-timeout=10s \
           --health-retries=3 \
           myapp:latest
```

### B5: Docker Compose Advanced (25 min)

```yaml
# docker-compose.advanced.yml
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
      args:
        - NODE_ENV=production
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    secrets:
      - db_password
    configs:
      - app_config

secrets:
  db_password:
    file: ./secrets/db_password.txt

configs:
  app_config:
    file: ./configs/app.conf
```

**Hästi tehtud!** Teil on nüüd nii põhi- kui ka ekspert-tasemel container kogemused! 🐳
