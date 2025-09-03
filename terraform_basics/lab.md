# 🧪 Terraform Basics Lab: Infrastructure Automation

**Kestus:** 2 tundi  
**Eesmärk:** Õppida Terraform'i praktilist kasutamist ja luua lihtsa infrastruktuuri

## 🎯 Samm 1: Õpiväljundid

Pärast laborit oskate:
- **Kirjutada lihtsaid Terraform faile** - HCL süntaks ja põhilised ressursid
- **Kasutada local provider'it** - failide ja kataloogide loomine
- **Mõista Terraform workflow** - init, plan, apply, destroy
- **Debugida probleeme** - logide vaatamine ja veateadete mõistmine
- **Kasutada dokumentatsiooni** - abi leidmine ja näidete kasutamine

---

## 📋 Samm 1: Terraform'i installimine ja seadistamine (15 min)

### 1.1: Terraform'i installimine

**Valige oma operatsioonisüsteem ja järgige juhiseid:**

**macOS:**
```bash
brew install terraform
terraform --version
```

**Linux (Ubuntu/Debian):**
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
terraform --version
```

**Windows:**
```powershell
choco install terraform
terraform --version
```

### 1.2: Projekti struktuuri loomine

```bash
# Projekti kataloogi loomine
mkdir ~/terraform-basics-lab
cd ~/terraform-basics-lab

# Lihtne struktuur
mkdir -p configs scripts
```

### 1.3: Terraform'i seadistamine

**Kontrollige, et Terraform töötab:**
```bash
# Check Terraform version
terraform version

# Check available commands
terraform --help
```

---

## 📋 Samm 2: Lihtsa Terraform projekti loomine (45 min)

### 2.1: Põhilise Terraform faili loomine

**Kasutage valmis näidet teacher_repo'st:**

```bash
# Kopeerige lihtne näide
cp teacher_repo/terraform-basics-starter/examples/simple-local/main.tf main.tf
```

**Või looge oma fail:**

```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# Looge lihtne tekstifail
resource "local_file" "hello" {
  content  = "Tere! See fail on loodud Terraform'i abil."
  filename = "hello.txt"
}

# Looge kataloog
resource "local_directory" "example" {
  path = "example_dir"
}
```

**Mida see teeb?**
- `local_file` - loob faili
- `local_directory` - loob kataloogi
- `content` - faili sisu
- `filename` - faili nimi
- `path` - kataloogi tee

### 2.2: Terraform'i käivitamine

Terraform'i kasutamine koosneb kolmest põhilises sammust: **init**, **plan**, ja **apply**. Kujutage ette neid kui "valmistamine", "kontrollimine" ja "tegemine".

**1. Initialize Terraform (init) - valmistamine:**
```bash
# Initialize the project - valmista ette töökeskkond
terraform init
```

**Mida see teeb?**
- **Allalaadib vajalikud provider'id** - nagu "tõlgi" installimine
- **Seadistab backend'i** - kus state fail salvestatakse (praegu kohalik)
- **Valmistab ette töökeskkonna** - kontrollib, et kõik vajalik on olemas
- **Loob .terraform kausta** - sisaldab allalaaditud faile

**Miks see vajalik?**
- Esimest korda, kui kasutad uut provider'it
- Kui muudad provider'i versiooni
- Kui muudad backend'i konfiguratsiooni

**2. Plan the changes (plan) - kontrollimine:**
```bash
# See what Terraform will do - vaata, mida Terraform teeb
terraform plan
```

**Mida see teeb?**
- **Analüüsib koodi** - kontrollib süntaksit ja loogikat
- **Võrdleb praeguse olekuga** - mis on juba olemas vs mida soovid
- **Näitab muudatusi** - mida luuakse, muudetakse või kustutatakse
- **Ei tee midagi** - ainult näitab, mida teeks

**Miks see oluline?**
- **Turvalisus** - näed, mida tehakse enne tegemist
- **Debugging** - leiad probleemid enne rakendamist
- **Dokumentatsioon** - näed, mis muudatused toimuvad

**3. Apply the changes (apply) - tegemine:**
```bash
# Apply the configuration - rakenda konfiguratsioon
terraform apply
```

**Mida see teeb?**
- **Loob ressursid** - teeb tegelikud muudatused
- **Salvestab state faili** - märgib, mis on loodud
- **Näitab väljundit** - tagastab loodud ressursside infot
- **Küsib kinnitust** - "Do you want to perform these actions?"

**Miks see kriitiline?**
- **Tegelikud muudatused** - see teeb päris asju
- **State management** - jälgib, mis on olemas
- **Idempotent** - sama käsk teeb sama tulemuse
```

