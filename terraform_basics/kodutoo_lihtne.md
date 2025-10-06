#  Terraform Kodutöö: Lihtne Infrastruktuur (Alternatiiv)

**Tähtaeg:** Järgmise nädala alguseks  

**Raskusaste:** Lihtne

---

##  Ülesande kirjeldus

Lihtsam alternatiiv Terraform kodutööle. Fookus on Terraform'i ja Infrastructure as Code'i õppimisel kohalikus keskkonnas lihtsama ülesandega!

---

##  **Projekt: Kohalik Infrastruktuur Terraform'iga**

### Mis on see projekt?

Looge kohalik infrastruktuur Terraform'i abil. See on nagu "digitaalse maja ehitamine" kohalikus arvutis - kirjutate üles, mida soovite, ja Terraform teeb selle teie eest.

### Mida te ehitate?

** Kohalik Infrastruktuur**
- **Failid ja kaustad** - projektifailide struktuur
- **Konfiguratsioonid** - JSON ja YAML failid
- **Skriptid** - automatiseerimise skriptid

### Miks see on kasulik?

- **Õpite Terraform'i** - praktiline kogemus
- **Lihtne alustada** - töötab kohalikus arvutis
- **Reaalne projekt** - failide ja konfiguratsiooni haldamine
- **Taaskasutatav** - sama kood töötab erinevates arvutites

---

##  **Ülesanne 1: Projekti struktuuri loomine (20 min)**

### Samm 1: Põhifailid

**Looge järgmine failide struktuur:**

```bash
terraform-basics-homework/
├── main.tf          # Põhiline Terraform fail
├── variables.tf     # Muutujad
├── outputs.tf       # Väljundid
├── terraform.tfvars # Muutujate väärtused
└── README.md        # Projekti kirjeldus
```

### Samm 2: main.tf fail

```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

# Loo projekti põhikaust
resource "local_directory" "project_root" {
  path = "${path.module}/${var.project_name}"
}

# Loo alamkaustad
resource "local_directory" "config" {
  path = "${local_directory.project_root.path}/config"
}

resource "local_directory" "scripts" {
  path = "${local_directory.project_root.path}/scripts"
}

resource "local_directory" "docs" {
  path = "${local_directory.project_root.path}/docs"
}

# Projekti konfiguratsioon
resource "local_file" "project_config" {
  content = jsonencode({
    project_name = var.project_name
    environment  = var.environment
    version      = "1.0.0"
    created_at   = timestamp()
    author       = "Terraform Student"
    features = [
      "local_file_management",
      "configuration_generation",
      "script_automation"
    ]
  })
  filename = "${local_directory.config.path}/project.json"
}

# YAML konfiguratsioon
resource "local_file" "app_config" {
  content = yamlencode({
    app = {
      name        = var.project_name
      environment = var.environment
      port        = 8080
      debug       = var.environment == "development" ? true : false
    }
    database = {
      type = "sqlite"
      file = "app.db"
    }
    logging = {
      level = var.environment == "production" ? "warn" : "debug"
      file  = "app.log"
    }
  })
  filename = "${local_directory.config.path}/app.yaml"
}

# Käivitamise skript
resource "local_file" "startup_script" {
  content = <<-EOF
    #!/bin/bash
    echo "======================================"
    echo "Tere tulemast ${var.project_name} projekti!"
    echo "======================================"
    echo "Keskkond: ${var.environment}"
    echo "Versioon: 1.0.0"
    echo "Kuupäev: $(date)"
    echo "Kaust: $(pwd)"
    echo ""
    echo "Saadaolevad konfiguratsioonid:"
    ls -la config/
    echo ""
    echo "Saadaolevad skriptid:"
    ls -la scripts/
    echo "======================================"
  EOF
  filename        = "${local_directory.scripts.path}/startup.sh"
  file_permission = "0755"
}

# Puhastamise skript
resource "local_file" "cleanup_script" {
  content = <<-EOF
    #!/bin/bash
    echo "Puhastan ${var.project_name} projekti..."
    echo "Kustutan ajutised failid..."
    rm -f *.tmp *.log
    echo "Puhastamine lõpetatud!"
  EOF
  filename        = "${local_directory.scripts.path}/cleanup.sh"
  file_permission = "0755"
}

# Juhuslik ID failide jaoks
resource "random_id" "file_suffix" {
  byte_length = 4
}

# Loo mitu näidisfaili
resource "local_file" "example_files" {
  count = var.file_count
  
  content = <<-EOF
    # Näidisfail ${count.index + 1}
    
    Projekti nimi: ${var.project_name}
    Keskkond: ${var.environment}
    Faili number: ${count.index + 1}
    Loodud: ${timestamp()}
    Unikaalne ID: ${random_id.file_suffix.hex}
    
    See on näidisfail, mis demonstreerib Terraform'i võimalusi.
    Saate seda faili kasutada oma projektides.
  EOF
  
  filename = "${local_directory.docs.path}/example_${count.index + 1}_${random_id.file_suffix.hex}.txt"
}

# README fail
resource "local_file" "readme" {
  content = <<-EOF
    # ${var.project_name}
    
    ## Kirjeldus
    
    See projekt on loodud Terraform'i abil demonstreerima Infrastructure as Code põhimõtteid.
    
    ## Struktuuri
    
    ```
    ${var.project_name}/
    ├── config/          # Konfiguratsioonifailid
    ├── scripts/         # Skriptid
    ├── docs/           # Dokumentatsioon ja näited
    └── README.md       # See fail
    ```
    
    ## Kasutamine
    
    1. Käivita projekt: `./scripts/startup.sh`
    2. Vaata konfiguratsioone: `cat config/project.json`
    3. Puhasta projekt: `./scripts/cleanup.sh`
    
    ## Keskkond
    
    - Keskkond: ${var.environment}
    - Versioon: 1.0.0
    - Loodud: ${timestamp()}
    
    ## Terraform info
    
    See projekt loodi kasutades:
    - Local provider
    - Random provider
    - File resources
    - Directory resources
  EOF
  filename = "${local_directory.project_root.path}/README.md"
}
```

