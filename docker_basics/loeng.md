#  Docker: Konteinerite Põhitõed

**Teemad:** Container vs VM, Docker põhikäsud, Dockerfile, volumes, best practices

---

##  Õpiväljundid

Pärast seda moodulit oskate:
- Selgitada, mis probleemi Docker lahendab ja miks see on parem kui VM
- Käivitada ja hallata Docker container'eid (`run`, `ps`, `logs`, `exec`)
- Kirjutada Dockerfile'i ja ehitada image'e
- Kasutada volume'e andmete säilitamiseks ja port mapping'u
- Rakendada põhilisi best practices'eid (`.dockerignore`, cache, väiksemad image'd)

---

## 1. Miks Docker?

### Probleem enne Dockerit

#### "Works on My Machine" sündroom
```bash
Arendaja: "Mul töötab!"
Testija: "Mul crashib..."
DevOps: "Serveris error..."
Klient: "Miks ei tööta?!"
```

**Näide:** Python rakendus
- Arendaja: Python 3.8 + Ubuntu 20.04
- Server: Python 3.6 + CentOS 7  
- Tulemus:  Dependency conflict

See probleem tekkis, sest rakendused sõltusid oma ümbritsevast keskkonnast rohkem kui arvasime. Isegi väike erinevus Python versioonis või operatsioonisüsteemi teekides võis põhjustada raskesti jälgitavaid vigu. Arendajad kulutasid tunde keskkondade sünkroniseerimisele, kuid serverid olid ikkagi erinevad.

#### Kuidas lahendati varem?

**1. Virtuaalmasinad (2000-2010)**
```
 Aeglased (30s+ käivitus)
 Ressursinõudlikud (GB RAM per VM)
 Keerulised haldada
```

Virtuaalmasinad lahendas küll keskkonna probleemi, kuid lõi uued väljakutsed. Iga VM sisaldas tervet operatsioonisüsteemi, mis tähendas, et iga rakendus vajas gigabaite ruumi ja mällu. Serverisse mahus ainult 5-10 VM'i, mis piiras skaleeritavust.

**2. Configuration Management (2010-2015)**
```bash
# Puppet/Ansible
- package: python3.8
- service: nginx
- config: /etc/nginx/nginx.conf
```
```
 Drift (serverid muutuvad aja jooksul)
 Keeruline debugida
 Snowflake serverid
```

Configuration management tööriistad automaatsesid serveri seadistamise, kuid ei lahendanud põhiprobleemi. Serverid muutusid ikkagi aja jooksul - keegi käivitas käsu käsitsi, uuendused muutsid süsteemiteeke, või logifailid täitsid ketta. Iga server muutus unikaalseks "lumehelbekeseks" (snowflake), mida oli võimatu täpselt kopeerida.

### Docker'i revolutsioon (2013)

#### Konteinerite idee

```mermaid
graph TB
    subgraph "Host OS (Linux)"
        Docker[Docker Engine]
        C1[ Container 1<br/>Python app]
        C2[ Container 2<br/>Node.js app]
        C3[ Container 3<br/>Database]
        C4[ Container 4<br/>Redis]
        
        Docker --> C1
        Docker --> C2
        Docker --> C3
        Docker --> C4
    end
    
    style Docker fill:#2496ed,color:#fff
    style C1 fill:#f0f0f0
    style C2 fill:#f0f0f0
    style C3 fill:#f0f0f0
    style C4 fill:#f0f0f0
```

Docker tõi revolutsiooni, kasutades Linuxi kernel'i olemasolevaid võimalusi (namespaces, cgroups) uudsel viisil. Erinevalt VM'dest ei sisalda konteinerid tervet operatsioonisüsteemi - nad jagavad host'i kernel'it, kuid on ikkagi isoleeritud. See tähendab, et konteinerid käivituvad sekundite, mitte minutitega, ja nõuavad megabaite, mitte gigabaite.

#### Peamised eelised
1. **Kiirus:** 1-2 sekundit käivituseks
2. **Ressursid:** MB mitte GB  
3. **Portability:** Töötab kõikjal
4. **Consistency:** Sama käitumine kõikjal

Portability tähendab päriselt "kõikjal" - sama container töötab teie arendaja laptopil, CI/CD serveris, test keskkonnas, ja produktsiooni Kubernetes cluster'is. Kui container käivitub ühes kohas, siis ta käivitub igas kohas. See elimineerib "works on my machine" probleemi täielikult.