### 2.3: Tulemuste kontrollimine

**Kontrollige loodud faile:**
```bash
# List created files
ls -la

# Check the content of hello.txt
cat hello.txt

# Check the JSON config
cat config.json

# Check the directory
ls -la example_dir/
```

**Kontrollige state faili:**
```bash
# Show state
terraform show

# List resources in state
terraform state list
```

---

## 📋 Samm 3: Muudatuste tegemine ja haldamine (30 min)

### 3.1: Konfiguratsiooni muutmine

**Muutke `main.tf` faili:**

```hcl
# Configure Terraform
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# Create a simple text file
resource "local_file" "hello" {
  content  = "Hello, Terraform! This file was created by Terraform. Updated content!"
  filename = "${path.module}/hello.txt"
}

# Create a directory
resource "local_directory" "example" {
  path = "${path.module}/example_dir"
}

# Create a configuration file
resource "local_file" "config" {
  content = jsonencode({
    project_name = "Week 23 Lab"
    environment  = "development"
    created_by   = "Terraform"
    timestamp    = timestamp()
    version      = "2.0"
  })
  filename = "${path.module}/config.json"
}

# Add a new resource - a script file
resource "local_file" "script" {
  content = <<-EOF
    #!/bin/bash
    echo "This is a script created by Terraform"
    echo "Current time: $(date)"
    echo "Projekt: Terraform Alused"
  EOF
  filename = "${path.module}/scripts/startup.sh"
}
```

### Samm 2: Muudatuste rakendamine

```bash
# Plan the changes
terraform plan

# Apply the changes
terraform apply
```

**Mida märkate?**
- Terraform näitab, mis muudetakse
- Ainult muudetud ressursid uuendatakse
- Uus ressurss lisatakse

### Samm 3: Ressursside kustutamine

```bash
# Destroy all resources
terraform destroy
```

**Mida see teeb?**
- Kustutab kõik loodud ressursid
- Säilitab state faili (kui soovite)

---

## 📋 Samm 4: Variables ja Outputs (30 min)

### 4.1: Variables faili loomine

**Looge fail `variables.tf`:**

Variables (muutujad) võimaldavad teha koodi dünaamiliseks ja taaskasutatavaks. Kujutage ette neid kui "seadistusi", mida saab muuta ilma koodi muutmata.

#### Projekti nimi muutuja

```hcl
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "Terraform Alused"
}
```

**Mida see teeb?**
- `description` - kirjeldus, mida muutuja teeb
- `type` - andmetüüp (string, number, bool, list, map)
- `default` - vaikeväärtus, kui midagi pole määratud

#### Keskkond muutuja

```hcl
variable "environment" {
  description = "Keskkond (arendus, test, toodang)"
  type        = string
  default     = "arendus"
  
  validation {
    condition     = contains(["arendus", "test", "toodang"], var.environment)
    error_message = "Keskkond peab olema arendus, test või toodang."
  }
}
```

**Mida see teeb?**
- `validation` - kontrollib, et väärtus oleks korrektne
- `contains()` - funktsioon, mis kontrollib, kas väärtus on nimekirjas
- Lubatud väärtused: "development", "staging", "production"

#### Failide arv muutuja

```hcl
variable "file_count" {
  description = "Loodavate failide arv"
  type        = number
  default     = 3
  
  validation {
    condition     = var.file_count > 0 && var.file_count <= 10
    error_message = "Failide arv peab olema vahemikus 1-10."
  }
}
```

**Mida see teeb?**
- `type = number` - andmetüüp on arv
- `validation` - kontrollib, et arv oleks vahemikus 1-10
- Lubatud väärtused: 1, 2, 3, ..., 10

#### Täiendavad muutujad

Võite lisada rohkem muutujaid vastavalt vajadusele:

```hcl
variable "file_prefix" {
  description = "Failide nimede prefiks"
  type        = string
  default     = "fail"
}

variable "enable_backup" {
  description = "Luba varukoopia failid"
  type        = bool
  default     = false
}
```

### 4.2: Outputs faili loomine

**Looge fail `outputs.tf`:**

