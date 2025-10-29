# Terraform Docker Labor: Remote Container Infrastruktuur

**Eeldused:** Terraform põhitõed (loeng + labor), SSH juurdepääs Ubuntu serveritele, Provider loeng läbitud

**Platvorm:** Docker (remote - 2x Ubuntu serverit)

**Setup:** Windows Client (VS Code, Terraform) → SSH → Ubuntu-1 & Ubuntu-2 (Docker hosts)

**Ajakulu:** ~75 min

## Õpiväljundid

Pärast seda labor'it õpilane:

- Konfigureerib Docker provider'it remote SSH connection'iga
- Loob Docker ressursse kahes erinevas host'is
- Kasutab count ja for_each remote deployment'iks
- Haldab distributed container infrastruktuuri
- Mõistab remote state management'i

---

## 1. Lab Arhitektuur

```
┌─────────────────┐
│ Windows Client  │
│                 │
│ - VS Code       │
│ - Terraform     │
│ - SSH keys      │
└────────┬────────┘
         │ SSH
    ┌────┴─────┐
    │          │
┌───▼──────┐ ┌─▼────────┐
│ Ubuntu-1 │ │ Ubuntu-2 │
│          │ │          │
│ Docker   │ │ Docker   │
│ daemon   │ │ daemon   │
└──────────┘ └──────────┘
```

**Mis toimub:**
- Terraform jookseb Windows'is
- Docker provider ühendub SSH üle Ubuntu'tesse
- Containerid tekivad remote host'ides

---

## 2. Ansible Setup (Docker Installimine)

Enne Terraform'i kasutamist peame installima Docker'i mõlemasse Ubuntu serverisse. Kasutame selleks Ansible'it (mida te juba õppisite).

### Ansible Installimine WinKlient'is

Ansible vajab Python'it. Kontrollige ja installige:

```powershell
# Kontrolli Python
python --version
# Peaks olema Python 3.8+
```

**Installige Ansible:**
```powershell
# PowerShell
pip install ansible

# Kontrolli
ansible --version
```

### Ansible Playbook Docker'i Jaoks

Looge VS Code'is (terraform-docker-lab kaustas) fail `docker-setup.yml`:

```powershell
# PowerShell
cd C:\terraform-docker-lab
code docker-setup.yml
```
nano docker-setup.yml
```

**docker-setup.yml:**
```yaml
---
- name: Install Docker on Ubuntu servers
  hosts: docker_hosts
  become: yes
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install prerequisites
      apt:
        name:
          - apt-transport-https
          - ca-certificates
          - curl
          - gnupg
          - lsb-release
        state: present
    
    - name: Add Docker GPG key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present
    
    - name: Add Docker repository
      apt_repository:
        repo: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
        state: present
    
    - name: Install Docker
      apt:
        name:
          - docker-ce
          - docker-ce-cli
          - containerd.io
        state: present
        update_cache: yes
    
    - name: Add user to docker group
      user:
        name: "{{ ansible_user }}"
        groups: docker
        append: yes
    
    - name: Start and enable Docker
      systemd:
        name: docker
        state: started
        enabled: yes
    
    - name: Test Docker installation
      command: docker --version
      register: docker_version
      changed_when: false
    
    - name: Display Docker version
      debug:
        msg: "Docker installed: {{ docker_version.stdout }}"
```

### Ansible Inventory

Looge `inventory.ini`:

```ini
[docker_hosts]
ubuntu-1 ansible_host=10.0.X.20 ansible_user=student
ubuntu-2 ansible_host=10.0.X.21 ansible_user=student

[docker_hosts:vars]
ansible_ssh_private_key_file=C:/Users/YourName/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3
```

**OLULINE:** Asendage `10.0.X.20/21` oma võrgu numbriga ()

### Käivitage Playbook

```bash
# WSL'is või Ubuntu-1's
ansible-playbook -i inventory.ini docker-setup.yml

# Kui küsib parooli ja teil pole SSH key't:
ansible-playbook -i inventory.ini docker-setup.yml --ask-pass
```

**Oodatav väljund:**
```
PLAY [Install Docker on Ubuntu servers] ********************************

TASK [Update apt cache] ************************************************
ok: [ubuntu-1]
ok: [ubuntu-2]

TASK [Install Docker] **************************************************
changed: [ubuntu-1]
changed: [ubuntu-2]

...

PLAY RECAP *************************************************************
ubuntu-1  : ok=8  changed=5  unreachable=0  failed=0
ubuntu-2  : ok=8  changed=5  unreachable=0  failed=0
```

### Kontrollige Docker'i

SSH mõlemasse serverisse ja kontrollige:

```bash
# Ubuntu-1
ssh student@10.0.X.20
docker --version
docker ps
exit

