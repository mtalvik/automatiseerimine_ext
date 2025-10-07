# Terraform Edasijõudnud Labor: AWS VPC ja Veebiserver

**Eeldused:** Terraform basics labor tehtud, AWS CLI seadistatud, AWS konto olemas

**Platvorm:** AWS (kasutage Free Tier)

## Õpiväljundid

Pärast seda labor'it õpilane:

- Seadistab AWS provider autentimise turvaliselt
- Loob VPC infrastruktuuri subnet'ide ja gatewayga
- Käivitab EC2 instance'i user data'ga
- Rakendab security group reegleid võrguturvalisuseks
- Kasutab outputs'e ressurside info edastamiseks

---

## 1. AWS Provider Seadistamine

Alustame AWS provider konfigureerimisega. Provider ühendab Terraform'i AWS API'ga.

AWS credentials on juba seadistatud AWS CLI kaudu (`aws configure`). Terraform kasutab automaatselt samu credentials'eid.

Looge töökataloog:
```bash
mkdir -p ~/terraform-aws-lab
cd ~/terraform-aws-lab
```

Looge `main.tf`:
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
  region = "eu-west-1"  # Iirimaa
}
```

Initsialiseerige:
```bash
terraform init
```

Näete, kuidas Terraform laeb alla AWS provider plugina. See plugin sisaldab kogu loogika AWS API'ga suhtlemiseks.

### Validation
```bash
# Kontrollige, et provider töötab
terraform providers

# Peaks näitama:
# provider[registry.terraform.io/hashicorp/aws]
```

Kui näete viga "No valid credential sources found", siis käivitage `aws configure` ja sisestage oma AWS access key ja secret key.

---

## 2. VPC Loomine

VPC (Virtual Private Cloud) on isoleeritud võrgukeskkond AWS'is. Kõik teised ressursid lähevad selle võrgu sisse.

Lisage `main.tf` faili:
```hcl
# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name      = "terraform-lab-vpc"
    ManagedBy = "Terraform"
  }
}

# Internet Gateway (võimaldab internetiühendust)
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "terraform-lab-igw"
  }
}

# Public Subnet (kus server elabvpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "eu-west-1a"
  
  tags = {
    Name = "terraform-lab-public-subnet"
    Type = "public"
  }
}

# Route Table (suunab internetiliikluse gateway'le)
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "terraform-lab-public-rt"
  }
}

# Ühenda route table subnet'iga
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
```

Mõelge sellele nagu maja ehitamisele. VPC on krunt, subnet on tuba, internet gateway on uks ja route table on silt, mis näitab, kuidas ukse juurde jõuda.

Apply muudatused:
```bash
terraform plan
# Vaadake põhjalikult, mida luuakse

terraform apply
# Kirjutage "yes"
```

### Validation
```bash
# Vaadake loodud ressursse
terraform show

# Kontrollige AWS konsoolist:
# https://console.aws.amazon.com/vpc/
# Peaks nägema VPC nimega "terraform-lab-vpc"
```

Terraform dependency graph hoolitses, et ressursid loodi õiges järjekorras: VPC → Internet Gateway → Subnet → Route Table → Association.

---

## 3. Security Group Firewall

Security Group kontrollib, milline võrguliiklus serveri juurde jõuab.

Lisage `main.tf` faili:
```hcl
resource "aws_security_group" "web" {
  name_prefix = "terraform-lab-web-"
  description = "Allow HTTP and SSH"
  vpc_id      = aws_vpc.main.id
  
  # HTTP sisse (port 80)
  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # SSH sisse (port 22) - AINULT TEIE IP!
  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # MUUTKE see oma IP'ks!
  }
  
  # Kõik välja
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "terraform-lab-web-sg"
  }
  
  lifecycle {
    create_before_destroy = true
  }
}
```

OLULINE: Tootmises ei tohiks SSH'd avada kõigile IP'dele (0.0.0.0/0). Saate oma IP kätte nii:
```bash
curl ifconfig.me
# Näiteks: 85.253.123.45
# Siis muutke cidr_blocks = ["85.253.123.45/32"]
```

Apply:
```bash
terraform apply
```

### Validation

AWS konsool → EC2 → Security Groups → Peaks nägema "terraform-lab-web-..."

---

## 4. EC2 Instance (Server)

Nüüd loome serveri, mis jookseb meie VPC public subnet'is.

Esmalt vajame SSH võtmepaari. Kui teil pole veel:
```bash
# Looge SSH key (kui pole)
ssh-keygen -t rsa -b 2048 -f ~/.ssh/terraform-lab -N ""
```

Lisage `main.tf` faili:
```hcl
# SSH key pair
resource "aws_key_pair" "deployer" {
  key_name   = "terraform-lab-key"
  public_key = file("~/.ssh/terraform-lab.pub")
}

