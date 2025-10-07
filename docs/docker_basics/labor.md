# Docker Labor

**Eeldused:** Loeng läbitud, Docker installitud  
**Platvorm:** Docker (Ubuntu/Debian või Docker Desktop)

Labor keskendub praktilisele Docker'i kasutamisele. Loote image'eid, käivitate container'eid ja haldate volume'eid. Töö võtab umbes 2-3 tundi.

---

## Õpiväljundid

Pärast seda labor'it oskad:

- **Käivitada ja hallata container'eid**
  - `run`, `stop`, `logs`, `exec` käsud
- **Kirjutada Dockerfile'i**
  - image loomine nullist
- **Kasutada volume'eid**
  - andmete säilitamine
- **Luua Docker network'e**
  - container'ite vaheline suhtlus
- **Debug'ida probleeme**
  - logide vaatamine, container'isse sisenemine

---

## 1. Docker Installatsiooni Kontrollimine

Kontrollige, et Docker on installitud ja töötab:
```bash
docker --version
docker info
```

Oodatav tulemus: versiooninumber (20.10+) ja süsteemi info ilma vigadeta.

Kui Docker nõuab `sudo`:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

**Validation:** Käivitage testimiseks:
```bash
docker run hello-world
```

Peaksite nägema "Hello from Docker!" sõnumit.

---

## 2. Esimesed Container'id

### 2.1 Nginx Web Server

Käivitage Nginx container:
```bash
docker run -d --name web -p 8080:80 nginx
```

Käsu selgitus:
- `-d` - detached mode (taustal)
- `--name web` - annab container'ile nime
- `-p 8080:80` - port mapping (host:container)
- `nginx` - image nimi

**Validation:** Avage brauseris `http://localhost:8080` - peaksite nägema Nginx tervituslehte.

### 2.2 Container'ite Vaatamine
```bash
# Töötavad container'id
docker ps

# Kõik container'id
docker ps -a

# Container detailid
docker inspect web

# Ressursikasutus
docker stats web --no-stream
```

### 2.3 Logide Vaatamine
```bash
# Vaata logisid
docker logs web

# Follow logs (ctrl+C väljumiseks)
docker logs -f web

# Viimased 10 rida
docker logs --tail 10 web
```

**Validation:** Refresh'ige brauserit ja vaadake `docker logs web` - näete GET päringu logis.

### 2.4 Container'isse Sisenemine
```bash
# Käivita bash container'is
docker exec -it web bash

# Container'is:
ls /usr/share/nginx/html/
cat /etc/nginx/nginx.conf
exit
```

### 2.5 Container'i Peatamine ja Kustutamine
```bash
docker stop web
docker rm web

# Või ühel käsul (force)
docker rm -f web
```

---

## 3. Image'ide Loomine

### 3.1 Lihtsa HTML Rakenduse Loomine

Looge töökaust:
```bash
mkdir docker-web-app
cd docker-web-app
```

Looge fail `index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Docker Lab</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f0f0f0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Docker Labor</h1>
        <p>Tudeng: <strong>[TEIE NIMI]</strong></p>
        <p>Kuupäev: <span id="date"></span></p>
        <p>Container ID: <span id="hostname"></span></p>
    </div>
    <script>
        document.getElementById('date').innerText = new Date().toLocaleString();
        fetch('/hostname')
            .then(r => r.text())
            .then(h => document.getElementById('hostname').innerText = h)
            .catch(() => document.getElementById('hostname').innerText = 'N/A');
    </script>
</body>
</html>
```

Asendage `[TEIE NIMI]` oma nimega.

### 3.2 Dockerfile Kirjutamine

Looge fail `Dockerfile`:
```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Käskude selgitus:
- `FROM` - base image (nginx alpine versioon, 23MB)
- `COPY` - kopeeri HTML fail container'isse
- `EXPOSE` - dokumentatsioon portide kohta
- `CMD` - vaikimisi käsk

### 3.3 Image'i Ehitamine
```bash
docker build -t minu-web:v1 .
```

Näete build protsessi:
```
[+] Building 2.3s (7/7) FINISHED
=> [internal] load build definition
=> [internal] load .dockerignore
=> [1/2] FROM nginx:alpine
=> [2/2] COPY index.html /usr/share/nginx/html/
=> exporting to image
=> naming to docker.io/library/minu-web:v1
```

**Validation:**
```bash
# Kontrolli, et image loodi
docker images | grep minu-web