# Ubuntu-2
ssh student@10.0.X.21
docker --version
docker ps
exit
```

Peaks nägema: `Docker version 24.0.x`

**OLULINE:** Logige Ubuntu'test välja ja sisse uuesti, et docker group membership aktiveeruks:
```bash
ssh student@10.0.X.20
# Logige välja (Ctrl+D)
# Logige sisse uuesti
docker ps  # Ei tohiks küsida sudo
```

---

## 3. Eeldused ja Kontroll

Nüüd kui Docker on installitud, kontrollige kõik enne Terraform'iga jätkamist.

### Windows Client'is

Kontrollige, et Terraform on installitud:
```powershell
terraform version
```

Kontrollige SSH võtmed:
```powershell
# PowerShell
ls ~\.ssh\
# Peaks nägema: id_rsa, id_rsa.pub (või teised võtmed)
```

### Ubuntu Serverites (Docker töötab)

```bash
# Mõlemad serverid
ssh student@10.0.X.20 "docker ps"
ssh student@10.0.X.21 "docker ps"
# Peaks töötama ilma sudo'ta
```

---

## 4. Töökataloog Windows'is

Looge projekt VS Code'is:
```powershell
# PowerShell
mkdir C:\terraform-docker-lab
cd C:\terraform-docker-lab
code .
```

VS Code peaks avanema selles kaustas.

---

## 5. Provider Konfiguratsioon (Remote SSH)

Docker provider saab ühenduda remote host'idega SSH üle. Kuna meil on **kaks** Ubuntu serverit, vajame **kahte** provider'it.

**Miks kaks provider'it?**
- Terraform peab teadma, millisesse serverisse iga resource läheb
- `alias` annab igale providerile nime
- Hiljem ütleme: "Loo see container `provider = docker.ubuntu1` serverisse"

**Kuidas SSH ühendus töötab:**
1. Terraform loeb provider konfiguratsiooni
2. Avab SSH ühenduse Ubuntu'sse (kasutab teie SSH võtit)
3. Saadab Docker käsud üle SSH
4. Container tekib remote serveris

**variables.tf:**
```hcl
variable "ubuntu1_host" {
  description = "Ubuntu-1 SSH host"
  type        = string
  default     = "10.0.X.20"  # Asendage X oma võrgu numbriga
}

variable "ubuntu2_host" {
  description = "Ubuntu-2 SSH host"
  type        = string
  default     = "10.0.X.21"  # Asendage X oma võrgu numbriga
}

variable "ssh_user" {
  description = "SSH username"
  type        = string
  default     = "student"
}

variable "ssh_key_path" {
  description = "Path to SSH private key"
  type        = string
  default     = "C:/Users/YourName/.ssh/id_rsa"  # Windows path
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "tf-lab"
}
```

**OLULINE:** Asendage IP aadressides `X` oma lab võrgu numbriga.

**main.tf:**
```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Provider Ubuntu-1 jaoks
provider "docker" {
  alias = "ubuntu1"  # Nimi sellele providerile
  
  host = "ssh://${var.ssh_user}@${var.ubuntu1_host}:22"
  
  ssh_opts = [
    "-i", var.ssh_key_path,                    # SSH võti
    "-o", "StrictHostKeyChecking=no",          # Ei küsi "trust this host?"
    "-o", "UserKnownHostsFile=/dev/null"       # Ei salvesta known_hosts
  ]
}

# Provider Ubuntu-2 jaoks
provider "docker" {
  alias = "ubuntu2"  # Teine nimi
  
  host = "ssh://${var.ssh_user}@${var.ubuntu2_host}:22"
  
  ssh_opts = [
    "-i", var.ssh_key_path,
    "-o", "StrictHostKeyChecking=no",
    "-o", "UserKnownHostsFile=/dev/null"
  ]
}
```

**Selgitus:**
- `alias = "ubuntu1"` - annab providerile nime (nagu muutuja)
- `host = "ssh://..."` - kuhu ühenduda (SSH protokoll)
- `${var.ubuntu1_host}` - kasutab IP'd variables.tf failist
- `ssh_opts` - SSH parameetrid (nagu `ssh -i key.pem -o StrictHost...`)

**Miks StrictHostKeyChecking=no?**
Muidu SSH küsib esimesel korral: "Trust this host? (yes/no)" ja Terraform jääb kinni. Labor'is see on OK, production'is kasuta proper known_hosts.

**OLULINE:** Muutke `variables.tf` failis:
- `ubuntu1_host` ja `ubuntu2_host` oma võrgu IP'deks
- `ssh_user` oma kasutajanimeks
- `ssh_key_path` oma SSH võtme asukohaks Windows'is

Init:
```powershell
terraform init
```

Peaks nägema: "Installing kreuzwerker/docker v3.x.x..."

---

## 6. SSH Connection Test

Enne ressursside loomist testib Terraform SSH connection'i.

**test.tf** (ajutine fail testimiseks):
```hcl
# Test Ubuntu-1 connection
resource "docker_image" "test_ubuntu1" {
  provider = docker.ubuntu1
  name     = "hello-world"
}