#### Numbrites
```
Traditional VM    vs    Docker Container
├── 30-120s startup    ├── 1-5s startup
├── 1-8GB RAM         ├── 10-100MB RAM  
├── 10-50 per server  ├── 100-1000 per server
└── 10-50GB disk      └── 100MB-1GB disk
```

Need numbrid ei ole teoreetilised - need on reaalse maailma statistika. Näiteks tüüpiline Node.js rakendus VM'is võtab 2GB RAM'i ja 45 sekundit käivituseks. Sama rakendus containeris võtab 50MB RAM'i ja 2 sekundit. See erinevus tähendab, et ühte serverisse mahub 50x rohkem containereid kui VM'e.

### Kasutusstatistika
- **87%** ettevõtetest kasutab konteinereid (2024)
- **Netflix:** 1 miljardit konteinerit nädalas
- **Google:** 2 miljardit konteinerit nädalas

Google on tegelikult kasutanud konteinereid (nende sisesüsteemis nimega Borg) juba 2000ndate algusest. Docker populariseeris seda tehnoloogiat massidele. Netflix'i ja Google'i numbrid näitavad reaalset skaala - need ettevõtted ei käivitaks miljardeid konteinereid, kui see ei oleks majanduslikult mõistlik.

---

## 2. Docker Install ja Esimesed Käsud

### Docker'i arhitektuur

```mermaid
graph TB
    subgraph "Docker Host"
        Client[Docker CLI]
        Daemon[Docker Daemon]
        Images[Images]
        Containers[Containers]
    end
    
    subgraph "External"
        Registry[Docker Hub Registry]
    end
    
    Client -->|commands| Daemon
    Daemon --> Images
    Daemon --> Containers
    Daemon <-->|pull/push| Registry
```

#### Komponendid
- **Docker CLI:** Kasutaja käsud
- **Docker Daemon:** Taustaprotsess (dockerd)  
- **Images:** Template'id rakenduste jaoks
- **Containers:** Töötavad instantsid
- **Registry:** Image'ide ladu (Docker Hub)

Docker kasutab client-server arhitektuuri. Kui te kirjutate `docker run`, siis CLI (client) saadab selle käsu daemonile (server) üle UNIX socket'i või HTTP API. Daemon teeb kogu töö - laeb image'd, loob konteineri, haldab võrku. See tähendab, et teoreetiliselt võite juhtida Dockerit remote serveris, käivitades CLI kohalikult - kuigi praktikas tehakse seda harva.

### Installation

**Ubuntu/Debian:**
```bash
# Automatic install script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker run hello-world
```

`usermod -aG docker` on oluline samm, mis võimaldab Dockerit kasutada ilma `sudo`ta. Ilma selleta peaksite iga käsu ees kirjutama `sudo docker`, mis on tüütu ja ebaturvaline (liiga palju õigusi). Docker grupp annab teile õiguse rääkida Docker daemoniga, mis jookseb root'ina.

**Windows/Mac:**
- **Docker Desktop:** https://www.docker.com/products/docker-desktop/
- GUI + Linux VM taustal

Windows ja Mac'is on Docker keerulisem, sest Docker vajab Linuxi kernel'it. Docker Desktop loob vaikse Linux VM'i taustal (kasutades WSL2 Windowsis või Hypervisor frameworki Mac'is) ja jooksutab Docker daemoni seal. Teile tundub, et kasutate Dockerit natiivselt, aga tegelikult töötavad konteinerid selles peidetud VM'is.

### Põhimõisted

```mermaid
graph LR
    Registry[ Registry<br/>Docker Hub]
    Image[ Image<br/>read-only template]
    Container[ Container<br/>running instance]
    
    Registry -->|docker pull| Image
    Image -->|docker run| Container
    Container -->|docker commit| Image
    Image -->|docker push| Registry
    
    style Registry fill:#0db7ed,color:#fff
    style Image fill:#384d54,color:#fff
    style Container fill:#2496ed,color:#fff
```

**1. Image**
- **Read-only template** 
- Sisaldab: OS + runtime + dependencies + rakendus
- **Immutable** (ei muutu)