Outputs (väljundid) võimaldavad näha loodud ressursside infot ja tagastada väärtusi. Kujutage ette neid kui "vastuseid" - mida Terraform tagastab pärast töö lõpetamist.

```hcl
# ==========================================
# OUTPUTS - väljundid
# ==========================================
# Outputs võimaldavad näha loodud ressursside infot
# See on nagu "vastus" - mida Terraform tagastab pärast töö lõpetamist

# ==========================================
# PROJECT INFO OUTPUT - projekti info
# ==========================================
# Tagastab projekti kohta üldist infot
output "project_info" {
  description = "Projekti kohta info"  # Kirjeldus
  
  # value määrab, mida tagastada
  value = {
    name        = var.project_name    # Projekti nimi
    environment = var.environment     # Keskkond
    file_count  = var.file_count      # Failide arv
    created_at  = timestamp()         # Loomise aeg
  }
  
  # Kasutamine: terraform output project_info
  # Tulemus: JSON objekt projekti infoga
}

# ==========================================
# FILES CREATED OUTPUT - loodud failid
# ==========================================
# Tagastab kõikide loodud failide nimed
output "files_created" {
  description = "Loodud failide nimekiri"  # Kirjeldus
  
  # [*] tähendab "kõik" - võta kõik local_file.example ressursid
  # .filename tähendab "võta filename atribuut"
  value = local_file.example[*].filename
  
  # Kasutamine: terraform output files_created
  # Tulemus: nimekiri failide nimedest
}

# ==========================================
# ADDITIONAL OUTPUTS - täiendavad väljundid
# ==========================================
# Võite lisada rohkem väljundeid vastavalt vajadusele

# Tagasta kataloogi tee
output "directory_path" {
  description = "Loodud kataloogi tee"
  value       = local_directory.example.path
}

# Tagasta konfiguratsioonifaili tee
output "config_file_path" {
  description = "Konfiguratsioonifaili tee"
  value       = local_file.config.filename
}

# Tagasta projekti kokkuvõte
output "project_summary" {
  description = "Projekti kokkuvõte"
  value = "Projekt '${var.project_name}' ${var.environment} keskkonnas ${var.file_count} failiga loodud ${timestamp()}"
}
```

### 4.3: Main faili uuendamine

**Uuendage `main.tf` faili:**

```hcl
# Configure Terraform
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# Loo mitu faili kasutades count
resource "local_file" "example" {
  count    = var.file_count
  content  = "See on fail number ${count.index + 1} projektile ${var.project_name} ${var.environment} keskkonnas."
  filename = "${path.module}/fail_${count.index + 1}.txt"
}

# Loo konfiguratsioonifail
resource "local_file" "config" {
  content = jsonencode({
    projekt_nimi = var.project_name
    keskkond     = var.environment
    failide_arv  = var.file_count
    loodud_poolt = "Terraform"
    ajatempel    = timestamp()
  })
  filename = "${path.module}/konfiguratsioon.json"
}
```

### 4.4: Muudatuste rakendamine

```bash
# Plan the changes
terraform plan

# Apply the changes
terraform apply

# Check outputs
terraform output
```

---

## 📋 Samm 5: Advanced Features (30 min)

### 5.1: Data sources kasutamine

**Lisage `main.tf` faili:**

```hcl
# Loe olemasoleva faili sisu
data "local_file" "existing_config" {
  filename = "${path.module}/konfiguratsioon.json"
}

# Loo kokkuvõttefail kasutades data source
resource "local_file" "summary" {
  content = <<-EOF
    Projekti Kokkuvõte:
    - Projekt: ${var.project_name}
    - Keskkond: ${var.environment}  
    - Loodud failid: ${var.file_count}
    - Konfiguratsioonifail olemas: ${data.local_file.existing_config.content != "" ? "Jah" : "Ei"}
    - Loodud: ${timestamp()}
  EOF
  filename = "${path.module}/kokkuvote.txt"
}
```

### 5.2: Local values kasutamine

**Lisage `locals.tf` faili:**

```hcl
# Define local values
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    CreatedBy   = "Terraform"
    CreatedAt   = timestamp()
  }
  
  file_prefix = "${var.project_name}-${var.environment}"
}
```

### 5.3: Conditional logic

**Uuendage `main.tf` faili:**

