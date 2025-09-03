# 🧪 Nädal 21 Lab: Docker Compose Praktika

**Kestus:** 2 tundi  
**Eesmärk:** Õppida Docker Compose'i praktilist kasutamist ja luua lihtsa multi-container rakenduse

## 🎯 Samm 1: Õpiväljundid

Pärast laborit oskate:
- **Kirjutada lihtsa Docker Compose faili** - põhilised teenused
- **Käivitada multi-container rakendust** - ühe käsuga
- **Mõista teenuste sõltuvusi** - mis käivitub enne
- **Debugida probleeme** - logide vaatamine
- **Kasutada dokumentatsiooni** - abi leidmine

---

## 📋 Samm 1: Lihtsa rakenduse loomine (45 min)

### 1.1: Projekti struktuuri loomine

**Loome lihtsa web rakenduse, mis koosneb kahest osast:**
- **Web server** - kuvab veebilehte
- **Database** - salvestab andmeid

```bash
# Projekti kataloogi loomine
mkdir ~/docker-orchestration-lab
cd ~/docker-orchestration-lab

# Lihtne struktuur
mkdir app
```

### 1.2: Lihtsa web rakenduse loomine

**Kopeerime valmis HTML faili teacher_repo'st:**

```bash
# Kopeerige valmis HTML fail
cp teacher_repo/docker-orchestration-starter/templates/app/frontend/index.html.example app/index.html
```

**Mida see teeb?**
- Kuvab lihtsa veebilehe
- Näitab, et rakendus töötab
- Kuvab praeguse aja

**Miks me ei kirjuta HTML koodi?**
See on automation kursus, mitte veebiarenduse kursus. Me keskendume Docker Compose'i õppimisele, mitte HTML kirjutamisele.

### 1.3: Docker Compose faili loomine

**Kopeerime valmis Docker Compose faili teacher_repo'st:**

```bash
# Kopeerige valmis Docker Compose fail
cp teacher_repo/docker-orchestration-starter/templates/docker-compose.yml.example docker-compose.yml
```

**Mida see teeb?**
- **Web teenus** - kuvab HTML faili brauseris
- **Database teenus** - salvestab andmeid (praegu ei kasuta)

**Miks me ei kirjuta Docker Compose faili?**
See on lihtne lab, kus õpime Docker Compose'i kasutamist. Hiljem õpite ka failide kirjutamist.
- **Volumes** - püsivad andmed andmebaasi jaoks
            host=os.getenv('REDIS_HOST', 'redis'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )
        r.ping()
        return r
    except Exception as e:
        return None