### Samm 3: variables.tf fail

```hcl
variable "project_name" {
  description = "Projekti nimi"
  type        = string
  default     = "terraform-basics-homework"
  
  validation {
    condition     = length(var.project_name) > 3
    error_message = "Projekti nimi peab olema vähemalt 4 tähemärki pikk."
  }
}

variable "environment" {
  description = "Keskkonna nimi"
  type        = string
  default     = "development"
  
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Keskkond peab olema: development, staging või production."
  }
}

variable "file_count" {
  description = "Loodavate näidisfailide arv"
  type        = number
  default     = 5
  
  validation {
    condition     = var.file_count > 0 && var.file_count <= 20
    error_message = "Failide arv peab olema vahemikus 1-20."
  }
}
```

### Samm 4: outputs.tf fail

```hcl
output "project_directory" {
  description = "Projekti kausta tee"
  value       = local_directory.project_root.path
}

output "project_structure" {
  description = "Projekti struktuur"
  value = {
    root_dir    = local_directory.project_root.path
    config_dir  = local_directory.config.path
    scripts_dir = local_directory.scripts.path
    docs_dir    = local_directory.docs.path
  }
}

output "created_files" {
  description = "Kõik loodud failid"
  value = {
    config_files = [
      local_file.project_config.filename,
      local_file.app_config.filename
    ]
    script_files = [
      local_file.startup_script.filename,
      local_file.cleanup_script.filename
    ]
    doc_files = local_file.example_files[*].filename
    readme_file = local_file.readme.filename
  }
}

output "project_summary" {
  description = "Projekti kokkuvõte"
  value = <<-EOF
    ═══════════════════════════════════════
    Terraform Projekt: ${var.project_name}
    ═══════════════════════════════════════
    Keskkond: ${var.environment}
    Failide arv: ${length(local_file.example_files) + 4}
    Loodud: ${timestamp()}
    Kaust: ${local_directory.project_root.path}
    ═══════════════════════════════════════
  EOF
}

output "next_steps" {
  description = "Järgmised sammud"
  value = [
    "1. Käivitage: cd ${local_directory.project_root.path}",
    "2. Vaadake struktuuri: tree . (või ls -la)",
    "3. Käivitage startup skript: ./scripts/startup.sh",
    "4. Vaadake konfiguratsioonifaile: cat config/*.json",
    "5. Muutke terraform.tfvars ja rakendage uuesti"
  ]
}
```

### Samm 5: terraform.tfvars fail

```hcl
project_name = "minu-terraform-projekt"
environment  = "development"
file_count   = 3
```

---

##  **Ülesanne 2: Projekti käivitamine (15 min)**

### Samm 1: Terraform'i initsialiseerimine

```bash
# Navigate to project directory
cd terraform-basics-homework

# Initialize Terraform
terraform init
```

### Samm 2: Planeerimine

```bash
# See what will be created
terraform plan
```

### Samm 3: Projekti loomine

```bash
# Create the infrastructure
terraform apply
```

### Samm 4: Tulemuste vaatamine

```bash
# Check outputs
terraform output

# Check created files
ls -la minu-terraform-projekt/
tree minu-terraform-projekt/  # kui tree on installitud
```

---

##  **Ülesanne 3: Eksperimenteerimine (30 min)**

### Samm 1: Muutujate muutmine

**Muutke `terraform.tfvars` faili:**

