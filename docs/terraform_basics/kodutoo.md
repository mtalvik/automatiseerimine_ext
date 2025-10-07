# Terraform Kodutöö: Kohalik Infrastruktuur

See kodutöö võtab umbes 3-4 tundi, sõltuvalt teie Terraform kogemusest. Keskendu me kohaliku infrastruktuuri loomisele, mis on ideaalne IaC põhimõtete õppimiseks ilma pilve kuludeta.

**Eeldused:** Terraform basics labor läbitud, HCL süntaksi põhiteadmised

**Esitamine:** GitHub repositoorium koos README.md failiga

**Tähtaeg:** Järgmise nädala alguseks

---

## 1. Ülesande Kirjeldus

Looge Terraform'iga projekt, mis genereerib automaatselt projekti failide struktuuri koos konfiguratsioonidega. See ülesanne simuleerib reaalset vajadust - iga kord kui alustate uut projekti, vajate standardset kaustade struktuuri, konfiguratsioonifaile ja skripte.

Teie Terraform kood peaks looma:
- Projekti kaustade struktuuri (config, scripts, docs)
- Konfiguratsioonifaile JSON ja YAML vormingus
- Skripte projekti haldamiseks
- README faili projekti dokumentatsiooniga

Kõik failid peavad kasutama variables, et koodi saaks korduvkasutada erinevate projektide jaoks. Sama Terraform kood peaks töötama nii development, staging kui production keskkondades, muutes ainult muutujate väärtusi.

---

## 2. Projekti Failide Struktuuri Loomine

Alustage projekti põhikaustade loomisega. Kasutage `local_directory` ressurssi kolme põhikausta jaoks: config, scripts ja docs.

```hcl
resource "local_directory" "project_root" {
  path = "${path.module}/${var.project_name}"
}

resource "local_directory" "config" {
  path = "${local_directory.project_root.path}/config"
}

resource "local_directory" "scripts" {
  path = "${local_directory.project_root.path}/scripts"
}

resource "local_directory" "docs" {
  path = "${local_directory.project_root.path}/docs"
}
```

Iga kataloog peaks kasutama eelmise kataloogi teed, et tagada õige hierarhia. `path.module` viitab kausta, kus Terraform fail asub, ja `var.project_name` võimaldab dünaamilist nime.

---

## 3. Konfiguratsioonifailide Genereerimine

Looge JSON konfiguratsioonifail, mis sisaldab projekti metaandmeid. See fail peaks kajastama praegust keskkonda, versiooni ja projekti detaile.

```hcl
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
```

Lisaks JSON failile looge ka YAML konfiguratsioonifail rakenduse seadete jaoks. YAML on tihti kasutatav formaadis, mida paljud tööriistad eelistavad.

```hcl
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
```

Pange tähele, kuidas kasutame tingimuslikku loogikat: debug režiim on sisse lülitatud ainult development keskkonnas, ja logimine on produktsioonis range, kuid development's verbose.

---

## 4. Skriptifailide Loomine

Looge kaks skriptifaili: startup.sh projekti käivitamiseks ja cleanup.sh puhastamiseks.

Startup skript peaks kuvama projekti info ja kontrollima keskkonda:

```hcl
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
```

Cleanup skript peaks puhastama ajutised failid:

```hcl
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
```

Pange tähele `file_permission = "0755"` kasutamist, mis muudab skriptid käivitatavaks.

---

## 5. Näidisfailide Genereerimine

Kasutage `count` või `for_each` loomaks mitu näidisfaili docs kausta. Failide arv peaks olema muutuja kaudu konfigureeritav.

```hcl
resource "random_id" "file_suffix" {
  byte_length = 4
}

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
```

Random ID kasutamine tagab, et failinimed on unikaalsed isegi siis, kui sama koodi käivitatakse mitu korda.

---

## 6. Variables ja Outputs

Defineerige kõik vajalikud muutujad `variables.tf` failis:

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

Outputs peaksid näitama olulisi infosid pärast infrastruktuuri loomist:

```hcl
output "project_directory" {
  description = "Projekti kausta tee"
  value       = local_directory.project_root.path
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
```

---

## 7. README Genereerimine

Looge README fail, mis dokumenteerib projekti struktuuri ja kasutamist:

```hcl
resource "local_file" "readme" {
  content = <<-EOF
    # ${var.project_name}
    
    ## Kirjeldus
    
    See projekt on loodud Terraform'i abil demonstreerima Infrastructure as Code põhimõtteid.
    
    ## Struktuur
    
    ```
    ${var.project_name}/
    ├── config/          # Konfiguratsioonifailid
    ├── scripts/         # Skriptid
    ├── docs/            # Dokumentatsioon ja näited
    └── README.md        # See fail
    ```
    
    ## Kasutamine
    
    1. Käivita projekt: `./scripts/startup.sh`
    2. Vaata konfiguratsioone: `cat config/project.json`
    3. Puhasta projekt: `./scripts/cleanup.sh`
    
    ## Keskkond
    
    - Keskkond: ${var.environment}
    - Versioon: 1.0.0
    - Loodud: ${timestamp()}
    
    ## Terraform Info
    
    See projekt loodi kasutades:
    - Local provider
    - Random provider
    - File resources
    - Directory resources
  EOF
  filename = "${local_directory.project_root.path}/README.md"
}
```

---

## 8. Esitamine

### Repositooriumi ettevalmistamine

Looge avalik GitHub repositoorium nimega `terraform-basics-homework`. Repositooriumi peakski sisaldama:

```
terraform-basics-homework/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars.example
├── .gitignore
└── README.md
```

### .gitignore fail

Looge `.gitignore` fail, et vältida tundlike failide üleslaadimist:

```
# Terraform files
.terraform/
.terraform.lock.hcl
terraform.tfstate
terraform.tfstate.backup
*.tfvars
!terraform.tfvars.example

# OS files
.DS_Store
Thumbs.db

# Generated files
terraform-basics-homework/
```

### terraform.tfvars.example

Looge näidisfail, mis näitab, milliseid väärtusi saab seadistada:

```hcl
project_name = "minu-projekt"
environment  = "development"
file_count   = 3
```

### README.md

Teie repositooriumi README.md peab sisaldama:

1. Projekti kirjeldust - mis see on ja mida teeb
2. Kuidas seadistada - `terraform init` ja sõltuvused
3. Kuidas käivitada - `terraform plan`, `terraform apply`
4. Näidisväärtused - mis muutujaid saab seada
5. Refleksioon - vastused viiele küsimusele

---

## Refleksioon

Lisa oma README.md faili lõppu peatükk "## Refleksioon" ja vasta järgmistele küsimustele kahest kolme lausega igaühele:

### 1. Mis oli selle kodutöö juures kõige raskem ja kuidas sa selle lahendasid?

Kirjelda konkreetset tehnilist väljakutset, mida kogesid. Võib olla state haldamine, HCL süntaks, või resources vahel sõltuvuste seadmine. Selgita, milliseid ressursse kasutasid (dokumentatsioon, Stack Overflow, klassikaaslased) ja kuidas probleemi lahendasid.

### 2. Milline Terraform kontseptsioon oli sulle kõige suurem "ahaa!" elamus ja miks?

Mõtle hetkele, kui midagi lõpuks klikkis. Võib olla state faili roll, providers süsteem, või kuidas variables ja outputs töötavad koos. Kirjelda, miks see kontseptsioon oli oluline ja kuidas see muutis su arusaamist IaC-st.

### 3. Kuidas saaksid Terraform'i kasutada oma teistes projektides või töös?

Ole konkreetne. Ära kirjuta lihtsalt "automatiseerimine on hea". Kirjelda reaalset kasutusjuhtu: kas see on projekti struktuuri loomine, development keskkondade seadistamine, või millegi muu. Kuidas Terraform lahendaks konkreetse probleemi, mis sul on?

### 4. Kui peaksid oma sõbrale selgitama, mis on Infrastructure as Code ja miks see on kasulik, siis mida ütleksid?

Kasuta lihtsat keelt ilma žargoonita. Võrdle IaC-d millegagi tuttavaga (näiteks retsept vs iga kord uuesti leiutamine). Selgita kolme peamist eelist, mida IaC annab traditsioonilise lähenemise ees.

### 5. Mis oli selle projekti juures kõige lõbusam või huvitavam osa?

See võib olla tehnilne avastus, mõni ootamatu tulemus, või lihtsalt rahuldus kui `terraform apply` töötas. Ära ole liiga formaalne - ausus ja isiklik perspektiiv on väärtuslikud.

---

## Kontrollnimekiri Enne Esitamist

Kontrolli need asjad enne kui esitad:

- [ ] GitHub repositoorium on avalik
- [ ] Kõik Terraform failid (`main.tf`, `variables.tf`, `outputs.tf`) on commititud
- [ ] `terraform init` töötab ilma vigadeta
- [ ] `terraform plan` näitab oodatud ressursse
- [ ] `terraform apply` loob kõik failid ja kaustad
- [ ] `terraform destroy` kustutab kõik ressursid
- [ ] `.gitignore` fail on lisatud ja töötab
- [ ] `terraform.tfvars.example` fail on olemas
- [ ] README.md sisaldab:
  - [ ] Projekti kirjeldust
  - [ ] Seadistamise juhiseid
  - [ ] Kasutamise juhiseid
  - [ ] Refleksiooni (5 küsimust, 2-3 lauset iga)
- [ ] Kõik muudatused on push'itud GitHub'i

---

## Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **Terraform failid** | 25% | `main.tf`, `variables.tf`, `outputs.tf` on korrektsed ja töötavad |
| **Variables kasutamine** | 20% | Variables on õigesti defineeritud, validation töötab, ei ole hardcoded väärtuseid |
| **Outputs** | 15% | Outputs kuvavad õigeid väärtuseid, on hästi struktureeritud |
| **Ressursside loomine** | 20% | Kõik nõutud failid ja kaustad luuakse õigesti, skriptid töötavad |
| **README kvaliteet** | 10% | Projekti kirjeldus on selge, juhised on täielikud, dokumentatsioon on professionaalne |
| **Refleksioon** | 10% | 5 küsimust on vastatud sisukalt, näitab mõistmist, on isiklik ja aus |

**Kokku:** 100%

### Hindamine

90-100%: Suurepärane. Kõik töötab flawlessly, kood on puhas, dokumentatsioon on põhjalik, refleksioon näitab sügavat mõistmist.

75-89%: Väga hea. Peaaegu kõik töötab, mõned väikesed vead või puudulikud osad, hea refleksioon.

60-74%: Hea. Põhifunktsionaalsus töötab, aga on puudusi või vigu, refleksioon on pinnapealne.

50-59%: Rahuldav. Osalised tulemused, mitmed vead, minimaalne refleksioon.

Alla 50%: Mitterahuldav. Ei tööta või on ebatäielikud, puuduv dokumentatsioon.

---

## Abimaterjalid

**Terraform dokumentatsioon:**
- [Get Started](https://developer.hashicorp.com/terraform/tutorials/aws-get-started)
- [Configuration Language](https://developer.hashicorp.com/terraform/language)
- [Local Provider](https://registry.terraform.io/providers/hashicorp/local/latest/docs)
- [Random Provider](https://registry.terraform.io/providers/hashicorp/random/latest/docs)

**Kui abi vaja:**
1. Vaata loengumaterjalide ja laborikoodide
2. Kasuta `terraform console` interaktiivseks testimiseks
3. Küsi klassikaaslaselt või õpetajalt
4. Stack Overflow: otsi "terraform [sinu probleem]"

**Testimine:**
```bash
# Kontrolli süntaksit
terraform fmt
terraform validate

# Vaata, mis juhtub
terraform plan

# Rakenda
terraform apply

# Puhasta
terraform destroy
```

---

## Boonus (valikuline, +10%)

Kui tahad ekstra punkte, tee üks või mitu neist:

### 1. Terraform Workspaces

Loo eraldi workspaces development ja production jaoks:

```bash
terraform workspace new development
terraform workspace new production
terraform workspace select development
terraform apply
```

Dokumenteeri README's, kuidas workspaces töötavad.

### 2. Data Sources

Kasuta data source'e olemasolevate failide lugemiseks:

```hcl
data "local_file" "template" {
  filename = "${path.module}/templates/config.tpl"
}

resource "local_file" "generated" {
  content  = data.local_file.template.content
  filename = "${local_directory.config.path}/generated.conf"
}
```

### 3. Conditional Resources

Loo ressursse ainult konkreetses keskkonnas:

```hcl
resource "local_file" "prod_only" {
  count    = var.environment == "production" ? 1 : 0
  content  = "Production only config"
  filename = "${local_directory.config.path}/prod.conf"
}
```

### 4. For_Each Map

Kasuta for_each map'iga:

```hcl
variable "services" {
  type = map(object({
    port = number
    env  = string
  }))
  default = {
    "web" = { port = 8080, env = "production" }
    "api" = { port = 3000, env = "development" }
  }
}

resource "local_file" "service_configs" {
  for_each = var.services
  content  = "Port: ${each.value.port}, Env: ${each.value.env}"
  filename = "${local_directory.config.path}/${each.key}.conf"
}
```

Dokumenteeri README's, mida boonuses tegid ja miks.
