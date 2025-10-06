# Docker Kodutöö: Chat Bot Container

**Tähtaeg:** Järgmise nädala algus  
**Eesmärk:** Näidata, et oskad Docker'i praktikas kasutada  

---

## Mis sa teed?

Ehita lihtne Flask/Node chat bot Docker container'is! See on nagu sinu esimene "päris" Dockeri projekt – näita, et oskad konteinereid teha nagu professionaal! 

---

##  Samm-sammult juhend

### Ülesanne (soovituslik ajakava)
- 0–30 min: Loo Python/Node rakendus (chat bot API)
- 30–60 min: Kirjuta Dockerfile ja `.dockerignore`
- 60–90 min: Build image, testi container, kirjuta README refleksiooniga

---

# SAMM 1: Flask API Loomine

## Looge töökaust

```bash
mkdir docker-chatbot
cd docker-chatbot
```

## Looge Python API

Looge fail `app.py`:

```python
from flask import Flask, render_template, request, jsonify
import random
import datetime
import os

app = Flask(__name__)

# Chat bot vastused
RESPONSES = {
    "tere": ["Tere!", "Tsau!", "Mis toimub?"],
    "kuidas": ["Hästi läheb!", "Olen container'is!", "Docker on äge!"],
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
    
# Leia vastus
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
        'python_version': '3.9',
        'framework': 'Flask',
        'container_id': os.environ.get('HOSTNAME', 'unknown')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Looge HTML template

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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: #667eea;
            color: white;
            padding: 20px;
            text-align: center;
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
            word-wrap: break-word;
        }
        
        .user-message {
            background: #667eea;
            color: white;
            align-self: flex-end;
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
        }
        
#messageInput {
            flex: 1;
            padding: 10px 15px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            outline: none;
            font-size: 14px;
        }
        
#sendButton {
            margin-left: 10px;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
        }
        
#sendButton:hover {
            background: #5a6fd8;
        }
        
        .info-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
            font-size: 12px;
        }
        
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
            <h2> Docker Chat Bot</h2>
            <p>Tudeng: <strong>[SINU NIMI]</strong></p>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message">
                Tere! Olen Docker container'is töötav chat bot. 
                Proovi kirjutada: "tere", "kuidas", "kes", "aeg", "info"
            </div>
            <div class="info-box">
                 See rakendus töötab Python Flask serveris Docker container'is!
            </div>
        </div>
        
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Kirjuta sõnum..." 
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button id="sendButton" onclick="sendMessage()">Saada</button>
        </div>
    </div>

    <script>
        // Load container info
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('containerInfo').innerText = 
                    `Container: ${data.container_id}`;
            });

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user-message');
            input.value = '';
            
            // Send to API
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, 'bot-message');
            })
            .catch(error => {
                addMessage('Viga: Server ei vasta', 'bot-message');
            });
        }
        
        function addMessage(text, className) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${className}`;
            messageDiv.textContent = text;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // Auto-focus input
        document.getElementById('messageInput').focus();
    </script>
</body>
</html>
```

## Looge requirements fail

Looge fail `requirements.txt`:

```
Flask==2.3.3
```

---

# SAMM 2: Dockerfile

Looge fail `Dockerfile`:

```dockerfile
FROM python:3.9-alpine

WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser -D -s /bin/sh appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
```

---

# SAMM 3: Ehitamine ja Testimine

```bash
# Build image
docker build -t chatbot-app .

# Run container
docker run -d --name chatbot -p 5000:5000 chatbot-app

# Test API
curl http://localhost:5000/api/stats

# Test brauseris
echo "Avage: http://localhost:5000"
```

Nüüd saate chat bot'iga rääkida!

---

# SAMM 4: Docker Compose

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
      - ./nginx.conf:/etc/nginx/nginx.conf
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

Nüüd töötab nginx reverse proxy port 80 peal!

---

# SAMM 6: Docker Hub Publishing

## Looge Docker Hub konto

1. Minge https://hub.docker.com/
2. Registreeruge (tasuta konto)
3. Kinnitage email

## Logige sisse

```bash
# Login Docker Hub'i
docker login