Image on nagu klass objektorienteeritud programmeerimises - see on blueprint, mille põhjal luuakse konteinereid. Kui te laasite `nginx` image, siis te ei saa seda image'i muuta - see on lukus. Kui soovite muudatusi teha, peate looma uue image.

**2. Container**
- **Running instance** image'ist
- **Writable layer** image'i peal
- **Isolated process**

Container on nagu objekti instantsi - image'ist loodud töötav koopia. Iga container saab oma writable layer'i, kuhu ta saab kirjutada faile, kuid see ei mõjuta image'i ennast. Kui kustutate konteineri, kaob ka see writable layer - seega andmed peavad olema volume'ides, kui te tahate neid säilitada.

**3. Registry**
- **Repository** image'ide jaoks
- **Docker Hub:** avalik registry
- **Private registries:** ettevõtte sisesed

Registry on nagu Git repository, ainult image'ide jaoks. Docker Hub on nagu GitHub - avalik koht, kust igaüks saab image'id alla laadida. Ettevõtted kasutavad sageli private registry'sid (nagu AWS ECR või GitLab Container Registry), et hoida oma image'd turvaliselt ja privaatselt.

### DEMO: Esimesed käsud

**Image operations:**
```bash
# Search images
docker search nginx
docker search python --filter stars=100

# Pull image  
docker pull nginx
docker pull nginx:alpine  # specific tag

# List local images
docker images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Inspect image
docker image inspect nginx
docker image history nginx  # layer history
```

`docker pull` laeb image'i Docker Hub'ist teie kohalikku masinasse. Tag'id (nagu `alpine`) määravad konkreetse versiooni - kui te ei määra tag'i, siis kasutatakse `latest`. `inspect` näitab image'i metaandmeid JSON formaadis, sealhulgas environment variable'id, exposed porte, ja entry point'i.

**Container operations:**
```bash
# Run container (foreground)
docker run nginx

# Run in background
docker run -d nginx

# Run with port mapping
docker run -d -p 8080:80 nginx

# Run with name
docker run -d -p 8080:80 --name minu-nginx nginx

# List running containers
docker ps

# List all containers
docker ps -a

# View logs
docker logs minu-nginx
docker logs -f minu-nginx  # follow

# Execute command in container
docker exec minu-nginx ls /etc/nginx
docker exec -it minu-nginx bash  # interactive

# Stop container
docker stop minu-nginx

# Remove container
docker rm minu-nginx

# Remove image
docker rmi nginx
```

`-d` (detached) on kõige sagedamini kasutatav flag - see paneb konteineri käivituma taustal. Ilma selleta jääb terminal kinni konteineri output'i. Port mapping `-p 8080:80` tähendab "suuna host'i port 8080 konteineri port 80 peale" - nüüd saate avada brauseris `http://localhost:8080` ja näete nginx'i.

`docker exec -it` on debug'imise jaoks hädavajalik. `-i` (interactive) hoiab STDIN lahti, `-t` (tty) loob pseudo-terminali. Koos võimaldavad need teil käivitada bash'i konteineris ja uurida, mis seal toimub.

**Cleanup commands:**
```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove everything unused
docker system prune

# See disk usage
docker system df
```

Docker kogub prügi kiiresti - peatatud konteinereid, kasutamata image'id, orphaned volume'id. `prune` käsud kustutavad kõik, mis ei ole aktiivselt kasutuses. Hea tava on käivitada `docker system prune` regulaarselt, et vabastada kettaruumi. `docker system df` näitab, kui palju ruumi erinevad Docker objektid võtavad.

---

## 3. Dockerfile ja Image'ide Loomine

### Dockerfile põhitõed

**Mis on Dockerfile?**
- **Text file** mis kirjeldab kuidas image ehitada
- **Layer-based:** iga käsk = uus layer
- **Cached:** korduvad layerid kasutatakse uuesti

```mermaid
graph TD
    DF[ Dockerfile]
    Build[docker build]
    L1[Layer 1: FROM ubuntu]
    L2[Layer 2: RUN apt-get update]
    L3[Layer 3: COPY app.py]
    L4[Layer 4: CMD python app.py]
    Image[ Final Image]
    
    DF --> Build
    Build --> L1
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> Image
    
    style DF fill:#f9f9f9
    style Build fill:#2496ed,color:#fff
    style L1 fill:#e8f4f8
    style L2 fill:#e8f4f8
    style L3 fill:#e8f4f8
    style L4 fill:#e8f4f8
    style Image fill:#384d54,color:#fff
```