# Test Ubuntu-2 connection
resource "docker_image" "test_ubuntu2" {
  provider = docker.ubuntu2
  name     = "hello-world"
}
```

Apply:
```powershell
terraform apply
```

Kui töötab, kustutage test fail:
```powershell
rm test.tf
terraform apply  # Kustutab test image'id
```

---

## 7. Network Ubuntu-1's

Loome Docker network Ubuntu-1 serverisse. See on nagu VPC AWS'is - isoleeritud võrk containeritele.

**Resource reference:**
Terraform lubab ressurssidel üksteisele viidata. Näiteks container saab viidata network'ile: `docker_network.ubuntu1_net.name`. See loob **automaatse sõltuvuse** - Terraform loob network'i enne container'it.

Lisage **main.tf** faili:
```hcl
# Network Ubuntu-1's
resource "docker_network" "ubuntu1_net" {
  provider = docker.ubuntu1  # OLULINE: millisesse serverisse
  name     = "${var.project_name}-net"
  
  ipam_config {
    subnet  = "172.20.0.0/16"  # IP vahemik selles võrgus
    gateway = "172.20.0.1"      # Gateway aadress
  }
}
```

**Selgitus:**
- `provider = docker.ubuntu1` - kasutab ubuntu1 provider'it (alias sealt!)
- `docker_network` - ressursi tüüp
- `"ubuntu1_net"` - meie nimi sellele (Terraform'is, mitte Docker'is)
- `name = "..."` - nimi Docker'is (see, mida `docker network ls` näitab)
- Hiljem viitame: `docker_network.ubuntu1_net.name`

Apply:
```powershell
terraform apply
```

Kontrollige Ubuntu-1's:
```bash
ssh student@10.0.X.20
docker network ls | grep tf-lab
exit
```

---

## 8. Database Ubuntu-1's

Loome PostgreSQL container Ubuntu-1 serverisse. Container vajab image't ja volume'it.

**Image vs Container:**
- **Image** = template (nagu ISO fail)
- **Container** = jooksev instance image'ist (nagu VM ISO'st)

**Viited teistele ressurssidele:**
- `docker_image.postgres.image_id` - viitab image resource'ile (Terraform loob image enne)
- `docker_volume.ubuntu1_db_data.name` - viitab volume'ile
- `docker_network.ubuntu1_net.name` - viitab network'ile

Terraform näeb neid viiteid ja teab automaatselt: "Loon image → volume → network → siis container"

Lisage **main.tf** faili:
```hcl
# Volume Ubuntu-1's
resource "docker_volume" "ubuntu1_db_data" {
  provider = docker.ubuntu1
  name     = "${var.project_name}-db-data"
}

# DB Image
resource "docker_image" "postgres" {
  provider = docker.ubuntu1
  name     = "postgres:15-alpine"
}

