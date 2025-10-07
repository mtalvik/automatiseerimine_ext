# Docker Seadistus

**Nõuded:** Windows/Mac/Linux arvuti

---

## Ülevaade

See juhend aitab teil seadistada Docker keskkonna kodu arvutis, et saaksite harjutada konteineritega.

---

## 1. Operatsioonisüsteemi valik

### Windows - WSL2
```bash
# PowerShell (Admin)
wsl --install -d Ubuntu-22.04
# Restart PC
```

### macOS - Multipass
```bash
brew install --cask multipass
multipass launch --name docker-vm --memory 4G --disk 20G 22.04
multipass shell docker-vm
```

### Linux - Native
```bash
# You're already there!
```

## 2. Docker installeerimine
```bash
# One command install
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
exit
# Log back in
```

## 3. Installatsiooni testimine
```bash
docker --version
docker run hello-world
```

## 4. Docker Compose
```bash
# Install compose plugin
sudo apt update && sudo apt install docker-compose-plugin -y

# Test
docker compose version
```

## 5. VSCode Setup

Install extensions:
- `ms-vscode-remote.remote-wsl` (Windows)
- `ms-vscode-remote.remote-ssh` (Mac/Multipass)  
- `ms-azuretools.vscode-docker`
- `redhat.vscode-yaml`

## 6. Test projekti loomine
```bash
mkdir ~/docker-test && cd ~/docker-test

cat > docker-compose.yml << EOF
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
EOF

docker compose up -d
# Open http://localhost:8080
docker compose down
```

## 7. Docker Hub
```bash
# Create account at hub.docker.com
docker login

# Push image
docker tag myapp username/myapp
docker push username/myapp

# Pull anywhere
docker pull username/myapp
```

## 8. Kasulikud aliased

Lisa faili `~/.bashrc`:
```bash
alias dc='docker compose'
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias dlog='docker logs -f'
alias dex='docker exec -it'
```

## 9. Põhilised käsud
```bash
# List everything
docker ps -a          # containers
docker images         # images  
docker volume ls      # volumes
docker network ls     # networks

# Cleanup
docker system prune -af    # remove everything unused

# Enter container
docker exec -it container_name bash

# View logs
docker logs -f container_name

# Stop all
docker stop $(docker ps -q)
```

## 10. Levinud probleemid

**"Cannot connect to Docker daemon"**
```bash
sudo service docker start    # Linux/WSL
```

**"Permission denied"**
```bash
newgrp docker    # or logout/login
```

**Port already in use**
```bash
lsof -i :8080    # find what's using port
```

**WSL2 specific - aeglane performance**
- Hoia failid Linux'is (`~/`), mitte Windows'is (`/mnt/c/`)

**Multipass specific - file sharing**
```bash
multipass mount ~/projects docker-vm:/home/ubuntu/projects
```

## Registry valikud

| Teenus | Tasuta | Private Repos | Piirang |
|---------|------|---------------|-------|
| Docker Hub | Jah | 1 | 200 pulls/6h |
| GitHub | Jah | Unlimited | 1GB/month |
| GitLab | Jah | Unlimited | 5GB/project |

## Projekti struktuuri näide
```
myapp/
├── docker-compose.yml
├── .env
├── .dockerignore
├── api/
│   ├── Dockerfile
│   └── src/
├── frontend/
│   ├── Dockerfile
│   └── src/
└── nginx/
    └── default.conf
```

## Cloud registries (edasijõudnutele)

### Google Cloud
```bash
# Vaja: Google account + card (free $300 credit)
gcloud auth login
gcloud config set project PROJECT_ID

# Push to GCR
docker tag myapp gcr.io/PROJECT_ID/myapp
docker push gcr.io/PROJECT_ID/myapp

# Or Artifact Registry (newer)
gcloud auth configure-docker europe-north1-docker.pkg.dev
docker tag myapp europe-north1-docker.pkg.dev/PROJECT/REPO/myapp
docker push europe-north1-docker.pkg.dev/PROJECT/REPO/myapp
```

### AWS ECR
```bash
# Vaja: AWS account (free tier: 500MB/month)
aws configure  # enter credentials

# Create repo & push
aws ecr create-repository --repository-name myapp
aws ecr get-login-password | docker login --username AWS --password-stdin 123456789.dkr.ecr.region.amazonaws.com
docker tag myapp 123456789.dkr.ecr.region.amazonaws.com/myapp
docker push 123456789.dkr.ecr.region.amazonaws.com/myapp
```

