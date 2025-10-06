#  Terraform Edasijõudnud Labor: Pilve infrastruktuur (3×45 min)

## Lab'i eesmärk
Täna õpid Terraform'i edasijõudnud funktsioone - workspaces, modules, remote state! Nüüd lood päris pilve infrastruktuuri! 

##  Õpiväljundid
Pärast seda lab'i oskad:
- Seadistada AWS/Azure provider'id Terraform'iga
- Luua pilve ressursse (EC2, S3, VPC)
- Kasutada Terraform workspaces'eid (dev/prod)
- Hallata remote state'i (S3, Azure Blob)
- Luua ja kasutada Terraform modules

---

### Blokk 1 (45 min) – AWS/Azure provider ja esimene resource
- **Tegevused:**
  - AWS/Azure credentials seadistamine
  - Provider konfiguratsioon `main.tf` failis
  - Esimene pilve ressurss (S3 bucket või Storage Account)
  - `terraform apply` pilvesse
  - Ressursside vaatamine AWS/Azure console's
- **Kontrollnimekiri:**
  - [ ] AWS/Azure credentials töötavad
  - [ ] Provider on seadistatud
  - [ ] Esimene ressurss on loodud pilvesse
  - [ ] Näed ressurssi cloud console's
- **Kontrollküsimus:** "Mis vahe on local provider ja AWS/Azure provider vahel?"
- **Refleksioon (1 min):** "Esimene pilve ressurss loomise tunne: A) hirmutav  B) põnev  C) võimas "

---

### Blokk 2 (45 min) – Workspaces ja environments
- **Tegevused:**
  - Workspaces loomine (`terraform workspace new dev/prod`)
  - Variables erinevate workspace'ide jaoks
  - Conditional logic (`terraform.workspace == "prod"`)
  - Dev ja Prod ressursside loomine
  - Workspaces vahetamine
- **Kontrollnimekiri:**
  - [ ] Dev ja Prod workspaces on loodud
  - [ ] Ressursid on erinevad erinevates workspace'ides
  - [ ] Saad workspace'ide vahel liikuda
- **Kontrollküsimus:** "Miks kasutada workspaces, mitte lihtsalt kaks erinevat kausta?"
- **Refleksioon (1 min):** "Workspaces on nagu... A) Git branch'id  B) eraldi universumid  C) kaupluse erinevad korused "

---

### Blokk 3 (45 min) – Remote state ja modules
- **Tegevused:**
  - Remote state backend seadistamine (S3 + DynamoDB või Azure Blob)
  - State locking testimine
  - Esimese module loomine (`modules/vpc/`)
  - Module kasutamine `main.tf` failis
  - Module'i parameetrite passimine
- **Kontrollnimekiri:**
  - [ ] Remote state töötab (state on S3/Azure Blob'is)
  - [ ] State locking toimib
  - [ ] Module on loodud ja toimib
  - [ ] Mõistad, miks remote state on oluline
- **Kontrollküsimus:** "Mis juhtub kui kaks inimest jooksutavad `terraform apply` samaaegselt ilma lockinguta?"
- **Refleksioon (1 min):** "Kõige keeruline osa täna oli... A) workspaces B) remote state C) modules D) actually, ma sain hakkama! "

---

**Valmis? Alustame detailsete sammudega!** ⬇

---

##  Ettevalmistus

### Vajalikud tööriistad:
- Terraform installitud
- AWS CLI või Azure CLI seadistatud
- Pilve konto (AWS Free Tier või Azure Free Account)

### Seadistamine:
```bash
# AWS
aws configure

# Azure
az login
```

---

##  Samm 1: AWS Provider Seadistamine

### 1.1 Terraform konfiguratsioon

Loo `main.tf` fail:

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
  region = "us-east-1"
}

# VPC loomine
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "terraform-lab-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "terraform-lab-igw"
  }
}
```

### 1.2 Käivita Terraform

```bash
terraform init
terraform plan
terraform apply
```

---

##  Samm 2: EC2 Instance Loomine

### 2.1 Subnet ja Security Group

```hcl
# Public Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "terraform-lab-public-subnet"
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
    Name = "terraform-lab-public-rt"
  }
}

# Security Group
resource "aws_security_group" "web" {
  name_prefix = "terraform-lab-web-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "terraform-lab-web-sg"
  }
}
```

### 2.2 EC2 Instance

```hcl
# Key Pair
resource "aws_key_pair" "deployer" {
  key_name   = "terraform-lab-key"
  public_key = file("~/.ssh/id_rsa.pub")
}

# EC2 Instance
resource "aws_instance" "web" {
  ami                    = "ami-0c02fb55956c7d316" # Amazon Linux 2
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.web.id]
  subnet_id              = aws_subnet.public.id

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "<h1>Hello from Terraform!</h1>" > /var/www/html/index.html
              EOF

  tags = {
    Name = "terraform-lab-web-server"
  }
}
```

---

##  Samm 3: S3 Bucket ja Outputs

### 3.1 S3 Bucket

```hcl
# S3 Bucket
resource "aws_s3_bucket" "terraform_lab" {
  bucket = "terraform-lab-bucket-${random_string.bucket_suffix.result}"

  tags = {
    Name        = "Terraform Lab Bucket"
    Environment = "Lab"
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "terraform_lab" {
  bucket = aws_s3_bucket.terraform_lab.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

### 3.2 Outputs

```hcl
# Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.web.public_ip
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.terraform_lab.bucket
}

output "website_url" {
  description = "URL of the website"
  value       = "http://${aws_instance.web.public_ip}"
}
```

---

##  Samm 4: Workspaces Kasutamine

### 4.1 Loo erinevad keskkonnad

```bash
# Loo development workspace
terraform workspace new development

# Loo production workspace
terraform workspace new production

# Vaata praegust workspace'i
terraform workspace show

# Vaheta workspace'i
terraform workspace select development
```

### 4.2 Keskkonna-spetsiifilised muutujad

Loo `terraform.tfvars` fail:

```hcl
# Development keskkond
environment = "development"
instance_type = "t2.micro"
```

Loo `production.tfvars` fail:

```hcl
# Production keskkond
environment = "production"
instance_type = "t2.small"
```

---

##  Samm 5: Käivita ja Testi

### 5.1 Deploy

```bash
# Development keskkond
terraform workspace select development
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"

# Production keskkond
terraform workspace select production
terraform plan -var-file="production.tfvars"
terraform apply -var-file="production.tfvars"
```

### 5.2 Testi

```bash
# Vaata outputs
terraform output

# Testi veebilehte
curl $(terraform output -raw website_url)

# Vaata S3 bucket'it
aws s3 ls s3://$(terraform output -raw s3_bucket_name)
```

---

##  Puhastamine

```bash
# Kustuta kõik ressursid
terraform destroy

# Kustuta workspace'id
terraform workspace select default
terraform workspace delete development
terraform workspace delete production
```

---

##  Kokkuvõte

Pärast seda laborit oskate:
- Seadistada AWS provider'it Terraform'iga
- Luua VPC, subnetti, security group'e
- Käivitada EC2 instance'i user data'ga
- Luua S3 bucket'it versioneerimisega
- Kasutada Terraform workspaces'eid
- Hallata erinevaid keskkondi
- Kasutada outputs'e ja muutujaid

**Järgmine samm:** Terraform Advanced kodutöö! 