# DB Container Ubuntu-1's
resource "docker_container" "ubuntu1_db" {
  provider = docker.ubuntu1
  
  name  = "${var.project_name}-db"
  image = docker_image.postgres.image_id  # Viide image'ile (automaatne dependency!)
  
  networks_advanced {
    name = docker_network.ubuntu1_net.name  # Viide network'ile
  }
  
  volumes {
    volume_name    = docker_volume.ubuntu1_db_data.name  # Viide volume'ile
    container_path = "/var/lib/postgresql/data"          # Kus Postgres andmeid hoiab
  }
  
  env = [
    "POSTGRES_USER=appuser",
    "POSTGRES_PASSWORD=apppass",
    "POSTGRES_DB=appdb"
  ]
  
  restart = "unless-stopped"  # Kui crashib, Docker käivitab uuesti
  
  # Healthcheck - kontrollib, kas DB töötab
  healthcheck {
    test     = ["CMD-SHELL", "pg_isready -U appuser"]  # Käsk kontrolli jaoks
    interval = "10s"   # Kontrolli iga 10 sekundi tagant
    timeout  = "5s"    # Kui 5 sek ei vasta, on unhealthy
    retries  = 5       # 5 ebaõnnestumist järjest = unhealthy
  }
}
```

**Mis siin toimub:**
1. Terraform loob volume'i (püsiv salvestus)
2. Laeb alla postgres image'i
3. Loob container'i, mis:
   - Kasutab seda image't
   - Ühendub network'iga (et teised containerid näeksid)
   - Mountib volume'i (et andmed jääksid alles)
   - Saab env var'id (kasutajanimi, parool)
4. Healthcheck kontrollib, kas DB vastab (`pg_isready` käsk)

Apply:
```powershell
terraform apply
```

Kontrollige:
```bash
ssh student@10.0.X.20
docker ps | grep db
docker exec tf-lab-db pg_isready -U appuser
exit
```

---

## 9. Web Containers Mõlemas Serveris

Nüüd huvitav osa - loome web container'id **mõlemasse** serverisse korraga.

**Count - ressurssi kordamine:**
- `count = 2` tähendab: "Loo 2 identset"
- Terraform annab igaüle indeksi: 0, 1
- Viitame neile: `docker_container.ubuntu1_web[0]`, `docker_container.ubuntu1_web[1]`
- Kasutame `count.index` koodi sees: `name = "web-${count.index}"` → `web-0`, `web-1`

**Upload provisioner:**
- Saadab sisu container'isse
- Kasulik lihtsate failide jaoks (HTML, config)
- Alternatiiv: mount volume või build oma image

**Depends_on - explicit dependency:**
Tavaliselt Terraform avastab dependencies automaatselt (kui viitad teisele resource'ile). Aga vahel peame ütlema: "Oota, kuni DB on valmis, alles siis tee web". See on `depends_on`.

Lisage **main.tf** faili:
```hcl
# Nginx image Ubuntu-1's
resource "docker_image" "ubuntu1_nginx" {
  provider = docker.ubuntu1
  name     = "nginx:alpine"
}

# Nginx image Ubuntu-2's
resource "docker_image" "ubuntu2_nginx" {
  provider = docker.ubuntu2
  name     = "nginx:alpine"
}

# Network Ubuntu-2's (vajame selleks, et containerid seal töötaksid)
resource "docker_network" "ubuntu2_net" {
  provider = docker.ubuntu2
  name     = "${var.project_name}-net"
  
  ipam_config {
    subnet  = "172.21.0.0/16"
    gateway = "172.21.0.1"
  }
}

# Web containers Ubuntu-1's (2 tk)
resource "docker_container" "ubuntu1_web" {
  provider = docker.ubuntu1
  count    = 2  # Loob 2 identset container'it
  
  name  = "${var.project_name}-u1-web-${count.index}"  # web-0, web-1
  image = docker_image.ubuntu1_nginx.image_id
  
  networks_advanced {
    name = docker_network.ubuntu1_net.name
  }
  
  ports {
    internal = 80
    external = 8080 + count.index  # 8080, 8081 (count.index = 0, 1)
  }
  
  # Upload - saadab HTML sisu container'isse
  upload {
    content = <<-EOF
      <!DOCTYPE html>
      <html>
      <head><title>Ubuntu-1 Web ${count.index}</title></head>
      <body style="font-family: Arial; padding: 50px;">
        <h1>Terraform Remote Docker Lab</h1>
        <p><strong>Host:</strong> Ubuntu-1</p>
        <p><strong>Container:</strong> web-${count.index}</p>
        <p><strong>Network:</strong> ${docker_network.ubuntu1_net.name}</p>
        <p><strong>Database:</strong> ${docker_container.ubuntu1_db.name}</p>
      </body>
      </html>
    EOF
    file = "/usr/share/nginx/html/index.html"  # Kuhu panna
  }
  
  restart = "unless-stopped"
  
  # Explicit dependency: oota kuni DB on valmis
  depends_on = [docker_container.ubuntu1_db]
}