# EC2 Instance
resource "aws_instance" "web" {
  ami                    = "ami-0d71ea30463e0ff8d"  # Amazon Linux 2023
  instance_type          = "t2.micro"  # Free Tier
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.web.id]
  subnet_id              = aws_subnet.public.id
  
  user_data = <<-EOF
              #!/bin/bash
              # Uuenda pakid
              yum update -y
              
              # Installeeri nginx
              yum install -y nginx
              
              # Loo lihtne veebileht
              cat > /usr/share/nginx/html/index.html <<HTML
              <!DOCTYPE html>
              <html>
              <head>
                  <title>Terraform Lab</title>
                  <style>
                      body {
                          font-family: Arial, sans-serif;
                          max-width: 800px;
                          margin: 50px auto;
                          padding: 20px;
                          background: #f0f0f0;
                      }
                      h1 { color: #4285f4; }
                      .info { background: white; padding: 15px; border-radius: 5px; }
                  </style>
              </head>
              <body>
                  <h1>Tere! See on Terraform'iga loodud server</h1>
                  <div class="info">
                      <p><strong>Hostname:</strong> $(hostname)</p>
                      <p><strong>IP:</strong> $(hostname -I)</p>
                      <p><strong>Loodud:</strong> $(date)</p>
                  </div>
                  <p>See server käib AWS EC2 instance'is, mille lõi Terraform.</p>
              </body>
              </html>
HTML
              
              # Käivita nginx
              systemctl start nginx
              systemctl enable nginx
              EOF
  
  tags = {
    Name = "terraform-lab-web-server"
  }
}
```

User data skript käivitub serveri esimesel käivitumisel. See installib nginx'i ja loob lihtsa veebilehe.

Apply:
```bash
terraform apply
```

Server on valmis ~2 minuti pärast. Terraform tagastab kontrolli kohe, aga user data skript töötab taustal.

### Validation
```bash
# Vaata serveri IP'd
terraform output instance_public_ip

# Oota 2 minutit ja testi brauseris:
# http://<IP_AADRESS>

# Või curl'iga:
curl http://$(terraform output -raw instance_public_ip)
```

Kui lehte ei kuvata kohe, oodake veel minutike - nginx käivitub.

---

## 5. Outputs (Väljundid)

Outputs teevad olulise info kergesti kättesaadavaks.

Looge `outputs.tf`:
```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.web.id
}

output "instance_public_ip" {
  description = "Server public IP address"
  value       = aws_instance.web.public_ip
}

output "website_url" {
  description = "Website URL"
  value       = "http://${aws_instance.web.public_ip}"
}

output "ssh_command" {
  description = "SSH connection command"
  value       = "ssh -i ~/.ssh/terraform-lab ec2-user@${aws_instance.web.public_ip}"
}
```

Apply (outputs ei vaja resursse muuta):
```bash
terraform apply
```

Nüüd saate:
```bash
# Vaata kõiki outpute
terraform output

# Vaata üht outputi
terraform output website_url

# Kopeeri SSH käsk
echo $(terraform output -raw ssh_command)
```

### Validation
```bash
# Testi SSH ühendust
$(terraform output -raw ssh_command)

# Serveris (kui SSH töötab):
systemctl status nginx
# Peaks näitama "active (running)"

exit
```

---

## 6. Variables ja DRY Printsiip

Praegu on palju hardcoded väärtusi. Tehme need konfigureeritavaks.

Looge `variables.tf`:
```hcl
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public subnet CIDR"
  type        = string
  default     = "10.0.1.0/24"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "project_name" {
  description = "Project name for tagging"
  type        = string
  default     = "terraform-lab"
}
```

Nüüd uuendage `main.tf`, et kasutada neid muutujaid:
```hcl
# Provider blokis
provider "aws" {
  region = var.aws_region
}

