# Terraform Kodutöö: Kohalik Infrastruktuur

Loo kohalik infrastruktuur Terraform'iga. Õpid Infrastructure as Code põhimõtteid praktiliselt - kirjutad koodi mis loob faile, kaustu ja konfiguratsioone automaatselt. Kodutöö võtab umbes 90 minutit.

**Eeldused:** Terraform basics labor tehtud, HCL süntaks tuttav  
**Esitamine:** GitHub link Google Classroom'i  
**Tähtaeg:** Kokkulepitud tähtajaks

---

## 1. Projekti Ülevaade

Loote Terraform'iga projekti struktuuri mis sisaldab:
- Kaustu (config, scripts, docs)
- Konfiguratsioonifaile (JSON, YAML)
- Skripte (startup, cleanup)
- Dokumentatsiooni

Terraform loob kõik automaatselt kui käivitate `terraform apply`. Kui soovite muuta projekti nime või keskkonda, muudate ainult muutujaid ja Terraform uuendab kõike.

---

## 2. Failide Loomine

### 2.1 Projekti Struktuur

Looge kaust ja failid:```bash
mkdir terraform-homework
cd terraform-homework```

Looge 4 faili:
- `main.tf` - ressursside definitsioonid
- `variables.tf` - sisendmuutujad
- `outputs.tf` - väljundid
- `terraform.tfvars` - muutujate väärtused

### 2.2 main.tf

Looge `main.tf` fail järgmise sisuga:```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# Põhikaust
resource "local_directory" "project_root" {
  path = "${path.module}/${var.project_name}"
}

# Alamkaustad
resource "local_directory" "config" {
  path = "${local_directory.project_root.path}/config"
}

resource "local_directory" "scripts" {
  path = "${local_directory.project_root.path}/scripts"
}

resource "local_directory" "docs" {
  path = "${local_directory.project_root.path}/docs"
}

# JSON konfiguratsioon
resource "local_file" "project_config" {
  content = jsonencode({
    project_name = var.project_name
    environment  = var.environment
    version      = "1.0.0"
    created_at   = timestamp()
  })
  filename = "${local_directory.config.path}/project.json"
}

# YAML konfiguratsioon
resource "local_file" "app_config" {
  content = yamlencode({
    app = {
      name = var.project_name
      port = 8080
    }
    database = {
      type = "sqlite"
      file = "app.db"
    }
  })
  filename = "${local_directory.config.path}/app.yaml"
}

# Startup skript
resource "local_file" "startup_script" {
  content = <<-EOF
    #!/bin/bash
    echo "Tere tulemast ${var.project_name} projekti!"
    echo "Keskkond: ${var.environment}"
    ls -la config/
  EOF
  filename        = "${local_directory.scripts.path}/startup.sh"
  file_permission = "0755"
}

# README
resource "local_file" "readme" {
  content = <<-EOF
    # ${var.project_name}
    
    Projekt loodud Terraform'iga.
    
    ## Kasutamine
    
    1. Käivita: ./scripts/startup.sh
    2. Vaata config: cat config/project.json
    
    Keskkond: ${var.environment}
  EOF
  filename = "${local_directory.project_root.path}/README.md"
}```

### 2.3 variables.tf```hcl
variable "project_name" {
  description = "Projekti nimi"
  type        = string
  default     = "terraform-homework"
  
  validation {
    condition     = length(var.project_name) > 3
    error_message = "Nimi peab olema vähemalt 4 tähemärki."
  }
}

variable "environment" {
  description = "Keskkond"
  type        = string
  default     = "development"
  
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Keskkond peab olema: development, staging või production."
  }
}```

### 2.4 outputs.tf```hcl
output "project_path" {
  description = "Projekti tee"
  value       = local_directory.project_root.path
}

output "created_files" {
  description = "Loodud failid"
  value = {
    config  = local_file.project_config.filename
    yaml    = local_file.app_config.filename
    script  = local_file.startup_script.filename
    readme  = local_file.readme.filename
  }
}```

### 2.5 terraform.tfvars```hcl
project_name = "minu-projekt"
environment  = "development"```

---

## 3. Projekti Käivitamine

Nüüd kasutage Terraform'i:```bash
# Initsialiseeri
terraform init

# Planeeri
terraform plan

# Loo infrastruktuur
terraform apply```

Kontrolli tulemust:```bash
# Vaata outpute
terraform output

# Vaata loodud faile
ls -la minu-projekt/
tree minu-projekt/

# Käivita skript
./minu-projekt/scripts/startup.sh

