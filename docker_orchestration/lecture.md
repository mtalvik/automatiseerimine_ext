# Docker Compose ja Orchestration

**Teemad:** Docker Compose põhialused, Multi-container rakendused, Keskkondade haldamine, Orkestreerimise põhimõtted

---

## 🎯 Õpiväljundid

Pärast seda loengut oskate:
- Kirjutada ja käivitada Docker Compose faile
- Ehitada multi-container rakendusi
- Mõista teenuste vahelist suhtlust ja võrgustikku
- Hallata erinevaid keskkondi (development, production)
- Debuggida ja tõrkeotsingut teha
- Mõista orkestreerimise põhimõtteid ja vajadust

---

## 📖 Sissejuhatus: Miks me vajame orkestreerimist?

Tere tulemast orkestreerimise maailma! Kujutage ette, et ehitate tänapäevast veebirakendust. Teil on React'is ehitatud kasutajaliides, Node.js API server, PostgreSQL andmebaas ja Redis cache. Kuidas te kõik need komponendid koos tööle panete?

### Probleem: Käsitsi haldamine on valus

Vaatame, mis juhtub kui proovite kõiki komponente käsitsi hallata. Iga kord kui tahate oma rakendust käivitada, peate tegema midagi sellist:

```bash
# Esiteks käivitame andmebaasi
docker run -d \
  --name myapp-db \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_DB=myapp \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:13

# Ootame kuni andmebaas on valmis... aga kui kaua?
sleep 10  # Loodame, et 10 sekundit on piisav?

# Siis käivitame Redis cache
docker run -d \
  --name myapp-redis \
  redis:alpine

# Nüüd API server
docker run -d \
  --name myapp-api \
  -e DATABASE_URL=postgres://postgres:secret123@172.17.0.2:5432/myapp \
  -e REDIS_URL=redis://172.17.0.3:6379 \
  -p 3000:3000 \
  mycompany/api:latest

# Ja lõpuks frontend
docker run -d \
  --name myapp-frontend \
  -e API_URL=http://172.17.0.4:3000 \
  -p 80:80 \
  mycompany/frontend:latest
```

Näete probleemi? Te peate teadma IP-aadresse (mis muutuvad!), õiget käivitamise järjekorda, ootama et teenused oleksid valmis... Ja mis juhtub kui kolleeg tahab sama rakendust käivitada? Ta peab kõik need käsud kopeerima ja lootma, et midagi ei lähe valesti.

```mermaid
graph TD
    subgraph "😱 Käsitsi haldamise õudus"
        Start[Alusta]
        DB[Käivita DB<br/>docker run...]
        Wait1[Oota... kas on valmis?]
        Redis[Käivita Redis<br/>docker run...]
        Wait2[Oota... kas on valmis?]
        API[Käivita API<br/>docker run...]
        Wait3[Oota... kas on valmis?]
        Frontend[Käivita Frontend<br/>docker run...]
        Error{Kas kõik<br/>töötab?}
        Debug[Debug 4 erinevat<br/>containerit]
        Success[Õnnestus!<br/>...seekord]
    end
    
    Start --> DB
    DB --> Wait1
    Wait1 --> Redis
    Redis --> Wait2
    Wait2 --> API
    API --> Wait3
    Wait3 --> Frontend
    Frontend --> Error
    Error -->|Ei| Debug
    Debug --> Start
    Error -->|Jah| Success
    
    style Error fill:#ff9999
    style Debug fill:#ff6666
    style Success fill:#99ff99
```

### Lahendus: Docker Compose

Docker Compose lahendab kõik need probleemid. See on nagu dirigent orkestris - koordineerib kõiki "muusikuid" (konteinereid) nii et nad mängiksid koos harmooniliselt.

Sama rakendus Docker Compose'iga näeb välja selline:

```yaml
# docker-compose.yml
version: '3.8'

services:
  database:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: secret123
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

  api:
    image: mycompany/api:latest
    environment:
      DATABASE_URL: postgres://postgres:secret123@database:5432/myapp
      REDIS_URL: redis://redis:6379
    ports:
      - "3000:3000"
    depends_on:
      database:
        condition: service_healthy
      redis:
        condition: service_started

  frontend:
    image: mycompany/frontend:latest
    environment:
      API_URL: http://api:3000
    ports:
      - "80:80"
    depends_on:
      - api

volumes:
  postgres_data:
  redis_data:
```

Ja käivitamine? Lihtsalt:

```bash
docker-compose up
```