# Web containers Ubuntu-2's (2 tk)
resource "docker_container" "ubuntu2_web" {
  provider = docker.ubuntu2  # Teine server!
  count    = 2
  
  name  = "${var.project_name}-u2-web-${count.index}"
  image = docker_image.ubuntu2_nginx.image_id
  
  networks_advanced {
    name = docker_network.ubuntu2_net.name
  }
  
  ports {
    internal = 80
    external = 8080 + count.index
  }
  
  upload {
    content = <<-EOF
      <!DOCTYPE html>
      <html>
      <head><title>Ubuntu-2 Web ${count.index}</title></head>
      <body style="font-family: Arial; padding: 50px; background: #f0f8ff;">
        <h1>Terraform Remote Docker Lab</h1>
        <p><strong>Host:</strong> Ubuntu-2</p>
        <p><strong>Container:</strong> web-${count.index}</p>
        <p><strong>Network:</strong> ${docker_network.ubuntu2_net.name}</p>
      </body>
      </html>
    EOF
    file = "/usr/share/nginx/html/index.html"
  }
  
  restart = "unless-stopped"
}
```

Apply:
```powershell
terraform apply
```

Terraform loob:
- Ubuntu-1: 2 web container'it + 1 database
- Ubuntu-2: 2 web container'it

---

## 10. Outputs

Outputs teevad info kergesti kättesaadavaks pärast `terraform apply`.

**For loop Terraform'is:**
```hcl
for i in range(2) : "..."
```
See käib läbi 0, 1 ja teeb iga numbri jaoks midagi. Nagu `for i in [0, 1]` Python'is.

**Concat:**
Ühendab kaks list'i kokku: `concat([1,2], [3,4])` → `[1,2,3,4]`

**outputs.tf:**
```hcl
output "ubuntu1_containers" {
  description = "Ubuntu-1 containers"
  value = {
    database = docker_container.ubuntu1_db.name
    web = [
      for i in range(2) :  # For loop: i = 0, siis i = 1
      "${docker_container.ubuntu1_web[i].name} - http://${var.ubuntu1_host}:${8080 + i}"
    ]
  }
}

output "ubuntu2_containers" {
  description = "Ubuntu-2 containers"
  value = {
    web = [
      for i in range(2) :
      "${docker_container.ubuntu2_web[i].name} - http://${var.ubuntu2_host}:${8080 + i}"
    ]
  }
}

output "all_web_urls" {
  description = "All web URLs"
  value = concat(
    [for i in range(2) : "http://${var.ubuntu1_host}:${8080 + i}"],  # Ubuntu-1 URL'id
    [for i in range(2) : "http://${var.ubuntu2_host}:${8080 + i}"]   # Ubuntu-2 URL'id
  )  # Kokku 4 URL'i
}
```

**Mis siin toimub:**
- `for i in range(2)` käib läbi 0, 1
- `docker_container.ubuntu1_web[i]` - viitab container'ile indeksiga (count!)
- `concat(list1, list2)` - ühendab kaks list'i üheks
- Tulemus: Ubuntu-1 ja Ubuntu-2 URL'id ühes list'is

Apply:
```powershell
terraform apply
```

Vaadake outpute:
```powershell
terraform output
```

---

## 11. Testimine

### Windows'ist (brauser)

Avage URL'id outputist (asendage X oma võrgu numbriga):
- `http://10.0.X.20:8080` (Ubuntu-1, web-0)
- `http://10.0.X.20:8081` (Ubuntu-1, web-1)
- `http://10.0.X.21:8080` (Ubuntu-2, web-0)
- `http://10.0.X.21:8081` (Ubuntu-2, web-1)

### PowerShell'ist

```powershell
# Asendage X oma võrgu numbriga
Invoke-WebRequest -Uri "http://10.0.X.20:8080" -UseBasicParsing
Invoke-WebRequest -Uri "http://10.0.X.21:8080" -UseBasicParsing
```

### SSH üle

```bash
# Ubuntu-1
ssh student@10.0.X.20
docker ps
curl http://localhost:8080
exit

# Ubuntu-2
ssh student@10.0.X.21
docker ps
curl http://localhost:8080
exit
```

---

## 11. State Kontrollimine

```powershell
# Kõik ressursid
terraform state list

# Ubuntu-1 containerid
terraform state list | Select-String "ubuntu1"

# Ubuntu-2 containerid
terraform state list | Select-String "ubuntu2"

# Ühe ressursi detailid
terraform state show docker_container.ubuntu1_web[0]
```

State fail sisaldab **mõlema** Ubuntu serveri ressursse. Terraform haldab neid centraliseeritult Windows'ist.

---

## 12. Distributed Deployment Test

Muutke count'i:

**main.tf**, muutke count 2 → 3:
```hcl
resource "docker_container" "ubuntu1_web" {
  count = 3  # oli 2
  # ...
}

resource "docker_container" "ubuntu2_web" {
  count = 3  # oli 2
  # ...
}
```

Apply:
```powershell
terraform apply
```

Terraform lisab:
- Ubuntu-1: web-2 (port 8082)
- Ubuntu-2: web-2 (port 8082)

Kontrollige:
```bash
ssh student@10.0.X.20 "docker ps | grep web"
ssh student@10.0.X.21 "docker ps | grep web"
```

