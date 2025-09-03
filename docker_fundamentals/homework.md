# 📝 Nädal 19 Kodutöö: Süsteemi Oleku Dashboard Deployment

**Tähtaeg:** Järgmise nädala alguseks  
**Eesmärk:** Õppida Docker ja Podman container'ite kasutamist praktikas  
**Aeg:** 2-3 tundi (võib olla keeruline, aga jõukohane)

**Te saate valmis veebisaidi - keskenduge container tehnoloogiate õppimisele!**

---

## 🖥️ **Projekt: Süsteemi Oleku Dashboard**

**Mida see teeb:**
- Näitab container informatsiooni
- Kuvab serveri olekut
- Võimaldab testida connectivity
- Eristab Docker vs Podman deployment

**Mida te õpite:**
- Docker ja Podman deployment
- Environment variables kasutamine  
- Container networking
- docker-compose orchestration

---

## 📁 **Samm 1: Kloonige starter repository**

### 1.1 Kloonige kodutöö starter repository

```bash
# Clone valmis starter repository
git clone https://github.com/teacher/docker-dashboard-starter.git
cd docker-dashboard-starter

# Loo oma branch
git checkout -b homework-TEIE-NIMI

# Näiteks: git checkout -b homework-maria-talvik
```

**Mida me saime?**
- Valmis HTML dashboard
- Dockerfile template
- docker-compose.yml
- nginx.conf konfiguratsioon
- README dokumentatsioon

**Ei pea ise kirjutama - fookus container'itel!**

### 1.2 Tutvuge starter failidega

**Kontrollige, mis failid on olemas:**
```bash
ls -la
# Peaksite nägema:
# index.html - Dashboard rakendus
# Dockerfile - Container juhised
# docker-compose.yml - Multi-container setup
# nginx.conf - Web server config
# README.md - Dokumentatsioon
```

**`index.html` on valmis dashboard rakendus** - see näitab:
- Container runtime info (Docker/Podman)
- Süsteemi olek ja uptime
- Interaktiivsed nupud testimiseks
- Responsive disain

### 1.3 Testage starter rakendust brauseris

```bash
# Avage index.html otse brauseris (ilma container'ita)
open index.html
# Või Linux'is: firefox index.html

# Dashboard peaks avanema ja näitama:
# - Süsteemi oleku info
# - Container runtime: "Unknown" 
# - Interactive buttons töötavad
```

**Mida need failid teevad?**
- `index.html` - Dashboard rakendus (juba valmis!)
- `Dockerfile` - Container ehitamise juhised
- `docker-compose.yml` - Mitme-container haldamine
- `nginx.conf` - Veebserveri täpsemad seadistused

---

## 🔧 **Samm 2: Docker container loomine**

### 2.1 Tutvuge Dockerfile'iga

**Vaadake olemas olevat `Dockerfile` faili:**
```bash
cat Dockerfile
```

**Dockerfile sisu ja selgitus:**
```dockerfile
FROM nginx:alpine              # Kasutame nginx web server'it
COPY index.html /usr/share/nginx/html/   # Kopeerime HTML faili
COPY nginx.conf /etc/nginx/conf.d/default.conf  # Custom config
EXPOSE 80                      # Container port 80
```

**Mida see teeb:**
- Alustab nginx serveriga (väike Alpine Linux)
- Kopeerib meie HTML faili õigesse kohta
- Lisab custom nginx konfiguratsiooni
- Avab port 80 HTTP liikluseks

### 2.2 Testige Docker build

```bash
# Ehitage container image
docker build -t my-dashboard .

# Mida see käsk teeb?
# - Loeb Dockerfile faili
# - Laadib nginx:alpine image
# - Kopeerib index.html faili
# - Loob uue image nimega "my-dashboard"

# Kontrollige, et image on loodud
docker images | grep my-dashboard
```

### 2.3 Esimene commit oma branch'iga

```bash
# Commit esialgsed muudatused (kui tegite mõnda)
git add .
git commit -m "Alustasin kodutööd: kontrollisin starter failid ja Docker build"

# Push oma branch GitHub'i
git push origin homework-TEIE-NIMI

# Miks me commit'ime?
# - Salvestame oma töö progressi
# - Näitame, et alustasime tööd
# - Saame tagasi minna kui midagi läheb valesti
```

---

## 🐳 **Samm 3: Container'ite käivitamine**

### 3.1 Docker'iga deploy

```bash
# Käivitage container
docker run -d --name my-docker-app -p 8080:80 my-dashboard

# Mida see käsk teeb?
# -d = detached mode (taustal)
# --name = anname container'ile nime "my-docker-app"
# -p 8080:80 = ühendame host port 8080 → container port 80
# my-dashboard = kasutame meie loodud image't

# Kontrollige, et container töötab
docker ps

# Testidige brauseris
echo "Avage brauser: http://localhost:8080"
```

### 3.2 Podman'iga deploy

```bash
# Ehitage image Podman'iga
podman build -t my-dashboard-podman .

# Käivitage Podman container
podman run -d --name my-podman-app -p 8081:80 my-dashboard-podman

# Kontrollige Podman container'eid
podman ps

# Testidige brauseris
echo "Avage brauser: http://localhost:8081"
```

**Docker vs Podman erinevused:**
- Docker vajab daemon'it (background service)
- Podman töötab ilma daemon'ita
- Käsud on peaaegu identilised
- Mõlemad kasutavad sama container format

### 3.3 Docker-compose kasutamine

**Looge `docker-compose.yml` fail:**
```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8080:80"
    container_name: compose-dashboard
```