# Käivita container'isse
docker run -d -p 8081:80 --name minu-app minu-web:v1
```

Avage `http:
- //localhost:8081`
- peaks näitama teie HTML lehte.

### 3.4 Image'i Modifitseerimine

Muutke `index.html` faili - lisage midagi uut. Ehitage uus versioon:
```bash
docker build -t minu-web:v2 .
docker run -d -p 8082:80 --name minu-app-v2 minu-web:v2
```

**Validation:** Avage `http://localhost:8082` - näete uut versiooni.

Võrrelge image'ide suurusi:
```bash
docker images | grep minu-web
```

---

## 4. Dockerfile Optimeerimine

### 4.1 Layer Caching Näide

Looge kaust Python rakendusele:
```bash
mkdir docker-python-app
cd docker-python-app
```

Looge `app.py`:
```python
from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return f'''
    <h1>Docker Lab - Python</h1>
    <p>Aeg: {datetime.datetime.now()}</p>
    <p>Python rakendus container'is</p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Looge `requirements.txt`:
```
Flask==3.0.0
```

### 4.2 Algne Dockerfile (Optimeerimata)

Looge `Dockerfile.bad`:
```dockerfile
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
```

Ehitage:
```bash
docker build -t python-app:bad -f Dockerfile.bad .
```

Muutke `app.py` faili (lisage kommentaar). Ehitage uuesti ja jälgige, et `pip install` käivitatakse uuesti, kuigi `requirements.txt` ei muutunud.

### 4.3 Optimeeritud Dockerfile

Looge `Dockerfile`:
```dockerfile
FROM python:3.11-alpine

WORKDIR /app

# Kopeeri requirements enne koodi
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Nüüd kopeeri kood
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Ehitage:
```bash
docker build -t python-app:good .
```

Muutke `app.py` ja ehitage uuesti. Märkige, et `pip install` kasutab cache'i.

**Validation:** Käivitage:
```bash
docker run -d -p 5000:5000 --name python-api python-app:good
curl http://localhost:5000
```

### 4.4 .dockerignore

Looge `.dockerignore`:
```
__pycache__/
*.pyc
*.pyo
*.log
.git/
.env
venv/
```

Ehitage image uuesti ja võrrelge suurust:
```bash
docker build -t python-app:final .
docker images | grep python-app
```

---

## 5. Volumes ja Andmete Säilitamine

### 5.1 Probleem Demonstratsioon
```bash
# Käivita container
docker run -d --name demo-db alpine sh -c 'echo "andmed" > /data/file.txt && sleep 3600'

# Vaata faili
docker exec demo-db cat /data/file.txt

# Kustuta container
docker rm -f demo-db

# Proovi uuesti - andmed kadunud
docker run -d --name demo-db alpine sh -c 'cat /data/file.txt'
docker logs demo-db  # cat: can't open '/data/file.txt'
```

### 5.2 Named Volume
```bash
# Loo volume
docker volume create testdata

# Kasuta volume'i
docker run -d --name demo-vol -v testdata:/data alpine sh -c 'echo "püsivad andmed" > /data/file.txt && sleep 3600'

# Kontrolli
docker exec demo-vol cat /data/file.txt

# Kustuta container
docker rm -f demo-vol

# Loo uus container sama volume'iga
docker run --name demo-vol2 -v testdata:/data alpine cat /data/file.txt
docker logs demo-vol2  # "püsivad andmed"
```

**Validation:** Andmed säilivad!

### 5.3 Bind Mount (Arendus)
```bash
# Loo kaust host'is
mkdir ~/shared-data
echo "host fail" > ~/shared-data/test.txt

# Mount host'i kaust
docker run -d --name bind-test -v ~/shared-data:/app alpine sh -c 'while true; do ls -la /app; sleep 5; done'

# Vaata logisid
docker logs bind-test

# Muuda host'is
echo "muudetud" >> ~/shared-data/test.txt

# Container näeb muudatust kohe
docker exec bind-test cat /app/test.txt
```

