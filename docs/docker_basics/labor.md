# Docker Labor

**Eeldused:** Docker põhitõed loeng läbitud, Linux CLI kogemus  
**Platvorm:** Docker Engine 20.10+, Ubuntu/Debian või Docker Desktop

Labor keskendub praktilisele Docker'i kasutamisele läbi progressiivsete ülesannete. Loote Dockerfile'e, ehitate image'eid, haldate container'eid ja volume'eid. Ülesanded on järjestatud lihtsast keeruliseni ning iga sammu järel saate kohe valideerida tulemust. Töö võtab umbes kaks kuni kolm tundi.

**Enne alustamist:** Veenduge, et Docker on installitud ja töötab. Kui Docker pole veel installitud, järgige allpool olevaid juhiseid.

## Õpiväljundid

Pärast seda labor'it oskad:

- Installid ja konfigureerid Docker'i oma süsteemis
- Käivitad ja haldate container'eid kasutades põhikäske
- Kirjutad Dockerfile'i ja ehitad optimeeritud image'eid
- Kasutad volume'eid andmete püsivuse tagamiseks
- Loob Docker network'e ja konfigureerib container'ite vahelist suhtlust
- Debugid levinud probleeme logide ja inspect käskude abil

---

## 1. Docker'i Installimine

### 1.1 Ubuntu/Debian (Proxmox VM)

Kui kasutate kooli Proxmox keskkonda, on Docker install lihtne:

```bash
# Uuenda pakettide nimekirja
sudo apt update

# Installi Docker
sudo apt install -y docker.io

# Käivita Docker daemon
sudo systemctl start docker
sudo systemctl enable docker

# Kontrolli versiooni
docker --version
```

Lisage oma kasutaja docker gruppi, et vältida sudo kasutamist:

```bash
sudo usermod -aG docker $USER
```

**OLULINE:** Pärast gruppi lisamist logige välja ja uuesti sisse (või käivitage `newgrp docker`), et muudatused rakenduksid.

### 1.2 Windows (Docker Desktop)

Kui kasutate Windowsi:

1. Laadige alla **Docker Desktop for Windows**: https://www.docker.com/products/docker-desktop
2. Käivitage installer ja järgige juhiseid
3. Docker Desktop vajab WSL 2 (Windows Subsystem for Linux)
4. Pärast installimist restart'ige arvuti
5. Käivitage Docker Desktop rakendus

**Validation:** Avage PowerShell või CMD ja käivitage:

```bash
docker --version
docker run hello-world
```

### 1.3 macOS (Docker Desktop)