## Turvalisus ja tulemüür

### Portide avamine
```bash
# Windows PowerShell (Admin)
New-NetFirewallRule -DisplayName "Docker" -Direction Inbound -Protocol TCP -LocalPort 80,443,8080,3000,5000 -Action Allow

# Linux UFW
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp  
sudo ufw allow 8080/tcp
sudo ufw status

# Kontrolli mis kuulab
netstat -tuln | grep LISTEN
lsof -i -P -n | grep LISTEN
```

### Turvalisuse skaneerimine
```bash
# Skaneeri image'id haavatavuste suhtes
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image myapp:latest

# Docker Scout (built-in)
docker scout cves myapp:latest

# Snyk (free tier available)
npm install -g snyk
snyk test --docker myapp:latest
```

## Võrgustik ja DNS

### Custom võrgud
```bash
# Loo võrk (konteinerid saavad rääkida nime järgi)
docker network create app-net

# Käivita võrguga
docker run -d --name db --network app-net postgres
docker run -d --name api --network app-net -e DB_HOST=db myapp

# Lokaalne DNS
echo "127.0.0.1 myapp.local api.local" | sudo tee -a /etc/hosts
```

## Volumes ja varundamine

### Andmete püsimine
```bash
# Named volume
docker volume create mydata
docker run -v mydata:/data myapp

# Varunda volume
docker run --rm -v mydata:/source -v $(pwd):/backup alpine tar czf /backup/mydata-$(date +%Y%m%d).tar.gz /source

# Taasta
docker run --rm -v mydata:/target -v $(pwd):/backup alpine tar xzf /backup/mydata-20240315.tar.gz -C /target
```

## Jõudluse optimeerimine

### WSL2 mälu
```bash
# Loo: C:\Users\YOU\.wslconfig
[wsl2]
memory=4GB
processors=2
swap=2GB

# Siis: wsl --shutdown
```

### Docker piirangud
```bash
# Piira konteineri ressursse
docker run -m 512m --cpus="1.0" myapp

# Daemon config: /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

## Monitoring

### Lihtne monitoring
```bash
# Real-time stats
docker stats

# Kettakasutus
docker system df

# Täielik monitoring stack
docker run -d -p 19999:19999 \
  -v /proc:/host/proc:ro \
  -v /sys:/host/sys:ro \
  -v /var/run/docker.sock:/var/run/docker.sock \
  netdata/netdata
```

## Git integratsioon
```bash
# Seadista Git
git config --global user.name "Your Name"
git config --global user.email "you@email.com"

# SSH key GitHubi jaoks
ssh-keygen -t ed25519 -C "you@email.com"
cat ~/.ssh/id_ed25519.pub  # add to GitHub

# .gitignore Docker projektide jaoks
cat > .gitignore << EOF
.env
*.log
*_data/
node_modules/
__pycache__/
EOF
```

## Kasulikud tööriistad
```bash
# Installi productivity tools
sudo apt install -y htop tree jq curl wget nano tmux

# Docker utilities
# lazydocker - TUI for Docker
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock lazyteam/lazydocker

# dive - analyze image layers
wget https://github.com/wagoodman/dive/releases/download/v0.11.0/dive_0.11.0_linux_amd64.deb
sudo dpkg -i dive_0.11.0_linux_amd64.deb
dive myapp:latest
```

## Ketta puhastamine
```bash
# Manual cleanup
docker system prune -af --volumes  # HOIATUS: kustutab kõik!

# Auto cleanup cron
crontab -e
# Lisa: 0 2 * * * docker system prune -af

# WSL2 shrink disk
wsl --shutdown
# Siis kasuta diskpart Windows'is et compactida vhdx
```

## Keskkonna haldamine
```bash
# .env fail
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=postgres
DB_PASS=secret123

# docker-compose.yml
services:
  api:
    env_file: .env
    environment:
      - NODE_ENV=production  # override

# Mitu keskkonda
docker compose --env-file .env.dev up
docker compose --env-file .env.prod up
```

## Järgmised sammud

1. Docker installeeritud ja töötab
2. VSCode konfigureeritud  
3. Turvalisuse põhitõed teada
4. Tead kuhu image'id pushida
5. Alusta päris rakenduste ehitamist

---

## Abi vaja?

- Docker dokumentatsioon: https://docs.docker.com
- See juhend: Hoia järjehoidjates
- Klassi Discord: Küsi küsimusi

**Pro tip:** Alusta lihtsast, lisa keerukust järk-järgult