### 5.4 PostgreSQL Volume Näide
```bash
# Loo volume
docker volume create pgdata

# Käivita Postgres
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15-alpine

# Oota, kuni postgres valmis
sleep 5

# Loo andmebaas
docker exec postgres psql -U postgres -c "CREATE DATABASE testdb;"

# Peataja container
docker stop postgres
docker rm postgres

# Käivita uuesti
docker run -d \
  --name postgres2 \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15-alpine

sleep 5

# Andmebaas on alles
docker exec postgres2 psql -U postgres -c "\l" | grep testdb
```

---

## 6. Networking

### 6.1 Default Behavior
```bash
# Käivita 2 container'it
docker run -d --name cont1 alpine sleep 3600
docker run -d --name cont2 alpine sleep 3600

# Proovi ping'ida
docker exec cont1 ping -c 2 cont2  # Ebaõnnestub
```

### 6.2 Custom Network
```bash
# Loo network
docker network create mynet

# Vaata network'e
docker network ls

# Käivita container'id samas network'is
docker run -d --name cont3 --network mynet alpine sleep 3600
docker run -d --name cont4 --network mynet alpine sleep 3600

# Nüüd töötab
docker exec cont3 ping -c 2 cont4
```

**Validation:** Ping õnnestub - DNS resolution toimib.

### 6.3 Multi-Container Rakendus
```bash
# Loo network
docker network create webapp

# Postgres
docker run -d \
  --name db \
  --network webapp \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=app \
  postgres:15-alpine

# Redis
docker run -d \
  --name cache \
  --network webapp \
  redis:alpine

# Kontrolli connectivity
docker run --rm --network webapp alpine sh -c 'ping -c 2 db && ping -c 2 cache'
```

---

## 7. Troubleshooting

### 7.1 Container Ei Käivitu
```bash
# Vaata vigasid
docker logs container-name

# Interaktiivne debugimine
docker run -it image-name sh

# Kontrolli image history
docker history image-name
```

### 7.2 Port Ei Ole Kättesaadav
```bash
# Kontrolli port mapping
docker port container-name

# Kontrolli, mis portidel kuulatakse
docker exec container-name netstat -tlnp

# Host'i firewall
sudo ufw status
```

### 7.3 Volume Probleemid
```bash
# Volume asukoht
docker volume inspect volume-name

# Vaata volume sisu (kui bind mount)
ls -la /var/lib/docker/volumes/volume-name/_data/

# Permissions
docker exec container-name ls -la /mounted/path/
```

---

## 8. Cleanup

### 8.1 Puhastamine
```bash
# Peata kõik container'id
docker stop $(docker ps -q)

# Kustuta kõik container'id
docker rm $(docker ps -aq)

# Kustuta kasutamata image'd
docker image prune

# Kustuta kasutamata volume'd (ettevaatust!)
docker volume prune

# Kustuta kõik
docker system prune -a --volumes
```

### 8.2 Kettaruumi Vaatamine
```bash
docker system df
docker system df -v
```

---

## Kontrollnimekiri

Kontrollige, et oskate:

- [ ] Käivitada container'i (`docker run`)
- [ ] Vaadata töötavaid container'eid (`docker ps`)
- [ ] Vaadata logisid (`docker logs`)
- [ ] Siseneda container'isse (`docker exec -it`)
- [ ] Kirjutada Dockerfile'i
- [ ] Ehitada image'i (`docker build`)
- [ ] Kasutada volume'eid
- [ ] Luua network'e
- [ ] Debug'ida probleeme

---

## Järgmised Sammud

Labor andis praktilised oskused Docker'i kasutamiseks. Kodutöös rakendage neid teadmisi reaalse rakenduse containeriseerimiseks.

**Näpunäited kodutööks:**
- Alustage lihtsast - esmalt käivitage rakendus, siis optimeeri
- Kasutage `.dockerignore` faili
- Testize image'i enne esitamist
- Dokumenteerige README.md'