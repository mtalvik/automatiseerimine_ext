# 🐳 Docker Fundamentals Lab
*Esimene kogemus konteineritega*

---

## Lab'i Eesmärk

Täna õpite Docker'i alused praktiliselt. Lab kestab 2 tundi ja ei ole vaja eelteadmisi!

[![Docker Tutorial](https://img.youtube.com/vi/Wfou2bBtiMU/mqdefault.jpg)](https://www.youtube.com/shorts/Wfou2bBtiMU?feature=share)

---

# SAMM 1: Docker Kiirus ja Põhimõisted

## Miks Docker on oluline?

Enne Docker'it oli rakenduste käivitamine keeruline:
- Iga server vajab erinevaid programme
- Versioonide konfliktid
- "Mul töötab, aga serveris ei tööta" probleem

Docker lahendab selle - rakendus töötab kõikjal ühesuguselt.

## Image vs Container - mis vahe?

**Image (pilt)** = resept toidu valmistamiseks  
**Container (konteiner)** = valmis toit retsepti järgi

Ühest image'ist saab teha palju container'eid, nagu ühest retseptist palju toite.

## Proovige Docker'i kiirust

**Esimene container:**
```bash
# Käivitage esimene container
docker run hello-world
```

Märkage kui kiire see oli! Container käivitus mõne sekundiga.

**Võrdlus tavalisega:**
- Virtuaalmasin käivitub: 30-60 sekundit
- Docker container käivitub: 1-3 sekundit
- Erinevus: 10-20x kiirem!

```bash
# Proovige teist käsku
docker run alpine echo "Tere maailm!"
```

`alpine` on väga väike Linux operatsioonisüsteem (5MB). Docker laadis selle alla ja käivitas sekundiga.

```bash
# Käivitage sama käsk uuesti
docker run alpine echo "Tere maailm!"
```

Teine kord oli veelgi kiirem! Miks? Docker säilitas image'i cache'is ja ei pidanud uuesti alla laadima.

## Käivitage lihtne web server

**Mis on nginx?**  
Nginx on populaarne web server, mis serveerib veebilehed. Tavaliselt võtab nginx'i installimine ja seadistamine palju aega. Docker'iga saab selle käivitada ühte käsuga!

```bash
# Käivitage nginx web server
docker run -d --name minu-server -p 8080:80 nginx
```

**Käsu selgitus:**
- `docker run` = käivita uus container
- `-d` = käivita taustal (daemon mode)
- `--name minu-server` = anna container'ile nimi
- `-p 8080:80` = suuna host'i port 8080 container'i port'ile 80
- `nginx` = kasuta nginx image'i

**Port mapping selgitus:**  
Teie arvuti (host) port 8080 → Container port 80

```
Internet → localhost:8080 → Container:80 → nginx
```

Avage brauseris: http://localhost:8080

Näete nginx'i tervituse lehte! See töötab container'is, kuid on juurdepääsetav teie arvutist.

## Registry ja Image'ide allalaadimine

Kust Docker sai nginx image'i? **Docker Hub'ist** - see on suur avalik ladu (registry) kus on tuhandeid valmis image'eid.

```bash
# Vaata mis Docker tegi taustalt:
# 1. Otsis nginx image'i Docker Hub'ist
# 2. Laadis alla (pull)
# 3. Käivitas container'i

# Võite ka käsitsi alla laadida:
docker pull python:3.9
docker pull redis
docker pull postgres
```

## Vaadake mis toimub

```bash
# Millised container'id töötavad?
docker ps
```

**Tulemus näeb välja umbes nii:**
```
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS                  NAMES
abc123def456   nginx   "..."     2 min ago Up 2 min 0.0.0.0:8080->80/tcp   minu-server
```

**Tulpade selgitus:**
- `CONTAINER ID` = container'i unikaalne ID
- `IMAGE` = millist image'i kasutati
- `CREATED` = millal loodi
- `STATUS` = kas töötab (Up) või on peatunud
- `PORTS` = port mapping
- `NAMES` = container'i nimi

```bash
# Kõik container'id (ka peatunud)
docker ps -a
```

See näitab KA peatunud container'eid. Märkate, et `hello-world` ja `alpine` container'id lõpetasid töö (status "Exited").

```bash
# Millised image'id teil on?
docker images
```

**Tulemus:**
```
REPOSITORY   TAG      IMAGE ID       CREATED       SIZE
nginx        latest   abc123def456   2 weeks ago   140MB
alpine       latest   def456abc123   3 weeks ago   5.61MB
hello-world  latest   ghi789jkl012   4 months ago  13.3kB
```

**Tulpade selgitus:**
- `REPOSITORY` = image'i nimi
- `TAG` = versioon (latest = viimane)
- `SIZE` = image'i suurus kõvakettall

**Märkate suurusi:**
- hello-world: 13KB (väga väike!)
- alpine: 5.6MB (minimaalne Linux)
- nginx: 140MB (suurem, sest sisaldab nginx'i + Linux'i)

## Docker Hub tutvustus

Docker Hub on nagu "app store" container'itele. Seal on:
- **Official images:** Docker'i meeskonna hallatud (nginx, python, mysql)
- **Community images:** kasutajate tehtud
- **Private repositories:** privaatsed ettevõtte image'id

Populaarsed image'id:
- `nginx` - web server
- `python` - Python arenduskeskkond  
- `node` - JavaScript runtime
- `mysql` - andmebaas
- `redis` - cache server

## Peatage server

```bash
docker stop minu-server
docker rm minu-server
```

---

# SAMM 2: Ehitage Oma Rakendus

## Looge töökaust

```bash
mkdir docker-projekt
cd docker-projekt
```

## Looge HTML fail

```bash
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Minu Docker App</title>
    <style>
        body {
            font-family: Arial;
            text-align: center;
            margin-top: 100px;
            background: #f0f8ff;
        }
        .box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>🐳 Minu Esimene Docker Rakendus!</h1>
        <p>Tervitused: <strong>KIRJUTA SIIA OMA NIMI</strong></p>
        <p>Kuupäev: <span id="date"></span></p>
    </div>
    <script>
        document.getElementById('date').innerText = new Date().toLocaleDateString();
    </script>
</body>
</html>
EOF
```

Muutke HTML failis "KIRJUTA SIIA OMA NIMI" osa oma nimega!

## Looge Dockerfile

**Mis on Dockerfile?**  
Dockerfile on tekstifail, mis sisaldab juhiseid kuidas ehitada Docker image'i. See on nagu "retsept" teie rakenduse jaoks.

```bash
cat > Dockerfile << 'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
EOF
```

**Dockerfile'i käskude selgitus:**

**FROM nginx:alpine**
- Alustame nginx:alpine image'iga
- `alpine` on väiksem versioon (40MB vs 140MB)
- Alpine Linux on turvalisem ja kiirem

**COPY index.html /usr/share/nginx/html/**
- Kopeeri meie HTML fail container'i sisse
- `/usr/share/nginx/html/` on kaust kus nginx otsib veebilehed
- See on nginx'i vaikimisi "document root"

**EXPOSE 80**
- Dokumentatsioon, et container kasutab port 80
- Ei ava port'i automaatselt - see on ainult info

**Dockerfile vs shell script:**
- Shell script käivitab käske järjest
- Dockerfile ehitab "layered" image'i
- Igast käsust saab uus layer
- Layer'id on cacheable = kiirem rebuild

## Image'i layer'id

Docker image koosneb layer'itest nagu sibula kihid:

```
Layer 4: EXPOSE 80
Layer 3: COPY index.html /usr/share/nginx/html/
Layer 2: nginx:alpine (base image)
Layer 1: Alpine Linux
```

**Cache'i eelised:**
- Kui muudate ainult HTML'i, ainult ülemine layer builditakse uuesti
- Base layer'id jäävad cache'i
- Rebuild on kiire!

## Ehitage image

```bash
docker build -t minu-app .
```

**Käsu selgitus:**
- `docker build` = ehita image Dockerfile'i järgi
- `-t minu-app` = anna image'ile tag (nimi) "minu-app"
- `.` = kasuta käesolevat kausta (siin on Dockerfile)

**Build output selgitus:**
```
[+] Building 0.5s (7/7) FINISHED
=> [internal] load build definition from Dockerfile
=> [internal] load .dockerignore
=> [internal] load metadata for docker.io/library/nginx:alpine
=> [1/2] FROM docker.io/library/nginx:alpine
=> [internal] load build context
=> [2/2] COPY index.html /usr/share/nginx/html/
=> exporting to image
=> naming to docker.io/library/minu-app
```

**Step-by-step:**
1. **Load Dockerfile** - Docker loeb juhised
2. **Pull base image** - laeb nginx:alpine kui pole cache'is
3. **Create layer** - kopeeri HTML fail
4. **Export image** - salvestab valmis image'i
5. **Tag image** - annab nime "minu-app"

**Image nimetamine:**
- Lokaalne: `minu-app`
- Full name: `docker.io/library/minu-app:latest`
- Registry: `docker.io` (Docker Hub)
- Namespace: `library` (default)
- Repository: `minu-app`
- Tag: `latest` (default)

## Käivitage oma rakendus

```bash
docker run -d --name minu-rakendus -p 8080:80 minu-app
```

## Testinge

Avage brauseris: http://localhost:8080

Näete oma nime seal!

## Muutke rakendust

Muutke index.html faili - lisage midagi uut.

```bash
# Ehitage uus versioon
docker build -t minu-app:v2 .

# Peatage vana
docker stop minu-rakendus
docker rm minu-rakendus

# Käivitage uus
docker run -d --name minu-rakendus-v2 -p 8080:80 minu-app:v2
```

Värskendage brauserit - näete muudatusi!

---

# SAMM 3: Container'ite Haldamine

## Vaadake container'i sisemust

```bash
# Minge container'i sisse
docker exec -it minu-rakendus-v2 sh

# Container'i sees:
ls /usr/share/nginx/html/
cat /usr/share/nginx/html/index.html
exit
```

## Vaadake logisid

```bash
docker logs minu-rakendus-v2
```

## Ressursside kasutus

```bash
docker stats minu-rakendus-v2 --no-stream
```

---

# SAMM 4: Mitme Container'i Võrgustik

## Miks on võrgustik oluline?

Päris rakendused koosnevad tavaliselt mitmest osast:
- **Frontend** (veebileht)
- **Backend** (API server)  
- **Database** (andmebaas)
- **Cache** (Redis)

Need peavad omavahel suhtlema turvaliselt.

## Docker Network'ide tüübid

**Bridge network (default):**
- Container'id saavad omavahel suhelda
- Isoleeritud väline internetist
- Host'i jaoks juurdepääsetav port mapping'uga

**Host network:**
- Container kasutab host'i võrku otse
- Kiirem, aga vähem turvaline

**None network:**
- Container'il pole võrguühendust
- Kasutatakse turvalistes rakendustes

## Looge võrgustik

```bash
docker network create minu-network
```

**Mida see teeb:**
- Loob eraldatud võrgu
- Assign'ib IP vahemiku (nt 172.18.0.0/16)
- Seadistab DNS resolveri
- Container'id selles võrgus näevad üksteist

```bash
# Vaata võrke
docker network ls
```

**Tulemus:**
```
NETWORK ID     NAME           DRIVER    SCOPE
abc123def456   bridge         bridge    local
def456ghi789   host           host      local  
ghi789jkl012   none           null      local
jkl012mno345   minu-network   bridge    local
```

## Container'ite DNS

Docker'is toimib **automaatne DNS**:
- Container'i nimi = DNS hostname
- `ping web1` töötab, kui mõlemad on samas network'is
- Ei pea IP adresse meelde jätma!

## Käivitage mitu container'it

```bash
# Esimene container
docker run -d --name web1 --network minu-network nginx:alpine

# Teine container  
docker run -d --name web2 --network minu-network nginx:alpine
```

## Testinge ühendust

```bash
# Esimesest teise
docker exec web1 ping -c 3 web2

# Teisest esimese
docker exec web2 ping -c 3 web1
```

Container'id saavad omavahel suhelda!

---

# SAMM 5: Andmete Säilitamine (Volumes)

## Container'ite probleem

Container'id on **ephemeral** (ajutised):
- Container kustutamisel kaovad kõik andmed
- Restart'imisel failid nullitakse
- Database andmed lähevad kaduma!

**Näide probleem:**
```bash
# Käivita database
docker run -d --name db postgres
# Lisa andmeid...
docker stop db && docker rm db
# ❌ Kõik andmed kadunud!
```

## Volume'ide tüübid

**1. Named volumes (soovitatav produktsioonis):**
- Docker haldab volume'i asukohta
- Automaatne backup ja restore
- Jagamine container'ite vahel

**2. Bind mounts (arenduseks):**
- Host'i kaust → Container'i kaust
- Muudatused host'is on kohe container'is nähtavad
- Live reload development

**3. tmpfs mounts:**
- Salvestab RAM'is
- Kiire, aga kaob restart'imisel
- Cache jaoks

## Named Volume näide

Named volume on nagu "ämbrik" millel on nimi, kuhu saab asju hoida.

## Looge volume

```bash
docker volume create minu-andmed
```

**Mida see teeb:**
- Loob nimega volume'i
- Docker salvestab `/var/lib/docker/volumes/minu-andmed/`
- Volume eksisteerib iseseisvalt container'itest

```bash
# Vaata volume'eid
docker volume ls

# Volume detailid
docker volume inspect minu-andmed
```

## Volume lifecycle

```
1. Create volume → docker volume create mydata
2. Mount to container → -v mydata:/data  
3. Container writes data → echo "hello" > /data/file.txt
4. Container dies → docker rm container
5. Volume persists → data is still there!
6. New container mounts → -v mydata:/data
7. Data is restored → cat /data/file.txt shows "hello"
```

## Kasutage volume'i

```bash
docker run -d --name data-container \
    -v minu-andmed:/data \
    alpine sleep 3600
```

## Lisage andmeid

```bash
docker exec data-container sh -c 'echo "See on püsiv fail" > /data/test.txt'
```

## Kustutage container

```bash
docker stop data-container
docker rm data-container
```

## Looge uus container sama volume'iga

```bash
docker run -d --name uus-container \
    -v minu-andmed:/data \
    alpine sleep 3600
```

## Kontrollige andmeid

```bash
docker exec uus-container cat /data/test.txt
```

Andmed on alles! Volume säilitas need.

---

# Kokkuvõte ja Süvendamine

## Mida te täna õppisite:

### 1. Docker'i eelised
- **Kiirus:** Container'id käivituvad sekundiga
- **Portable:** Töötab ühesuguselt kõikjal
- **Isoleeritud:** Iga rakendus omaette "kastis"
- **Efficient:** Jagab OS kernel'i

### 2. Põhimõisted
- **Image:** Template/retsept rakenduse jaoks
- **Container:** Töötav instantsi image'ist  
- **Registry:** Image'ide ladu (Docker Hub)
- **Dockerfile:** Juhised image'i ehitamiseks

### 3. Lifecycle
```
1. Write Dockerfile
2. Build image (docker build)
3. Run container (docker run)
4. Stop container (docker stop)
5. Remove container (docker rm)
```

### 4. Essential Docker commands

**Image'id:**
```bash
docker build -t myapp .          # Ehita image
docker images                    # Vaata image'eid
docker rmi myapp                 # Kustuta image
docker pull nginx                # Lae image Docker Hub'ist
```

**Container'id:**
```bash
docker run -d -p 8080:80 nginx   # Käivita container
docker ps                        # Vaata töötavaid
docker ps -a                     # Vaata kõiki
docker stop container-name       # Peata
docker rm container-name         # Kustuta
docker logs container-name       # Vaata loge
docker exec -it container sh     # Mine sisse
```

**Networks:**
```bash
docker network create mynet      # Loo network
docker network ls                # Vaata võrke
docker run --network mynet app   # Kasuta network'i
```

**Volumes:**
```bash
docker volume create mydata      # Loo volume
docker volume ls                 # Vaata volume'eid
docker run -v mydata:/data app   # Mount volume
```

### 5. Troubleshooting

**Container ei käivitu:**
```bash
docker logs container-name       # Vaata error'eid
docker exec -it container sh     # Mine sisse uurima
```

**Port ei ole kättesaadav:**
- Kontrolli port mapping'u: `-p 8080:80`
- Kontrolli firewall'i
- Proovi: `curl localhost:8080`

**Image ei builde:**
- Kontrolli Dockerfile süntaksit
- Vaata error message'i tähelepanelikult
- Kontrolli failide olemasolu

## Praktilised kasutusviisid

### Development Environment
```bash
# Python arenduskeskkond
docker run -it -v $(pwd):/workspace python:3.9 bash

# Node.js live reload
docker run -d -v $(pwd):/app -p 3000:3000 node:16-alpine npm start
```

### Database Development
```bash
# PostgreSQL andmebaas
docker run -d --name devdb \
  -e POSTGRES_PASSWORD=secret \
  -v db-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

# MySQL andmebaas  
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8
```

### Web Development Stack
```bash
# Nginx + Redis + PostgreSQL
docker network create webapp
docker run -d --name redis --network webapp redis:alpine
docker run -d --name db --network webapp -e POSTGRES_PASSWORD=secret postgres:13
docker run -d --name web --network webapp -p 80:80 nginx:alpine
```

## Docker vs Traditsioonilised lahendused

| Aspekt | Traditional | Docker |
|--------|-------------|---------|
| **Setup Time** | Hours/Days | Minutes |
| **Consistency** | "Works on my machine" | Works everywhere |
| **Resource Usage** | High (full VMs) | Low (shared kernel) |
| **Startup Time** | 30-60 seconds | 1-3 seconds |
| **Deployment** | Complex scripts | Single command |
| **Scaling** | Manual server setup | Container orchestration |

## Industry adoption

**Wh uses Docker:**
- **Netflix:** 1+ billion containers per week
- **Spotify:** Entire infrastructure containerized  
- **Uber:** Microservices architecture
- **Airbnb:** 50% cost reduction
- **PayPal:** Faster deployments

**Statistics:**
- 83% of enterprises use containers (2024)
- 30x faster deployment cycles
- 50% reduction in infrastructure costs

## Puhastus

```bash
# Peatage kõik container'id
docker stop $(docker ps -q)

# Kustutage kõik container'id
docker rm $(docker ps -aq)

# Vaadake mis jäi alles
docker images
```

---

## Järgmised Sammud

### 1. Docker Compose
Mitme container'i haldamine ühes failis:
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "80:80"
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: secret
```

### 2. Container Orchestration
- **Docker Swarm:** Built-in clustering
- **Kubernetes:** Industry standard orchestrator
- **Nomad:** HashiCorp's orchestrator

### 3. CI/CD Integration
- GitHub Actions + Docker
- GitLab CI + Container Registry
- Jenkins pipelines

### 4. Production Considerations
- Security scanning (Trivy, Clair)
- Resource limits and monitoring
- Logging and observability
- Multi-stage builds for optimization

### 5. Alternative Container Runtimes
- **Podman:** Daemonless, rootless
- **containerd:** Low-level runtime
- **CRI-O:** Kubernetes focused

---

## BONUS HARJUTUSED

### Bonus 1: Multi-stage Build

**Probleem:** Node.js rakenduse image on suur (800MB) sest sisaldab build tools'e.

**Lahendus:** Multi-stage build

```bash
# Loo package.json
cat > package.json << 'EOF'
{
  "name": "myapp",
  "scripts": {
    "build": "echo 'Building app...' && mkdir -p dist && echo '<h1>Built App</h1>' > dist/index.html"
  }
}
EOF

# Multi-stage Dockerfile
cat > Dockerfile.multi << 'EOF'
# Build stage
FROM node:16 AS builder
WORKDIR /app
COPY package.json .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EOF

# Build ja võrdle suurusi
docker build -f Dockerfile.multi -t optimized-app .
docker images | grep optimized-app
```

### Bonus 2: Health Checks

```bash
# Dockerfile with health check
cat > Dockerfile.health << 'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1
EOF

docker build -f Dockerfile.health -t healthy-app .
docker run -d --name health-test healthy-app

# Vaata health status
docker ps  # HEALTH column
docker inspect health-test | grep Health -A 10
```

### Bonus 3: Environment Variables

```bash
# Muudetav rakendus
cat > index-template.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>{{TITLE}}</title></head>
<body>
    <h1>{{HEADING}}</h1>
    <p>Environment: {{ENV}}</p>
</body>
</html>
EOF

cat > Dockerfile.env << 'EOF'
FROM nginx:alpine
COPY index-template.html /tmp/
RUN apk add --no-cache envsubst
ENV TITLE="Default Title"
ENV HEADING="Default Heading"  
ENV ENV="development"
CMD envsubst < /tmp/index-template.html > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'
EOF

# Build ja testi erinevate ENV'idega
docker build -f Dockerfile.env -t env-app .

docker run -d -p 8081:80 \
  -e TITLE="Production App" \
  -e HEADING="Live System" \
  -e ENV="production" \
  env-app

docker run -d -p 8082:80 \
  -e TITLE="Test App" \
  -e HEADING="Testing" \
  -e ENV="testing" \
  env-app

# Testi mõlemat
curl localhost:8081
curl localhost:8082
```

### Bonus 4: Docker Registry

```bash
# Tag your image for registry
docker tag minu-app localhost:5000/minu-app:v1.0

# Run local registry
docker run -d -p 5000:5000 --name registry registry:2

# Push to registry
docker push localhost:5000/minu-app:v1.0

# Pull from registry (simulate different machine)
docker rmi minu-app localhost:5000/minu-app:v1.0
docker pull localhost:5000/minu-app:v1.0
```

### Bonus 5: Container Performance

```bash
# Resource-limited container
docker run -d --name limited \
  --memory="256m" \
  --cpus="0.5" \
  -p 8083:80 \
  nginx:alpine

# Monitor performance
docker stats limited

# Stress test
docker exec limited sh -c 'dd if=/dev/zero of=/tmp/test bs=1M count=300'
```

---

## Edasine Õpe

### Raamatud
- "Docker Deep Dive" by Nigel Poulton
- "Docker in Action" by Jeff Nickoloff
- "Kubernetes in Action" by Marko Lukša

### Online Kursused
- Docker Official Documentation
- Kubernetes Academy
- Cloud Provider tutorials (AWS, Azure, GCP)

### Praktilised projektid
1. **3-tier web app:** Frontend + API + Database
2. **Microservices:** Multiple APIs with service discovery
3. **CI/CD pipeline:** GitHub → Docker → Production
4. **Monitoring stack:** Prometheus + Grafana + containers

### Sertifikaadid
- Docker Certified Associate (DCA)
- Certified Kubernetes Administrator (CKA)
- Cloud provider certifications

---

**Palju õnne!** 🎉 

Te olete edukalt läbinud Docker fundamentals lab'i ja olete valmis järgmiseks tasemeks!