Kõik. Docker Compose teeb ülejäänu - käivitab teenused õiges järjekorras, ootab kuni nad on valmis, seadistab võrgu, ja isegi taaskäivitab kui midagi kukub.

---

## 📖 Docker Compose põhitõed

### Kuidas Docker Compose töötab?

Docker Compose on deklaratiivne - te ütlete **mida** tahate, mitte **kuidas** seda saavutada. See on nagu restoranis tellimuse tegemine versus ise toidu valmistamine.

```mermaid
graph LR
    subgraph "🍕 Restorani analoogia"
        Order[📝 Tellimus<br/>"Tahan pitsat<br/>juustu ja sinkiga"]
        Kitchen[👨‍🍳 Köök<br/>Teab kuidas<br/>pitsat teha]
        Pizza[🍕 Valmis pitsa<br/>Täpselt nagu<br/>tellisite]
    end
    
    subgraph "🐳 Docker Compose"
        YAML[📄 docker-compose.yml<br/>"Tahan PostgreSQL<br/>ja Redis"]
        Compose[⚙️ Docker Compose<br/>Teab kuidas<br/>käivitada]
        System[🏭 Töötav süsteem<br/>Kõik teenused<br/>töötavad koos]
    end
    
    Order --> Kitchen
    Kitchen --> Pizza
    
    YAML --> Compose
    Compose --> System
    
    style Order fill:#ffcc99
    style YAML fill:#ffcc99
    style Kitchen fill:#99ccff
    style Compose fill:#99ccff
    style Pizza fill:#99ff99
    style System fill:#99ff99
```

### Compose faili struktuur

Iga Docker Compose fail koosneb kolmest põhiosast:

```yaml
version: '3.8'  # Compose faili formaat - kasutage alati 3.8 või uuemat

services:       # Siin kirjeldame kõik teenused
  # ...

volumes:        # Püsivad andmed
  # ...

networks:       # Võrgukonfiguratsioon (valikuline)
  # ...
```

Vaatame igat osa lähemalt.

### Services - süsteemi südamed

Iga teenus on eraldi konteiner, millel on oma roll. Mõelge neist kui osakondadest ettevõttes:

```mermaid
graph TB
    subgraph "🏢 Ettevõtte osakonnad"
        Reception[👥 Vastuvõtt<br/>Suhtleb klientidega]
        Sales[💼 Müük<br/>Töötleb tellimusi]
        Warehouse[📦 Ladu<br/>Hoiab kaupu]
        Accounting[📊 Raamatupidamine<br/>Haldab rahavooge]
    end
    
    subgraph "🐳 Docker teenused"
        Nginx[🌐 nginx<br/>Reverse proxy]
        API[⚙️ api<br/>Äriloogika]
        DB[🗄️ database<br/>Andmete hoidla]
        Cache[⚡ redis<br/>Kiire mälu]
    end
    
    Reception --> Sales
    Sales --> Warehouse
    Sales --> Accounting
    
    Nginx --> API
    API --> DB
    API --> Cache
    
    style Reception fill:#99ccff
    style Sales fill:#99ff99
    style Warehouse fill:#ffcc99
    style Accounting fill:#ff99ff
    style Nginx fill:#99ccff
    style API fill:#99ff99
    style DB fill:#ffcc99
    style Cache fill:#ff99ff
```

Iga teenus vajab vähemalt image'd, aga tavaliselt määrame ka:

```yaml
services:
  api:
    image: node:16-alpine           # Base image
    build: ./api                    # Või ehitame ise
    environment:                    # Keskkonnamuutujad
      NODE_ENV: production
      DATABASE_URL: ${DATABASE_URL}
    ports:                          # Avatud pordid
      - "3000:3000"
    volumes:                        # Failide jagamine
      - ./api:/app
      - /app/node_modules          # Anonymous volume
    depends_on:                     # Sõltuvused
      - database
    restart: unless-stopped         # Taaskäivituse poliitika
    command: npm start             # Käivituskäsk
```

### Volumes - püsivad andmed

Konteinerid on ajutised - kui nad kustutatakse, kaob ka nende sisu. Volumes'id on nagu välised kõvakettad, mis säilitavad andmeid konteinerite vahel.

```mermaid
graph LR
    subgraph "💾 Ilma volume'ita"
        Container1[📦 Container v1]
        Data1[💭 Andmed]
        Deleted1[❌ Kustutatud]
        Lost[😱 Andmed kadunud!]
        
        Container1 --> Data1
        Data1 --> Deleted1
        Deleted1 --> Lost
    end
    
    subgraph "💾 Volume'iga"
        Container2[📦 Container v1]
        Volume[💾 Named Volume]
        Container3[📦 Container v2]
        Data2[✅ Samad andmed]
        
        Container2 --> Volume
        Volume --> Container3
        Container3 --> Data2
    end
    
    style Lost fill:#ff9999
    style Data2 fill:#99ff99
    style Volume fill:#99ff99
```