**Käivitage docker-compose'iga:**
```bash
# Ehitage ja käivitage
docker-compose up -d

# Mida see teeb?
# - Loeb docker-compose.yml faili
# - Ehitab image kui vaja
# - Käivitab container'i
# - Seadistab networking automaatselt

# Kontrollige
docker-compose ps

# Testidige: http://localhost:8080
```

### 3.4 Commit oma edu

```bash
git add docker-compose.yml
git commit -m "Docker ja Podman deployment töötab - mõlemad testitud"
```

---

## 📊 **Samm 4: Container'ite haldamine**

### 4.1 Container'ite info vaatamine

```bash
# Vaadake kõiki töötavaid container'eid
docker ps

# Vaadake container'i logisid
docker logs my-docker-app

# Sisenege container'isse (debugging)
docker exec -it my-docker-app sh

# Container'ist väljumine
exit
```

**Mida need käsud teevad?**
- `docker ps` - näitab töötavaid container'eid
- `docker logs` - näitab container'i väljundit
- `docker exec -it` - lubab container'isse siseneda

### 4.2 Container'ite peatamine ja kustutamine

```bash
# Peatage container
docker stop my-docker-app

# Kustutage container
docker rm my-docker-app

# Teha mõlemat korraga
docker rm -f my-docker-app

# Kustutage ka image (kui vaja)
docker rmi my-dashboard
```

### 4.3 Docker-compose haldamine

```bash
# Vaadake docker-compose staatust
docker-compose ps

# Vaadake logisid
docker-compose logs

# Peatage kõik teenused
docker-compose down

# Käivitage uuesti
docker-compose up -d
```

### 4.4 Ressursside kasutus

```bash
# Vaadake container'ite ressursside kasutust
docker stats

# Vaadake Docker disk kasutust
docker system df

# Puhastage unused resources
docker system prune -f
```

**Commit haldamise oskused:**
```bash
git add .
git commit -m "Õppisin container'ite haldamist - start, stop, logs, cleanup"
```

---

## 📋 **Samm 5: Lõplik dokumentatsioon (10 min)**

### 5.1 Muutke README.md faili

**Fail: `README.md`** (kopeerige ja täitke oma andmed):
```markdown
# System Status Dashboard - [TEIE NIMI]

## Mis see on?
System Status Dashboard on veebirakendus, mis näitab container informatsiooni,
süsteemi olekut ja võimaldab testida erinevaid operations.

## Kuidas käivitada?

### Docker'iga:
```bash
docker build -t dashboard .
docker run -d -p 8080:80 dashboard
# Avage: http://localhost:8080?type=Docker
```

### Podman'iga:
```bash
podman build -t dashboard .
podman run -d -p 8081:80 dashboard  
# Avage: http://localhost:8081?type=Podman
```

### Docker-compose'iga:
```bash
docker-compose up -d
# Docker: http://localhost:8080?type=Docker
# Podman: http://localhost:8081?type=Podman
```

## Funktsioonid
- System status monitoring
- Container runtime detection
- Interactive operations testing
- Real-time uptime counter
- Health check endpoint
- Custom nginx configuration

## Keskkonnamuutujad
| Muutuja | Kirjeldus |
|----------|-------------|
| `CONTAINER_TYPE` | Näitab Docker või Podman |
| `DEPLOY_DATE` | Millal container deployiti |

## Tervise kontroll
Külastage `/health` endpoint'i container'i tervise staatuse kontrollimiseks.

## Ekraanipildid
[Lisage oma screenshot'id siia]

## Mida ma õppisin
- [Teie kogemus 1]
- [Teie kogemus 2] 
- [Teie kogemus 3]

## Probleemid ja lahendused
**Probleem:** [Kirjeldage probleem mis teil tekkis]  
**Lahendus:** [Kuidas te selle lahendasite]
```

### 5.2 Tehke screenshot'id

**Vajalikud screenshot'id:**
1. Dashboard töötab Docker'is: `http://localhost:8080?type=Docker`
2. Dashboard töötab Podman'is: `http://localhost:8081?type=Podman`  
3. Terminal output: `docker ps` ja `podman ps`
4. Tervise kontrolli test: `curl http://localhost:8082/health`

**Salvestage screenshot'id `screenshots/` kausta.**

---

### 5.2 Lõplik push oma branch'iga

```bash
# Veenduge, et kõik on commit'itud
git add .
git commit -m "Lõplik esitamine: Docker kodutöö valmis - kõik containerid testitud"

# Push final version
git push origin homework-TEIE-NIMI

# GitHub'is saate luua Pull Request õpetajale
# Teacher repository → Pull Requests → New Pull Request
```

---

## 📋 **Esitamise nõuded**

### **Repository peab sisaldama:**

```
docker-fundamentals-homework/
├── README.md                    # Projekti kirjeldus
├── index.html                   # Veebisaidi fail
├── Dockerfile                   # Container definitsioon
├── docker-compose.yml           # Multi-container setup
└── screenshots/ (valikuline)    # Töötavate container'ite pildid
```

### **Esitamine:**
1. **GitHub Pull Request link** esitage õppetoolis
2. **Oma branch** teacher repository's: `homework-TEIE-NIMI`
3. **Töötav demonstratsioon** - õpetaja saab checkout'ida ja testida

### **Repository peab näitama:**
- **Töötav rakendus Docker'is**
- **Töötav rakendus Podman'is**
- **docker-compose setup**
- **Selge dokumentatsioon README.md's**
- **Git commit history näitab progressi**

 