Layer-based süsteem on Docker'i geniaalsus. Iga käsk Dockerfile'is loob uue layer'i, mis on read-only. Kui ehitate image'i uuesti ja mõni layer ei ole muutunud, siis Docker kasutab cache'ist vana layer'i. See tähendab, et teine build võtab sekundeid, mitte minuteid - Docker ei pea tegema tööd, mida ta juba on teinud.

**Dockerfile süntaks:**
```dockerfile
# Comment
INSTRUCTION arguments
```

Dockerfile kasutab lihtsat süntaksit - iga rida on instruction (suur tähtedega) ja selle argumendid. Instruction'id käivitatakse ülalt alla järjekorras. Kui üks instruction ebaõnnestub, siis build peatub ja te näete viga.

### Dockerfile instruction'id

**FROM - alus image:**
```dockerfile
FROM ubuntu:20.04          # specific version
FROM python:3.9-alpine     # smaller base  
FROM scratch               # empty base
```

`FROM` peab alati olema esimene instruction. See määrab, milliselt base image'ilt te alustate. Alpine image'd on palju väiksemad (5MB vs 100MB Ubuntu puhul), aga neil on vähem tööriistu installitud - valige sõltuvalt vajadusest.

**WORKDIR - töökaust:**
```dockerfile
WORKDIR /app
# Equivalent to: mkdir -p /app && cd /app
```

**COPY vs ADD:**
```dockerfile
# COPY - lihtne faili kopeerimine
COPY src/ /app/src/
COPY requirements.txt .

# ADD - extended features (avoid!)
ADD https://example.com/file.tar.gz /app/  # downloads
ADD archive.tar.gz /app/                   # auto-extracts
```

Kasutage alati `COPY`, mitte `ADD`. `ADD` teeb liiga palju "maagilist" - ta ekstraktib automaatselt archive'e ja saab laadida URL'e. See teeb Dockerfile'i raskemini ennustatavaks. `COPY` teeb täpselt seda, mida te eeldate.

**RUN - käsu käivitamine:**
```dockerfile
# Separate commands (bad)
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y pip

# Combined (good)
RUN apt-get update && \
    apt-get install -y python3 pip && \
    rm -rf /var/lib/apt/lists/*
```