```hcl
# Create environment-specific file
resource "local_file" "env_specific" {
  content = var.environment == "production" ? "PRODUCTION ENVIRONMENT - BE CAREFUL!" : "Development environment - safe to test"
  filename = "${path.module}/${local.file_prefix}-env.txt"
  
  tags = local.common_tags
}

# Create backup file only in production
resource "local_file" "backup" {
  count    = var.environment == "production" ? 1 : 0
  content  = "This is a backup file for production environment."
  filename = "${path.module}/backup.txt"
}
```

### 5.4: Final test

```bash
# Plan and apply
terraform plan
terraform apply

# Check all outputs
terraform output

# List all files
ls -la

# Check summary
cat summary.txt
```

---

## 🎯 Samm 2: Kokkuvõte

Täna õppisime:

**Terraform'i installimist ja seadistamist** - töökeskkonna valmistamine
**Põhilise Terraform workflow** - init, plan, apply, destroy
**HCL süntaksit** - ressursid, muutujad, väljundid
**Local provider'i kasutamist** - failide ja kataloogide haldamine
**Advanced features** - data sources, locals, conditional logic  

**Järgmise nädala teemad:**
- Multi-environment Terraform
- Kohalikud provider'id (local, null, random)
- State management best practices

---

## 🚀 **BOONUSÜLESANDED** (Terraform'i oskajatele)

### B1: Advanced Local Infrastructure (30 min)

```hcl
# locals.tf - Advanced local values
locals {
  timestamp = formatdate("YYYY-MM-DD-hhmm", timestamp())
  project_prefix = "${var.project_name}-${var.environment}"
  
  # Complex data structures
  service_configs = {
    web = {
      port = 8080
      replicas = var.environment == "production" ? 3 : 1
      memory = "512M"
    }
    api = {
      port = 3000
      replicas = 2
      memory = "256M"
    }
    worker = {
      port = null
      replicas = 1
      memory = "1G"
    }
  }
  
  # Conditional resources
  monitoring_enabled = var.environment != "development"
  backup_enabled = var.environment == "production"
}

# Service configuration files
resource "local_file" "service_configs" {
  for_each = local.service_configs
  
  content = templatefile("${path.module}/templates/service.tpl", {
    service_name = each.key
    port         = each.value.port
    replicas     = each.value.replicas
    memory       = each.value.memory
    environment  = var.environment
  })
  
  filename = "${local_directory.config.path}/${each.key}-service.yaml"
}
```

### B2: Template Files ja Functions (25 min)

```hcl
# templates/nginx.conf.tpl
upstream ${service_name} {
%{ for i in range(replicas) ~}
    server ${service_name}-${i}:${port};
%{ endfor ~}
}

server {
    listen 80;
    server_name ${domain};
    
    location / {
        proxy_pass http://${service_name};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
%{ if ssl_enabled ~}
    listen 443 ssl;
    ssl_certificate /etc/ssl/certs/${domain}.crt;
    ssl_certificate_key /etc/ssl/private/${domain}.key;
%{ endif ~}
}

# Use template
resource "local_file" "nginx_config" {
  content = templatefile("${path.module}/templates/nginx.conf.tpl", {
    service_name = "webapp"
    replicas     = 3
    port         = 8080
    domain       = "myapp.local"
    ssl_enabled  = var.environment == "production"
  })
  
  filename = "${local_directory.config.path}/nginx.conf"
}
```

### B3: Modules ja Code Organization (35 min)

```hcl
# modules/webapp/main.tf
resource "local_directory" "app_dir" {
  path = "${var.base_path}/${var.app_name}"
}

resource "local_file" "app_config" {
  content = jsonencode({
    app_name    = var.app_name
    environment = var.environment
    database_url = var.database_url
    api_key     = var.api_key
    features    = var.features
  })
  filename = "${local_directory.app_dir.path}/config.json"
}

resource "local_file" "docker_compose" {
  content = templatefile("${path.module}/docker-compose.tpl", {
    app_name     = var.app_name
    image_tag    = var.image_tag
    environment  = var.environment
    replicas     = var.replicas
  })
  filename = "${local_directory.app_dir.path}/docker-compose.yml"
}

# modules/webapp/variables.tf
variable "app_name" {
  description = "Application name"
  type        = string
}

variable "environment" {
  description = "Environment"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "replicas" {
  description = "Number of replicas"
  type        = number
  default     = 1
  validation {
    condition     = var.replicas > 0 && var.replicas <= 10
    error_message = "Replicas must be between 1 and 10."
  }
}

# Use module
module "frontend" {
  source = "./modules/webapp"
  
  app_name    = "frontend"
  environment = var.environment
  replicas    = var.environment == "prod" ? 3 : 1
  base_path   = local_directory.project_root.path
  
  database_url = "postgres://user:pass@db:5432/frontend"
  api_key      = var.frontend_api_key
  features = {
    analytics = var.environment == "prod"
    debug     = var.environment != "prod"
  }
}

module "backend" {
  source = "./modules/webapp"
  
  app_name    = "backend"
  environment = var.environment
  replicas    = 2
  base_path   = local_directory.project_root.path
  
  database_url = "postgres://user:pass@db:5432/backend"
  api_key      = var.backend_api_key
  features = {
    worker_mode = true
    cache       = var.environment == "prod"
  }
}
```

