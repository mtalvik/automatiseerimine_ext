# Terraform Edasijõudnud Kodutöö: Dockeriseeritud Node.js App AWS'is

See kodutöö ehitab labori teadmistele peale. Loote AWS VPC infrastruktuuri, kus jookseb Node.js rakendus Docker konteineris. Eeldatav aeg: 1.5 tundi.

**Eeldused:** Labor tehtud, Docker põhiteadmised, AWS konto Free Tier'iga

**Esitamine:** GitHub repo link (public või private + õpetaja access)

**Tähtaeg:** 1 nädal alates labori tegemisest

---

## Ülesande kirjeldus

Loote pilve infrastruktuuri Terraform'iga, mis:

- Käivitab EC2 instance'i Free Tier t2.micro'ga
- Jooksutab seal Docker'it
- Deploy'ib lihtsa Node.js To-Do API rakenduse
- Võimaldab avalikku ligipääsu HTTP kaudu

See ei ole toy project - see on päris minimaalne architecture, mis sarnaneb reaalsete startup'ide MVP'dele.

---

## 1. Projekti Struktuur

Looge selline failide struktuur:
```
terraform-aws-homework/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── app/
│   ├── server.js
│   ├── package.json
│   └── Dockerfile
└── README.md
```

---

## 2. Node.js Rakendus

Esmalt looge rakendus, mida deploy'ida.

### app/package.json
```json
{
  "name": "todo-api",
  "version": "1.0.0",
  "main": "server.js",
  "dependencies": {
    "express": "^4.18.0"
  },
  "scripts": {
    "start": "node server.js"
  }
}
```

### app/server.js
```javascript
const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

// In-memory storage
let todos = [
  { id: 1, task: "Õpi Terraform'i", done: false },
  { id: 2, task: "Deploy pilve", done: false }
];

// GET /todos - List all
app.get('/todos', (req, res) => {
  res.json(todos);
});

// POST /todos - Create new
app.post('/todos', (req, res) => {
  const newTodo = {
    id: todos.length + 1,
    task: req.body.task,
    done: false
  };
  todos.push(newTodo);
  res.status(201).json(newTodo);
});

// DELETE /todos/:id - Delete
app.delete('/todos/:id', (req, res) => {
  todos = todos.filter(t => t.id !== parseInt(req.params.id));
  res.status(204).send();
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date() });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Todo API running on port ${PORT}`);
});
```

### app/Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json .
RUN npm install --production

COPY server.js .

EXPOSE 3000

CMD ["npm", "start"]
```

---

## 3. Terraform Konfiguratsioon

### variables.tf
```hcl
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "my_ip" {
  description = "Your IP address for SSH access (get from ifconfig.me)"
  type        = string
}

variable "docker_image" {
  description = "Docker image name"
  type        = string
  default     = "todo-api"
}
```

### terraform.tfvars
```hcl
project_name = "nimi-projekti"  # MUUTKE OMA NIMEKS!
my_ip        = "0.0.0.0/0"      # MUUTKE OMA IP'KS! (curl ifconfig.me)
```

### main.tf - VPC ja Võrk
```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Public Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"
  
  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

# Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

# Route Table Association
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
```

### main.tf - Security Group
```hcl
# Security Group
resource "aws_security_group" "app" {
  name_prefix = "${var.project_name}-app-"
  description = "Allow HTTP for app and SSH for management"
  vpc_id      = aws_vpc.main.id
  
  # HTTP in (port 3000 - Node.js app)
  ingress {
    description = "HTTP to Node app"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # SSH in (ainult teie IP!)
  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }
  
  # All out
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-app-sg"
  }
  
  lifecycle {
    create_before_destroy = true
  }
}
```

### main.tf - EC2 Instance
```hcl
# SSH Key
resource "aws_key_pair" "deployer" {
  key_name   = "${var.project_name}-key"
  public_key = file("~/.ssh/id_rsa.pub")  # Kasutage olemasolevat või looge uus
}

# EC2 Instance
resource "aws_instance" "app" {
  ami                    = "ami-0d71ea30463e0ff8d"  # Amazon Linux 2023
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.app.id]
  subnet_id              = aws_subnet.public.id
  
  user_data = <<-EOF
              #!/bin/bash
              set -e
              
              # Update ja install Docker
              yum update -y
              yum install -y docker git
              
              # Start Docker
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ec2-user
              
              # Install Docker Compose
              curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              
              # Clone app files või copy (see on placeholder - päris elus clone GitHubist)
              mkdir -p /home/ec2-user/app
              cd /home/ec2-user/app
              
              # Build ja run konteiner
              # SIIN TULEB TEIL DEPLOYDA OMA APP!
              # Võimalused:
              # 1. Git clone from GitHub
              # 2. Copy files via S3
              # 3. Bake into custom AMI
              
              echo "App deployment placeholder - customize this!"
              EOF
  
  tags = {
    Name = "${var.project_name}-app-server"
  }
}
```