Mõlemad serverid said uue container'i **korraga**.

---

## 13. Database Connection Test

Kontrollige, et web container näeb database't:

```bash
ssh student@10.0.X.20

# Web container'ist DB'sse
docker exec tf-lab-u1-web-0 ping -c 2 tf-lab-db

# Või otse psql'iga
docker exec tf-lab-db psql -U appuser -d appdb -c "SELECT version();"

exit
```

---

## 14. Cleanup

Kustutage **kõik** ressursid **mõlemas** serveris:

```powershell
terraform destroy
```

Kirjutage "yes".

Terraform kustutab:
1. Ubuntu-2: web containers → network
2. Ubuntu-1: web containers → db container → volume → network

Kontrollige:
```bash
ssh student@10.0.X.20 "docker ps -a"
ssh student@10.0.X.21 "docker ps -a"
# Peaks olema tühi
```

---

## Kokkuvõte

**Lõite:**
- Remote Docker infrastruktuuri kahes serveris
- Database Ubuntu-1's volume'iga
- Web containerid mõlemas serveris
- Distributed deployment count'iga
- Centraliseeritud state management Windows'is

**Õppisite:**
- Docker provider SSH connection'iga
- Multi-provider konfiguratsioon (alias)
- Remote resource management
- Distributed container orchestration
- Cross-host networking concepts

**Mis see annab:**
- Simuleerib päris multi-server setup'i
- Õpetab remote infrastructure management'i
- Valmistab ette AWS/Azure deployment'iks
- Näitab Terraform'i võimsust distributed systems'is

**Järgmine samm:**
- AWS labor: Same concept, aga EC2 instances pilves
- Kubernetes: Container orchestration järgmine level

---

## Troubleshooting

### SSH connection fails

```powershell
# Windows'ist testi SSH käsitsi (asendage X oma võrgu numbriga)
ssh -i C:/Users/YourName/.ssh/id_rsa student@10.0.X.20

# Kui ei tööta, kontrolli:
# 1. IP aadress õige?
# 2. SSH key path õige?
# 3. SSH daemon töötab Ubuntu's?
```

Ubuntu'is:
```bash
sudo systemctl status ssh
sudo systemctl start ssh
```

### Docker daemon not accessible

```bash
# Ubuntu'is
sudo systemctl status docker
sudo systemctl start docker

# Lisa user docker gruppi
sudo usermod -aG docker $USER
# Logige välja ja sisse
```

### Port conflicts

Kui port juba kasutusel:

**main.tf:**
```hcl
ports {
  internal = 80
  external = 9080 + count.index  # Muutke 8080 -> 9080
}
```

### Firewall blocks ports

Ubuntu'is:
```bash
# Luba port 8080-8082
sudo ufw allow 8080:8082/tcp

# Või keela firewall (labor'is OK)
sudo ufw disable
```

### State lock

```powershell
terraform force-unlock <LOCK_ID>
```

### Provider alias confusion

Alati määrake provider:
```hcl
resource "docker_container" "web" {
  provider = docker.ubuntu1  # Ära unusta!
  # ...
}
```

Ilma provider'ita Terraform ei tea, millisesse serverisse luua.

---

## 2. Provider ja Variables

Loome provider konfiguratsiooni ja muutujad korraga.

**variables.tf:**
```hcl
variable "project_name" {
  description = "Project name for naming resources"
  type        = string
  default     = "tf-docker-lab"
}

variable "environment" {
  description = "Environment (dev/prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Environment must be dev or prod"
  }
}

variable "web_count" {
  description = "Number of web containers"
  type        = number
  default     = 2
}
```

**main.tf:**
```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}
```

Init:
```bash
terraform init
```

Peaks nägema: "Installing kreuzwerker/docker v3.x.x..."

---

## 3. Network ja Volume

Network on nagu VPC AWS'is - isoleeritud võrk containeritele. Volume säilitab andmeid ka siis, kui container kustutatakse.

Lisage **main.tf** faili:
```hcl
# Network (VPC equivalent)
resource "docker_network" "app" {
  name = "${var.project_name}-network"
  
  ipam_config {
    subnet  = "172.20.0.0/16"
    gateway = "172.20.0.1"
  }
}

# Volume andmebaasile (EBS equivalent)
resource "docker_volume" "db_data" {
  name = "${var.project_name}-db-data"
}
```

Apply:
```bash
terraform plan
terraform apply
```

Kontrollige:
```bash
docker network ls | grep tf-docker-lab
docker volume ls | grep tf-docker-lab
```

---

## 4. Database Container

Loome PostgreSQL container'i, mis kasutab volume'it andmete säilitamiseks.