Volumes'e saab defineerida kahel viisil:

```yaml
services:
  database:
    image: postgres:13
    volumes:
      # Named volume - Docker haldab
      - postgres_data:/var/lib/postgresql/data
      
      # Bind mount - otse hosti failisüsteemist
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
      
      # Anonymous volume - ajutine, aga säilib restart'ide vahel
      - /tmp

volumes:
  postgres_data:  # Named volume definitsioon
    driver: local
```

### Networks - kuidas teenused omavahel suhtlevad

Docker Compose loob automaatselt võrgu kus kõik teenused näevad üksteist. See on nagu ettevõtte sisevõrk - kõik osakonnad saavad omavahel suhelda, aga välismaailm ei näe neid otse.

```mermaid
graph TB
    subgraph "🌍 Internet"
        User[👤 Kasutaja<br/>Brauser]
    end
    
    subgraph "🏢 Docker Network: myapp_default"
        subgraph "Avalikud teenused"
            Nginx[🌐 nginx<br/>Port 80 avatud]
        end
        
        subgraph "Sisemised teenused"
            API[⚙️ api<br/>Ainult sisevõrgus]
            DB[🗄️ database<br/>Ainult sisevõrgus]
            Cache[⚡ cache<br/>Ainult sisevõrgus]
        end
    end
    
    User -->|"http://localhost"| Nginx
    Nginx -->|"http://api:3000"| API
    API -->|"postgres://database:5432"| DB
    API -->|"redis://cache:6379"| Cache
    
    User -.->|"❌ Ei pääse ligi"| API
    User -.->|"❌ Ei pääse ligi"| DB
    User -.->|"❌ Ei pääse ligi"| Cache
    
    style User fill:#ffcc99
    style Nginx fill:#99ccff
    style API fill:#ccffcc
    style DB fill:#ccffcc
    style Cache fill:#ccffcc
```

Teenused leiavad üksteist nime järgi. Kui teil on teenus nimega `database`, saavad teised teenused sellega ühenduda kasutades hostname'i `database`:

```yaml
services:
  api:
    environment:
      # 'database' lahendatakse automaatselt õigeks IP-ks
      DATABASE_URL: postgres://user:pass@database:5432/mydb
    
  database:
    image: postgres:13
```

---

## 📖 Dependency management ja järjekord

### Kuidas depends_on töötab

Docker Compose oskab teenuseid käivitada õiges järjekorras kui kasutate `depends_on`. See on nagu ehitamine - peate vundamendi valmis tegema enne kui saate maja ehitada.

```mermaid
graph TD
    subgraph "🏗️ depends_on toimine"
        Start[🚀 docker-compose up]
        
        subgraph "1️⃣ Esimene laine"
            DB[🗄️ database<br/>Sõltuvusi pole]
            Cache[⚡ cache<br/>Sõltuvusi pole]
        end
        
        subgraph "2️⃣ Teine laine"
            API[⚙️ api<br/>depends_on: database, cache]
        end
        
        subgraph "3️⃣ Kolmas laine"
            Web[🌐 frontend<br/>depends_on: api]
            Admin[👨‍💼 admin<br/>depends_on: api]
        end
        
        Ready[✅ Süsteem valmis]
    end
    
    Start --> DB
    Start --> Cache
    DB --> API
    Cache --> API
    API --> Web
    API --> Admin
    Web --> Ready
    Admin --> Ready
    
    style Start fill:#99ff99
    style Ready fill:#99ff99
    style DB fill:#ffcc99
    style Cache fill:#ffcc99
    style API fill:#99ccff
    style Web fill:#ccffcc
    style Admin fill:#ccffcc
```

Aga ettevaatust! Vaikimisi `depends_on` ootab ainult kuni konteiner käivitub, mitte kuni teenus on päriselt valmis. See on nagu ootamine kuni arvuti sisse lülitub, aga mitte ootamine kuni Windows on täielikult käivitunud.

### Healthcheck - kas teenus on päriselt valmis?

Lahendus on kasutada health check'e:

```yaml
services:
  database:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    healthcheck:
      # See käsk kontrollib kas PostgreSQL on valmis
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s      # Kontrolli iga 10 sekundi tagant
      timeout: 5s        # Käsk peab vastama 5 sekundi jooksul
      retries: 5         # Proovi 5 korda enne kui anna alla
      start_period: 30s  # Anna 30 sekundit aega käivituda

  api:
    image: myapp/api
    depends_on:
      database:
        # Oota kuni database on "healthy", mitte lihtsalt käivitunud
        condition: service_healthy
```

Erinevad teenused vajavad erinevaid health check'e:

```yaml
# PostgreSQL
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]

# MySQL
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]

# Redis
healthcheck:
  test: ["CMD", "redis-cli", "ping"]

# HTTP teenus
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]

# Või lihtsalt kontrolli kas port on avatud
healthcheck:
  test: ["CMD-SHELL", "nc -z localhost 3000"]
```

---

## 📖 Environment management

### Development vs Production

Tõenäoliselt vajate erinevaid seadeid arenduses ja toodangus. Docker Compose laseb teil kasutada mitut konfiguratsioonifaili:

```mermaid
graph LR
    subgraph "📁 Failide struktuur"
        Base[📄 docker-compose.yml<br/>Base konfiguratsioon]
        Dev[📄 docker-compose.dev.yml<br/>Arenduse lisad]
        Prod[📄 docker-compose.prod.yml<br/>Toodangu lisad]
    end
    
    subgraph "🔧 Arendus"
        DevMerge[Base + Dev<br/>Merged config]
        DevResult[💻 Dev environment<br/>• Debug mode<br/>• Hot reload<br/>• Exposed ports]
    end
    
    subgraph "🏭 Toodang"
        ProdMerge[Base + Prod<br/>Merged config]
        ProdResult[🌍 Production<br/>• Optimized<br/>• Secure<br/>• Scaled]
    end
    
    Base --> DevMerge
    Dev --> DevMerge
    DevMerge --> DevResult
    
    Base --> ProdMerge
    Prod --> ProdMerge
    ProdMerge --> ProdResult
    
    style Base fill:#ffcc99
    style Dev fill:#99ccff
    style Prod fill:#99ff99
```

Base konfiguratsioon (`docker-compose.yml`):

```yaml
version: '3.8'

services:
  api:
    build: ./api
    environment:
      DATABASE_URL: postgres://user:pass@database:5432/myapp
      REDIS_URL: redis://cache:6379
    depends_on:
      - database
      - cache

  database:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user

  cache:
    image: redis:alpine
```

Arenduse override (`docker-compose.dev.yml`):

```yaml
version: '3.8'

services:
  api:
    volumes:
      # Hot reload - failide muudatused kajastuvad kohe
      - ./api/src:/app/src
      - ./api/package.json:/app/package.json
    environment:
      NODE_ENV: development
      DEBUG: "true"
      LOG_LEVEL: debug
    ports:
      - "3000:3000"  # Debugimiseks
      - "9229:9229"  # Node.js debug port

  database:
    ports:
      - "5432:5432"  # Saame pgAdmin'iga ühenduda
    environment:
      POSTGRES_PASSWORD: devpassword
    volumes:
      # Testimisandmed
      - ./dev-data.sql:/docker-entrypoint-initdb.d/init.sql
```

Toodangu override (`docker-compose.prod.yml`):

```yaml
version: '3.8'

services:
  api:
    image: mycompany/api:${VERSION:-latest}
    restart: unless-stopped
    environment:
      NODE_ENV: production
      LOG_LEVEL: error
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  database:
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}  # From secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups

  cache:
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    
volumes:
  postgres_data:
    driver: local
```

Kasutamine:

```bash
# Arenduses
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Toodangus
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Või kasutades environment muutujat
export COMPOSE_FILE=docker-compose.yml:docker-compose.prod.yml
docker-compose up -d
```

### Environment variables ja .env failid

Docker Compose loeb automaatselt `.env` faili juurkataloogist:

```bash
# .env fail
NODE_ENV=development
DATABASE_PASSWORD=secret123
API_PORT=3000
DEBUG=true
```

Kasutamine compose failis:

```yaml
services:
  api:
    environment:
      # Kasuta muutujat, vaikeväärtusega
      NODE_ENV: ${NODE_ENV:-production}
      DATABASE_PASSWORD: ${DATABASE_PASSWORD}
      
    ports:
      # Muutujad töötavad igal pool
      - "${API_PORT:-3000}:3000"
```

Pro tip: Tehke erinevad env failid erinevatele keskkondadele:

```bash
# .env.example (commit to git)
NODE_ENV=
DATABASE_PASSWORD=
API_PORT=

# .env.development
NODE_ENV=development
DATABASE_PASSWORD=devpass123
API_PORT=3000

# .env.production (never commit!)
NODE_ENV=production
DATABASE_PASSWORD=supersecret789
API_PORT=80
```

---

## 📖 Debugging ja troubleshooting

### Kui asjad lähevad valesti

Ja nad lähevad. See on normaalne! Siin on teie tööriistakast probleemide lahendamiseks:

```mermaid
graph TD
    subgraph "🔍 Debugging flow"
        Problem[❌ Midagi ei tööta]
        Check1[📋 docker-compose ps<br/>Kas konteinerid töötavad?]
        Running{Töötavad?}
        
        CheckLogs[📝 docker-compose logs<br/>Vaata vigu]
        CheckSpecific[📝 docker-compose logs api<br/>Konkreetse teenuse logid]
        
        CheckNetwork[🌐 Kontrolli võrku<br/>docker-compose exec api ping database]
        CheckEnv[🔧 Kontrolli environment<br/>docker-compose exec api env]
        CheckFiles[📁 Kontrolli faile<br/>docker-compose exec api ls -la]
        
        Shell[💻 Mine konteinerisse<br/>docker-compose exec api sh]
        Debug[🔍 Debug käsitsi<br/>Test connections, run commands]
        
        Fix[✅ Paranda probleem]
        Restart[🔄 docker-compose restart api]
    end
    
    Problem --> Check1
    Check1 --> Running
    Running -->|Ei| CheckLogs
    Running -->|Jah| CheckNetwork
    
    CheckLogs --> CheckSpecific
    CheckSpecific --> Fix
    
    CheckNetwork --> CheckEnv
    CheckEnv --> CheckFiles
    CheckFiles --> Shell
    Shell --> Debug
    Debug --> Fix
    Fix --> Restart
    
    style Problem fill:#ff9999
    style Fix fill:#99ff99
    style Restart fill:#99ccff
```

### Põhilised debug käsud

```bash
# 1. Vaata mis toimub
docker-compose ps
# NAME                COMMAND             SERVICE   STATUS      PORTS
# myapp-api-1        "npm start"         api       Up          0.0.0.0:3000->3000/tcp
# myapp-database-1   "postgres"          database  Up (healthy) 5432/tcp
# myapp-cache-1      "redis-server"      cache     Up          6379/tcp

# 2. Kui midagi on "Exit" staatuses, vaata logisid
docker-compose logs database
# database_1  | FATAL: password authentication failed for user "postgres"

# 3. Jälgi logisid reaalajas (nagu tail -f)
docker-compose logs -f api
# Ctrl+C väljumiseks

# 4. Vaata ainult viimased 50 rida
docker-compose logs --tail=50 api

# 5. Mine konteinerisse sisse
docker-compose exec api sh
# Nüüd olete konteineri sees, saate kontrollida:
$ ps aux           # Mis protsessid jooksevad
$ netstat -tlpn   # Mis pordid on avatud  
$ env             # Environment muutujad
$ cat /etc/hosts  # DNS nimed
$ ping database   # Kas näeb teisi teenuseid
$ curl http://localhost:3000/health  # Test endpoint

# 6. Kui konteiner on surnud ja ei käivitu
docker-compose run --rm api sh
# Käivitab ajutise konteineri debugging jaoks

# 7. Vaata täpset konfiguratsiooni
docker-compose config
# Näitab merged konfiguratsiooni kõigi override'idega

# 8. Vaata mis võrgud on loodud
docker network ls
docker network inspect myapp_default

# 9. Vaata ressursikasutust
docker stats
# Näitab CPU/Memory kasutust reaalajas
```

### Tavalised probleemid ja lahendused

#### 1. "Cannot connect to database"

```mermaid
graph LR
    subgraph "❌ Probleem"
        API[⚙️ API]
        DB[🗄️ Database]
        Error[Cannot connect<br/>to database]
        
        API -.->|"❌"| DB
    end
    
    subgraph "✅ Lahendused"
        Wait[⏱️ Lisa health check<br/>ja depends_on]
        DNS[🌐 Kasuta õiget nime<br/>database, mitte localhost]
        Network[🔌 Kontrolli võrku<br/>Peavad olema samas]
        Creds[🔑 Kontrolli parool<br/>Environment muutujad]
    end
    
    Error --> Wait
    Error --> DNS
    Error --> Network
    Error --> Creds
```

Lahendus:

```yaml
services:
  api:
    environment:
      # ❌ Vale - localhost on konteineri enda localhost
      # DATABASE_URL: postgres://user:pass@localhost:5432/db
      
      # ✅ Õige - kasuta teenuse nime
      DATABASE_URL: postgres://user:pass@database:5432/db
    depends_on:
      database:
        condition: service_healthy
        
  database:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s
      retries: 10
```

#### 2. "Port already in use"

```bash
# Kontrolli mis kasutab porti
sudo lsof -i :3000
# või
sudo netstat -tlpn | grep 3000

# Tapa protsess või muuda porti
services:
  api:
    ports:
      - "3001:3000"  # Kasuta teist välist porti
```

#### 3. "Permission denied" volume'ides

```yaml
services:
  api:
    # Lisa user mapping
    user: "${UID:-1000}:${GID:-1000}"
    volumes:
      - ./data:/app/data
```

#### 4. Container käivitub ja sureb kohe

```bash
# Vaata mis juhtus
docker-compose logs api

# Hoia konteiner elus debugimiseks
services:
  api:
    command: tail -f /dev/null  # Ajutine käsk
    # Originaal: command: npm start
```

---

## 📖 Praktiline näide: Multi-tier rakendus

Ehitame päris töötava blog rakenduse koos kõigi komponentidega:

```mermaid
graph TB
    subgraph "🌐 Blog Application Architecture"
        subgraph "Frontend Layer"
            User[👤 User Browser]
            Nginx[🌐 Nginx<br/>Reverse Proxy<br/>:80]
        end
        
        subgraph "Application Layer"
            API[⚙️ Node.js API<br/>Business Logic<br/>:3000]
            Worker[👷 Background Worker<br/>Email, notifications]
        end
        
        subgraph "Data Layer"
            Postgres[🗄️ PostgreSQL<br/>Main Database<br/>:5432]
            Redis[⚡ Redis<br/>Cache & Sessions<br/>:6379]
            S3[☁️ MinIO<br/>File Storage<br/>:9000]
        end
        
        subgraph "Monitoring"
            Grafana[📊 Grafana<br/>Dashboards<br/>:3001]
            Prometheus[📈 Prometheus<br/>Metrics<br/>:9090]
        end
    end
    
    User --> Nginx
    Nginx --> API
    API --> Postgres
    API --> Redis
    API --> S3
    Worker --> Postgres
    Worker --> Redis
    Prometheus --> API
    Grafana --> Prometheus
    
    style User fill:#ffcc99
    style Nginx fill:#99ccff
    style API fill:#99ff99
    style Worker fill:#99ff99
    style Postgres fill:#ffcc99
    style Redis fill:#ff99ff
    style S3 fill:#ccffff
    style Grafana fill:#ccccff
    style Prometheus fill:#ccccff
```

### Täielik docker-compose.yml