@app.route('/api/status')
def status():
    db_status = "Connected" if get_db_connection() else "Disconnected"
    redis_status = "Connected" if get_redis_connection() else "Disconnected"
    
    return jsonify({
        'status': 'OK',
        'environment': os.getenv('NODE_ENV', 'development'),
        'database': db_status,
        'cache': redis_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('DEBUG', 'false').lower() == 'true')
```

**Backend requirements (app/backend/requirements.txt):**
```
Flask==2.3.3
psycopg2-binary==2.9.7
redis==4.6.0
```

### 1.4: Docker Compose konfiguratsioon

**Base configuration (docker-compose.yml):**
```yaml
version: '3.8'

services:
  frontend:
    image: nginx:alpine
    ports:
      - "${FRONTEND_PORT:-80}:80"
    volumes:
      - ./app/frontend:/usr/share/nginx/html:ro
    depends_on:
      - backend
    networks:
      - frontend

  backend:
    build:
      context: ./app/backend
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - DEBUG=${DEBUG:-false}
      - DB_HOST=db
      - DB_NAME=${DB_NAME:-app}
      - DB_USER=${DB_USER:-postgres}
      - DB_PASSWORD=${DB_PASSWORD:-secret}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - db
      - redis
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=${DB_NAME:-app}
      - POSTGRES_USER=${DB_USER:-postgres}
      - POSTGRES_PASSWORD=${DB_PASSWORD:-secret}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

volumes:
  postgres_data:
  redis_data:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

**Backend Dockerfile (app/backend/Dockerfile):**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### 1.5: Rakenduse käivitamine

**Käivitage rakendus:**
```bash
# Käivita kõik teenused
docker-compose up -d

# Vaata, kas kõik töötab
docker-compose ps

# Vaata logisid
docker-compose logs web
```

**Testige rakendust:**
- Avage brauser ja minge aadressile: `http://localhost:8080`
- Peaksite nägema veebilehte "🚀 Week 21 Lab"

**Peatage rakendus:**
```bash
# Peata kõik teenused
docker-compose down
```

---

## 📋 Samm 2: Probleemide lahendamine (30 min)

### 2.1: Levinud probleemid ja lahendused

**Probleem: Port on juba kasutusel**
```bash
# Vea sõnum: "port is already allocated"
# Lahendus: Muutke porti docker-compose.yml failis
ports:
  - "8081:80"  # 8080 asemel 8081
```

**Probleem: Container ei käivitu**
```bash
# Vaata logisid
docker-compose logs web

# Vaata kõiki logisid
docker-compose logs
```

**Probleem: Fail ei leia**
```bash
# Kontrollige, kas fail eksisteerib
ls -la app/index.html

# Kontrollige faili õigused
chmod 644 app/index.html
```

### 2.2: Debugimise käsud

```bash
# Vaata kõiki container'eid
docker ps

# Vaata container'i sisu
docker exec -it docker-orchestration-lab_web_1 sh

# Vaata faili sisu container'is
docker exec docker-orchestration-lab_web_1 cat /usr/share/nginx/html/index.html
```

### 2.3: Podman Compose konfiguratsioon

**Podman-specific docker-compose.yml:**
```yaml
version: '3.8'

services:
  frontend:
    image: nginx:alpine
    ports:
      - "${FRONTEND_PORT:-80}:80"
    volumes:
      - ./app/frontend:/usr/share/nginx/html:ro
    depends_on:
      - backend
    networks:
      - frontend

  backend:
    build:
      context: ./app/backend
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - DEBUG=${DEBUG:-false}
      - DB_HOST=db
      - DB_NAME=${DB_NAME:-app}
      - DB_USER=${DB_USER:-postgres}
      - DB_PASSWORD=${DB_PASSWORD:-secret}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - db
      - redis
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=${DB_NAME:-app}
      - POSTGRES_USER=${DB_USER:-postgres}
      - POSTGRES_PASSWORD=${DB_PASSWORD:-secret}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

volumes:
  postgres_data:
  redis_data:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

### Samm 3: Podman Compose käivitamine

```bash
# Peatage Docker Compose teenused
docker-compose down

# Käivitage Podman Compose
podman-compose --env-file .env.development up -d

# Kontrollige teenuseid
podman-compose ps

# Vaadake logisid
podman-compose logs -f backend

# Testige rakendust
curl http://localhost:8080/api/status
```

---

## 📋 Samm 3: Võrdlus ja Analüüs (30 min)

### Samm 1: Performance võrdlus

```bash
# Docker Compose resource usage
docker stats

# Podman resource usage
podman stats

# Võrdle mälu ja CPU kasutust
```

### Samm 2: Security võrdlus

```bash
# Docker process info
ps aux | grep docker

# Podman process info
ps aux | grep podman

# User context
docker ps
podman ps
```

### Samm 3: Logide ja monitoring

```bash
# Docker Compose logid
docker-compose logs --tail=50

# Podman Compose logid
podman-compose logs --tail=50

# Võrdle logide formaati ja sisu
```

---

## 🎯 Samm 2: Labori Kokkuvõte

### Õpitud kontseptsioonid:

**Docker Compose faili kirjutamine** - lihtne YAML süntaks
**Multi-container rakenduse käivitamine** - ühe käsuga
**Teenuste haldamine** - käivitamine, peatamine, logide vaatamine
**Probleemide lahendamine** - debugimise oskused
**Dokumentatsiooni kasutamine** - abi leidmine  

### Järgmised sammud:

1. **Rohkem teenuseid** - lisage backend ja cache
2. **Environment variables** - erinevate keskkondade haldamine
3. **Production setup** - turvaline ja skaleeritav konfiguratsioon
4. **Kubernetes** - kui vajate rohkem funktsionaalsust

---

## 🔧 Troubleshooting

### Levinud probleemid:

**Probleem:** Teenused ei käivitu õiges järjekorras
```bash
# Lahendus: Lisa health checks ja depends_on
depends_on:
  db:
    condition: service_healthy
```

**Probleem:** Podman network error
```bash
# Lahendus: Lisa selgesõnaline network konfiguratsioon
networks:
  default:
    driver: bridge
```

**Probleem:** Volume permissions
```bash
# Lahendus: Lisa user mapping
services:
  db:
    user: "1000:1000"
```

---

## 📚 Lisaressursid ja abi

### 🎓 **Õppimiseks:**
- [Docker Compose Quickstart](https://docs.docker.com/compose/gettingstarted/) - kiire algus
- [Docker Compose Examples](https://github.com/docker/awesome-compose) - palju näiteid
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/) - kõik võimalikud seaded

### 🆘 **Abi saamiseks:**
- [Docker Community](https://forums.docker.com/) - foorumid
- [Stack Overflow](https://stackoverflow.com/questions/tagged/docker-compose) - küsimused ja vastused
- [Docker Documentation](https://docs.docker.com/) - ametlik dokumentatsioon

### 🔧 **Praktikaks:**
- [Docker Compose Best Practices](https://docs.docker.com/compose/production/) - tootmiskeskkonna nõuded
- [Docker Compose Networking](https://docs.docker.com/compose/networking/) - võrgu konfiguratsioon
- [Docker Compose Environment Variables](https://docs.docker.com/compose/environment-variables/) - keskkonnamuutujad