# Vaata JSON faili
cat minu-projekt/config/project.json```

---

## 4. Muudatuste Tegemine

Muuda `terraform.tfvars`:```hcl
project_name = "minu-uus-projekt"
environment  = "production"```

Rakenda:```bash
terraform apply```

Terraform loob uue kausta ja kustutab vana!

---

## 5. Lisaülesanne: Cleanup Skript

Lisa `main.tf` faili veel üks skript:```hcl
resource "local_file" "cleanup_script" {
  content = <<-EOF
    #!/bin/bash
    echo "Puhastan ${var.project_name}..."
    rm -f *.tmp *.log
    echo "Valmis!"
  EOF
  filename        = "${local_directory.scripts.path}/cleanup.sh"
  file_permission = "0755"
}```

Lisa ka `outputs.tf` faili:```hcl
cleanup = local_file.cleanup_script.filename```

Rakenda:```bash
terraform apply
./minu-uus-projekt/scripts/cleanup.sh```

---

## 6. Puhastamine

Kui oled valmis:```bash
terraform destroy```

See kustutab kõik Terraform'i loodud failid ja kaustad.

---

## Esitamine

### Kontroll Enne Esitamist

- [ ] Kõik 4 Terraform faili on loodud
- [ ] `terraform init` töötab
- [ ] `terraform apply` loob struktuuri ilma erroriteta
- [ ] Loodud failide struktuur on õige:
  ```
  minu-projekt/
  ├── README.md
  ├── config/
  │   ├── project.json
  │   └── app.yaml
  └── scripts/
      └── startup.sh
  ```
- [ ] Skript käivitub: `./minu-projekt/scripts/startup.sh`
- [ ] `terraform output` näitab õigeid teid
- [ ] Muutujate muutmine ja uuesti apply töötab
- [ ] Lisaülesanne tehtud (cleanup skript)
- [ ] `terraform destroy` kustutab kõik
- [ ] Kõik failid on commit'itud GitHub'i

### GitHub Repository

Loo uus repository:```bash
git init
git add .
git commit -m "Add Terraform homework"
git branch -M main
git remote add origin https://github.com/[sinu-nimi]/terraform-homework.git
git push -u origin main```

Lisa ka README.md mis selgitab:
- Mis see projekt teeb
- Kuidas käivitada
- Mis faile see loob

### Esitamine Google Classroom'i

Esita oma GitHub repository link Google Classroom'i ülesande alla. Veendu, et repository on avalik (public) või anna õpetajale ligipääs. Link peaks viima otse sinu projekti põhilehele kus on näha README.md ja kõik Terraform failid.

---

## Refleksioon

Vasta küsimustele (2-3 lauset igaüks):

1. **Mis oli kõige lihtsam osa Terraform'i juures?**
   
   [Sinu vastus siia]

2. **Mis oli keerulisem kui arvasid?**
   
   [Sinu vastus siia]

3. **Kuidas Infrastructure as Code erineb käsitsi failide loomisest?**
   
   [Sinu vastus siia]

4. **Kus saaksid seda päris töös kasutada?**
   
   [Sinu vastus siia]

5. **Mida tahaksid järgmisena Terraform'i kohta õppida?**
   
   [Sinu vastus siia]

---

## Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **Põhifunktsioonid** | 60% | |
| - Kõik 4 faili olemas | 15% | main.tf, variables.tf, outputs.tf, terraform.tfvars |
| - Terraform töötab | 15% | init, plan, apply käsud töötavad |
| - Loodud struktuur õige | 15% | Kaustad ja failid õiges kohas |
| - Skriptid käivituvad | 15% | startup.sh töötab |
| **Kood** | 20% | |
| - Variables kasutatud | 10% | Muutujad variables.tf failis |
| - Outputs õigesti | 10% | Näitab failide teid |
| **Dokumentatsioon** | 10% | |
| - README selge | 5% | Selgitab mis ja kuidas |
| - Refleksioon täidetud | 5% | Vastused on mõtestatud |
| **Boonus** | +10% | |
| - Cleanup skript | +5% | Lisaülesanne tehtud |
| - Validation rules | +5% | Variables'itel validation |

**Kokku:** 100% + 10% boonus = max 110%

**Hindeskaalaa:**
- 90-100%: Hinne 5 (suurepärane)
- 75-89%: Hinne 4 (hea)
- 60-74%: Hinne 3 (rahuldav)
- <60%: Hinne 2 (puudulik)

---

## Boonus (+10%)

### 1. Tingimused (+5%)

Lisa `main.tf` faili resource mis loob backup skripti **ainult** production keskkonnas:```hcl
resource "local_file" "backup_script" {
  count = var.environment == "production" ? 1 : 0
  
  content         = "#!/bin/bash\necho 'Backup...'\n"
  filename        = "${local_directory.scripts.path}/backup.sh"
  file_permission = "0755"
}```

### 2. Validation Rules (+5%)

Lisa `variables.tf` faili rohkem validation'eid:```hcl
variable "project_name" {
  # ... olemasolev kood ...
  
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Nimi võib sisaldada ainult väikseid tähti, numbreid ja kriipse."
  }
}```

---

## Abi ja Troubleshooting

### "Error: Invalid provider"```bash
# Lahendus: Initsialiseeri uuesti
terraform init```

### "Error: path already exists"```bash
# Lahendus: Kustuta vana kaust või muuda project_name
rm -rf minu-projekt
terraform apply```

### Skript ei käivitu```bash
# Lahendus: Lisa executable õigus
chmod +x minu-projekt/scripts/startup.sh```

### Terraform destroy ei kustuta kõike```bash
# Terraform ei kustuta faile mis ei ole state'is
# Kustuta käsitsi:
rm -rf minu-projekt```

---

Edu kodutööga! Kui abi vaja, küsi Discordis või järgmises tunnis.