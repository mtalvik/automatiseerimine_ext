# Docker Kodutöö: Chat Bot Container

Pärast seda kodutööd oskad luua Docker container'eid, kirjutada Dockerfile'e ja publitseerida image'id Docker Hub'is. Kodutöö võtab umbes 2 tundi.

**Eeldused:** Labor läbitud, Docker installitud  
**Esitamine:** GitHub repository URL + Docker Hub repository URL  
**Tähtaeg:** Järgmise nädala algus

---

## 1. Ülesande Kirjeldus

Loote lihtsa Flask chat bot'i, mis töötab Docker container'is. See demonstreerib järgmisi oskusi:

- Dockerfile loomine ja image ehitamine
- Docker Compose mitme teenuse orkestreerimiseks
- Image publitseerimine Docker Hub'is
- Projekti dokumenteerimine

Soovitatav ajakava: 0-30 min (rakenduse loomine), 30-60 min (Dockerfile), 60-90 min (testimine), 90-120 min (dokumentatsioon ja publitseerimine).

---

## 2. Flask API Loomine

### 2.1 Töökaust
```bash
mkdir docker-chatbot
cd docker-chatbot
```

### 2.2 Python Rakendus

Looge fail `app.py`:
```python
from flask import Flask, render_template, request, jsonify
import random
import datetime
import os

app = Flask(__name__)

RESPONSES = {
    "tere": ["Tere!", "Tsau!", "Mis toimub?"],
    "kuidas": ["Hästi läheb!", "Olen container'is!", "Docker on praktiline!"],
    "kes": ["Olen chat bot", "Container bot", "Sinu Docker assistent"],
    "aeg": [f"Praegu on {datetime.datetime.now().strftime('%H:%M')}"],
    "info": ["Töötab Docker'is", "Python + Flask", "Port 5000"]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    
    response = "Ei saa aru... Proovi: tere, kuidas, kes, aeg, info"
    for keyword, replies in RESPONSES.items():
        if keyword in user_message:
            response = random.choice(replies)
            break
    
    return jsonify({
        'response': response,
        'timestamp': datetime.datetime.now().isoformat(),
        'container_id': os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/api/stats')
def stats():
    return jsonify({
        'uptime': 'Docker container töötab',
        'python_version': '3.11',
        'framework': 'Flask',
        'container_id': os.environ.get('HOSTNAME', 'unknown')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### 2.3 HTML Template

Looge kaust ja fail `templates/index.html`:
```bash
mkdir templates
```
```html
<!DOCTYPE html>
<html lang="et">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docker Chat Bot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .chat-container {
            width: 400px;
            height: 600px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
        }
        .chat-header {
            background: #667eea;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        .message {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 80%;
        }
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
        }
        .bot-message {
            background: #e9ecef;
            color: #333;
        }
        .chat-input {
            display: flex;
            padding: 20px;
            background: white;
            border-radius: 0 0 10px 10px;
        }
        input {
            flex: 1;
            padding: 10px;
            border: 2px solid #e9ecef;
            border-radius: 20px;
            outline: none;
        }
        button {
            margin-left: 10px;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
        }
        button:hover { background: #5568d3; }
        .container-info {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container-info" id="containerInfo">Loading...</div>
    <div class="chat-container">
        <div class="chat-header">
            <h2>Docker Chat Bot</h2>
            <p>Tudeng: <strong>[TEIE NIMI]</strong></p>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message">
                Tere! Olen Docker container'is töötav chat bot. 
                Proovi: "tere", "kuidas", "kes", "aeg", "info"
            </div>
        </div>
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Kirjuta sõnum..."
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Saada</button>
        </div>
    </div>
    <script>
        fetch('/api/stats')
            .then(r => r.json())
            .then(d => {
                document.getElementById('containerInfo').innerText = 
                    `Container: ${d.container_id}`;
            });

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, 'user-message');
            input.value = '';
            
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(r => r.json())
            .then(d => addMessage(d.response, 'bot-message'))
            .catch(() => addMessage('Viga: Server ei vasta', 'bot-message'));
        }
        
        function addMessage(text, className) {
            const div = document.createElement('div');
            div.className = `message ${className}`;
            div.textContent = text;
            document.getElementById('chatMessages').appendChild(div);
            div.scrollIntoView();
        }
    </script>
