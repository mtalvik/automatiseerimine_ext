# Docker: Konteinerite Põhitõed

**Eeldused:** Linux CLI põhitõed, tekstiredaktor  
**Platvorm:** Platform-agnostic (Docker, Podman)

Loeng tutvustab konteinerite tehnoloogiat, Docker'i arhitektuuri ja kasutusvõimalusi professionaalses IT keskkonnas. Käsitleme Docker'i eeliseid võrreldes virtuaalmasinatega, image'ide ja container'ite loomist ning andmehaldust.

---

## Õpiväljundid

Pärast seda loengut mõistad:

- **Miks konteinerite tehnoloogia on vajalik**
- millist probleemi see lahendab
- **Kuidas Docker erineb VM'idest**
- arhitektuurilised erinevused ja mõju jõudlusele
- **Mis on image ja container**
- nende suhe ja elutsükkel
- **Kuidas Dockerfile töötab**
- image'ide loomine ja optimeerimise põhimõtted
- **Millal kasutada volume'e**
- andmete püsivus ja jagamine

---

## 1. Konteinerite Tehnoloogia Motiiv

### 1.1 Keskkondade Probleem

IT infrastruktuuris on alati eksisteerinud konfiguratsioonide lahknevus. Arendaja laptop sisaldab Pythoni versiooni 3.9 Ubuntu 20.04 peal, testimisserver kasutab Pythoni 3.7 CentOS'il, produktsioonikeskkond jooksutab Pythoni 3.10 Debian'il. Igaüks nendest keskkondadest sisaldab erinevaid süsteemiteeke, sõltuvusi ja seadistusi.

Tulemus on ennustatav: kood töötab ühes keskkonnas, ebaõnnestub teises. Arendajad kulutavad tunde keskkondade sünkroniseerimisele, DevOps meeskonnad haldavad keerukaid deployment skripte, testimine muutub ebausaldusväärseks.

### 1.2 Varasemad Lahendused

**Virtuaalmasinad** (2000-2010): Lahendas isolatsiooni probleemi, kuid hinnaga. Iga VM sisaldab täielikku operatsioonisüsteemi koopiat, mida haldab hypervisor. See tähendab gigabaitide jagu kettaruumi ja RAM'i igale rakendusele, koos 30-60 sekundilise käivitusajaga.

**Configuration Management** (2010-2015): Puppet, Ansible ja Chef automatiseerisid serveri seadistamise. Probleem püsib - serverid muutuvad aja jooksul, drift on vältimatu. Manuaalsed sekkumised, sõltuvuste uuendused ja logifailide kuhjumine muudavad iga serveri unikaalseks.

### 1.3 Docker'i Revolutsioon

Docker kasutas 2013. aastal Linux'i kernel'i olemasolevaid võimeid (namespaces, cgroups) uudsel viisil. Container'id jagavad host'i kernel'it, kuid on protsesside tasandil isoleeritud. See tähendab:

- **Käivitusaeg:** 1-3 sekundit
- **Mälukasutus:** 10-100 MB per container
- **Kettaruum:** 100 MB
- 1 GB
- **Server mahutab:** 100-1000 container'it

Võrdluseks: VM käivitub 30-60 sekundiga, vajab 1-8 GB RAM'i, serverisse mahub 10-50 VM'i.

### 1.4 Tööstuse Kasutusnäited

Netflix käivitab üle miljardi container'i nädalas. Google'i infrastruktuur on alates 2000. aastatest olnud container-põhine (Borg, Kubernetes). 87% IT ettevõtetest kasutab konteinereid produktsioonis 2024. aasta seisuga.

---

## 2. Docker Arhitektuur ja Mõisted

### 2.1 Client-Server Mudel