# Sisestage username ja password
```

## Tagige ja pushige image

```bash
# Tag image oma username'iga
docker tag chatbot-app [teie-username]/chatbot-app:latest
docker tag chatbot-app [teie-username]/chatbot-app:v1.0

# Push Docker Hub'i (public repository)
docker push [teie-username]/chatbot-app:latest
docker push [teie-username]/chatbot-app:v1.0
```

## Testinge public image'i

```bash
# Kustutage local image
docker rmi chatbot-app
docker rmi [teie-username]/chatbot-app:latest

# Tõmmake Docker Hub'ist
docker pull [teie-username]/chatbot-app:latest

# Käivitage public image
docker run -d --name public-chatbot -p 5003:5000 [teie-username]/chatbot-app:latest
```

## Repository seadistused

Docker Hub'is:
1. Minge oma repository'sse
2. Settings tab
3. Tehke repository **Public**
4. Lisage kirjeldus: "Docker Fundamentals homework - Chat bot API"

---

# SAMM 7: Podman Alternatiiv

```bash
# Install Podman
sudo apt install podman

# Build sama image
podman build -t chatbot-podman .

# Run different port
podman run -d --name chatbot-podman -p 5001:5000 chatbot-podman

# Test
curl http://localhost:5001/api/stats
```

Nüüd teil töötab:
- Docker: http://localhost:5000
- Podman: http://localhost:5001  
- Nginx proxy: http://localhost:80

---

# SAMM 8: Lisafunktsioonid

## Chat logi salvestamine

Lisage `app.py` faili:

```python
import json
from datetime import datetime

# Chat log
chat_log = []

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    
# ... existing code ...
    
# Save to log
    chat_log.append({
        'user': user_message,
        'bot': response,
        'timestamp': datetime.now().isoformat(),
        'container': os.environ.get('HOSTNAME', 'unknown')
    })
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat(),
        'container_id': os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/api/logs')
def get_logs():
    return jsonify(chat_log[-10:])  # Last 10 messages
```

## Environment variables

```bash
# Run with custom environment
docker run -d --name chatbot-custom \
    -p 5002:5000 \
    -e BOT_NAME="DockerBot" \
    -e BOT_MOOD="happy" \
    chatbot-app