</body>
</html>
```

Asendage `[TEIE NIMI]` oma nimega.

### 2.4 Requirements

Looge fail `requirements.txt`:
```
Flask==3.0.0
```

---

## 3. Dockerfile Loomine

Looge fail `Dockerfile`:
```dockerfile
FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser -D -s /bin/sh appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
```

Dockerfile selgitus:

- `python:3.11-alpine`
- väike base image
- `COPY requirements.txt`
- dependencies enne koodi (cache)
- `pip install --no-cache-dir`
- ei salvesta cache'i
- `adduser`
- non-root kasutaja turvalisuseks
- `USER appuser`
- lülitub non-root kasutajale

---

## 4. Ehitamine ja Testimine

### 4.1 Image Ehitamine
```bash
docker build -t chatbot-app .
```

### 4.2 Container Käivitamine
```bash
docker run -d --name chatbot -p 5000:5000 chatbot-app
```

### 4.3 Testimine
```bash
# API testimine
curl http://localhost:5000/api/stats

# Brauseris
echo "Avage: http://localhost:5000"
```

Proovige chat bot'iga rääkida - sisestage "tere", "kuidas", "kes".

---

## 5. Docker Compose

Looge fail `docker-compose.yml`:
```yaml
version: '3.8'

services:
  chatbot:
    build: .
    ports:

      - "5000:5000"
    environment:

      - FLASK_ENV=production
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:

      - "80:80"
    volumes:

      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:

      - chatbot
