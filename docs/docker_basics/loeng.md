# Docker: Konteinerite Põhitõed

**Eeldused:** Linux CLI põhitõed, tekstiredaktor  
**Platvorm:** Docker (platform-agnostic), Podman

**Dokumentatsioon:** [docs.docker.com](https://docs.docker.com/)

## Õpiväljundid

- Selgitad konteinerite tehnoloogia vajadust ja eeliseid
- Eristab Docker'i arhitektuuri komponente
- Võrdleb konteineri tehnoloogiaid virtuaalmasinatega
- Mõistad image'ide ja container'ite vahelist suhet
- Kirjeldad Dockerfile'i struktuuri ja ehitusprotsessi
- Kasutad volume'e andmete püsivuse tagamiseks

---

## 1. Konteinerite Tehnoloogia Motiiv

### 1.1 Keskkondade Probleem

IT infrastruktuuris on alati eksisteerinud konfiguratsioonide lahknevus. Arendaja laptop sisaldab Pythoni versiooni 3.9 Ubuntu 20.04 peal, testimisserver kasutab Pythoni 3.7 CentOS'il, produktsioonikeskkond jooksutab Pythoni 3.10 Debian'il. Igaüks nendest keskkondadest sisaldab erinevaid süsteemiteeke, sõltuvusi ja seadistusi.

```mermaid
graph LR
    A[Arendaja<br/>Python 3.9<br/>Ubuntu 20.04] -->|"Töötab"| B[Git Push]
    B --> C[Test Server<br/>Python 3.7<br/>CentOS 7]
    C -->|"❌ Error"| D[Debug]
    D --> E[Production<br/>Python 3.10<br/>Debian 11]
    E -->|"❌ Error"| F[Crisis]
    
    style C fill:#ffcccc
    style E fill:#ffcccc
```

Tulemus on ennustatav: kood töötab ühes keskkonnas, ebaõnnestub teises. Arendajad kulutavad tunde keskkondade sünkroniseerimisele, DevOps meeskonnad haldavad keerukaid deployment skripte, testimine muutub ebausaldusväärseks. Need probleemid pole uued, kuid nende mõju kasvab eksponentsiaalselt koos rakenduste keerukusega.

### 1.2 Varasemad Lahendused

Virtuaalmasinad pakkusid 2000-2010 isolatsiooni probleemile lahendust, kuid hinnaga. Iga VM sisaldab täielikku operatsioonisüsteemi koopiat, mida haldab hypervisor. See tähendab gigabaitide jagu kettaruumi ja RAM'i igale rakendusele, koos 30-60 sekundilise käivitusajaga. Serveri ressursid ammenduvad kiiresti.

Configuration Management tööriistad nagu Puppet, Ansible ja Chef automatiseerisid serveri seadistamise 2010-2015. Probleem püsib - serverid muutuvad aja jooksul, **drift** on vältimatu. Manuaalsed sekkumised, sõltuvuste uuendused ja logifailide kuhjumine muudavad iga serveri unikaalseks. Süsteemi taastamine või replikatsioon muutub iga korraga keerulisemaks.

### 1.3 Docker'i Revolutsioon

Docker kasutas 2013. aastal Linux'i kernel'i olemasolevaid võimeid uudsel viisil. Linux'i **namespaces** isoleerivad protsesse, **cgroups** piiravad ressursse. Docker raames container'id jagavad host'i kernel'it, kuid on protsesside tasandil täielikult isoleeritud.

```mermaid
graph TB
    subgraph VM["Virtuaalmasinad"]
        H1[Hardware]
        HV[Hypervisor]
        VM1[Guest OS 1<br/>2GB RAM]
        VM2[Guest OS 2<br/>2GB RAM]
        VM3[Guest OS 3<br/>2GB RAM]
        APP1[App 1]
        APP2[App 2]
        APP3[App 3]
        
        H1 --> HV
        HV --> VM1 & VM2 & VM3
        VM1 --> APP1
        VM2 --> APP2
        VM3 --> APP3
    end
    
    subgraph CONT["Containerid"]
        H2[Hardware]
        OS[Host OS + Docker]
        C1[Container 1<br/>50MB]
        C2[Container 2<br/>50MB]
        C3[Container 3<br/>50MB]
        A1[App 1]
        A2[App 2]
        A3[App 3]
        
        H2 --> OS
        OS --> C1 & C2 & C3
        C1 --> A1
        C2 --> A2
        C3 --> A3
    end
    
    style VM1 fill:#ffcccc
    style VM2 fill:#ffcccc
    style VM3 fill:#ffcccc
    style C1 fill:#ccffcc
    style C2 fill:#ccffcc
    style C3 fill:#ccffcc
```

Võrdlus näitab erinevust:

| Kriteerium | Container | Virtuaalmasin |
|------------|-----------|---------------|
| Käivitusaeg | 1-3 sekundit | 30-60 sekundit |
| Mälukasutus | 10-100 MB | 512 MB - 8 GB |
| Kettaruum | 100 MB - 1 GB | 10-50 GB |
| Server mahutab | 100-1000+ | 10-50 |
| Isolatsioon | Kernel jagatud | Täielik |

Container'i käivitamine on sisuliselt protsessi käivitamine koos isolatsioonimeetmetega. VM käivitamine tähendab terve OS'i boot'imist. See fundamentaalne erinevus selgitab jõudluse ja ressursikasutuse erinevusi.

### 1.4 Tööstuse Kasutusnäited

Netflix käivitab üle miljardi container'i nädalas oma sisuhaldus- ja soovitussüsteemides. Google'i infrastruktuur on alates 2000. aastatest olnud container-põhine, alustades Borg süsteemist, mis hiljem arenes Kuberneteseks. Wise (endine TransferWise) kasutab konteineri tehnoloogiat mikroteenuste arhitektuuris, võimaldades igas riigis eraldi regulatiivsetele nõuetele vastavat deployment'i.

87% IT ettevõtetest kasutab konteinereid produktsioonis 2024. aasta seisuga. See pole enam eksperimentaalne tehnoloogia, vaid standardne lähenemine rakenduste käivitamisele.

---

## 2. Docker Arhitektuur ja Mõisted

### 2.1 Client-Server Mudel

Docker kasutab klassikalist **client-server arhitektuuri**. Docker CLI (client) suhtleb Docker daemoniga (dockerd) üle UNIX socket'i või HTTP API. Daemon haldab image'eid, container'eid, võrke ja volume'e. See eraldamine võimaldab remote haldust - CLI võib asuda ühes masinas, daemon teises.

```mermaid
graph LR
    CLI[Docker CLI<br/>docker run nginx]
    API[REST API<br/>UNIX socket]
    DAEMON[Docker Daemon<br/>dockerd]
    RUNTIME[Container Runtime<br/>containerd + runc]
    STORAGE[(Image Storage<br/>Volume Storage)]
    NET[Network Driver]
    
    CLI -->|HTTP/UNIX| API
    API --> DAEMON
    DAEMON --> RUNTIME
    DAEMON --> STORAGE
    DAEMON --> NET
    
    RUNTIME -->|Creates| CONT1[Container 1]
    RUNTIME -->|Creates| CONT2[Container 2]
    
    style CLI fill:#e1f5ff
    style DAEMON fill:#fff4e1
    style RUNTIME fill:#e8f5e9
```

Daemon kasutab **containerd** runtime'i, mis omakorda kasutab **runc**'i container'ite käivitamiseks. See kihistatud arhitektuur järgib Unix filosoofiat - iga komponent teeb üht asja hästi.

### 2.2 Image

**Image** on read-only template, mis sisaldab operatsioonisüsteemi baasi, runtime'i, sõltuvusi ja rakenduse koodi. Image on immutable - pärast loomist ei muutu kunagi. Iga muudatus loob uue image'i versiooni. See immutability tagab reprodutseeritavuse.

Image koosneb **layer'itest**. Iga Dockerfile käsk loob uue layer'i, mis salvestatakse overlay failisüsteemis. Layer'id on jagatud - kui kümme image't kasutab sama base layer'it, salvestatakse see kettale ainult üks kord. Layer'id on ka cacheable - kui Dockerfile'is ei muutu rida, kasutatakse vana layer'it cache'ist, kiirendades järgnevaid build'e.

```mermaid
graph TB
    subgraph "Image Layers (Read-Only)"
        L1[Layer 1: Alpine Linux - 5MB]
        L2[Layer 2: Python 3.11 - 45MB]
        L3[Layer 3: pip install requirements - 30MB]
        L4[Layer 4: COPY app code - 2MB]
    end
    
    subgraph "Container"
        WL[Writable Layer - 10MB<br/>logs, temp files]
    end
    
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> WL
    
    IMG1[nginx image] -.shares.-> L1
    IMG2[another app] -.shares.-> L1
    IMG3[another app] -.shares.-> L2
    
    style L1 fill:#e8f5e9
    style L2 fill:#e8f5e9
    style L3 fill:#e8f5e9
    style L4 fill:#e8f5e9
    style WL fill:#fff4e1
```

Base layer võib olla `alpine` (5MB), `ubuntu` (30MB) või `debian` (120MB). Igale lisandub rakenduse layer'id. Optimeeritud image võib olla 50-100MB, optimeerimata võib ulatuda gigabaitideni.

### 2.3 Container

**Container** on töötav instantsi image'ist. Container saab writable layer'i image'i peale, kuhu saab kirjutada ajutisi faile. See layer on ajutine - container kustutamisel kaob ka writable layer koos kõigi muudatustega. Container isoleerib protsesse, võrku, failisüsteemi ja ressursse.

```mermaid
stateDiagram-v2
    [*] --> Created: docker create
    Created --> Running: docker start
    Running --> Paused: docker pause
    Paused --> Running: docker unpause
    Running --> Stopped: docker stop
    Stopped --> Running: docker start
    Stopped --> [*]: docker rm
    Running --> [*]: docker rm -f
    
    note right of Running
        Container töötab
        Protsessid käivad
        Võrk aktiivne
    end note
    
    note right of Stopped
        Protsessid peatatud
        Writable layer säilib
        Saab uuesti käivitada
    end note
```

Container ei ole VM. See on isoleeritud protsess host operatsioonisüsteemis. Container jagab kernel'it host'iga, seega ei saa native Windows container'it käivitada Linux host'il ilma virtualisatsioonita. WSL2 Windows'is kasutab taustal kerget VM'i, et pakkuda Linux kernel'it.

### 2.4 Registry

**Registry** on image'ide ladu. Docker Hub on avalik registry, kust saab alla laadida tuhandeid valmis image'eid. Ametlikud image'd nagu nginx, postgres, python on Docker Inc poolt auditeeritud. Ettevõtted kasutavad private registry'sid (AWS ECR, Google Container Registry, Harbor) kontrolli ja turvalisuse jaoks.

Image'i täisnimi järgib formaati: `registry/namespace/repository:tag`

- Docker Hub: `nginx:alpine` on lühend täisnimest `docker.io/library/nginx:alpine`
- Private: `gcr.io/my-project/api-server:v1.2.3`

Tag on optional - kui puudub, kasutatakse `latest`. **Oluline:** `latest` ei tähenda kõige uuemat versiooni, vaid default tag'i. Produktsioonis kasuta alati spetsiifilisi versioone.

---

## 3. Docker vs Podman vs Virtuaalmasinad

### 3.1 Arhitektuuriline Võrdlus

| Kriteerium | Docker | Podman | VM (KVM/VMware) |
|------------|--------|--------|-----------------|
| Daemon | Vajab dockerd | Daemonless | Hypervisor |
| Õigused | Root privileegid vajalikud | Rootless võimalik | Root + hypervisor |
| Networking | Bridge/overlay/host | Sama | Virtual NIC |
| Image formaat | OCI compliant | OCI compliant | Disk image (qcow2, vmdk) |
| Orchestration | Swarm/Kubernetes | Kubernetes native | - |
| Pod support | Ei (ainult containers) | Jah | - |

**OCI** (Open Container Initiative) määratleb image ja runtime standardid. Podman ja Docker kasutavad sama formaati, seega `docker pull` image töötab `podman run` käsuga. See standardiseerimine võimaldab vendor lock-in'i vältimist.

### 3.2 Millal Kasutada Mida

**Docker:** Küps ökosüsteem, Docker Compose de facto standard arenduses, lai tööstuslik toetus. Õppimiskõvera algus on lihtne. Kubernetes'e migratsiooni tee on hästi dokumenteeritud.

**Podman:** Turvalisem arhitektuur tänu rootless režiimile, ei vaja daemon'it (vähem attack surface), pod kontseptsiooni native tugi. Sobib hästi ettevõtete turvapõhimõtetega. Drop-in asendus Docker CLI'le.

**VM:** Erinev OS kernel (Windows rakendus Linux host'il), range turvaisolatsioon kriitiliste süsteemide jaoks, legacy rakendused mis vajavad spetsiifilist kernel versiooni või driver'eid.

Praktikas kasutatakse sageli koos - VM'id füüsilise infrastruktuuri isoleerimiseks, container'id rakenduste isoleerimiseks.

---

## 4. Dockerfile ja Image'ide Loomine

### 4.1 Dockerfile Süntaks

Dockerfile on tekstifail käskudega image'i ehitamiseks. Iga rida loob potentsiaalselt uue layer'i. Formaadilt lihtne, kuid optimeerimise võimalused on sügavad.

**Põhilised käsud:**

| Käsk | Otstarve | Näide |
|------|----------|-------|
| **FROM** | Base image | `FROM python:3.11-alpine` |
| **WORKDIR** | Töökataloog | `WORKDIR /app` |
| **COPY** | Kopeeri failid | `COPY . .` |
| **RUN** | Käivita build ajal | `RUN pip install -r requirements.txt` |
| **ENV** | Environment variable | `ENV PORT=8000` |
| **EXPOSE** | Dokumenteeri port | `EXPOSE 8000` |
| **CMD** | Vaikimisi käsk | `CMD ["python", "app.py"]` |
| **ENTRYPOINT** | Peamine käsk | `ENTRYPOINT ["nginx"]` |

**Lihtsustatud näide:**

```dockerfile
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### 4.2 Build Protsess

```bash
docker build -t myapp:v1.0 .
```

Docker loeb Dockerfile'i, käivitab iga käsu järjest temporary container'is, commitib tulemuse uueks layer'iks. **Cache'imine** on kriitiline jõudluse jaoks - kui layer ei ole muutunud, kasutab Docker cached versiooni.

```mermaid
graph TB
    DF[Dockerfile] --> R1[Read: FROM python:3.11]
    R1 --> L1[Layer 1: Base image]
    L1 --> R2[Read: RUN pip install...]
    R2 --> CHK{Cache hit?}
    CHK -->|Yes| L2C[Use cached layer]
    CHK -->|No| L2N[Build new layer]
    L2C --> R3
    L2N --> R3[Read: COPY . .]
    R3 --> L3[Layer 3: App code]
    L3 --> IMG[Final Image]
    
    style CHK fill:#fff4e1
    style L2C fill:#e8f5e9
```

Build context (`.` eelmises näites) saadetakse daemonile. Suur context aeglustab build'i. Kasuta `.dockerignore` et välistada `node_modules/`, `.git/`, log failid.

### 4.3 Multi-Stage Build

Suurte rakenduste puhul on build dependencies oluliselt suuremad kui runtime vajadus. Multi-stage build eraldab need:

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
CMD ["node", "dist/main.js"]
```

Tulemus: final image sisaldab ainult runtime'i ja kompileeritud koodi, mitte build tools'e. Image suurus väheneb 1.2GB → 150MB.

```mermaid
graph LR
    subgraph "Stage 1: Builder"
        B1[node:18<br/>1.2GB]
        B2[npm install<br/>+300MB]
        B3[npm build<br/>+50MB]
    end
    
    subgraph "Stage 2: Runtime"
        R1[node:18-alpine<br/>120MB]
        R2[Copy dist/<br/>+30MB]
    end
    
    B1 --> B2 --> B3
    B3 -.copy dist.-> R2
    R1 --> R2
    R2 --> FINAL[Final: 150MB]
    
    style B1 fill:#ffcccc
    style R1 fill:#ccffcc
    style FINAL fill:#ccffcc
```

### 4.4 Image Optimeerimise Põhimõtted

**Vali väiksem base image:** `python:3.11-alpine` (50MB) vs `python:3.11` (900MB).

**Kombineeri RUN käsud:** Iga `RUN` loob layer'i. Kolm `RUN` käsku = kolm layer'it.

**Järjesta Dockerfile:** Harvem muutuvad read algusesse. `COPY requirements.txt` enne `COPY . .` võimaldab cache'ida sõltuvuste installimist.

**.dockerignore näide:**
```
node_modules/
.git/
*.log
.env
__pycache__/
*.pyc
.pytest_cache/
```
---

## 5. Volumes ja Andmehaldus

### 5.1 Probleem

Container'i writable layer on ajutine. Container kustutamisel kaovad andmed. Andmebaasid, logid, kasutaja-poolt laaditud failid vajavad püsivat salvestust.

```mermaid
graph LR
    subgraph "Container Without Volume"
        C1[Container] --> WL1[Writable Layer<br/>DB data]
        WL1 -.->|docker rm| X1[❌ Data lost]
    end
    
    subgraph "Container With Volume"
        C2[Container] --> WL2[Writable Layer<br/>temp files]
        C2 --> V[Volume<br/>DB data]
        WL2 -.->|docker rm| X2[Temp files lost]
        V -.->|docker rm| OK[✓ Data persists]
    end
    
    style X1 fill:#ffcccc
    style OK fill:#ccffcc
```

### 5.2 Volume Tüübid

**Named volumes:** Docker haldab volume'i asukohta. Soovitatav produktsioonis.

```bash
docker volume create pgdata
docker run -d -v pgdata:/var/lib/postgresql/data postgres
```

**Bind mounts:** Host'i kataloog mountitakse container'isse. Kasutatakse arenduses.

```bash
docker run -d -v /host/path:/container/path nginx
```

**tmpfs mounts:** Salvestab RAM'is. Kiire, aga kaob restart'imisel.

| Tüüp | Kasutus | Püsivus | Jõudlus |
|------|---------|---------|---------|
| Named volume | Production data | Püsiv | Hea |
| Bind mount | Development | Püsiv | Host'ist sõltuv |
| tmpfs | Cache, temp | Kadub | Väga kiire |

### 5.3 Volume Elutsükkel

Volume eksisteerib iseseisvalt container'ist:

```bash
# Container 1 kirjutab
docker run -v mydata:/data alpine sh -c 'echo "test" > /data/file.txt'

# Container 2 loeb sama volume'i
docker run -v mydata:/data alpine cat /data/file.txt  # "test"
```

Volume ei kustutata automaatselt. Kasuta `docker volume prune` kasutamata volume'ide kustutamiseks.

---

## 6. Networking

### 6.1 Network Driver'id

**Bridge (default):** Privaatne võrk host'is. Container'id saavad omavahel suhelda.

**Host:** Container kasutab host'i võrku otse. Kõige kiirem, kuid vähem isoleeritud.

**None:** Container'il pole võrguühendust.

```mermaid
graph TB
    subgraph "Bridge Network (Default)"
        BR[Docker Bridge<br/>172.17.0.0/16]
        C1[Container 1<br/>172.17.0.2] --> BR
        C2[Container 2<br/>172.17.0.3] --> BR
        BR -->|NAT| HOST1[Host Network]
    end
    
    subgraph "Custom Network"
        NET[mynet<br/>172.18.0.0/16]
        C3[web<br/>172.18.0.2] --> NET
        C4[db<br/>172.18.0.3] --> NET
        NET -->|NAT| HOST2[Host Network]
        
        C3 -.DNS: db.-> C4
    end
    
    style NET fill:#e8f5e9
```

### 6.2 Container-to-Container Communication

```bash
docker network create mynet
docker run -d --name db --network mynet postgres
docker run -d --name api --network mynet myapi
```

Container'id samas network'is näevad üksteist DNS'i kaudu. Container `db` on kättesaadav hostname'iga `db`. Port mapping (`-p`) on välise ligipääsu jaoks.

---

## 7. Turvalisus

### 7.1 Container vs VM Turvalisus

Container'id jagavad kernel'it - kernel exploit võib mõjutada host'i. VM'id on isoleeritud hypervisori tasemel.

```mermaid
graph TB
    subgraph "VM Isolation"
        HW1[Hardware]
        HYP[Hypervisor]
        VM1[Guest Kernel 1] 
        VM2[Guest Kernel 2]
        APP1[App 1]
        APP2[App 2]
        
        HW1 --> HYP
        HYP --> VM1 & VM2
        VM1 --> APP1
        VM2 --> APP2
    end
    
    subgraph "Container Isolation"
        HW2[Hardware]
        K[Shared Kernel]
        NS1[Namespace 1]
        NS2[Namespace 2]
        A1[App 1]
        A2[App 2]
        
        HW2 --> K
        K --> NS1 & NS2
        NS1 --> A1
        NS2 --> A2
    end
    
    style VM1 fill:#e8f5e9
    style VM2 fill:#e8f5e9
    style K fill:#fff4e1
```

### 7.2 Best Practices

**Non-root user:**
```dockerfile
RUN adduser -D appuser
USER appuser
```

**Read-only filesystem:**
```bash
docker run --read-only --tmpfs /tmp myapp
```

**Image scanning:**
```bash
trivy image myapp:latest
```

**Minimal base images:** Alpine (5MB) vs Ubuntu (100MB) - vähem pakette = vähem haavatavusi.

---

## Kokkuvõte

Docker lahendab keskkondade sünkroniseerimise probleemi container'ite kaudu. Container'id on kiired, kerged ja portaalsed. Dockerfile kirjeldab image'i loomist, volume'id säilitavad andmeid, network'id võimaldavad suhtlust.

**Põhimõisted:**
- **Image** - immutable template
- **Container** - töötav instantsi 
- **Volume** - püsiv andmete salvestus
- **Network** - container'ite vaheline suhtlus

**Järgmised sammud:**
- Praktiline labor Docker käskude ja Dockerfile'idega
- Docker Compose mitme container'i haldamiseks
- Kubernetes orkestreerimiseks produktsioonis

---