### outputs.tf
```hcl
output "instance_public_ip" {
  description = "EC2 public IP"
  value       = aws_instance.app.public_ip
}

output "api_url" {
  description = "API URL"
  value       = "http://${aws_instance.app.public_ip}:3000"
}

output "health_check" {
  description = "Health check endpoint"
  value       = "http://${aws_instance.app.public_ip}:3000/health"
}

output "ssh_command" {
  description = "SSH connection command"
  value       = "ssh -i ~/.ssh/id_rsa ec2-user@${aws_instance.app.public_ip}"
}
```

---

## 4. Deployment Sammud

### 4.1 Lokaalne Testimine

Enne AWS'i deploy'imist teste lokaalselt:
```bash
cd app/

# Build Docker image
docker build -t todo-api .

# Run konteiner
docker run -p 3000:3000 todo-api

# Teises terminalis testi
curl http://localhost:3000/health
curl http://localhost:3000/todos

# Stop konteiner
docker stop $(docker ps -q --filter ancestor=todo-api)
```

### 4.2 Terraform Deploy
```bash
# Initsialiseerige
terraform init

# Vaadake plaani
terraform plan

# Deploy
terraform apply
```

### 4.3 App Deploy Serverisse

Terraform on loonud serveri, aga app pole veel seal. Teil on 3 võimalust:

**Variant A: Manual Deploy (kõige lihtsam õppimiseks)**
```bash
# SSH serverisse
ssh -i ~/.ssh/id_rsa ec2-user@<PUBLIC_IP>

# Loo app failid
mkdir -p ~/app
cd ~/app

# Kopeeri server.js sisu (vim või nano)
cat > server.js << 'JS'
[paste server.js sisu siia]
JS

# Kopeeri package.json
cat > package.json << 'JSON'
[paste package.json sisu siia]
JSON

# Kopeeri Dockerfile
cat > Dockerfile << 'DOCKER'
[paste Dockerfile sisu siia]
DOCKER

# Build ja run
sudo docker build -t todo-api .
sudo docker run -d -p 3000:3000 --name todo-api --restart unless-stopped todo-api

# Kontrolli
sudo docker ps
curl localhost:3000/health
```

**Variant B: GitHub Deploy (professionaalne)**

Pange app kaust GitHubi ja muutke user_data:
```bash
#!/bin/bash
# ...docker install...

cd /home/ec2-user
git clone https://github.com/TEIE-USERNAME/terraform-aws-homework.git
cd terraform-aws-homework/app
docker build -t todo-api .
docker run -d -p 3000:3000 --name todo-api --restart unless-stopped todo-api
```

**Variant C: S3 Deploy**

Upload app failid S3'i ja download user_data's.

---

## 5. Testimine

Kui app jookseb, teste:
```bash
# Health check
curl http://<PUBLIC_IP>:3000/health

# List todos
curl http://<PUBLIC_IP>:3000/todos

# Create todo
curl -X POST http://<PUBLIC_IP>:3000/todos \
  -H "Content-Type: application/json" \
  -d '{"task":"Test Terraform homework"}'

# List again (peaks nüüd 3 olema)
curl http://<PUBLIC_IP>:3000/todos

# Delete todo
curl -X DELETE http://<PUBLIC_IP>:3000/todos/3

# Brauseris
http://<PUBLIC_IP>:3000/todos
```

---

## 6. README.md

Kirjutage projekti dokumentatsioon. README.md peab sisaldama:
```markdown
# Terraform AWS Docker Deployment

## Projekti Kirjeldus
[Mida see projekt teeb]

## Arhitektuur
- **VPC:** 10.0.0.0/16
- **Subnet:** 10.0.1.0/24 (public)
- **Instance:** t2.micro Amazon Linux 2023
- **App:** Node.js To-Do API Docker konteineris
- **Port:** 3000

## Eeldused
- AWS konto Free Tier'iga
- Terraform >= 1.0
- AWS CLI configured
- SSH key ~/.ssh/id_rsa

## Seadistamine

1. Clone repo:
```bash
git clone <repo-url>
cd terraform-aws-homework
```

2. Muuda `terraform.tfvars`:
```hcl
project_name = "minu-nimi"
my_ip        = "xxx.xxx.xxx.xxx/32"  # curl ifconfig.me
```

3. Deploy:
```bash
terraform init
terraform apply
```

4. Deploy app (vaata juhendit allpool)

## App Deployment
[Täpsed sammud, kuidas te app'i deploy'isite]

## Kasutamine
```bash
# API endpoint
curl http://<IP>:3000/todos