1. Laadige alla **Docker Desktop for Mac**: https://www.docker.com/products/docker-desktop
2. Lohistage Docker.app Applications kausta
3. Käivitage Docker Desktop
4. Oodake kuni Docker daemon käivitub (ikoon menu bar'is muutub roheliseks)

**Validation:** Terminal'is:

```bash
docker --version
docker run hello-world
```

### 1.4 Alternatiiv: Podman

Kui eelistate rootless lahendust või teil on probleeme Docker'iga:

```bash
# Ubuntu/Debian
sudo apt install -y podman

# Alias Docker käskude jaoks
echo "alias docker=podman" >> ~/.bashrc
source ~/.bashrc
```

Podman käsud on identsed Docker'iga, seega ülejäänud lab töötab samamoodi.

---

## Video Demo: Docker Fundamentals

Enne praktilise töö alustamist vaadake 8-minutiline video, mis selgitab Docker'i põhimõisteid ja workflow'i:

**[Docker in 100 Seconds](https://www.youtube.com/watch?v=GZZQOwQAAeg&t=8s)** (Fireship)

<iframe width="560" height="315" src="https://www.youtube.com/embed/GZZQOwQAAeg?start=8" title="Docker in 100 Seconds" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Video annab kiire ülevaate sellest, mis on image ja container, kuidas Dockerfile töötab ning miks Docker on kasulik. Järgnevates ülesannetes rakendame neid põhimõtteid praktiliste näidete kaudu.

---

## 2. Docker Installatsiooni Kontrollimine

Enne lab'i alustamist veenduge, et Docker on korrektselt installitud ja daemon töötab. Käivitage terminalis:

```bash
docker --version
docker info
```

Esimene käsk peaks näitama versiooni (näiteks Docker version 24.0.7). Teine käsk kuvab detailse süsteemiinfo Docker daemoni kohta, sealhulgas container'ite arvu, image'ide arvu ja storage driver'i. Kui näete vigu, kontrollige kas Docker daemon töötab (`sudo systemctl status docker`).

Kui Docker nõuab kõikide käskude jaoks `sudo` õigusi, lisage oma kasutaja docker gruppi:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

**Validation:** Testige installatsiooni töötamist:

```bash
docker run hello-world
```

Peaks ilmuma "Hello from Docker!" sõnum koos selgitusega, kuidas Docker just käivitas esimese container'i.

---

## 3. Container'ite Põhikäsud

### 4.1 Nginx Web Serveri Käivitamine

Käivitage Nginx container port mapping'uga:

```bash
docker run -d --name web -p 8080:80 nginx
```

Docker laeb alla nginx image'i Docker Hub'ist (kui ei ole juba cached), loob sellest container'i nimega "web" ja käivitab selle detached režiimis. Parameter `-p 8080:80` mapib host'i pordi 8080 container'i pordile 80.

**Validation:** Avage veebibrauser ja navigeerige aadressile `http://localhost:8080`. Peaksite nägema Nginx vaikimisi tervituslehte "Welcome to nginx!". Kui lehte ei kuvata, kontrollige kas port 8080 on host masinas vaba (`sudo netstat -tlnp | grep 8080`).

### 4.2 Töötavate Container'ite Vaatamine

Container'ite nimekirja ja staatuse vaatamiseks:

```bash
docker ps
```

Näete tabelit container'i ID, image'i nime, käivitamise aja, staatuse ja portide kohta. Kõigi container'ite (sh peatatud) vaatamiseks lisage `-a` flag:

```bash
docker ps -a
```

Detailse informatsiooni saamiseks ühe container'i kohta:

```bash
docker inspect web
```

See väljastab JSON formaadis kogu konfiguratsiooni - võrgu seaded, volume'id, environment variable'id, käivitamise parameetrid.

Reaalajas ressursikasutuse jälgimiseks:

```bash
docker stats web --no-stream
```

Näete CPU protsenti, mälukasutust, võrgu I/O'd ja block I/O'd.

### 4.3 Logide Vaatamine

Container'i stdout ja stderr vaatamiseks:

```bash
docker logs web
```

Live logide jälgimiseks (sarnane `tail -f` käsule):

```bash
docker logs -f web
```

Vajutage Ctrl+C logide jälgimisest väljumiseks. Ainult viimaste 10 rea kuvamiseks:

```bash
docker logs --tail 10 web
```

**Validation:** Refresh'ige veebibrauser mitu korda ja seejärel vaadake `docker logs web`. Peaksite nägema HTTP GET päringute ridu koos timestamp'idega, näiteks:

```
172.17.0.1 - - [11/Nov/2024:15:30:45 +0000] "GET / HTTP/1.1" 200 615
```

### 4.4 Container'isse Sisenemine

Interaktiivse shell'i käivitamiseks töötavas container'is:

```bash
docker exec -it web bash
```

Parameetrid: `-i` hoiab STDIN avatud, `-t` eraldab pseudo-TTY. Nüüd olete container'i sees ja saate käivitada käske:

```bash
# Container'i sees
ls /usr/share/nginx/html/
cat /etc/nginx/nginx.conf
ps aux
exit
```

**Validation:** Kontrollige et näete Nginx konfiguratsiooni faile ja HTML failid default document root'is.

### 4.5 Container'i Peatamine ja Kustutamine

Graceful shutdown (saadab SIGTERM, ootab 10s, siis SIGKILL):

```bash
docker stop web
```

Container'i kustutamine (ei kustuta image't):

```bash
docker rm web
```

Või mõlemad tegevused ühel käsul force'itud kustutamisega:

```bash
docker rm -f web
```

**Validation:** Kontrollige et container on eemaldatud:

```bash
docker ps -a | grep web
```

Ei tohiks midagi kuvada.

---

## 4. Dockerfile'ide Loomine

### 4.1 Staatilise HTML Rakenduse Loomine

Looge töökaust projektile:

```bash
mkdir -p ~/docker-lab/web-app
cd ~/docker-lab/web-app
```

Looge fail `index.html` järgneva sisuga:

```html
<!DOCTYPE html>
<html lang="et">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docker Labor</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        .info {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Docker Labor Rakendus</h1>
        <div class="info">
            <p><strong>Tudeng:</strong> [TEIE NIMI]</p>
            <p><strong>Kuupäev:</strong> <span id="date"></span></p>
            <p><strong>Container Hostname:</strong> <span id="hostname"></span></p>
        </div>
        <p>See lehekülg töötab Docker container'is, demonstreerides containeriseeritud veebirakenduste deployment'i.</p>
    </div>
    <script>
        document.getElementById('date').innerText = new Date().toLocaleString('et-EE');
        document.getElementById('hostname').innerText = window.location.hostname;
    </script>
</body>
</html>
```

Asendage `[TEIE NIMI]` oma nimega failis.

### 4.2 Dockerfile Kirjutamine

Looge fail nimega `Dockerfile` (täpselt see nimi, ilma laiendita) samasse kausta:

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Iga rea selgitus: `FROM` määrab base image'i (nginx alpine variant on väike, ainult 23MB). `COPY` kopeerib HTML faili container'i Nginx default document root'i. `EXPOSE` dokumenteerib millised pordid on kasutusel (ei avalda tegelikult porti, ainult dokumentatsioon). `CMD` määrab vaikimisi käsu - käivitab Nginx'i foreground režiimis.

### 4.3 Image'i Ehitamine

Ehitage image käsuga (punkt lõpus viitab build context'ile - praegusele kataloogile):

```bash
docker build -t minu-web:v1 .
```

Näete build protsessi sammsammult:

```
[+] Building 3.2s (7/7) FINISHED
=> [internal] load build definition from Dockerfile
=> [internal] load .dockerignore
=> [internal] load metadata for docker.io/library/nginx:alpine
=> [1/2] FROM docker.io/library/nginx:alpine
=> [2/2] COPY index.html /usr/share/nginx/html/
=> exporting to image
=> => naming to docker.io/library/minu-web:v1
```

Iga samm on layer, mis cache'itakse järgmiste build'ide jaoks.

**Validation:** Kontrollige, et image loodi edukalt:

```bash
docker images | grep minu-web
```

Peaksite nägema rida kujul:

```
minu-web   v1   abc123def456   10 seconds ago   42.6MB
```

Käivitage container loodud image'ist:

```bash
docker run -d -p 8081:80 --name minu-app minu-web:v1
```

Avage brauseris `http://localhost:8081` ja veenduge, et näete oma HTML lehte koos oma nimega.

### 4.4 Image'i Modifitseerimine ja Versioonimine

Muutke `index.html` faili - näiteks lisage uus lõik või muutke värve. Seejärel ehitage uus versioon erinevate tag'iga:

```bash
docker build -t minu-web:v2 .
```

Tänu layer caching'ule on teine build kiirem kui esimene. Käivitage v2 container:

```bash
docker run -d -p 8082:80 --name minu-app-v2 minu-web:v2
```

**Validation:** Avage `http://localhost:8082` ja veenduge, et näete uuendatud versiooni. Võrrelge image'ide suurusi:

```bash
docker images | grep minu-web
```

Mõlemad image'd peaksid olema sarnase suurusega, kuna jagavad base layer'eid.

---

## 5. Dockerfile Optimeerimine

### 9.1 Python Flask Rakenduse Loomine

Looge uus kaust Python projektile:

```bash
mkdir -p ~/docker-lab/python-app
cd ~/docker-lab/python-app
```

Looge Python rakenduse fail `app.py`:

```python
from flask import Flask, jsonify
import datetime
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docker Lab - Python</title>
        <style>
            body {{ font-family: Arial; max-width: 800px; margin: 50px auto; }}
            .info {{ background: #e8f5e9; padding: 20px; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <h1>Docker Python Rakendus</h1>
        <div class="info">
            <p><strong>Server Time:</strong> {datetime.datetime.now()}</p>
            <p><strong>Hostname:</strong> {socket.gethostname()}</p>
            <p>See Python Flask rakendus töötab Docker container'is</p>
        </div>
    </body>
    </html>
    '''

@app.route('/api/info')
def info():
    return jsonify({
        'hostname': socket.gethostname(),
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'running'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

Looge `requirements.txt` fail sõltuvustega:

```
Flask==3.0.0
Werkzeug==3.0.1
```

### 9.2 Optimeerimata Dockerfile

Looge fail `Dockerfile.unoptimized` et demonstreerida halba praktikat:

```dockerfile
FROM python:3.11

WORKDIR /app

# Probleem: kopeerib kõik enne dependencies install
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
```

Ehitage see image:

```bash
docker build -t python-app:bad -f Dockerfile.unoptimized .
```

Jälgige build aega. Nüüd muutke `app.py` faili (lisage kommentaar või muutke teksti) ja ehitage uuesti:

```bash
docker build -t python-app:bad -f Dockerfile.unoptimized .
```

Märkige, et `pip install` samm käivitub uuesti, kuigi `requirements.txt` ei muutunud. See on ajaraiskamine.

### 9.3 Optimeeritud Dockerfile

Looge proper Dockerfile järjestusega:

```dockerfile
FROM python:3.11-alpine

WORKDIR /app

# Kopeeri AINULT requirements ENNE source koodi
COPY requirements.txt .

# Install dependencies - see layer cache'itakse
RUN pip install --no-cache-dir -r requirements.txt

# Nüüd kopeeri rakenduse kood
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

Põhimõte: harvem muutuvad failid (requirements.txt) kopeeritakse enne, sageli muutuvad failid (app.py) kopeeritakse hiljem. Alpine base image on väiksem (50MB vs 900MB).

Ehitage optimeeritud image:

```bash
docker build -t python-app:good .
```

**Validation:** Muutke `app.py` faili ja ehitage uuesti. Märkige build output'is:

```
=> CACHED [2/4] COPY requirements.txt .
=> CACHED [3/4] RUN pip install --no-cache-dir -r requirements.txt
```

`pip install` samm kasutab cache'i, tehes build'i 10x kiiremaks.

Käivitage container:

```bash
docker run -d -p 5000:5000 --name python-api python-app:good
```

Testige API't:

```bash
curl http://localhost:5000
curl http://localhost:5000/api/info
```

### 9.4 Dockerignore Fail

Looge `.dockerignore` fail et välistada tarbetuid faile build context'ist:

```
__pycache__/
*.pyc
*.pyo
*.pyd
*.log
*.sqlite
.git/
.gitignore
.env
.venv/
venv/
*.md
.vscode/
.idea/
```

See fail töötab sarnaselt `.gitignore` failile. Välistatud failid ei kopeerita build context'i, vähendades image suurust ja build kiirust.

Ehitage image uuesti ja võrrelge suurusi:

```bash
docker build -t python-app:final .
docker images | grep python-app
```

**Validation:** Kontrollige image suurust:

```bash
docker images python-app:final
```

---

## 6. Volumes ja Andmete Püsivus

### 9.1 Probleem: Kaduv Data

Demonstreerime andmete kadumist ilma volume'ita:

```bash
docker run -d --name demo-db alpine sh -c 'echo "important data" > /data/file.txt && sleep 3600'
```

Kontrollige et fail eksisteerib:

```bash
docker exec demo-db cat /data/file.txt
```

Output: `important data`

Nüüd kustutage container:

```bash
docker rm -f demo-db
```

Proovige andmeid taastada uue container'iga:

```bash
docker run --name demo-db-new alpine cat /data/file.txt 2>&1
```

Näete veateadet `cat: can't open '/data/file.txt': No such file or directory`. Andmed kadusid, kuna writable layer kustutatakse koos container'iga.

### 9.2 Named Volume Lahendus

Looge named volume:

```bash
docker volume create persistent-data
```

Vaadake volume detaile:

```bash
docker volume inspect persistent-data
```

Output näitab mountpoint'i host failisüsteemis, tavaliselt `/var/lib/docker/volumes/persistent-data/_data`.

Kasutage volume'i container'is:

```bash
docker run -d --name demo-vol -v persistent-data:/data alpine sh -c 'echo "persistent data" > /data/file.txt && sleep 3600'
```

Kontrollige:

```bash
docker exec demo-vol cat /data/file.txt
```

Kustutage container:

```bash
docker rm -f demo-vol
```

**Validation:** Looge uus container SAMA volume'iga:

```bash
docker run --name demo-vol-new -v persistent-data:/data alpine cat /data/file.txt
```

Output: `persistent data` - andmed säilivad!

### 9.3 Bind Mount Arenduseks

Bind mount võimaldab jagada host'i kataloogi container'iga, mis on kasulik arenduses live reload'i jaoks.

Looge kaust host masinas:

```bash
mkdir -p ~/shared-data
echo "host file content" > ~/shared-data/test.txt
```

Käivitage container bind mount'iga:

```bash
docker run -d --name bind-test -v ~/shared-data:/app alpine sh -c 'while true; do ls -la /app && sleep 5; done'
```

Jälgige logisid:

```bash
docker logs -f bind-test
```

Teises terminali aknas muutke faili host'is:

```bash
echo "updated from host" >> ~/shared-data/test.txt
```

**Validation:** Container näeb muudatust kohe:

```bash
docker exec bind-test cat /app/test.txt
```

### 9.4 PostgreSQL Püsivate Andmetega

Käivitage PostgreSQL koos volume'iga:

```bash
docker volume create pgdata

docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=secret123 \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15-alpine
```

Oodake 5-10 sekundit kuni Postgres käivitub. Looge test andmebaas:

```bash
docker exec postgres psql -U postgres -c "CREATE DATABASE labor_test;"
docker exec postgres psql -U postgres -c "\l" | grep labor_test
```

Peaksite nägema `labor_test` andmebaasi loetelus.

Peatage ja kustutage container:

```bash
docker stop postgres
docker rm postgres
```

**Validation:** Käivitage uus Postgres container SAMA volume'iga:

```bash
docker run -d \
  --name postgres-new \
  -e POSTGRES_PASSWORD=secret123 \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15-alpine

sleep 5

docker exec postgres-new psql -U postgres -c "\l" | grep labor_test
```

Andmebaas `labor_test` on endiselt olemas!

---

## 7. Docker Networking

### 9.1 Default Bridge Network Piirangud

Käivitage kaks container'it ilma custom network'ita:

```bash
docker run -d --name container1 alpine sleep 3600
docker run -d --name container2 alpine sleep 3600
```

Proovige container1'st container2'le ligi pääseda:

```bash
docker exec container1 ping -c 2 container2
```

Näete veateadet: `ping: bad address 'container2'`. Default bridge network'is ei tööta hostname resolution.

### 9.2 Custom Network Loomine

Looge custom bridge network:

```bash
docker network create app-network
```

Vaadake network'e:

```bash
docker network ls
docker network inspect app-network
```

Käivitage container'id custom network'is:

```bash
docker run -d --name web1 --network app-network alpine sleep 3600
docker run -d --name web2 --network app-network alpine sleep 3600
```

**Validation:** Container'id näevad üksteist hostname'i järgi:

```bash
docker exec web1 ping -c 3 web2
```

Näete ICMP echo reply'sid. DNS resolution töötab automaatselt custom network'ides.

### 9.3 Multi-Container Rakendus

Looge network ja käivitage kaks teenust:

```bash
docker network create webapp

# Backend: PostgreSQL
docker run -d \
  --name database \
  --network webapp \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_DB=appdb \
  postgres:15-alpine

# Cache: Redis
docker run -d \
  --name cache \
  --network webapp \
  redis:alpine
```

Testige connectivity't kolmanda container'iga:

```bash
docker run --rm --network webapp alpine sh -c 'ping -c 2 database && ping -c 2 cache'
```

**Validation:** Mõlemad ping'id peaksid õnnestuma. Container'id saavad üksteisega suhelda hostname'ide kaudu ilma IP aadresse teadmata.

### 9.4 Network Isolation

Container'id erinevates network'ides ei näe üksteist:

```bash
docker network create isolated-net

docker run -d --name isolated --network isolated-net alpine sleep 3600
docker exec isolated ping -c 2 database 2>&1
```

Näete veateadet, kuna `isolated` container ei ole `webapp` network'is.

---

## 8. Troubleshooting

### 9.1 Container Ei Käivitu

Kui container ei käivitu või läheb kohe stopped olekusse:

```bash
# Vaata exit code't ja põhjust
docker ps -a

# Vaata logisid
docker logs container-name

# Proovi käivitada interaktiivselt
docker run -it image-name sh
```

Levinud põhjused: vale CMD käsk, puuduvad sõltuvused, port konflik.

### 9.2 Port Ei Ole Kättesaadav

Kui rakendus ei reageeri port mapping'uga:

```bash
# Kontrolli millised pordid on mapped
docker port container-name

# Kontrolli kas rakendus kuulatakse õigel pordil
docker exec container-name netstat -tlnp

# Kontrolli host'i firewall
sudo ufw status
sudo iptables -L -n | grep 8080
```

### 9.3 Image Build Ebaõnnestub

Kui `docker build` annab vea:

```bash
# Kontrolli Dockerfile süntaksit
cat Dockerfile

# Build'i verbose output'iga
docker build --no-cache -t test:latest .

# Kontrolli .dockerignore
cat .dockerignore
```

### 9.4 Volume Permissions

Kui container ei saa volume'i kirjutada:

```bash
# Kontrolli volume õigusi
docker exec container-name ls -la /mounted/path

# Volume inspect
docker volume inspect volume-name

# Bind mount puhul kontrolli host'i õigusi
ls -la /host/path
```

Lahendus: Dockerfile'is määra USER direktiiviga õige kasutaja või muuda host'i õigusi.

### 9.5 Container Memory/CPU Probleemid

```bash
# Vaata resource usage't
docker stats container-name

# Määra resource limit'id
docker run -d --memory="512m" --cpus="1.0" image-name

# Kontrolli Docker daemon limit'e
docker info | grep -i memory
```

---

## 9. Cleanup ja Resource Management

### 9.1 Container'ite Puhastamine

Peata kõik töötavad container'id:

```bash
docker stop $(docker ps -q)
```

Kustuta kõik (peatatud ja töötavad) container'id:

```bash
docker rm -f $(docker ps -aq)
```

### 9.2 Image'ide Puhastamine

Kustuta kasutamata image'd (dangling):

```bash
docker image prune
```

Kustuta KÕIK kasutamata image'd:

```bash
docker image prune -a
```

### 9.3 Volume'ide Puhastamine

HOIATUS: See kustutab andmed!

```bash
# Kustuta kasutamata volume'd
docker volume prune

# Kustuta spetsiifiline volume
docker volume rm volume-name
```

### 9.4 Süsteemi Puhastamine

Kustuta kõik kasutamata ressursid (container'id, image'd, volume'd, network'id):

```bash
docker system prune -a --volumes
```

### 9.5 Kettaruumi Monitoorimine

Vaadake Docker ressursside kasutust:

```bash
docker system df
```

Output näitab kasutust kategooriate kaupa:

```
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          15        5         2.5GB     1.8GB (72%)
Containers      8         2         150MB     100MB (66%)
Local Volumes   10        3         800MB     500MB (62%)
```

Detailne vaade:

```bash
docker system df -v
```

---

## Järgmised Sammud

Labor andis teile praktilised oskused Docker'i kasutamiseks - container'ite käivitamisest kuni image'ide optimeerimiseni. Järgmises kodutöös rakendage neid teadmisi reaalse rakenduse containeriseerimiseks.

**Soovitused kodutööks:**

Alustage lihtsast - esmalt saage rakendus container'is tööle, seejärel optimeerige. Kasutage `.dockerignore` faili tarbetute failide välistamiseks. Testize image'i põhjalikult enne esitamist - käivitage container ja kontrollige, et kõik funktsioonid töötavad. Dokumenteerige README.md failis käivitamise juhised ja arhitektuuri otsused.

Edukaid eksperimente!

---