```

Looge fail `nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream chatbot {
        server chatbot:5000;
    }
    
    server {
        listen 80;
        
        location / {
            proxy_pass http://chatbot;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

Käivitage:
```bash
docker-compose up -d
```

Nüüd töötab nginx reverse proxy port 80 peal: `http://localhost`

---

## 6. Docker Hub Publitseerimine

### 6.1 Docker Hub Konto

Looge konto: https://hub.docker.com (tasuta, kinnitage email)

### 6.2 Login
```bash
docker login
# Sisestage username ja password
```

### 6.3 Tag ja Push
```bash
# Tag image oma username'iga
docker tag chatbot-app [teie-username]/chatbot-app:latest
docker tag chatbot-app [teie-username]/chatbot-app:v1.0

# Push Docker Hub'i (public repository)
docker push [teie-username]/chatbot-app:latest
docker push [teie-username]/chatbot-app:v1.0
```

Asendage `[teie-username]` oma Docker Hub username'iga.

### 6.4 Repository Seadistused

Docker Hub'is:
1. Minge oma repository'sse
2. Settings tab
3. Tehke repository **Public**
4. Lisage kirjeldus: "Docker homework - Chat bot API"

### 6.5 Public Image Testimine
```bash
# Kustutage local image
docker rmi chatbot-app
docker rmi [teie-username]/chatbot-app:latest

# Tõmmake Docker Hub'ist
docker pull [teie-username]/chatbot-app:latest

# Käivitage public image
docker run -d --name public-chatbot -p 5001:5000 [teie-username]/chatbot-app:latest

# Test
curl http://localhost:5001/api/stats
```

---

## 7. README.md Kirjutamine

Looge fail `README.md` järgmise struktuuriga:
```markdown
# Docker Chat Bot

Lihtne chat bot Docker container'is, mis demonstreerib Docker põhiteadmisi.

## Autor

[Teie Nimi]

## Kirjeldus

Flask-põhine chat bot, mis vastab lihtsatele küsimustele. Demonstreerib:

- Dockerfile kirjutamist
- Multi-container setup (Docker Compose)
- Nginx reverse proxy
- Image publitseerimist Docker Hub'is

## Käivitamine

### Lokaalselt

\
```bash
docker run -d -p 5000:5000 [username]/chatbot-app:latest
\
```

Avage: http://localhost:5000

### Docker Compose

\
```bash
docker-compose up -d
\
```

Avage: http://localhost

## API Endpoints

- `GET /`
- HTML interface
- `POST /api/chat`
- Chat API
- `GET /api/stats`
- Container statistika

## Tehnoloogiad

- Python 3.11
- Flask 3.0
- Docker
- Nginx (reverse proxy)

## Docker Hub

Image: https://hub.docker.com/r/[username]/chatbot-app
```

---

## 8. Refleksioon

Lisage README.md lõppu peatükk **"## Refleksioon"**. Vastake järgmistele küsimustele (2-3 lauset igale):

### 8.1 Mis oli kõige raskem?

Kirjeldage, milline osa kodutööst oli kõige väljakutsuvam ja kuidas selle lahendasite.

### 8.2 Suurim õppetund

Milline Docker kontseptsioon või käsk oli teile kõige suurem avastus ja miks?

### 8.3 Kuidas kasutada tulevikus?

Kuidas saaksite Docker'i kasutada oma teistes projektides või koolitöödes?

### 8.4 Selgitus sõbrale

Kui peaksite sõbrale selgitama, mis on Docker ja miks see on kasulik, siis mida ütleksite?

### 8.5 Kõige huvitavam osa

Mis oli selle projekti juures kõige meeldivam või huvitavam?

---

## Esitamine

### 9.1 Repository Struktuur
```
docker-chatbot/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── nginx.conf
├── templates/
│   └── index.html
└── README.md
```

### 9.2 .dockerignore

Looge fail `.dockerignore`:
```
__pycache__/
*.pyc
*.pyo
*.log
.git/
.env
venv/
.vscode/
.idea/
```

### 9.3 Esitamise Viis

1. **GitHub repository link** - esitage õppetoolis
2. **Docker Hub repository link** - esitage samuti
3. Mõlemad peavad olema **avalikud**
4. Kõik failid peavad olema commit'itud
5. Chat bot peab töötama

### 9.4 Kontroll Enne Esitamist

- [ ] GitHub repository on avalik ja sisaldab kõiki vajalikke faile
- [ ] Dockerfile on olemas ja töötab (image build'ub)
- [ ] `.dockerignore` on olemas
- [ ] `docker-compose.yml` on olemas ja töötab
- [ ] Image on Docker Hub'i push'itud ja avalik
- [ ] Container käivitub ja on ligipääsetav
- [ ] Chat bot vastab küsimustele
- [ ] README.md sisaldab:
  - [ ] Projekti kirjeldus
  - [ ] Käivitamisjuhend
  - [ ] API endpoints
  - [ ] Refleksioon (5 küsimust, 2-3 lauset igaüks)

---

## Hindamiskriteeriumid

| Kriteerium | Osakaal | Kirjeldus |
|------------|---------|-----------|
| **Dockerfile kvaliteet** | 25% | Toimib, kasutab best practices (cache, väike image) |
| **Container töötab** | 25% | Image build'ub ja container käivitub õigesti |
| **Funktsioon** | 20% | Chat bot vastab küsimustele, API töötab |
| **Docker Hub** | 10% | Image on push'itud ja avalik |
| **README** | 10% | Projekti kirjeldus, käivitamisjuhend, selge |
| **Refleksioon** | 10% | 5 küsimust vastatud, sisukas, näitab mõistmist |

---

## Abimaterjalid

**Dokumentatsioon:**

- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Docker Hub dokumentatsioon](https://docs.docker.com/docker-hub/)

**Kui abi vaja:**
1. Vaadake labor'i materjale
2. Kasutage `docker --help` või `docker <käsk> --help`
3. Küsige klassikaaslaselt või õpetajalt

---

## Boonus (Valikuline, +10%)

### 10.1 Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/api/stats || exit 1
```

### 10.2 Multi-Stage Build

Optimeerige Dockerfile'i kasutades multi-stage build'i.

### 10.3 Environment Variables

Lisage `.env` fail ja kasutage environment variable'eid:
```yaml
services:
  chatbot:
    environment:

      - BOT_NAME=${BOT_NAME:-DefaultBot}
      - DEBUG=${DEBUG:-False}
```

### 10.4 Monitoring

Lisage `/health` endpoint, mis kontrollib rakenduse seisundit.