Lisage **main.tf** faili:
```hcl
# Database image
resource "docker_image" "postgres" {
  name = "postgres:15-alpine"
}

# Database container
resource "docker_container" "db" {
  name  = "${var.project_name}-db"
  image = docker_image.postgres.image_id
  
  networks_advanced {
    name = docker_network.app.name
  }
  
  volumes {
    volume_name    = docker_volume.db_data.name
    container_path = "/var/lib/postgresql/data"
  }
  
  env = [
    "POSTGRES_USER=appuser",
    "POSTGRES_PASSWORD=apppass",
    "POSTGRES_DB=appdb"
  ]
  
  restart = "unless-stopped"
  
  # Healthcheck
  healthcheck {
    test     = ["CMD-SHELL", "pg_isready -U appuser"]
    interval = "10s"
    timeout  = "5s"
    retries  = 5
  }
}
```

Apply:
```bash
terraform apply
```

Kontrollige:
```bash
# Container jookseb?
docker ps | grep db

# DB vastab?
docker exec tf-docker-lab-db pg_isready -U appuser
```

---

## 5. Web Containers (Count)

Loome mitu nginx container'it korraga kasutades `count`. See on nagu AWS'is luua mitu EC2 instance'i.

Lisage **main.tf** faili:
```hcl
# Web image
resource "docker_image" "nginx" {
  name = "nginx:alpine"
}

# Web containers (multiple)
resource "docker_container" "web" {
  count = var.web_count
  
  name  = "${var.project_name}-web-${count.index}"
  image = docker_image.nginx.image_id
  
  networks_advanced {
    name = docker_network.app.name
  }
  
  ports {
    internal = 80
    external = 8080 + count.index
  }
  
  # Custom HTML
  upload {
    content = <<-EOF
      <!DOCTYPE html>
      <html>
      <head><title>Web ${count.index}</title></head>
      <body style="font-family: Arial; padding: 50px;">
        <h1>Terraform Docker Lab</h1>
        <p><strong>Container:</strong> web-${count.index}</p>
        <p><strong>Environment:</strong> ${var.environment}</p>
        <p><strong>Network:</strong> ${docker_network.app.name}</p>
      </body>
      </html>
    EOF
    file = "/usr/share/nginx/html/index.html"
  }
  
  restart = "unless-stopped"
  
  # Web sõltub DB'st
  depends_on = [docker_container.db]
}
```

Apply:
```bash
terraform apply
```

Terraform loob 2 web container'it (default `web_count = 2`):
- tf-docker-lab-web-0 (port 8080)
- tf-docker-lab-web-1 (port 8081)

Kontrollige:
```bash
# Mõlemad jooksevad?
docker ps | grep web

# Testi brauseris
curl http://localhost:8080
curl http://localhost:8081
```

---

## 6. Outputs

Outputs teevad info kergesti kättesaadavaks.

Looge **outputs.tf:**
```hcl
output "network_id" {
  description = "Network ID"
  value       = docker_network.app.id
}

output "database_name" {
  description = "Database container name"
  value       = docker_container.db.name
}

output "web_urls" {
  description = "Web container URLs"
  value = [
    for i in range(var.web_count) :
    "http://localhost:${8080 + i}"
  ]
}

output "container_ips" {
  description = "Container IP addresses in network"
  value = {
    database = docker_container.db.network_data[0].ip_address
    web = [
      for container in docker_container.web :
      container.network_data[0].ip_address
    ]
  }
}
```

Apply:
```bash
terraform apply
```

Vaadake outpute:
```bash
terraform output
terraform output -json | jq
```

---

## 7. Muudatuste Testimine

Muutke `web_count` 2 → 3:

**terminal:**
```bash
terraform apply -var="web_count=3"
```

Terraform lisab ühe container'i. Pole vaja kõike uuesti luua - see on Terraform'i tugevus.

Vaadake:
```bash
docker ps | grep web
# Peaks nägema: web-0, web-1, web-2

curl http://localhost:8082
# Uus container vastab
```

Muutke tagasi:
```bash
terraform apply -var="web_count=2"
```

Terraform kustutab web-2. web-0 ja web-1 jäävad puutumata.

---

## 8. State Kontrollimine

State fail sisaldab kogu infrastruktuuri infot:

```bash
# Kõik ressursid
terraform state list

# Ühe ressursi detailid
terraform state show docker_container.web[0]

# Kontrolli sünkroniseeritust
terraform plan
# Peaks näitama "No changes"
```

Kui plan näitab muudatusi (aga te ei muutnud koodi), siis keegi muutis container'eid käsitsi Docker'iga - see on **drift**.

