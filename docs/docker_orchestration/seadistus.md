# Docker Seadistus

**Eesmärk:** Saada töötav Docker keskkond laboriteks

**Vali oma variant:**
- [Proxmox VM](#1-proxmox-vm-kool) - koolis
- [VirtualBox](#2-virtualbox-kodu) - kodus, VM
- [Native/WSL2](#3-nativewsl2multipass) - kodus, otse

---

## 1. Proxmox VM (Kool)

### VM loomine

**Proxmox veebiliides:**
1. Create VM → ISO: Ubuntu 22.04 Server
2. Settings:
   - RAM: 4GB (4096 MB)
   - Disk: 20GB
   - CPU: 2 cores
   - Network: vmbr0 (bridge)

**Ubuntu install:**
- Vali "Ubuntu Server (minimized)"
- Kasutaja: oma nimi
- Install OpenSSH server: **JAH** ✓

### SSH ühendus

```bash
# Proxmox consolist saa IP
ip addr show

# Siis oma arvutist
ssh username@VM_IP_ADDRESS
```

### Docker install

```bash
# Üks käsk
curl -fsSL https://get.docker.com | sudo sh

# Lisa end docker gruppi
sudo usermod -aG docker $USER

# Logi välja ja sisse
exit
ssh username@VM_IP_ADDRESS

# Kontrolli
docker --version
docker run hello-world
```

### Docker Compose

```bash
sudo apt update
sudo apt install -y docker-compose-plugin

docker compose version
```

**Valmis!** → [Mine labori juurde](#testimine)

---

## 2. VirtualBox (Kodu)

### VM loomine

**Download:**
- VirtualBox: [virtualbox.org](https://www.virtualbox.org/wiki/Downloads)
- Ubuntu: [ubuntu.com](https://ubuntu.com/download/server) (22.04 LTS)

**VirtualBox seaded:**
1. New VM → Type: Linux, Version: Ubuntu (64-bit)
2. Memory: 4096 MB
3. Hard disk: 20 GB (VDI, dynamically allocated)
4. Settings → System → Processor: 2 CPUs
5. Settings → Network → Adapter 1: Bridged Adapter

**Ubuntu install:**
- Sama kui Proxmox variant
- Enable OpenSSH

### Port Forwarding (kui Bridged ei tööta)

VirtualBox → VM → Settings → Network → Advanced → Port Forwarding:

| Name | Protocol | Host Port | Guest Port |
|------|----------|-----------|------------|
| HTTP | TCP | 8080 | 80 |
| SSH | TCP | 2222 | 22 |

SSH siis:
```bash
ssh -p 2222 username@localhost
```

### Docker install

Sama kui Proxmox:
```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
exit
# Log back in
```

**Valmis!** → [Mine labori juurde](#testimine)

---

## 3. Native/WSL2/Multipass

### Windows - WSL2

```bash
# PowerShell (Admin)
wsl --install -d Ubuntu-22.04

# Restart PC

# Ava Ubuntu terminal
# Docker install
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

Restart WSL:
```bash
# PowerShell
wsl --shutdown
# Ava Ubuntu uuesti
```

### macOS - Multipass

```bash
# Install Multipass
brew install --cask multipass

# Loo VM
multipass launch --name docker-vm --memory 4G --disk 20G 22.04

# Shell
multipass shell docker-vm

# Docker install (VM sees)
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
exit

# Shell uuesti
multipass shell docker-vm
```

### Linux Native

```bash
# Docker install
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER

# Logout/login või
newgrp docker
```

**Valmis!** → [Mine labori juurde](#testimine)

---

## Git Seadistus

**Kõik variandid:**

```bash
# Seadista Git
git config --global user.name "Sinu Nimi"
git config --global user.email "email@example.com"

# Kontrolli
git config --list

# SSH key GitHubile (optional)
ssh-keygen -t ed25519 -C "email@example.com"
cat ~/.ssh/id_ed25519.pub
# Lisa GitHub Settings → SSH Keys
```

---

## Testimine

**Kontrolli installatsiooni:**

```bash
# Docker versioon
docker --version
# Peaks: Docker version 20.10+ või 24.0+

# Docker Compose
docker compose version
# Peaks: Docker Compose version v2.x

# Hello World
docker run hello-world
# Peaks näitama: "Hello from Docker!"

# Test projekt
mkdir ~/docker-test && cd ~/docker-test

cat > docker-compose.yml << 'EOF'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
EOF

docker compose up -d
curl http://localhost:8080
# Peaks näitama: "Welcome to nginx!"

docker compose down
cd ~ && rm -rf docker-test
```

**Kui kõik toimib** ✓ → Mine labori juurde!

---

## Kasulikud Käsud

```bash
# Konteinerid
docker ps                    # töötavad
docker ps -a                 # kõik
docker stop container_name   # peata
docker rm container_name     # kustuta

# Image'id
docker images                # loend
docker pull nginx            # tõmba
docker rmi image_name        # kustuta

# Logs
docker logs container_name
docker logs -f container_name  # live

# Shell
docker exec -it container_name bash

# Cleanup
docker system prune -a       # kustuta kõik kasutamata
```

---

## Troubleshooting

### "Cannot connect to Docker daemon"

```bash
# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Kontrolli
sudo systemctl status docker
```

### "Permission denied"

```bash
# Lisa end gruppi
sudo usermod -aG docker $USER

# Logout/login või
newgrp docker

# Kontrolli
groups
# Peaks sisaldama: docker
```

### "Port already in use"

```bash
# Leia mis kasutab
sudo lsof -i :8080
# VÕI
sudo netstat -tulpn | grep :8080

# Sulge see või muuda porti
```

### VirtualBox - "No Internet"

**Variant 1:** Bridged Adapter
- Settings → Network → Bridged Adapter
- Select: Sinu aktiivsem võrgukaart (WiFi või Ethernet)

**Variant 2:** NAT + Port Forwarding
- Settings → Network → NAT
- Port Forwarding: 8080 → 80

### WSL2 - Aeglane

```bash
# Hoia failid WSL-is, MITTE Windows-is
pwd
# HEA: /home/username/projects
# HALB: /mnt/c/Users/...
```

### Proxmox - SSH ei tööta

```bash
# VM consolis kontrolli IP
ip addr show

# Kontrolli SSH teenus
sudo systemctl status ssh

# Kui ei ole
sudo apt install -y openssh-server
sudo systemctl start ssh
```

### VSCode - Docker extension ei näe konteinereid

**Põhjus:** VSCode ei pääse Docker socket'ile ligi

**Lahendus 1: Lisa user docker gruppi (ÕIGE)**
```bash
sudo usermod -aG docker $USER

# Siis PEAD restartima VSCode:
# - Close ALL VSCode windows
# - Restart terminal
# - VÕI logout/login

# Kontrolli
groups
# Peaks sisaldama: docker
```

**Lahendus 2: Socket permission (kiire fix)**
```bash
sudo chmod 666 /var/run/docker.sock
```

**HOIATUS:** Lahendus 2 kaob pärast reboot! Kasuta Lahendust 1.

**Pärast fixi:**
- VSCode: `Ctrl+Shift+P` → "Developer: Reload Window"
- Docker extension peaks nüüd näitama konteinereid

---

## Järgmised Sammud

✓ Docker installeeritud ja töötab  
✓ Docker Compose töötab  
✓ Git konfigureeritud  
✓ Test projekt õnnestus

**Nüüd:**
1. Mine `labor.md` juurde
2. Alusta Docker Compose õppimist
3. Ehita multi-container rakendusi

---

## Ressursid

- **Docker dokumentatsioon:** [docs.docker.com](https://docs.docker.com)
- **Docker Hub:** [hub.docker.com](https://hub.docker.com) - image'id
- **Compose dokumentatsioon:** [docs.docker.com/compose](https://docs.docker.com/compose/)
- **GitHub:** [github.com](https://github.com) - kood ja collaboration

---

**Küsimused?** Küsi õpetajalt või klassikaaslastelt!

---

## VSCode Setup

### Extension'id

Install extensions:
- `ms-vscode-remote.remote-ssh` - SSH ühendus VM'idega
- `ms-vscode-remote.remote-wsl` - WSL2 support (Windows)
- `ms-azuretools.vscode-docker` - Docker support
- `redhat.vscode-yaml` - YAML syntax

### Remote SSH kasutamine

**Variant 1: VSCode HOST masinas**

1. VSCode → Extensions → Install "Remote-SSH"
2. `Ctrl+Shift+P` → "Remote-SSH: Connect to Host"
3. `ssh user@VM_IP`
4. File → Open Folder → `/home/user/projects`

**Variant 2: VSCode VM sees**

```bash
# Ubuntu VM-is
sudo snap install code --classic

# Ava projekt
cd ~/projects
code .
```

### Port Forwarding (VirtualBox)

Kui kasutad VirtualBox VM'i ja tahad HOST brauserist ligi:

1. VirtualBox → Select VM → Settings
2. Network → Adapter 1 → Advanced → Port Forwarding
3. Lisa reeglid:

| Name | Protocol | Host Port | Guest Port |
|------|----------|-----------|------------|
| HTTP | TCP | 8080 | 80 |
| HTTPS | TCP | 8443 | 443 |
| Custom | TCP | 3000 | 3000 |

Siis HOST masinas: `http://localhost:8080`

**Alternatiiv: Bridged Adapter**

Settings → Network → Adapter 1 → Bridged Adapter

VM saab IP samast võrgust (192.168.x.x) ja pääsed otse ligi.
