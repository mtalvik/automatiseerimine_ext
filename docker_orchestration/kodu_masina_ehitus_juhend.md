# 🏠 Kodu Masina Ehitus Juhend

**Eesmärk:** Seadistada arenduskeskkond kodus Kubernetes ja Docker õppimiseks

---

## 📋 Sisukord

1. [Virtuaalse masina loomine](#virtuaalse-masina-loomine)
2. [VSCode seadistamine](#vscode-seadistamine)
3. [SSH ühenduse seadistamine](#ssh-ühenduse-seadistamine)
4. [Docker ja Kubernetes installimine](#docker-ja-kubernetes-installimine)
5. [Probleemide lahendamine](#probleemide-lahendamine)

---

## 🖥️ Virtuaalse masina loomine

### **Süsteemi nõuded:**
- **RAM:** Vähemalt 8GB (soovituslik 16GB)
- **CPU:** Vähemalt 4 tuuma (soovituslik 8 tuuma)
- **Ketas:** Vähemalt 50GB vaba ruumi
- **OS:** Windows 10/11, macOS, või Linux

### **1. Multipass (soovituslik - Ubuntu)**

**Windows:**
```bash
# 1. Laadige alla: https://multipass.run/download/windows
# 2. Installige ja taaskäivitage arvuti
# 3. Avage PowerShell ja käivitage:

# Looge virtuaalne masin
multipass launch --name dev-lab --memory 8G --disk 30G --cpus 4

# Ühenduge masinaga
multipass shell dev-lab
```

**macOS:**
```bash
# Installige Homebrew'iga
brew install --cask multipass

# Looge virtuaalne masin
multipass launch --name dev-lab --memory 8G --disk 30G --cpus 4
multipass shell dev-lab
```

**Linux:**
```bash
# Installige Snap'iga
sudo snap install multipass

# Looge virtuaalne masin
multipass launch --name dev-lab --memory 8G --disk 30G --cpus 4
multipass shell dev-lab
```

### **2. VirtualBox + Ubuntu Server**

**1. VirtualBox installimine:**
- Laadige alla: https://www.virtualbox.org/
- Installige ja taaskäivitage arvuti

**2. Ubuntu Server allalaadimine:**
- Laadige alla: https://ubuntu.com/download/server
- Valige LTS versioon (22.04 LTS)

**3. Virtuaalse masina loomine:**
```bash
# VirtualBox'is:
# 1. "New" → "Expert mode"
# 2. Nimi: "Dev-Lab"
# 3. OS: Ubuntu 64-bit
# 4. RAM: 8192 MB (8GB)
# 5. CPU: 4 tuuma
# 6. Ketas: 50GB
# 7. Käivitage ja installige Ubuntu Server
```

### **3. WSL2 (Windows 10/11)**

```bash
# Avage PowerShell administraatorina
wsl --install -d Ubuntu

# Taaskäivitage arvuti
# Avage Ubuntu terminal ja seadistage kasutaja
```

---

## 💻 VSCode seadistamine

### **1. VSCode installimine**

**Windows/macOS/Linux:**
- Laadige alla: https://code.visualstudio.com/
- Installige ja avage

### **2. Kasulikud laiendused**

**Kubernetes ja Docker:**
```bash
# Installige järgmised laiendused:
# 1. "Docker" - Microsoft
# 2. "Kubernetes" - Microsoft
# 3. "YAML" - Red Hat
# 4. "Remote - SSH" - Microsoft
# 5. "Remote - WSL" - Microsoft (Windows)
```

**Arenduskeskkond:**
```bash
# 6. "GitLens" - Git integreerimine
# 7. "Auto Rename Tag" - HTML/XML
# 8. "Bracket Pair Colorizer" - koodi lugemine
# 9. "Material Icon Theme" - failide ikoonid
# 10. "One Dark Pro" - tumm teema
```

### **3. VSCode seaded**

**settings.json:**
```json
{
    "editor.fontSize": 14,
    "editor.fontFamily": "Consolas, 'Courier New', monospace",
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "editor.wordWrap": "on",
    "files.autoSave": "onFocusChange",
    "terminal.integrated.fontSize": 14,
    "workbench.colorTheme": "One Dark Pro",
    "workbench.iconTheme": "material-icon-theme"
}
```

---

## 🔐 SSH ühenduse seadistamine

### **1. SSH võtmete loomine (host masinal)**

**Windows:**
```bash
# Avage PowerShell
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Salvestage: C:\Users\YourName\.ssh\id_rsa
```

**macOS/Linux:**
```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Salvestage: ~/.ssh/id_rsa
```

### **2. SSH võtme kopeerimine VM'i**

**Multipass:**
```bash
# Kopeerige avalik võti VM'i
multipass exec dev-lab -- bash -c 'mkdir -p ~/.ssh'
multipass transfer ~/.ssh/id_rsa.pub dev-lab:/home/ubuntu/.ssh/authorized_keys
multipass exec dev-lab -- bash -c 'chmod 600 ~/.ssh/authorized_keys'
```

**VirtualBox/WSL2:**
```bash
# Kopeerige avalik võti käsitsi või kasutage ssh-copy-id
ssh-copy-id username@vm-ip-address
```

### **3. SSH konfiguratsioon**

**~/.ssh/config (host masinal):**
```bash
Host dev-lab
    HostName 192.168.1.100  # VM'i IP aadress
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### **4. VSCode Remote SSH seadistamine**

**1. Avage VSCode**
**2. Vajutage `Ctrl+Shift+P` (Windows/Linux) või `Cmd+Shift+P` (macOS)**
**3. Otsige "Remote-SSH: Connect to Host"**
**4. Valige "Add New SSH Host"**
**5. Sisestage: `ssh ubuntu@192.168.1.100`**
**6. Ühenduge ja avage kaust**

---

## 🐳 Docker ja Kubernetes installimine

### **1. Docker installimine VM's**

```bash
# Ühenduge VM'iga
ssh dev-lab

# Docker installimine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Lisa kasutaja docker gruppi
sudo usermod -aG docker $USER

# Taaskäivitage terminal
newgrp docker

# Kontrollige installimist
docker --version
docker run hello-world
```

### **2. Minikube installimine**

```bash
# Kubectl installimine
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Minikube installimine
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Minikube käivitamine
minikube start --driver=docker --memory=4096 --cpus=2

# Kontrollige
kubectl get nodes
```

### **3. Kubernetes Dashboard**

```bash
# Dashboard installimine
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Proxy käivitamine
kubectl proxy --address='0.0.0.0' --port=8001 --accept-hosts='.*'

# Avage brauser: http://vm-ip:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

---

## 🔧 Probleemide lahendamine

### **1. SSH ühenduse probleemid**

**Ühendus ei tööta:**
```bash
# Kontrollige VM'i IP aadressi
ip addr show

# Kontrollige SSH teenust
sudo systemctl status ssh

# Käivitage SSH teenus
sudo systemctl start ssh
sudo systemctl enable ssh
```

**Võtme probleemid:**
```bash
# Kontrollige võtmete õigusi
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub

# Kontrollige VM'i võtmete õigusi
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### **2. Docker probleemid**

**Docker ei käivitu:**
```bash
# Kontrollige Docker teenust
sudo systemctl status docker

# Käivitage Docker
sudo systemctl start docker
sudo systemctl enable docker

# Kontrollige kasutaja gruppi
groups $USER
```

**Minikube probleemid:**
```bash
# Minikube logid
minikube logs

# Minikube taaskäivitamine
minikube stop
minikube delete
minikube start --driver=docker

# Ressursi kontroll
free -h
df -h
```

### **3. VSCode probleemid**

**Remote SSH ei ühendu:**
```bash
# Kontrollige SSH konfiguratsiooni
ssh -T dev-lab

# Kontrollige VSCode Remote SSH laiendust
# Vajutage Ctrl+Shift+P ja otsige "Remote-SSH: Show Log"
```

**Failide sünkroniseerimise probleemid:**
```bash
# Kontrollige faili õigusi
ls -la

# Muutke faili omanikku
sudo chown -R $USER:$USER /path/to/project
```

---

## 📚 Lisaressursid

### **Dokumentatsioon:**
- [Multipass Documentation](https://multipass.run/docs)
- [VSCode Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)
- [Docker Installation](https://docs.docker.com/engine/install/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)

### **Video juhendid:**
- [VSCode Remote SSH Setup](https://www.youtube.com/watch?v=5qjqoqfV7hI)
- [Docker Installation on Ubuntu](https://www.youtube.com/watch?v=3c-iBn73dDE)
- [Minikube Quick Start](https://www.youtube.com/watch?v=7uA1wJq8pzE)

### **Kasulikud käsud:**
```bash
# VM'i info
multipass info dev-lab

# Ressursi kasutus
htop
free -h
df -h

# Võrgu info
ip addr show
netstat -tulpn

# Logide vaatamine
journalctl -f
docker logs <container>
kubectl logs <pod>
```

---

 
