# Terraform Alused Labor

**Eeldused:** Terraform installitud, Linux CLI, teksteditor, Git

**Platvorm:** Terraform local provider (ei vaja AWS/Azure accounti)

**Ajakulu:** Umbes 2-3 tundi

**Dokumentatsioon:** [Local Provider](https://registry.terraform.io/providers/hashicorp/local/latest/docs)

---

## Õpiväljundid

Pärast seda laborit õpilane:

- Loob Terraform projekti struktuuri ja seadistab provider'eid
- Kirjutab HCL koodi ressursside loomiseks kasutades resources, variables ja outputs
- Käivitab Terraform workflow'i: init, plan, apply, destroy
- Debugib Terraform vigu kasutades logisid ja valideerimist
- Rakendab state haldamist ja mõistab state'i rolli

---

## Labori Ülesehitus

Selles laboris loome Terraform'iga lokaalseid ressursse (faile ja kaustaid). Kasutame **local provider'it**, mis tähendab et ei vaja AWS/Azure accounti - kõik toimub sinu masinas.

**Mis me teeme:**
1. Seadistame Terraform projekti
2. Loome lihtsaid ressursse
3. Kasutame muutujaid ja output'e
4. Töötame sõltuvuste ja count'iga
5. Testimine ja troubleshooting
6. State haldamine

**Miks local provider?** See on ideaalne õppimiseks - näed kohe tulemusi, ei kulu raha, saad eksperimenteerida.

---

## 1. Terraform Projekti Setup

### 1.1 Töökeskkonna Ettevalmistus

Loome puhta töökeskkonna.

```bash
# Loo töökataloog
mkdir -p ~/terraform-lab
cd ~/terraform-lab

# Kontrolli, et Terraform on installitud
terraform version
```

**Oodatav output:**

```
Terraform v1.6.0
on linux_amd64
```

Kui `terraform: command not found`, siis [installi Terraform](https://developer.hashicorp.com/terraform/downloads).

### 1.2 Esimese Faili Loomine

Loome `main.tf` faili.

```bash
nano main.tf
```

Lisa järgmine sisu:

```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "Tere, see on minu esimene Terraform fail!"
}
```

**Selgitus:**

- `terraform {}` block - seadistused
- `required_version` - minimaalne Terraform versioon
- `required_providers` - provider'id mida kasutame
- `local` provider - lokaalsete failide haldamine
- `resource "local_file"` - loome faili
- `${path.module}` - praegune kaust (turvaline)

Salvesta: `Ctrl+O`, `Enter`, `Ctrl+X`

### 1.3 Terraform Init

Initsialiseerime projekti.

```bash
terraform init
```

**Oodatav output:**

```
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/local versions matching "~> 2.4"...
- Installing hashicorp/local v2.4.0...
- Installed hashicorp/local v2.4.0 (signed by HashiCorp)

Terraform has been successfully initialized!
```

**Mis toimus:**
- Terraform laadiis alla local provider'i
- Loodi `.terraform/` kaust
- Loodi `terraform.lock.hcl` fail (dependency lock)

**Kontrolli:**

```bash
ls -la
```

Peaks näitama:

```
drwxr-xr-x  3 user user 4096 ... .terraform/
-rw-r--r--  1 user user  xxx ... .terraform.lock.hcl
-rw-r--r--  1 user user  xxx ... main.tf
```

### Validation Checkpoint

- [ ] `terraform version` töötab
- [ ] `main.tf` fail on loodud
- [ ] `terraform init` õnnestus
- [ ] `.terraform/` kaust eksisteerib

---

## 2. Esimese Ressursi Loomine

### 2.1 Terraform Plan

Vaatame, mis Terraform kavatseb teha.

```bash
terraform plan
```

**Oodatav output:**

```
Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # local_file.hello will be created
  + resource "local_file" "hello" {
      + content              = "Tere, see on minu esimene Terraform fail!"
      + content_base64sha256 = (known after apply)
      + content_base64sha512 = (known after apply)
      + content_md5          = (known after apply)
      + content_sha1         = (known after apply)
      + content_sha256       = (known after apply)
      + content_sha512       = (known after apply)
      + directory_permission = "0777"
      + file_permission      = "0777"
      + filename             = "/home/user/terraform-lab/hello.txt"
      + id                   = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

**Selgitus:**
- `+ create` - loob uue ressursi
- `(known after apply)` - väärtus selgub pärast loomist
- `Plan: 1 to add` - lisatakse 1 ressurss

**OLULINE:** `terraform plan` **EI MUUDA MIDAGI**. See ainult näitab, mis juhtub.

### 2.2 Terraform Apply

Nüüd loome päriselt.

```bash
terraform apply
```

Terraform küsib kinnitust:

```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: 
```

Sisesta: `yes`

**Oodatav output:**

```
local_file.hello: Creating...
local_file.hello: Creation complete after 0s [id=9b5e...]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

### 2.3 Tulemuse Kontrollimine

Kontrolli, et fail on loodud:

```bash
ls -la hello.txt
cat hello.txt
```

**Oodatav output:**

```bash
# ls -la
-rw-r--r--  1 user user 45 ... hello.txt

# cat
Tere, see on minu esimene Terraform fail!
```

**Kontrolli state faili:**

```bash
cat terraform.tfstate
```

See on JSON fail, mis sisaldab infot loodud ressursside kohta. Näed seal `local_file.hello` kirjet koos kõikide atribuutidega.

### 2.4 Idempotentsuse Test

Käivita `terraform apply` uuesti:

```bash
terraform apply
```

**Oodatav output:**

```
local_file.hello: Refreshing state... [id=9b5e...]

No changes. Your infrastructure matches the configuration.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

**Õppetund:** Terraform on idempotent - sama käsk mitu korda ei muuda midagi.

### Validation Checkpoint

- [ ] `terraform plan` näitas `Plan: 1 to add`
- [ ] `terraform apply` lõi faili
- [ ] `hello.txt` fail eksisteerib ja on õige sisuga
- [ ] `terraform.tfstate` fail on loodud
- [ ] Teine `terraform apply` ei muutnud midagi

---

## 3. Variables ja Outputs

### 3.1 Variables Lisamine

Muutujad teevad koodi dünaamiliseks.

Loo fail `variables.tf`:

```bash
nano variables.tf
```

Lisa:

```hcl
variable "greeting" {
  description = "Tervituse tekst"
  type        = string
  default     = "Tere, Terraform!"
}

variable "files_count" {
  description = "Mitu faili luua"
  type        = number
  default     = 3
}

variable "file_prefix" {
  description = "Failinimede prefix"
  type        = string
  default     = "test"
}
```

**Selgitus:**
- `variable` block - deklareerib muutuja
- `description` - selgitus (dokumentatsioon)
- `type` - andmetüüp (string, number, bool, list, map, ...)
- `default` - vaikimisi väärtus

Salvesta fail.

### 3.2 Variables Kasutamine

Muuda `main.tf`:

```bash
nano main.tf
```

Asenda `resource "local_file" "hello"` block järgmisega:

```hcl
resource "local_file" "examples" {
  count = var.files_count
  
  filename = "${path.module}/${var.file_prefix}-${count.index + 1}.txt"
  content  = "${var.greeting}\nSee on fail number ${count.index + 1}"
}
```

**Selgitus:**
- `count = var.files_count` - loome 3 faili
- `var.greeting` - kasutame muutujat
- `count.index` - index (0, 1, 2)
- `count.index + 1` - index + 1 (1, 2, 3)

Salvesta fail.

### 3.3 Outputs Lisamine

Loo fail `outputs.tf`:

```bash
nano outputs.tf
```

Lisa:

```hcl
output "file_names" {
  description = "Loodud failide nimed"
  value       = local_file.examples[*].filename
}

output "files_count" {
  description = "Mitu faili loodi"
  value       = length(local_file.examples)
}

output "greeting_used" {
  description = "Kasutatud tervitus"
  value       = var.greeting
}
```

**Selgitus:**
- `output` block - näitab infot pärast apply
- `local_file.examples[*]` - kõik instantsid
- `length()` - loeb arvu

Salvesta fail.

### 3.4 Rakendamine

Kuna kood muutus, kustutame vana ressursi ja loome uued:

```bash
terraform apply
```

**Oodatav output:**

```
local_file.hello: Refreshing state... [id=9b5e...]

Terraform will perform the following actions:

  # local_file.examples[0] will be created
  + resource "local_file" "examples" {
      + content  = "Tere, Terraform!\nSee on fail number 1"
      + filename = "/home/user/terraform-lab/test-1.txt"
      ...
    }

  # local_file.examples[1] will be created
  + resource "local_file" "examples" {
      + content  = "Tere, Terraform!\nSee on fail number 2"
      + filename = "/home/user/terraform-lab/test-2.txt"
      ...
    }

  # local_file.examples[2] will be created
  + resource "local_file" "examples" {
      + content  = "Tere, Terraform!\nSee on fail number 3"
      + filename = "/home/user/terraform-lab/test-3.txt"
      ...
    }

  # local_file.hello will be destroyed
  - resource "local_file" "hello" {
      ...
    }

Plan: 3 to add, 0 to change, 1 to destroy.
```

Sisesta: `yes`

**Pärast apply:**

```
Apply complete! Resources: 3 added, 0 changed, 1 destroyed.

Outputs:

file_names = [
  "/home/user/terraform-lab/test-1.txt",
  "/home/user/terraform-lab/test-2.txt",
  "/home/user/terraform-lab/test-3.txt",
]
files_count = 3
greeting_used = "Tere, Terraform!"
```

### 3.5 Kontrollimine

```bash
ls -la test-*.txt
cat test-1.txt
cat test-2.txt
cat test-3.txt
```

**Oodatav output:**

```
-rw-r--r--  1 user user 42 ... test-1.txt
-rw-r--r--  1 user user 42 ... test-2.txt
-rw-r--r--  1 user user 42 ... test-3.txt
```

Kõik failid sisaldavad:

```
Tere, Terraform!
See on fail number X
```

### 3.6 Muutujate Ülekirjutamine

Käivita apply uue väärtusega:

```bash
terraform apply -var="greeting=Tere maailm!" -var="files_count=5"
```

**Tulemus:** Terraform loob 2 uut faili (kokku 5) ja uuendab olemasolevaid.

### Validation Checkpoint

- [ ] `variables.tf` fail on loodud
- [ ] `outputs.tf` fail on loodud
- [ ] `main.tf` kasutab muutujaid
- [ ] `terraform apply` lõi 3 faili
- [ ] Outputs näitavad õigeid väärtuseid
- [ ] `-var` flag töötab

---

## 4. Sõltuvused ja Struktuur

### 4.1 Kausta Loomine

Ressursid võivad sõltuda üksteisest. Loome kausta ja siis faili selle kausta sisse.

Muuda `main.tf`:

```bash
nano main.tf
```

Lisa pärast provider block'i:

```hcl
resource "local_file" "config_dir" {
  filename = "${path.module}/config/.gitkeep"
  content  = ""
}

resource "local_file" "config_file" {
  filename = "${path.module}/config/app.conf"
  content  = <<-EOF
    # Application Configuration
    port = 8080
    host = localhost
    debug = true
    
    # Generated by Terraform
    # Count: ${var.files_count}
  EOF
  
  depends_on = [local_file.config_dir]
}
```

**Selgitus:**
- `local_file.config_dir` - loob `/config/` kausta (`.gitkeep` trikk)
- `<<-EOF ... EOF` - heredoc süntaks (multi-line string)
- `depends_on` - eksplitsiitne sõltuvus

Salvesta fail.

### 4.2 Rakendamine

```bash
terraform apply
```

**Oodatav output:**

```
Plan: 2 to add, 0 to change, 0 to destroy.
```

Sisesta: `yes`

**Kontrolli:**

```bash
tree config/
cat config/app.conf
```

**Oodatav output:**

```
config/
├── .gitkeep
└── app.conf
```

### 4.3 Data Sources

Data source = loe olemasolevat infot, ära loo uut.

Lisa `main.tf` lõppu:

```hcl
data "local_file" "existing_config" {
  filename = "${path.module}/config/app.conf"
  
  depends_on = [local_file.config_file]
}
```

Lisa `outputs.tf` lõppu:

```hcl
output "config_content" {
  description = "Config faili sisu"
  value       = data.local_file.existing_config.content
}
```

**Selgitus:**
- `data "local_file"` - loeb olemasolevat faili (ei loo!)
- Output näitab faili sisu

Rakenda:

```bash
terraform apply
```

**Tulemus:** Output näitab config faili sisu.

### Validation Checkpoint

- [ ] `config/` kaust on loodud
- [ ] `config/app.conf` fail eksisteerib
- [ ] Data source loeb faili sisu
- [ ] Output näitab config sisu

---

## 5. Keerukamate Struktuuride Loomine

### 5.1 Locals

Locals = arvutatud väärtused, mida saad koodi sees kasutada.

Lisa `main.tf` lõppu:

```hcl
locals {
  timestamp = formatdate("YYYY-MM-DD-hhmm", timestamp())
  
  project_name = "terraform-lab"
  
  full_prefix = "${local.project_name}-${local.timestamp}"
  
  file_metadata = {
    author  = "Terraform"
    version = "1.0"
    date    = local.timestamp
  }
}

resource "local_file" "metadata" {
  filename = "${path.module}/metadata.json"
  content  = jsonencode(local.file_metadata)
}
```

**Selgitus:**
- `locals {}` - deklareerib lokaalseid muutujaid
- `timestamp()` - praegune aeg
- `formatdate()` - formateerib kuupäeva
- `jsonencode()` - teisendab JSON'iks
- `local.xxx` - kasutab local'i

Rakenda:

```bash
terraform apply
```

**Kontrolli:**

```bash
cat metadata.json
```

**Oodatav output:**

```json
{
  "author": "Terraform",
  "date": "2025-10-16-0845",
  "version": "1.0"
}
```

### 5.2 For_each

`for_each` on parem kui `count`, kui vajad key-value struktuure.

Lisa `main.tf` lõppu:

```hcl
variable "environments" {
  description = "Keskkonnad"
  type        = map(string)
  default = {
    dev     = "Development"
    staging = "Staging"
    prod    = "Production"
  }
}

resource "local_file" "env_configs" {
  for_each = var.environments
  
  filename = "${path.module}/envs/${each.key}.conf"
  content  = <<-EOF
    # ${each.value} Configuration
    environment = ${each.key}
    log_level = ${each.key == "prod" ? "error" : "debug"}
    
    # Generated: ${local.timestamp}
  EOF
}
```

**Selgitus:**
- `for_each = var.environments` - itereerib üle map'i
- `each.key` - võti (dev, staging, prod)
- `each.value` - väärtus (Development, ...)
- Ternary operator: `condition ? if_true : if_false`

Rakenda:

```bash
terraform apply
```

**Kontrolli:**

```bash
ls -la envs/
cat envs/dev.conf
cat envs/prod.conf
```

**Oodatav output:**

```
envs/
├── dev.conf
├── prod.conf
└── staging.conf
```

`envs/prod.conf`:

```
# Production Configuration
environment = prod
log_level = error

# Generated: 2025-10-16-0845
```

### Validation Checkpoint

- [ ] `metadata.json` on loodud ja sisaldab timestamp'i
- [ ] `envs/` kaust eksisteerib
- [ ] Kõik 3 env faili on loodud
- [ ] `prod.conf` kasutab `log_level = error`
- [ ] `dev.conf` kasutab `log_level = debug`

---

## 6. State Haldamine ja Manipulatsioon

### 6.1 State Ülevaade

Vaata state'i:

```bash
terraform state list
```

**Oodatav output:**

```
data.local_file.existing_config
local_file.config_dir
local_file.config_file
local_file.env_configs["dev"]
local_file.env_configs["prod"]
local_file.env_configs["staging"]
local_file.examples[0]
local_file.examples[1]
local_file.examples[2]
local_file.metadata
```

### 6.2 State Show

Vaata ühe ressursi detaile:

```bash
terraform state show local_file.metadata
```

**Oodatav output:**

```
# local_file.metadata:
resource "local_file" "metadata" {
    content              = "{\"author\":\"Terraform\",\"date\":\"...\",\"version\":\"1.0\"}"
    content_base64sha256 = "..."
    content_base64sha512 = "..."
    content_md5          = "..."
    content_sha1         = "..."
    content_sha256       = "..."
    content_sha512       = "..."
    directory_permission = "0777"
    file_permission      = "0777"
    filename             = "/home/user/terraform-lab/metadata.json"
    id                   = "..."
}
```

### 6.3 State Drift Detection

Terraform oskab tuvastada käsitsi muudatusi.

**Muuda faili käsitsi:**

```bash
echo "Muudetud käsitsi!" > test-1.txt
```

**Käivita plan:**

```bash
terraform plan
```

**Oodatav output:**

```
local_file.examples[0]: Refreshing state... [id=...]

Terraform will perform the following actions:

  # local_file.examples[0] has changed
  ~ resource "local_file" "examples" {
      ~ content              = "Muudetud käsitsi!" -> "Tere, Terraform!\nSee on fail number 1"
      ~ content_md5          = "..." -> "..."
      ...
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

**Selgitus:** Terraform märkab, et faili sisu on erinev ja plaanib selle parandada.

**Taasta:**

```bash
terraform apply -auto-approve
```

### 6.4 State Taint/Untaint

Mõnikord tahad ressursi uuesti luua ilma muudatusteta.

```bash
# Märgi "määrduks" (recreate järgmisel apply)
terraform taint local_file.metadata

# Vaata plaani
terraform plan
```

**Oodatav output:**

```
Plan: 1 to add, 0 to change, 1 to destroy.
```

**Untaint (võta tagasi):**

```bash
terraform untaint local_file.metadata

# Nüüd ei planeeri enam muudatust
terraform plan
```

### 6.5 State Backup

State failist tehakse automaatselt backup.

```bash
ls -la terraform.tfstate*
```

**Oodatav output:**

```
-rw-r--r--  1 user user 12345 ... terraform.tfstate
-rw-r--r--  1 user user 11234 ... terraform.tfstate.backup
```

**Taasta vana state (kui vaja):**

```bash
cp terraform.tfstate.backup terraform.tfstate
```

### Validation Checkpoint

- [ ] `terraform state list` näitab kõiki ressursse
- [ ] `terraform state show` näitab detaile
- [ ] Terraform tuvastas käsitsi muudatuse
- [ ] `terraform taint` märkis ressursi uuesti loomiseks
- [ ] State backup fail eksisteerib

---

## 7. Debugging ja Troubleshooting

### 7.1 Verbose Logging

Kui midagi ei tööta, lülita verbose logging sisse:

```bash
export TF_LOG=DEBUG
terraform apply
```

**Tulemus:** Näed palju rohkem detaile.

**Lülita välja:**

```bash
unset TF_LOG
```

### 7.2 Validation

Kontrolli koodi süntaksit:

```bash
terraform validate
```

**Kui kõik OK:**

```
Success! The configuration is valid.
```

**Kui viga:**

```
Error: Missing required argument

  on main.tf line 42:
  42: resource "local_file" "broken" {

The argument "content" is required, but no definition was found.
```

### 7.3 Format Check

Terraform oskab koodi automaatselt vormindada:

```bash
terraform fmt
```

**Tulemus:** Kõik `.tf` failid vormindatakse ühtselt.

**Kontrolli ilma muutmata:**

```bash
terraform fmt -check
```

### 7.4 Tavalisemad Vead

#### Viga 1: Provider Not Initialized

```
Error: Could not load plugin
```

**Lahendus:**

```bash
terraform init
```

#### Viga 2: Resource Already Exists

```
Error: file already exists and was not created by Terraform
```

**Lahendus:** Kustuta fail käsitsi või impordi state'i:

```bash
rm conflicting-file.txt
terraform apply
```

#### Viga 3: State Lock

```
Error: Error acquiring the state lock
```

**Lahendus:** Mõni teine Terraform protsess töötab. Oota või:

```bash
terraform force-unlock <LOCK_ID>
```

**HOIATUS:** Kasuta `force-unlock` ainult kui kindel!

#### Viga 4: Circular Dependency

```
Error: Cycle: resource.a, resource.b
```

**Lahendus:** Kaks ressurssi sõltuvad üksteisest. Muuda arhitektuuri.

### Validation Checkpoint

- [ ] `TF_LOG=DEBUG` töötab
- [ ] `terraform validate` kontrollib süntaksit
- [ ] `terraform fmt` vormindab koodi
- [ ] Tead kuidas debugida tavalisi vigu

---

## 8. Cleanup ja Kokkuvõte

### 8.1 Kõige Kustutamine

Kui oled valmis, kustuta kõik Terraform'iga loodud ressursid:

```bash
terraform destroy
```

**Oodatav output:**

```
Plan: 0 to add, 0 to change, 13 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value:
```

Sisesta: `yes`

**Tulemus:** Kõik failid ja kaustad kustutatakse.

**Kontrolli:**

```bash
ls -la
```

Ainult Terraform failid jäävad:

```
.terraform/
main.tf
outputs.tf
variables.tf
terraform.tfstate
terraform.tfstate.backup
terraform.lock.hcl
```

### 8.2 Projekti Puhastamine

Kui tahad alustada puhtalt:

```bash
rm -rf .terraform/
rm terraform.tfstate*
rm terraform.lock.hcl
```

---

## Labori Kontrollnimekiri

Kontrolli, et oled kõik sammud läbi teinud:

**Setup:**
- [ ] Terraform installitud ja töötab
- [ ] Töökataloog loodud
- [ ] `main.tf` fail loodud
- [ ] `terraform init` edukas

**Basic Operations:**
- [ ] `terraform plan` näitas muudatusi
- [ ] `terraform apply` lõi ressursse
- [ ] Idempotentsuse test õnnestus

**Variables ja Outputs:**
- [ ] `variables.tf` loodud ja kasutatud
- [ ] `outputs.tf` näitab infot
- [ ] `-var` flag töötab

**Sõltuvused:**
- [ ] Kaustad ja failid loodud õiges järjekorras
- [ ] Data source töötab
- [ ] `depends_on` kasutatud

**Advanced:**
- [ ] `locals` kasutatud
- [ ] `for_each` töötab
- [ ] Erinevad env failid loodud

**State:**
- [ ] `terraform state list` töötab
- [ ] State drift tuvastatud
- [ ] State backup eksisteerib

**Debugging:**
- [ ] `terraform validate` kasutatud
- [ ] `terraform fmt` vormindas koodi
- [ ] Debugging tehnikad testitud

**Cleanup:**
- [ ] `terraform destroy` käivitatud
- [ ] Kõik ressursid kustutatud

---

## Järgmised Sammud

**1. AWS/Azure Practice**

Järgmine samm: proovi sama AWS või Azure provider'iga.

**Erinevus:**
- Vajad AWS/Azure accounti
- Ressursid maksavad raha (väikesed summad)
- Real-world infrastructure

**Alusta:**
- [Terraform AWS Tutorial](https://developer.hashicorp.com/terraform/tutorials/aws-get-started)
- [Terraform Azure Tutorial](https://developer.hashicorp.com/terraform/tutorials/azure-get-started)

**2. Remote State**

Õpi salvestama state remote backend'is:
- AWS: S3 + DynamoDB (locking)
- Azure: Azure Storage + Lock

**Miks oluline:**
- Meeskonnatöö
- State lock
- Versioning + backup

**3. Moodulid**

Kirjuta korduvkasutatavaid mooduleid.

**Näide:**

```hcl
module "network" {
  source = "./modules/network"
  
  vpc_cidr = "10.0.0.0/16"
}
```

**4. Workspaces**

Halda mitut keskkonda (dev, staging, prod):

```bash
terraform workspace new dev
terraform workspace new prod
terraform workspace select dev
```

---

## Troubleshooting Guide

### Probleem: Terraform aeglane

**Põhjus:** Suur state fail, palju ressursse

**Lahendus:**
- Kasuta `-parallelism=10` (default: 10)
- Jaga projekt mitmeks

### Probleem: Provider download ebaõnnestub

**Põhjus:** Võrguprobleem, firewall

**Lahendus:**

```bash
# Kasuta mirror'it
terraform init -plugin-dir=/path/to/plugins

# Või:
export TF_PLUGIN_CACHE_DIR="$HOME/.terraform.d/plugin-cache"
mkdir -p $TF_PLUGIN_CACHE_DIR
```

### Probleem: State conflict

**Põhjus:** Kaks inimest käivitas samaaegselt

**Lahendus:**
- Kasuta remote backend (S3) + locking (DynamoDB)
- Koordineeri meeskonnaga

### Probleem: Resource import

**Stsenaarium:** Sul on käsitsi loodud ressurss, tahad Terraform haldusesse võtta.

**Lahendus:**

```bash
# 1. Kirjuta resource block (ilma atribuutideta)
resource "local_file" "existing" {
  filename = "/tmp/existing.txt"
  content  = ""  # Täitub import'imisel
}

# 2. Impordi
terraform import local_file.existing /tmp/existing.txt

# 3. Täienda atribuudid state'ist
terraform state show local_file.existing
```

---

## Kasulikud Käsud

```bash
# Ülevaade
terraform version
terraform -help

# Workflow
terraform init
terraform validate
terraform fmt
terraform plan
terraform apply
terraform destroy

# State
terraform state list
terraform state show <resource>
terraform state mv <source> <dest>
terraform state rm <resource>

# Workspace
terraform workspace list
terraform workspace new <name>
terraform workspace select <name>

# Debug
export TF_LOG=DEBUG
export TF_LOG_PATH=./terraform.log

# Graph (vajab graphviz)
terraform graph | dot -Tpng > graph.png
```

---

## Ressursid

**Dokumentatsioon:**
- [Terraform Docs](https://developer.hashicorp.com/terraform/docs)
- [Local Provider](https://registry.terraform.io/providers/hashicorp/local/latest/docs)
- [Terraform Registry](https://registry.terraform.io/)

**Õppimine:**
- [HashiCorp Learn](https://developer.hashicorp.com/terraform/tutorials)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

**Community:**
- [Terraform GitHub](https://github.com/hashicorp/terraform)
- [Terraform Discuss](https://discuss.hashicorp.com/c/terraform-core)

---

**Õnnitlused!** Oled läbinud Terraform alused labori. Nüüd oled valmis real-world projektidega alustama.

**Järgmine väljakutse:** AWS/Azure infrastruktuur Terraform'iga!