# Health check
curl http://<IP>:3000/health
```

## Cleanup
**OLULINE!** Kustuta ressursid kulude vältimiseks:
```bash
terraform destroy
```

## Refleksioon

### 1. Mis oli kõige raskem ja kuidas lahendasid?
[Teie vastus 2-3 lauset]

### 2. Milline kontseptsioon oli suurim "ahaa!" hetk?
[Teie vastus 2-3 lauset]

### 3. Kuidas kasutaksid seda tulevikus?
[Teie vastus 2-3 lauset]

### 4. Kuidas selgitaksid sõbrale, mis on Infrastructure as Code?
[Teie vastus 2-3 lauset]

### 5. Mis oli kõige huvitavam osa?
[Teie vastus 2-3 lauset]
```

---

## Esitamine

### Kontrollnimekiri

Enne esitamist veenduge:

- [ ] GitHub repo on loodud (public või private + õpetaja access)
- [ ] Kõik failid on Git'is (`main.tf`, `variables.tf`, `outputs.tf`, `app/*`, `README.md`)
- [ ] README.md sisaldab refleksiooni vastuseid
- [ ] `terraform apply` töötab ilma vigadeta
- [ ] API vastab HTTP päringutele
- [ ] Terraform output näitab õigeid väärtuseid
- [ ] **KRIITILINE:** `terraform destroy` on käivitatud (ressursid kustutatud!)
- [ ] Screenshot või video app tööst (lisage README.md'sse või repo)

### Esitamisviis

Esitage GitHub repo link õppejõule. Repo peab sisaldama:

- Kogu Terraform koodi
- App koodi
- README.md dokumentatsiooni
- (Valikuline) Screenshots või video demo

---

## Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **Terraform kood** | 30% | VPC, security groups, EC2 korrektsed |
| **App deployment** | 25% | Node.js app jookseb Docker konteineris |
| **API testimine** | 15% | Kõik endpoints töötavad |
| **Dokumentatsioon** | 15% | README täielik, refleksioon sisukas |
| **Infrastructure cleanup** | 10% | Tõendus, et destroy käivitati |
| **Koodikvaliteet** | 5% | Variables kasutatud, outputs selged |

**Kokku:** 100%

### Hindamisskaala

- **90-100%:** Suurepärane
- kõik töötab, dokumentatsioon professionaalne
- **75-89%:** Hea
- töötab, väiksed puudused dokumentatsioonis
- **60-74%:** Rahuldav
- põhifunktsionaalsus töötab
- **< 60%:** Mitterahuldav
- olulised osad puudu või ei tööta

---

## Boonus (+10%)

Tehke üks järgnevatest:

### Boonus 1: Nginx Reverse Proxy

Lisa nginx konteiner, mis proxy'b API:

- nginx kuulab port 80
- Proxy'b päringud port 3000'le
- HTTPS redirect (self-signed cert)

### Boonus 2: Docker Compose

Kasuta Docker Compose'i:

- Multi-container setup (app + nginx)
- Persistent volume To-Do storage'ks
- docker-compose.yml fail

### Boonus 3: CloudWatch Monitoring

Lisa AWS CloudWatch:

- CPU/Memory alarms
- Log group EC2 instance'ile
- SNS notification emailiga

### Boonus 4: Auto Scaling (Advanced!)

Lisa:

- Launch Template
- Auto Scaling Group (min 1, max 2)
- Application Load Balancer
- Health checks

---

## Kasulikud Ressursid

- [AWS Free Tier](https://aws.amazon.com/free/)
- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Docker Documentation](https://docs.docker.com/)
- [Express.js Guide](https://expressjs.com/en/starter/hello-world.html)

---

## Troubleshooting

### App ei vasta port 3000'l
```bash
# SSH serverisse
ssh -i ~/.ssh/id_rsa ec2-user@<IP>

# Kontrolli Docker containers
sudo docker ps

# Vaata logs
sudo docker logs todo-api

# Kontrolli, kas port avatud
sudo netstat -tulpn | grep 3000

# Restart container
sudo docker restart todo-api
```

### Security Group blokeerib
```bash
# Kontrolli security group rules AWS konsoolist
# EC2 → Security Groups → terraform-...-app-sg
# Peaks lubama port 3000 from 0.0.0.0/0
```

### User Data skript ei käivitunud
```bash
# Vaata user data logi
ssh ...
sudo cat /var/log/cloud-init-output.log

# Käivita käsitsi
sudo bash /var/lib/cloud/instance/user-data.txt
```

---

**Edu kodutööga! Ärge unustage destroy'da pärast testimist!**