```yaml
version: '3.8'

services:
  # Reverse proxy - kõik liiklus tuleb siit läbi
  nginx:
    image: nginx:alpine
    container_name: blog_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - static_content:/usr/share/nginx/html/static:ro
    depends_on:
      - api
    networks:
      - frontend_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # API server - põhiline äriloogika
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
      args:
        NODE_VERSION: 16
    container_name: blog_api
    environment:
      NODE_ENV: ${NODE_ENV:-development}
      PORT: 3000
      DATABASE_URL: postgres://${DB_USER}:${DB_PASS}@postgres:5432/${DB_NAME}
      REDIS_URL: redis://:${REDIS_PASS}@redis:6379
      S3_ENDPOINT: http://minio:9000
      S3_ACCESS_KEY: ${S3_ACCESS_KEY}
      S3_SECRET_KEY: ${S3_SECRET_KEY}
      JWT_SECRET: ${JWT_SECRET}
      EMAIL_SMTP_HOST: ${EMAIL_SMTP_HOST}
      EMAIL_SMTP_PORT: ${EMAIL_SMTP_PORT}
    volumes:
      - ./api/src:/app/src:ro
      - static_content:/app/public/static
      - api_logs:/app/logs
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      minio:
        condition: service_started
    networks:
      - frontend_network
      - backend_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Background worker - async töötlus
  worker:
    build:
      context: ./api
      dockerfile: Dockerfile.worker
    container_name: blog_worker
    environment:
      NODE_ENV: ${NODE_ENV:-development}
      DATABASE_URL: postgres://${DB_USER}:${DB_PASS}@postgres:5432/${DB_NAME}
      REDIS_URL: redis://:${REDIS_PASS}@redis:6379
      S3_ENDPOINT: http://minio:9000
      S3_ACCESS_KEY: ${S3_ACCESS_KEY}
      S3_SECRET_KEY: ${S3_SECRET_KEY}
    volumes:
      - ./api/src:/app/src:ro
      - worker_logs:/app/logs
    depends_on:
      - postgres
      - redis
    networks:
      - backend_network
    restart: unless-stopped

  # PostgreSQL - põhiandmebaas
  postgres:
    image: postgres:14-alpine
    container_name: blog_postgres
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASS}
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=C"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/01-init.sql:ro
      - ./database/seed.sql:/docker-entrypoint-initdb.d/02-seed.sql:ro
      - postgres_backups:/backups
    networks:
      - backend_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    ports:
      - "5432:5432"  # Ainult development jaoks!

  # Redis - cache ja sessions
  redis:
    image: redis:7-alpine
    container_name: blog_redis
    command: >
      redis-server
      --requirepass ${REDIS_PASS}
      --appendonly yes
      --appendfilename "redis.aof"
      --maxmemory 256mb
      --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - backend_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "--auth", "${REDIS_PASS}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # MinIO - S3-compatible file storage
  minio:
    image: minio/minio:latest
    container_name: blog_minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${S3_ACCESS_KEY}
      MINIO_ROOT_PASSWORD: ${S3_SECRET_KEY}
    volumes:
      - minio_data:/data
    networks:
      - backend_network
    ports:
      - "9000:9000"  # API
      - "9001:9001"  # Console
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  # Prometheus - metrics collection
  prometheus:
    image: prom/prometheus:latest
    container_name: blog_prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - backend_network
      - monitoring_network
    ports:
      - "9090:9090"
    restart: unless-stopped

  # Grafana - visualization
  grafana:
    image: grafana/grafana:latest
    container_name: blog_grafana
    environment:
      GF_SECURITY_ADMIN_USER: ${GRAFANA_USER}
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASS}
      GF_INSTALL_PLUGINS: redis-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources:ro
    networks:
      - monitoring_network
    ports:
      - "3001:3000"
    restart: unless-stopped
    depends_on:
      - prometheus

# Võrgud
networks:
  frontend_network:
    driver: bridge
    name: blog_frontend
    
  backend_network:
    driver: bridge
    internal: true  # Pole väliselt kättesaadav
    name: blog_backend
    
  monitoring_network:
    driver: bridge
    name: blog_monitoring

# Püsivad andmed
volumes:
  postgres_data:
    driver: local
  postgres_backups:
    driver: local
  redis_data:
    driver: local
  minio_data:
    driver: local
  static_content:
    driver: local
  api_logs:
    driver: local
  worker_logs:
    driver: local
  prometheus_data:
    driver: local
  grafana_data:
    driver: local
```

### Environment failid

`.env.development`:

```bash
# Node
NODE_ENV=development

# Database
DB_NAME=blog_dev
DB_USER=developer
DB_PASS=dev123456

# Redis
REDIS_PASS=redis123456

# S3/MinIO
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin123

# Security
JWT_SECRET=devsecret123456789

# Email (Mailhog for development)
EMAIL_SMTP_HOST=mailhog
EMAIL_SMTP_PORT=1025

# Monitoring
GRAFANA_USER=admin
GRAFANA_PASS=admin123
```

`.env.production`:

```bash
# Node
NODE_ENV=production

# Database
DB_NAME=blog_prod
DB_USER=blog_app
DB_PASS=${SECURE_DB_PASSWORD}  # From CI/CD secrets

# Redis
REDIS_PASS=${SECURE_REDIS_PASSWORD}

# S3
S3_ACCESS_KEY=${AWS_ACCESS_KEY_ID}
S3_SECRET_KEY=${AWS_SECRET_ACCESS_KEY}

# Security
JWT_SECRET=${SECURE_JWT_SECRET}

# Email
EMAIL_SMTP_HOST=smtp.sendgrid.net
EMAIL_SMTP_PORT=587

# Monitoring
GRAFANA_USER=admin
GRAFANA_PASS=${SECURE_GRAFANA_PASSWORD}
```

### Käivitamine ja haldamine