```

---

# Esitamine

## Nõuded

Teie repository peab sisaldama:

```
docker-chatbot/
├── app.py
├── requirements.txt  
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── templates/
│   └── index.html
└── README.md
```

**Docker Hub nõuded:**
- Image pushed Docker Hub'i: `[teie-username]/chatbot-app:latest`
- Repository on **public**
- Tag'itud ka versiooniga: `[teie-username]/chatbot-app:v1.0`

## Esitamise viis

1. **GitHub repository link** esitage õppetoolis
2. **Docker Hub repository link** esitage samuti
3. **Mõlemad peavad olema avalikud**
4. **Kõik failid commit'itud**
5. **Chat bot peab töötama**

## Testimine

Õpetaja testib:
- GitHub repository clone
- Docker Hub image pull ja run
- http://localhost:5000 - Flask app
- http://localhost:80 - Nginx proxy  
- Chat bot functionality
- API endpoints

**Docker Hub test:**
```bash
docker pull [teie-username]/chatbot-app:latest
docker run -d -p 5000:5000 [teie-username]/chatbot-app:latest
curl http://localhost:5000/api/stats
```

---

##  Refleksioon (kirjuta README.md lõppu)

Lisa oma README.md faili lõppu peatükk **"## Refleksioon"** ja vasta järgmistele küsimustele:

### Küsimused (vasta 2-3 lausega igaühele):

1. **Mis oli selle kodutöö juures kõige raskem ja kuidas sa selle lahendasid?**
   - Näide: "Kõige raskem oli mõista, kuidas port mapping töötab. Aitasin end sellest välja, et joonistasin diagrammi."

2. **Milline Docker kontseptsioon või käsk oli sulle kõige suurem "ahaa!"-elamus ja miks?**
   - Näide: "Docker cache oli mulle suur avastus – esimene build võttis 5 min, teine ainult 10 sekundit!"

3. **Kuidas saaksid Docker'i kasutada oma teistes projektides või koolitöödes?**
   - Näide: "Võiksin Docker'i kasutada oma veebirakenduste testimiseks, et nad töötaksid sõprade arvutites ka."

4. **Kui peaksid oma sõbrale selgitama, mis on Docker ja miks see on kasulik, siis mida ütleksid?**
   - Näide: "Docker on nagu miniatuurne virtuaalmasin – super kiire ja töötab kõikjal ühesuguselt!"

5. **Mis oli selle projekti juures kõige lõbusam või huvitavam osa?**
   - Näide: "Mulle meeldis, et ma sain oma rakenduse Docker Hub'i panna ja nüüd saavad teised seda kasutada!"

---

## Kontrollnimekiri (enne esitamist)

**Kontrolli need asjad:**

- [ ] GitHub repos on avalik ja sisaldab kõiki vajalikke faile
- [ ] `Dockerfile` on olemas ja töötab (image build'ub ilma vigadeta)
- [ ] `.dockerignore` on olemas (ignoreeri `__pycache__/`, `*.pyc`, `venv/`)
- [ ] `docker-compose.yml` on olemas ja töötab
- [ ] Image on Docker Hub'i push'itud ja avalik
- [ ] Container käivitub ja on ligipääsetav (port mapping töötab)
- [ ] Chat bot vastab küsimustele õigesti
- [ ] README.md sisaldab:
  - [ ] Projekti kirjeldus (mis see on?)
  - [ ] Kuidas käivitada (Docker käsud)
  - [ ] Kuidas kasutada (API endpoints)
  - [ ] Refleksioon (5 küsimuse vastused, 2-3 lauset igaüks)

---

##  Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **Dockerfile kvaliteet** | 25% | Dockerfile toimib, kasutab best practices (cache, väike image) |
| **Container töötab** | 25% | Image build'ub ja container käivitub õigesti |
| **Funktsioon** | 20% | Chat bot vastab küsimustele, API töötab |
| **Docker Hub** | 10% | Image on Docker Hub'i push'itud ja avalik |
| **README** | 10% | Projekti kirjeldus, käivitamisjuhend, selge |
| **Refleksioon** | 10% | 5 küsimust vastatud, sisukas, näitab mõistmist |

**Kokku: 100%**

---

## Abimaterjalid ja lugemine (enne kodutöö tegemist)

**Kiirviited:**
- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker CLI Cheat Sheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)
- [Docker Hub dokumentatsioon](https://docs.docker.com/docker-hub/)

**Video tutor'id (valikuline):**
- [Docker in 100 Seconds](https://www.youtube.com/watch?v=Gjnup-PuquQ) (inglise keeles)
- [Learn Docker in 7 Easy Steps](https://www.youtube.com/watch?v=gAkwW2tuIqE) (inglise keeles)

**Kui abi vaja:**
1. Vaata lab'i materjalide (`labor.md`) näiteid
2. Kasuta `docker --help` või `docker <käsk> --help`
3. Küsi klassikaaslaselt või õpetajalt
4. Stack Overflow: search "docker [sinu probleem]"

---

## Boonus (valikuline, +10%)

**Kui tahad ekstra punkte, tee üks või mitu neist:**

1. **Lisa health check Dockerfile'i:**
   ```dockerfile
   HEALTHCHECK --interval=30s --timeout=3s \
     CMD curl -f http://localhost:5000/api/stats || exit 1
   ```

2. **Multi-stage build:** Optimeeri Dockerfile'i kasutades multi-stage build'i
   ```dockerfile
   FROM python:3.9 AS builder
# build steps
   FROM python:3.9-slim
   COPY --from=builder ...
   ```

3. **Docker Compose environment variables:** Lisa `.env` fail ja kasuta environment variables
   ```yaml
   services:
     app:
       environment:
         - API_KEY=${API_KEY}
         - DEBUG=${DEBUG:-False}
   ```

4. **Monitoring:** Lisa Prometheus metrics endpoint või lihtne `/health` endpoint

---

**Edu ja head Docker'itamist!** 

**P.S.** Pärast kodutöö esitamist võid jätkata projekti arendamist – see on sinu portfoolio! Näiteks: lisa autentimine, andmebaas (PostgreSQL container), või frontend (React container). 