# VPC blokis
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  # ...
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Subnet blokis
resource "aws_subnet" "public" {
  cidr_block = var.public_subnet_cidr
  # ...
  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

# Instance blokis
resource "aws_instance" "web" {
  instance_type = var.instance_type
  # ...
  tags = {
    Name = "${var.project_name}-web-server"
  }
}
```

Apply (ei muuda ressursse, sest väärtused on samad):
```bash
terraform plan
# Peaks näitama "No changes"

terraform apply
```

Nüüd saate väärtusi muuta ilma koodi muutmata:
```bash
terraform apply -var="project_name=minu-projekt"
```

### Validation
```bash
terraform output
# Vaata, et kõik endiselt töötab
```

---

## 7. State Kontrollimine

Terraform state fail sisaldab kogu infot teie infrastruktuuri kohta.
```bash
# Vaata kõiki ressursse
terraform state list

# Vaata ühe ressursi detaile
terraform state show aws_instance.web

# Vaata state faili suurust
ls -lh terraform.tfstate
```

State fail on JSON formaat. Saate seda vaadata:
```bash
cat terraform.tfstate | jq '.resources[] | {type, name}'
```

### Validation
```bash
# Kontrolli, et state ja AWS on sünkroonis
terraform plan
# Peaks näitama "No changes"
```

Kui plan näitab muudatusi, kuigi te ei muutnud koodi, siis kas:
- Keegi muutis ressursse AWS konsoolist (DRIFT!)
- State fail on aegunud
- Bug Terraform'is

---

## 8. Täiendavad Ressursid (Valikuline)

Kui teil on aega järgi, lisage:

### S3 Bucket
```hcl
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket" "website" {
  bucket = "${var.project_name}-bucket-${random_string.bucket_suffix.result}"
  
  tags = {
    Name = "${var.project_name}-bucket"
  }
}

resource "aws_s3_bucket_public_access_block" "website" {
  bucket = aws_s3_bucket.website.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

### Elastic IP (Static IP)
```hcl
resource "aws_eip" "web" {
  instance = aws_instance.web.id
  domain   = "vpc"
  
  tags = {
    Name = "${var.project_name}-eip"
  }
  
  depends_on = [aws_internet_gateway.main]
}

# Lisa output
output "elastic_ip" {
  value = aws_eip.web.public_ip
}
```

---

## 9. Cleanup (VÄGA OLULINE!)

AWS ressursid maksavad raha. Kustutage kõik pärast labori lõpetamist:
```bash
terraform destroy
```

Terraform küsib kinnitust. Kirjutage "yes".

Terraform kustutab ressursse vastupidises järjekorras: EC2 → Security Group → Route Table → Subnet → Internet Gateway → VPC.

### Validation
```bash
# Kontrollige AWS konsoolist:
# - EC2 Instances: peaks olema tühi
# - VPC: peaks olema ainult default VPC
# - Security Groups: ainult default
# - S3: peaks olema tühi (kui lõite)

# Või AWS CLI'ga:
aws ec2 describe-instances --filters "Name=tag:Name,Values=terraform-lab-*"
# Peaks olema tühi list
```

OLULINE: Kui unustate `destroy` käivitada, maksate iga päev ~$0.24 (t2.micro) + võrguliikluse eest!

---

## Kokkuvõte

Selles lab'is lõite:
- AWS VPC võrgu isolatsiooniga
- Public subnet'i internetiühendusega
- Security Group firewall'i
- EC2 instance'i nginx veebiserver'iga
- User data automatiseeritud seadistuseks
- Outputs info jagamiseks

**Järgmine samm:** Kodutöö, kus ehitate samasuguse struktuuri, aga hoopis teise rakendusega!

---

## Troubleshooting

### "Access Denied" viga
```bash
# Kontrolli AWS credentials
aws sts get-caller-identity

# Peaks näitama:
# {
#   "UserId": "...",
#   "Account": "...",
#   "Arn": "..."
# }
```

Kui ei tööta, seadistage uuesti:
```bash
aws configure
```

### Veebiserver ei vasta
```bash
# SSH serverisse
ssh -i ~/.ssh/terraform-lab ec2-user@<IP>

# Kontrolli nginx status
sudo systemctl status nginx

# Vaata loge
sudo journalctl -u nginx -n 50

# Käivita käsitsi
sudo systemctl start nginx
```

### Security Group blokeerib
```bash
# Kontrolli, et security group on õigesti seotud
terraform state show aws_instance.web | grep vpc_security_group_ids

# Testi ühendust
curl -v http://<IP>
```

### State lock viga
```bash
# Kui keegi teine (või crash) jättis luku kinni
terraform force-unlock <LOCK_ID>

# LOCK_ID on vea messages
```