```bash
# Arenduses - kõik logid nähtaval
docker-compose --env-file .env.development up

# Või taustal
docker-compose --env-file .env.development up -d

# Jälgi logisid
docker-compose logs -f api worker

# Skaleeri API servereid (arenduses testimiseks)
docker-compose up -d --scale api=3

# Backup andmebaas
docker-compose exec postgres pg_dump -U developer blog_dev > backup.sql

# Restore andmebaas
docker-compose exec -T postgres psql -U developer blog_dev < backup.sql

# Puhasta kõik ja alusta nullist
docker-compose down -v
docker-compose up --build

# Produktsioonis
docker-compose --env-file .env.production -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 📖 Best practices ja production nõuanded

### Turvalisus

```mermaid
graph TD
    subgraph "🔒 Security Layers"
        Secrets[🔑 Secrets Management<br/>Never in code]
        Network[🌐 Network Isolation<br/>Internal networks]
        MinPriv[👤 Min Privileges<br/>Non-root users]
        Scanning[🔍 Image Scanning<br/>Check vulnerabilities]
        Updates[🔄 Regular Updates<br/>Keep images fresh]
    end
    
    Secrets --> Network
    Network --> MinPriv
    MinPriv --> Scanning
    Scanning --> Updates
    
    style Secrets fill:#ff9999
    style Network fill:#ffcc99
    style MinPriv fill:#ffff99
    style Scanning fill:#99ff99
    style Updates fill:#99ccff
```

1. **Ärge kunagi pange paroole koodis:**

```yaml
# ❌ Vale
environment:
  DB_PASSWORD: mysecretpassword

# ✅ Õige
environment:
  DB_PASSWORD: ${DB_PASSWORD}
```

2. **Kasutage Docker secrets (Swarm mode):**

```yaml
services:
  api:
    secrets:
      - db_password
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    external: true
```

3. **Käivitage konteinerid non-root kasutajana:**

```dockerfile
# Dockerfile
FROM node:16-alpine
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs
```

4. **Isoleerige võrgud:**

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # Pole internetist kättesaadav
```

### Performance

1. **Kasutage multi-stage build'e:**

```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
CMD ["node", "server.js"]
```

2. **Määrake ressursipiirangud:**

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

3. **Kasutage health check'e ja restart policy't:**

```yaml
services:
  api:
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Logging ja monitoring

```yaml
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service=api,env=production"
```

---

## 📖 Alternatiivid ja edasine õppimine

### Docker Swarm

Docker'i enda clustering lahendus. Lihtsam kui Kubernetes:

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml myapp

# Scale service
docker service scale myapp_api=5

# Update service
docker service update --image myapp/api:v2 myapp_api
```

### Kubernetes (K8s)

Industry standard orkestreerimiseks, aga palju keerulisem:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: myapp/api:latest
        ports:
        - containerPort: 3000
```

### Podman Compose

Rootless alternatiiv Docker'ile:

```bash
# Sama syntax nagu Docker Compose
podman-compose up

# Podman genereerib systemd unit faile
podman generate systemd --new --name myapp > myapp.service
```

---

## 🎯 Kokkuvõte ja järgmised sammud

### Mida me õppisime

Oleme õppinud kuidas:
- Kirjutada Docker Compose faile multi-container rakendustele
- Hallata teenuste vahelisi sõltuvusi ja suhtlust
- Seadistada erinevaid keskkondi (dev/prod)
- Debuggida ja tõrkeotsingut teha
- Rakendada best practices'eid ja turvalisust

### Harjutused iseseisvaks tööks

1. **Lihtne harjutus**: Looge WordPress + MySQL setup
2. **Keskmine harjutus**: Lisage Redis cache ja Nginx reverse proxy
3. **Raske harjutus**: Lisage monitoring Prometheus + Grafana'ga
4. **Expert harjutus**: Migrate to Kubernetes

### Millal kasutada mida?

```mermaid
graph TD
    Start[Vajan orkestreerimist]
    Single{Üks masin?}
    Complex{Keeruline?}
    Scale{Auto-scale?}
    
    Start --> Single
    Single -->|Jah| Complex
    Single -->|Ei| K8s[Kubernetes]
    
    Complex -->|Ei| Compose[Docker Compose]
    Complex -->|Jah| Scale
    
    Scale -->|Ei| Swarm[Docker Swarm]
    Scale -->|Jah| K8s
    
    style Compose fill:#99ff99
    style Swarm fill:#ffcc99
    style K8s fill:#ff9999
```

**Lihtne reegel**: Alusta Docker Compose'iga. Kui jõuad selle piiranguteni, siis mõtle edasi liikumisele.

### Viimane soovitus

Orkestreerimine pole rakettide ehitamine. Alusta lihtsast, õpi põhimõtted selgeks, ja lisa keerukust ainult siis kui päriselt vajad. Docker Compose on piisav 90% projektidest. Ära mine Kubernetese juurde ainult sellepärast, et see on "cool" - mine siis kui sul on päris vajadus.

Edu ja julgust konteinerite maailmas!