Docker kasutab client-server arhitektuuri. Docker CLI (client) suhtleb Docker daemoniga (dockerd) üle UNIX socket'i või HTTP API. Daemon haldab image'eid, container'eid, võrke ja volume'e.
```
[Docker CLI] --REST API--> [Docker Daemon] --> [Container Runtime]
                                |
                                +--> [Image Storage]
                                +--> [Volume Storage]
                                +--> [Network Driver]
```

### 2.2 Image

Image on read-only template, mis sisaldab operatsioonisüsteemi, runtime'i, sõltuvusi ja rakenduse koodi. Image on **immutable** - pärast loomist ei muutu. Iga muudatus loob uue image'i.

Image koosneb **layer'itest**. Iga Dockerfile käsk loob uue layer'i, mis salvestatakse overlay failisüsteemis. Layer'id on cacheable - kui Dockerfile'is ei muutu rida, kasutatakse vana layer'it cache'ist.

### 2.3 Container

Container on töötav instantsi image'ist. Container saab writable layer'i image'i peale, kuhu saab kirjutada ajutisi faile. Container isoleerib protsesse, võrku, failisüsteemi ja ressursse.

Container ei ole VM - see on isoleeritud protsess host OS'is. Container jagab kernel'it host'iga, seega ei saa Windowsi container'it käivitada Linux host'il ilma virtualisatsioonita.

### 2.4 Registry

Registry on image'ide ladu. **Docker Hub** on avalik registry, kust saab alla laadida tuhandeid valmis image'eid (nginx, postgres, python). Ettevõtted kasutavad private registry'sid (AWS ECR, GitLab Container Registry, Harbor).

Image'i täisnimi: `registry/namespace/repository:tag`
- Docker Hub: `nginx:alpine` (lühend `docker.io/library/nginx:alpine`)
- Private: `gcr.io/my-project/api-server:v1.2.3`

---

## 3. Docker vs Podman vs Virtuaalmasinad

### 3.1 Arhitektuuriline Võrdlus

| Kriteerium | Docker | Podman | VM (KVM/VMware) |
|------------|--------|--------|-----------------|
| Daemon | Vajab dockerd | Daemonless | Hypervisor |
| Õigused | Root privileegid | Rootless võimalik | Root + hypervisor |
| Networking | Bridge/overlay | Same | Virtual NIC |
| Image formaat | OCI | OCI | Disk image |
| Orchestration | Swarm/K8s | Kubernetes native | - |

**OCI** (Open Container Initiative) määratleb image ja runtime standardid. Podman ja Docker kasutavad sama formaati, seega `docker pull` image töötab `podman run` käsuga.

### 3.2 Millal Kasutada Mida

**Docker:** Laia tööstuslik toetus, küps ökosüsteem, Docker Compose standardne.

**Podman:** Turvalisem (rootless), ei vaja daemon'it, drop-in asendus Docker CLI'le, sobib hästi Kubernetes keskkondadesse.