---

## 9. Environment Testimine

Muutke environment dev → prod:

```bash
terraform apply -var="environment=prod"
```

Terraform uuendab container'eid (HTML sisu muutub). Vaadake:
```bash
curl http://localhost:8080
# Peaks nägema: "Environment: prod"
```

Muutke tagasi:
```bash
terraform apply -var="environment=dev"
```

---

## 10. Andmete Püsivus

Testimine, et volume töötab:

```bash
# Looge andmed DB's
docker exec tf-docker-lab-db psql -U appuser -d appdb -c "CREATE TABLE test (id INT, data TEXT);"
docker exec tf-docker-lab-db psql -U appuser -d appdb -c "INSERT INTO test VALUES (1, 'Hello Terraform');"

# Kontrollige
docker exec tf-docker-lab-db psql -U appuser -d appdb -c "SELECT * FROM test;"

# Kustuta container (aga mitte volume)
docker stop tf-docker-lab-db
docker rm tf-docker-lab-db

# Loo container uuesti Terraform'iga
terraform apply

# Andmed on alles!
docker exec tf-docker-lab-db psql -U appuser -d appdb -c "SELECT * FROM test;"
```

See tõestab, et volume säilitab andmeid ka siis, kui container kustutatakse.

---

## 11. Cleanup

Kustutage kõik ressursid:
```bash
terraform destroy
```

Kirjutage "yes".

Kontrollige:
```bash
docker ps -a | grep tf-docker-lab
# Peaks olema tühi

docker network ls | grep tf-docker-lab
# Peaks olema tühi

docker volume ls | grep tf-docker-lab
# Peaks olema tühi
```

**OLULINE:** Kui unustate destroy, jooksevad containerid edasi ja võtavad ressursse (CPU, RAM).

---

## Kokkuvõte

**Lõite:**
- Docker network'i (isoleeritud võrk)
- PostgreSQL container'i volume'iga
- Mitu nginx container'it count'iga
- Custom HTML sisu upload'iga
- Outputs info jagamiseks

**Õppisite:**
- Docker provider konfiguratsioon
- Network loomine (VPC analoog)
- Volume'id püsivaks salvestuseks
- Count resource'ide korrutamiseks
- Dependencies (depends_on)
- Upload provisioner
- Variables kasutamine
- State management

**Mis edasi:**
- Kodutöö: Ehitage sama, aga teise rakendusega
- AWS labor: Rakendage neid kontsepte pilves (kellel konto on)

---

## Troubleshooting

### Provider connection error

```bash
# Kontrolli, et Docker daemon töötab
sudo systemctl status docker

# Kui ei tööta
sudo systemctl start docker

# Lisage end docker gruppi (kui vaja)
sudo usermod -aG docker $USER
# Logige välja ja sisse
```

### Port already in use

```bash
# Vaata, mis port 8080 kasutab
sudo lsof -i :8080

# Muutke external porti
# main.tf: external = 9080 + count.index
```

### Container ei käivitu

```bash
# Vaata loge
docker logs tf-docker-lab-web-0

# Käivita interaktiivselt
docker run -it --rm nginx:alpine sh
```

### Volume'i ei saa kustutada

```bash
# Peata kõik containerid
docker stop $(docker ps -aq)

# Kustuta käsitsi
docker volume rm tf-docker-lab-db-data

# Siis terraform destroy
terraform destroy
```

### State lock

```bash
# Kui crash jättis luku kinni
terraform force-unlock <LOCK_ID>
```

---

## 16. Esitamine

### Git Repository

**PowerShell'is** (terraform-docker-lab kaustas):

```powershell
# Git repo
git init

# .gitignore
@"
.terraform/
*.tfstate*
*.retry
.vscode/
*.pem
*.key
*_rsa*
"@ | Out-File .gitignore -Encoding utf8

# Commit
git add .
git commit -m "Terraform Docker lab"
```

### GitHub

1. [github.com](https://github.com) → New repository
2. **Name:** `terraform-docker-lab`
3. **Public**
4. Create

```powershell
git remote add origin https://github.com/USERNAME/terraform-docker-lab.git
git branch -M main
git push -u origin main
```

### README.md

```markdown
# Terraform Docker Lab

**Autor:** [Nimi]

## Infrastruktuur
- 2 Ubuntu serverit
- 5 containerit (1 DB + 4 web)
- Ansible + Terraform

## Kasutamine
\`\`\`bash
ansible-playbook -i inventory.ini docker-setup.yml
terraform apply
\`\`\`

## Screenshots
(lisa siia)
```