Iga `RUN` loob uue layer'i. Kolm eraldi `RUN` käsku = kolm layer'it = suurem image. Kombineerige käsud `&&` ja `\` abil ühte `RUN` käsku. Kustutage ka apt cache (`rm -rf /var/lib/apt/lists/*`), et vähendada image suurust.

**ENV - environment variables:**
```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
ENV DATABASE_URL=postgresql://user:pass@db:5432/mydb
```

**EXPOSE - dokumentatsioon:**
```dockerfile
EXPOSE 8080
# Doesn't actually publish port - just documentation
```

`EXPOSE` ei avalikusta tegelikult porti - see on ainult dokumentatsioon. Portide avaldamiseks kasutage `docker run -p`. Aga `EXPOSE` on ikkagi kasulik, sest see ütleb teistele, milliseid porte rakendus kasutab.

**USER - security:**
```dockerfile
# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001

USER appuser
```

Vaikimisi jooksevad konteinerid root kasutajana, mis on turvarisk. Looge spetsiaalne kasutaja ja lülituge sellele enne `CMD`. Kui keegi suudab teie containerisse sisse murda, siis tal ei ole root õigusi.

**CMD vs ENTRYPOINT:**
```dockerfile
# CMD - default command (can be overridden)
CMD ["python", "app.py"]

# ENTRYPOINT - always runs
ENTRYPOINT ["python", "app.py"]

# Combined usage
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]
```

`CMD` saab kasutaja `docker run` käsuga üle kirjutada. `ENTRYPOINT` käivitub alati. Kasutage neid koos: `ENTRYPOINT` põhikäsule, `CMD` default argumentidele.

### DEMO: Dockerfile loomine

**Lihtne Python app:**

**app.py:**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Docker!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**requirements.txt:**
```
Flask==2.3.3
```

**Algaja Dockerfile (kehv):**
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python app.py
```

**Probleemid:**
-  Ei kasuta cache'i optimaalselt
-  Suur base image
-  Runs as root
-  No health check

**Optimeeritud Dockerfile (hea):**
```dockerfile
FROM python:3.9-alpine

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001

WORKDIR /app

# Copy dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

EXPOSE 5000

CMD ["python", "app.py"]
```

Optimeeritud versioon kasutab Alpine'd (väiksem), loob non-root kasutaja, kopeerib `requirements.txt` enne koodi (parem cache), ja lisab health check'i. `requirements.txt` kopeeritakse esimesena, sest see muutub harvemini kui kood - nii Docker saab cache'ida pip install sammu.

**Build ja käivitamine:**
```bash
# Build image
docker build -t minu-python-app .

# Run container
docker run -d -p 5000:5000 --name python-app minu-python-app

# Test
curl http://localhost:5000

# View health status
docker ps  # shows health status
```

### Multi-stage build näide

```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runtime stage  
FROM nginx:alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Eelised:**
-  Väiksem final image (ainult runtime)
-  Turvalisem (no build tools)
-  Kiirem deployment

Multi-stage build võimaldab eraldada build keskkonda runtime'ist. Esimeses stage'is on kõik build tools (kompileerid, webpack, jne), teises stage'is ainult runtime (nginx). Final image sisaldab ainult teise stage'i, seega on palju väiksem ja turvalisem.

---

## 4. Volumes, Networks ja Docker Compose

### Volumes - andmete säilitamine

**Probleem:**
```bash
docker run -d --name db postgres
docker exec db createdb myapp
docker stop db
docker rm db

#  Kõik andmed kadunud!
```

Vaikimisi kaovad konteineri andmed, kui container kustutatakse. Container'i writable layer on ajutine - see on disainitud nii. Püsivate andmete jaoks vajate volume'id.

**Volume tüübid:**

**1. Anonymous volumes:**
```bash
docker run -d -v /var/lib/postgresql/data postgres
# Docker loob automaatselt volume'i
```

**2. Named volumes:**
```bash
# Create volume
docker volume create postgres_data

# Use volume
docker run -d -v postgres_data:/var/lib/postgresql/data postgres

# List volumes
docker volume ls

# Inspect volume
docker volume inspect postgres_data
```

Named volumes on soovitatud tootmiseks. Docker haldab neid ja te saate neid kergesti varundada. Volume'i andmed jäävad alles ka pärast konteineri kustutamist - peate selle käsitsi kustutama `docker volume rm`.

**3. Bind mounts:**
```bash
# Mount host directory
docker run -d -v /host/path:/container/path nginx

# Development example
docker run -d -v $(pwd):/app -p 3000:3000 node:16-alpine
```

Bind mount'id on ideaalsed arenduseks. Muudate faili host'is, muudatus on kohe containeris nähtav - ei pea image'i uuesti ehitama. Aga produktsioonis kasutage named volume'id, sest bind mount'id on host'i failisüsteemist sõltuvad.

**4. tmpfs mounts (memory):**
```bash
docker run -d --tmpfs /tmp nginx
# Data stored in RAM, lost on container stop
```

### Volume'ide võrdlus

| Type | Performance | Portability | Use Case |
|------|-------------|-------------|----------|
| **Named Volume** | ⭐⭐⭐ | ⭐⭐⭐ | Production data |
| **Bind Mount** | ⭐⭐ | ⭐ | Development |  
| **tmpfs** | ⭐⭐⭐ | ⭐⭐⭐ | Temporary cache |

### Networks - konteinerite suhtlus

**Default behavior:**
```bash
# Containers can't communicate by default
docker run -d --name web nginx
docker run -d --name app python:3.9-alpine

docker exec app ping web  #  Fails!
```

Vaikimisi on konteinerid isoleeritud ega näe üksteist. See on turvalisuse mõttes hea, aga te peate lubama suhtlust custom network'i abil.

**Custom networks:**
```bash
# Create network
docker network create myapp-network

# Run containers in same network
docker run -d --name web --network myapp-network nginx
docker run -d --name app --network myapp-network python:3.9-alpine

# Now they can communicate!
docker exec app ping web  #  Works!
docker exec app nslookup web  # DNS resolution
```

Custom network annab konteineritele automaatse DNS resolution'i. Container'i `web` on kättesaadav hostname'iga `web` - Docker loob selle DNS entry automaatselt. Te ei pea IP aadresse teadma.

**Network types:**

**1. Bridge (default):**
```bash
docker network create --driver bridge mybridge
# Isolated network with internet access
```

**2. Host:**
```bash
docker run --network host nginx
# Uses host networking directly
```

Host network eemaldab võrgu isolatsiooni täielikult - container kasutab host'i võrku otse. See on kõige kiirem, aga vähim turvaline. Kasutage ainult kui peate.

**3. None:**
```bash
docker run --network none alpine
# No networking
```

**Port publishing vs network:**
```bash
# Port publishing (external access)
docker run -p 8080:80 nginx

# Internal communication (no ports needed)
docker network create app-net
docker run --network app-net --name web nginx
docker run --network app-net --name app alpine
# app can reach web:80 directly
```

Port publishing (`-p`) on **välise** ligipääsu jaoks - brauserid, API kliendid. Internal communication vajab ainult custom network'i - konteinerid saavad otse üksteisega rääkida ilma porte publishimata.

### DEMO: Multi-container rakendus

**Architecture:**
```
Frontend (nginx) → Backend (Flask) → Database (PostgreSQL)
```

**Manual setup:**
```bash
# 1. Create network
docker network create webapp-net

# 2. Database
docker run -d \
  --name postgres \
  --network webapp-net \
  -e POSTGRES_DB=webapp \
  -e POSTGRES_USER=app \
  -e POSTGRES_PASSWORD=secret \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:13-alpine

# 3. Backend
docker run -d \
  --name backend \
  --network webapp-net \
  -e DATABASE_URL=postgresql://app:secret@postgres:5432/webapp \
  python:3.9-alpine

# 4. Frontend  
docker run -d \
  --name frontend \
  --network webapp-net \
  -p 80:80 \
  nginx:alpine
```

**Probleem:** Palju käske, keeruline hallata!

### Docker Compose

**Mis on Docker Compose?**
- **Tool** mitme konteineri haldamiseks
- **YAML file** konfiguratsiooniks
- **Single command** kogu stack'i haldamiseks

Docker Compose võtab need kümme `docker run` käsku ja paneb need ühte YAML faili. Seejärel käivitate kogu stack'i ühe käsuga: `docker-compose up`.

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: webapp
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  # Backend API
  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://app:secret@postgres:5432/webapp
    depends_on:
      - postgres
    networks:
      - backend
      - frontend

  # Frontend  
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
    networks:
      - frontend

# Define networks
networks:
  frontend:
  backend:

# Define volumes  
volumes:
  postgres_data:
```

`depends_on` ütleb Docker Compose'ile, millises järjekorras konteinereid käivitada. Aga tähtis detail: see ei oota, kuni teenus on **valmis**, ainult et container on **käivitatud**. Andmebaas võib võtta mõne sekundi enne valmis olemist.

**Compose käsud:**
```bash
# Start all services
docker-compose up -d

# View running services
docker-compose ps

# View logs
docker-compose logs
docker-compose logs backend

# Scale service
docker-compose up -d --scale backend=3

# Stop all
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

`docker-compose down -v` on ohtlik - see kustutab ka volume'd ehk **kõik andmed**. Kasutage ainult arenduses, mitte produktsioonis.

**Environment files:**

**.env:**
```bash
POSTGRES_PASSWORD=supersecret
DATABASE_URL=postgresql://app:${POSTGRES_PASSWORD}@postgres:5432/webapp
NODE_ENV=production
```

**docker-compose.yml:**
```yaml
services:
  postgres:
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

`.env` fail hoiab tundlikku infot väljaspool docker-compose.yml. Lisage `.env` faili `.gitignore` - ei tohi kunagi commitida paroole Git'i.

---

## 5. Produktsiooni Parimad Praktikad

### Security Best Practices

**1. Non-root user:**
```dockerfile
# BAD
USER root
CMD ["python", "app.py"]

# GOOD  
RUN adduser -D -s /bin/sh appuser
USER appuser
CMD ["python", "app.py"]
```

**2. Minimal base images:**
```dockerfile
# BAD - 1GB
FROM ubuntu:latest

# GOOD - 50MB
FROM python:3.9-alpine

# BETTER - 15MB (multi-stage)
FROM python:3.9-alpine AS builder
# ... build steps
FROM alpine:latest
COPY --from=builder /app /app
```

**3. No secrets in images:**
```dockerfile
# BAD
ENV API_KEY=secret123

# GOOD
ENV API_KEY_FILE=/run/secrets/api_key
```

Secrets kuuluvad Docker secrets või vault'i, mitte image'sse. Kui panete secrets ENV'i, siis need salvestatakse image'sse igaveseks - isegi kui kustutate selle rea hiljem, on see image history'st leitav.

**4. Specific versions:**
```dockerfile
# BAD
FROM python:latest

# GOOD
FROM python:3.9.18-alpine3.18
```

`latest` tag on nebulous - see võib tähendada erinevat versiooni järgmisel kuul. Kasutage konkreetseid versioone, et vältida üllatusi.

**5. Security Scanning (Trivy):**

Security scanning leiab haavatavused (vulnerabilities) image'itest. Trivy on populaarne, tasuta security scanner Docker image'itele.

**Trivy installimine ja kasutamine:**
```bash
# Installi Trivy
sudo apt install wget
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt update
sudo apt install trivy

# Skanni image
trivy image nginx:latest

# Näita ainult HIGH ja CRITICAL
trivy image --severity HIGH,CRITICAL python:3.9

# Skanni kohaliku Dockerfile
docker build -t myapp:test .
trivy image myapp:test
```

**Näide väljund:**
```
Total: 45 (HIGH: 8, CRITICAL: 2)

┌────────────┬──────────────┬──────────┬────────┬─────────────────┐
│  Library   │ Vulnerability│ Severity │ Status │    Title        │
├────────────┼──────────────┼──────────┼────────┼─────────────────┤
│ openssl    │ CVE-2023-123 │ CRITICAL │  fixed │ Buffer overflow │
│ curl       │ CVE-2023-456 │ HIGH     │  fixed │ Auth bypass     │
└────────────┴──────────────┴──────────┴────────┴─────────────────┘
```

**Mida teha tulemustega?**

**1. Update base image:**
```dockerfile
FROM python:3.9.18-alpine3.18  # vanem versioon, haavatavused
↓
FROM python:3.11.7-alpine3.19  # uuem, turvalisem
```

**2. Update dependencies:**
```dockerfile
RUN pip install requests==2.28.0  # vanem, haavatav
↓
RUN pip install requests==2.31.0  # uuem, parandatud
```

**3. Accept risk** (kui ei saa parandada):
- Dokumenteeri, miks ei saa uuendada
- Lisa `.trivyignore` fail

**CI/CD integration:**
```yaml
# GitLab CI
security_scan:
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity CRITICAL myapp:latest
  # Failib kui CRITICAL haavatavusi leitakse
```

**Hea tava:**
-  Skanni image'd enne production'i
-  Automaatne scanning CI/CD's
-  Blokeeri CRITICAL vulnerabilities
-  Fix regulaarselt (mitte ainult release'i ajal)

### Performance Optimization

**1. Layer caching:**
```dockerfile
# BAD - cache miss on code change
COPY . /app
RUN pip install -r requirements.txt

# GOOD - dependencies cached
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
```

**2. .dockerignore:**
```
# .dockerignore
node_modules/
.git/
*.log
.DS_Store
```

`.dockerignore` töötab nagu `.gitignore` - see väldib tarbetute failide kopeerimist image'sse. `.git` kaust võib olla gigabaite suurune ja on image'is täiesti kasutu.

**3. Multi-stage builds:**

Multi-stage build võimaldab:
- Ehitada rakendust ühes stage'is (build tools)
- Käivitada teises stage'is (ainult runtime)
- Väiksemad image'id (100MB+ → 10MB)

See on juba käsitletud jaotises 3 - vaadake "Multi-stage build näide" seal.

### Monitoring ja Logging

**Health checks:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

Health check ütleb Docker'ile, kas rakendus tegelikult töötab. Container võib olla käivitatud, aga rakendus crashinud - health check avastab selle. Docker märgib konteineri "unhealthy" ja orchestraatorid (Docker Swarm, Kubernetes) saavad selle automaatselt restartida.

**Structured logging:**
```python
import logging
import json

def json_log(message, level="info", **kwargs):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
        **kwargs
    }
    print(json.dumps(log_entry))
```

JSON logid on masinloetavad - log aggregaatorid (nagu ELK stack) saavad neid kergelt parsida ja indekseerida. Plain text logid on inimestele loetavad, aga masinatele keerulised.

**Resource limits:**
```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          memory: 256M
```

Resource limit'id kaitsevad teisi konteinereid. Kui üks container läheb luupima ja proovib kogu CPU või RAM'i võtta, siis Docker piirab seda. Ilma limit'ideta võib üks halvasti kirjutatud rakendus kogu serveri maha võtta.

### Production deployment patterns

**1. Blue-Green deployment:**
```bash
# Current: myapp-blue (v1.0)
# Deploy: myapp-green (v2.0)

docker run -d --name myapp-green -p 8081:8080 myapp:v2.0

# Test v2.0 on port 8081
# Switch load balancer: 8080 → 8081  
# Remove blue: docker stop myapp-blue
```

Blue-green deployment võimaldab zero-downtime deploy'e. Käivitate uue versiooni paralleelselt vanaga, testite seda, seejärel lülitate load balanceri üle. Kui midagi läheb valesti, rollback on kiire - lülitate lihtsalt tagasi vanale versioonile.

**2. Rolling updates:**
```yaml
# docker-compose.yml
services:
  app:
    image: myapp:v2.0
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
```

**3. Configuration management:**
```yaml
# docker-compose.prod.yml
services:
  app:
    image: myapp:${VERSION}
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    secrets:
      - db_password
      - api_keys

secrets:
  db_password:
    external: true
  api_keys:
    external: true
```

Docker secrets on produktsiooni standard tundliku info jaoks. Need salvestatakse krüpteeritult ja mountitakse konteinerisse faili kujul - ei jää ENV'i ega image history'sse.

### Container orchestration tutvustus

**Docker Swarm:**
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml myapp

# Scale service  
docker service scale myapp_web=5
```

Docker Swarm on Docker'i sisseehitatud orchestrator. See haldab mitut hosti, load balancing'ut, rolling update'sid. Lihtsam kui Kubernetes, aga vähem võimalusi.

**Kubernetes alternative:**
```bash
# Generate Kubernetes YAML from Compose
kompose convert docker-compose.yml

# Or use Podman
podman generate kube mycontainer > pod.yaml
kubectl apply -f pod.yaml
```

Kubernetes on industry standard produktsioonis. Keerulisem kui Swarm, aga palju võimsam - self-healing, auto-scaling, complex networking. Kui teil on üle 10 serveri ja keeruline infrastruktuur, siis Kubernetes on investeeringu väärt.

---

##  Kokkuvõte ja Refleksioon

### Põhiline töövoog

```bash
# Iga päev:
docker pull image-nimi          # võta uusim image
docker run -d -p 8080:80 image  # käivita container
docker ps                       # vaata, mis töötab
docker logs container-nimi      # debugi
docker stop container-nimi      # peata

# Arendus:
# 1. Kirjuta Dockerfile
# 2. docker build -t minu-app .
# 3. docker run minu-app
# 4. Testi ja paranda
# 5. Korda 2-4
```

### Refleksioonküsimused

1. **Kuidas Docker lahendab "Works on My Machine" probleemi?**
2. **Millal kasutada volume'e ja millal mitte?**
3. **Miks on cache oluline Dockerfile build'imisel?**
4. **Kuidas container erineb VM'ist? Mis on peamised eelised?**
5. **Mida MITTE panna Dockerfile'i või image'isse?** (paroolid, logid, cache)

### Järgmised sammud

- **Labor:** Harjuta kõiki neid käske praktikas
- **Kodutöö:** Loo oma rakendus Docker container'is
- **Edasijõudnud:** Docker Compose, Docker Swarm, Kubernetes

### Ressursid ja lugemine

- **Docker dokumentatsioon:** https://docs.docker.com/
- **Docker Hub:** https://hub.docker.com/
- **Best practices guide:** https://docs.docker.com/develop/dev-best-practices/
- **Play with Docker** (brauseris): https://labs.play-with-docker.com/
- **Docker Cheat Sheet:** https://docs.docker.com/get-started/docker_cheatsheet.pdf