**VM:** Erinev OS kernel (Windows container Linux host'il), range turvaisolatsioon, legacy rakendused.

---

## 4. Dockerfile ja Image'ide Loomine

### 4.1 Dockerfile Süntaks

Dockerfile on tekstifail käskudega image'i ehitamiseks:
```dockerfile
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

Peamised käsud:

**FROM:** Base image. Alusta olemasolevalt image'ilt.

**WORKDIR:** Töökataloogi määramine. Loob kataloogi kui puudub.

**COPY:** Kopeeri failid host'ist image'isse.

**RUN:** Käivita käsk build ajal. Loob uue layer'i.

**ENV:** Environment variable'id.

**EXPOSE:** Dokumentatsioon - milliseid porte rakendus kasutab.

**CMD:** Vaikimisi käsk container'i käivitamisel. Saab üle kirjutada.

**ENTRYPOINT:** Käsk mis alati käivitub. CMD lisab argumendid.

### 4.2 Build Protsess
```bash
docker build -t myapp:v1.0 .
```

Docker loeb Dockerfile'i, käivitab iga käsu järjest, salvestab iga sammu tulemusena layer'i. Layer'id salvestatakse `/var/lib/docker/overlay2/` all.

Cache'imine: kui layer ei ole muutunud, kasutab Docker vana layer'it. Seega `RUN apt-get update` käsk käivitatakse ainult siis, kui eelnevad read muutusid.

### 4.3 Multi-Stage Build

Suurte rakenduste puhul on build dependencies (kompileerimistarkvara, npm, maven) suuremad kui runtime vajadus. Multi-stage build eraldab need:
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/main.js"]
```

Tulemus: final image sisaldab ainult runtime'i ja kompileeritud koodi, mitte build tools'e. Image suurus väheneb 1.2GB → 150MB.

### 4.4 Image Optimeerimise Põhimõtted

**Vali väiksem base image:** `python:3.11-alpine` (50MB) vs `python:3.11` (900MB).

**Kombineeri RUN käsud:** Iga `RUN` loob layer'i. Kolm `RUN` käsku = kolm layer'it.

**Järjesta Dockerfile:** Pane harvem muutuvad read algusesse. `COPY requirements.txt` enne `COPY . .` võimaldab cache'ida pip install sammu.

**Kustuta tarbetu:** Apt cache, build artefaktid, .git kataloog.

**.dockerignore:** Väldi tarbetute failide kopeerimist:
```
node_modules/
.git/
*.log
.env
```

---

## 5. Container'ite Käivitamine ja Haldamine

### 5.1 Põhikäsud
```bash
# Käivita container
docker run nginx

# Käivita taustal
docker run -d --name web nginx

# Port mapping
docker run -d -p 8080:80 nginx

# Environment variables
docker run -d -e DATABASE_URL=postgres://... myapp

# Vaata töötavaid container'eid
docker ps

# Vaata logisid
docker logs web
docker logs -f web  # follow

# Käivita käsk container'is
docker exec web ls /etc/nginx
docker exec -it web bash

# Peata ja kustuta
docker stop web
docker rm web
```

### 5.2 Container Lifecycle
```
docker create → CREATED
docker start → RUNNING
docker stop → STOPPED (SIGTERM + SIGKILL)
docker restart → RUNNING
docker rm → deleted
```

`docker stop` saadab SIGTERM signaali, ootab 10 sekundit graceful shutdown'iks, seejärel SIGKILL. Kasuta `docker stop -t 30` pikema timeout'i jaoks.

### 5.3 Resource Limits
```bash
docker run -d \
  --memory="512m" \
  --cpus="1.5" \
  --pids-limit=100 \
  myapp
```

Ilma limit'ideta võib üks container tarbida kogu CPU ja RAM'i. Produktsioonis on limit'id kohustuslikud.

---

## 6. Volumes ja Andmehaldus

### 6.1 Probleem

Container'i writable layer on ajutine. Container kustutamisel kaovad andmed. Andmebaasid, logid, kasutaja-poolt laaditud failid vajavad püsivat salvestust.

### 6.2 Volume Tüübid

**Named volumes:**
```bash
docker volume create pgdata
docker run -d -v pgdata:/var/lib/postgresql/data postgres
```

Docker haldab volume'i asukohta (`/var/lib/docker/volumes/pgdata/`). Soovitatav produktsioonis.

**Bind mounts:**
```bash
docker run -d -v /host/path:/container/path nginx
```

Host'i kataloog mountitakse container'isse. Kasutatakse arenduses (live reload). Bind mount ei ole portable - sõltub host'i failisüsteemist.

**tmpfs mounts:**
```bash
docker run -d --tmpfs /tmp nginx
```

Salvestab RAM'is. Kiire, aga kaob restart'imisel. Cache või ajutised failid.

### 6.3 Volume Elutsükkel

Volume eksisteerib iseseisvalt container'ist:
```bash
docker run -v mydata:/data alpine sh -c 'echo "test" > /data/file.txt'
docker run -v mydata:/data alpine cat /data/file.txt  # "test"
```

Volume ei kustutata automaatselt. Kasuta `docker volume prune` kasutamata volume'ide kustutamiseks.

---

## 7. Networking

### 7.1 Network Driver'id

**Bridge (default):** Privaatne võrk host'is. Container'id saavad omavahel suhelda, väljapoole liikumine NAT'itakse.

**Host:** Container kasutab host'i võrku otse. Kõige kiirem, kuid vähem isoleeritud.

**None:** Container'il pole võrguühendust.

**Overlay:** Multi-host võrk Docker Swarm/Kubernetes jaoks.

### 7.2 Container-to-Container Communication
```bash
docker network create mynet
docker run -d --name db --network mynet postgres
docker run -d --name api --network mynet myapi
```

Container'id samas network'is näevad Ã¼ksteist DNS'i kaudu. Container `db` on kättesaadav hostname'iga `db`.

Port mapping (`-p`) on välise ligipääsu jaoks. Internal suhtlus ei vaja port mapping'ut.

---

## 8. Docker Compose

### 8.1 Miks Compose

Käsitsi käivitada 5 container'it (web, api, db, cache, queue) koos nende sõltuvustega on vigaderohke. Docker Compose kirjeldab kogu stack'i YAML formaadis:
```yaml
version: '3.8'

services:
  web:
    build: ./frontend
    ports:

      - "80:80"
    depends_on:

      - api
  
  api:
    build: ./backend
    environment:
      DATABASE_URL: postgres://db:5432/mydb
    depends_on:

      - db
  
  db:
    image: postgres:15-alpine
    volumes:

      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

Käivitamine: `docker-compose up -d`

### 8.2 Compose vs Kubernetes

Compose on arenduseks ja väikesteks deployment'ideks. Kubernetes on production-grade orchestrator suurematele süsteemidele (auto-scaling, self-healing, load balancing).

---

## 9. Turvalisus

### 9.1 Container vs VM Turvalisus

Container'id jagavad kernel'it - kernel exploit võib mõjutada host'i. VM'id on isoleeritud hypervisori tasemel - tugevam isolatsioon.

### 9.2 Best Practices

**Non-root user:**
```dockerfile
RUN adduser -D appuser
USER appuser
```

Vaikimisi jooksevad container'id root'ina. Kui keegi container'isse sisse murdab, on tal root õigused. Loo spetsiaalne kasutaja.

**Read-only filesystem:**
```bash
docker run --read-only --tmpfs /tmp myapp
```

**Secrets management:** Ära pane paroole ENV'i ega image'sse. Kasuta Docker secrets või vault'i.

**Image scanning:** Skanni haavatavusi (Trivy, Clair).
```bash
trivy image myapp:latest
```

**Minimal base images:** Vähem pakette = vähem haavatavusi. Alpine sisaldab 5MB, Ubuntu 100MB.

---

## 10. Monitoring ja Logging

### 10.1 Container Stats
```bash
docker stats
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### 10.2 Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

Docker märgib container'i unhealthy, kui health check ebaõnnestub. Orchestraator (Kubernetes, Swarm) saab selle automaatselt restartida.

### 10.3 Logging

Vaikimisi salvestab Docker logid JSON formaadis `/var/lib/docker/containers/`. Produktsioonis suunake logid tsentraliseeritud süsteemi (ELK stack, Loki):
```yaml
services:
  app:
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://192.168.1.100:514"
```

---

## Kokkuvõte

Docker lahendab keskkondade sünkroniseerimise probleemi container'ite kaudu. Container'id on kiired, kerged ja portaalsed. Dockerfile kirjeldab image'i loomist, volume'id säilitavad andmeid, network'id võimaldavad suhtlust.

Praktiline kasutus nõuab mõistmist image optimeerimisest, turvalisusest ja orchestration'ist. Järgmises lab'is rakendame neid teadmisi praktikas.

**Järgmised sammud:** Labor, kodutöö, Kubernetes tutvustus.