### B4: Terraform Workspaces ja State Management (20 min)

```bash
# Create workspaces for different environments
terraform workspace new development
terraform workspace new staging
terraform workspace new production

# Switch between workspaces
terraform workspace select development
terraform plan -var-file="environments/dev.tfvars"
terraform apply

terraform workspace select production
terraform plan -var-file="environments/prod.tfvars"
terraform apply

# List workspaces
terraform workspace list

# Workspace-specific variables
variable "workspace_configs" {
  description = "Workspace-specific configurations"
  type = map(object({
    replicas     = number
    memory_limit = string
    disk_size    = number
  }))
  
  default = {
    development = {
      replicas     = 1
      memory_limit = "256M"
      disk_size    = 10
    }
    staging = {
      replicas     = 2
      memory_limit = "512M"
      disk_size    = 20
    }
    production = {
      replicas     = 5
      memory_limit = "1G"
      disk_size    = 100
    }
  }
}

locals {
  workspace_config = var.workspace_configs[terraform.workspace]
}
```

### B5: Advanced Data Sources ja External Integration (25 min)

```hcl
# External data source
data "external" "git_info" {
  program = ["bash", "-c", <<-EOT
    echo '{"branch":"'$(git branch --show-current)'","commit":"'$(git rev-parse --short HEAD)'","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}'
  EOT
  ]
}

# HTTP data source (for external APIs)
data "http" "service_discovery" {
  url = "https://api.internal.com/services"
  request_headers = {
    Accept = "application/json"
    Authorization = "Bearer ${var.api_token}"
  }
}

locals {
  services = jsondecode(data.http.service_discovery.body)
  git_info = data.external.git_info.result
}

# Generate deployment metadata
resource "local_file" "deployment_info" {
  content = jsonencode({
    deployment_id   = random_uuid.deployment.result
    git_branch     = local.git_info.branch
    git_commit     = local.git_info.commit
    deployed_at    = local.git_info.timestamp
    environment    = var.environment
    terraform_version = "v${terraform.version}"
    services       = local.services
  })
  
  filename = "${local_directory.project_root.path}/deployment-info.json"
}

resource "random_uuid" "deployment" {}

# Integration with external systems
resource "local_file" "monitoring_config" {
  content = templatefile("${path.module}/templates/monitoring.yml.tpl", {
    services    = local.services
    environment = var.environment
    alerts = {
      cpu_threshold    = var.environment == "production" ? 80 : 90
      memory_threshold = var.environment == "production" ? 85 : 95
      disk_threshold   = 90
    }
  })
  
  filename = "${local_directory.config.path}/monitoring.yml"
}
```

**Kas teil on küsimusi?** 🤔

---

## 📚 Lisaressursid

- **Terraform CLI Commands:** https://www.terraform.io/docs/cli
- **Local Provider:** https://registry.terraform.io/providers/hashicorp/local/latest/docs
- **HCL Language:** https://www.terraform.io/docs/language
- **Terraform Best Practices:** https://www.terraform.io/docs/cloud/guides/recommended-practices

---

## 🔧 Troubleshooting

### Levinumad probleemid ja lahendused:

**1. Provider not found:**
```bash
# Solution: Run terraform init
terraform init
```

**2. State file issues:**
```bash
# Check state
terraform state list

# Refresh state
terraform refresh
```

**3. Permission issues:**
```bash
# Check file permissions
ls -la

# Fix permissions if needed
chmod 644 *.txt
```

**4. Variable validation errors:**
```bash
# Check variable values
terraform plan -var="environment=development"
```