```hcl
project_name = "minu-uus-projekt"
environment  = "production"
file_count   = 10
```

**Rakendage muudatused:**

```bash
terraform plan
terraform apply
```

### Samm 2: Uue ressursi lisamine

**Lisage `main.tf` faili:**

```hcl
# Loo konfiguratsioonifail iga keskkonna jaoks
resource "local_file" "env_config" {
  content = jsonencode({
    environment = var.environment
    settings = {
      debug_mode    = var.environment != "production"
      log_level     = var.environment == "production" ? "error" : "debug"
      feature_flags = {
        new_ui      = var.environment == "development"
        analytics   = var.environment != "development"
        monitoring  = var.environment == "production"
      }
    }
  })
  filename = "${local_directory.config.path}/environment.json"
}
```

### Samm 3: Output'ide uuendamine

**Lisage `outputs.tf` faili:**

```hcl
output "environment_config" {
  description = "Keskkonna konfiguratsioon"
  value       = local_file.env_config.filename
}
```

### Samm 4: Testimine

```bash
terraform apply
./minu-uus-projekt/scripts/startup.sh
cat minu-uus-projekt/config/environment.json
```

---

##  **Ülesanne 4: Puhastamine ja dokumenteerimine (10 min)**

### Samm 1: Infrastruktuuri kustutamine

```bash
terraform destroy
```

### Samm 2: Kokkuvõtte kirjutamine

**Vastake küsimustele:**

1. **Mis oli kõige lihtsam Terraform'i juures?**
2. **Mis oli kõige keerulisem?**
3. **Kuidas saaks seda projekti parandada?**
4. **Mida õppisite Infrastructure as Code kohta?**

---

##  **Boonusülesanded (valikuline)**

### 1. Tingimused ja tsüklid

```hcl
# Loo backup failid ainult production keskkonnas
resource "local_file" "backup_script" {
  count = var.environment == "production" ? 1 : 0
  
  content = "#!/bin/bash\necho 'Backup started...\n'"
  filename = "${local_directory.scripts.path}/backup.sh"
  file_permission = "0755"
}

# Loo erinevad konfiguratsioonie failure iga faili jaoks
resource "local_file" "app_configs" {
  for_each = toset(["api", "web", "worker"])
  
  content = jsonencode({
    service = each.key
    port    = each.key == "api" ? 3000 : each.key == "web" ? 8080 : 9000
    env     = var.environment
  })
  filename = "${local_directory.config.path}/${each.key}.json"
}
```

### 2. Locals ja funktsioonid

```hcl
locals {
  project_prefix = "${var.project_name}-${var.environment}"
  timestamp_formatted = formatdate("YYYY-MM-DD-hhmm", timestamp())
  
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    CreatedAt   = local.timestamp_formatted
  }
}

resource "local_file" "metadata" {
  content = jsonencode(local.common_tags)
  filename = "${local_directory.config.path}/metadata.json"
}
```

### 3. Moodulite struktuuri ettevalmistamine

```bash
mkdir -p modules/file-generator
# Liigutage osa koodist moodulitesse
```

---

##  **Kokkuvõte**

Täna õppisite:
- **Terraform'i põhitõdesid** - kuidas kirjutada HCL koodi
- **Local provider'i** - kuidas hallata kohalikke faile
- **Variables ja outputs** - kuidas teha koodi paindlikuks
- **Infrastructure as Code** - kuidas kood saab infrastruktuuri kirjeldada

**Järgmised sammud:**
- Õppige rohkem provider'ite kohta
- Proovige kohalikke provider'eid (local, null, random)
- Uurige Terraform module'eid
- Rakendage real-world projektides

**Küsimused?** 

---

##  **Failide näited**

### Oodatav terraform output:

```
project_directory = "./minu-terraform-projekt"
project_structure = {
  "config_dir" = "./minu-terraform-projekt/config"
  "docs_dir" = "./minu-terraform-projekt/docs"
  "root_dir" = "./minu-terraform-projekt"
  "scripts_dir" = "./minu-terraform-projekt/scripts"
}
project_summary = <<EOT
═══════════════════════════════════════
Terraform Projekt: minu-terraform-projekt
═══════════════════════════════════════
Keskkond: development
Failide arv: 7
Loodud: 2024-01-15T10:30:45Z
Kaust: ./minu-terraform-projekt
═══════════════════════════════════════
EOT
```

### Oodatav failide struktuur:

```
minu-terraform-projekt/
├── README.md
├── config/
│   ├── project.json
│   └── app.yaml
├── scripts/
│   ├── startup.sh
│   └── cleanup.sh
└── docs/
    ├── example_1_abc123.txt
    ├── example_2_abc123.txt
    └── example_3_abc123.txt
```
