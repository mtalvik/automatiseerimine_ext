# Terraform Alused - Self-Study Materjal

**Eeldused:** Linux CLI, Git, teksteditor

**Platvorm:** Terraform (kohalik)

**Ajakulu:** ~4-6 tundi (võid teha osade kaupa)

**Dokumentatsioon:** [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)

---

## Kuidas Seda Materjali Kasutada

See on **self-study** materjal - disainitud, et saad iseseisvalt läbi töötada ilma õpetajata.

**Struktuur:**
- 📖 **Teooria** - mõista kontseptsioone
- ⚡ **Praktiline harjutus** - kohe proovi ise
- ✅ **Checkpoint** - kontrolli kas said õigesti
- 🔧 **Troubleshooting** - kui midagi ei tööta

**Nõuanne:** Ära loe lihtsalt - **TEE harjutused**. Programmeerimist õpitakse programmeerides, mitte lugemisega.

---

## Õpiväljundid

Pärast selle materjali läbimist sa:

- Selgitad Infrastructure as Code eeliseid konkreetsete näidetega
- Eristad Terraform'i teistest IaC tööriistadest (Ansible, CloudFormation)
- Kirjeldad Terraform'i arhitektuuri (Core, Providers, State)
- Mõistad deklaratiivset lähenemist vs imperatiivne
- Kirjutad töötavat HCL koodi
- Kasutad Terraform workflow'i: init, plan, apply, destroy

---

## 1. Miks Infrastructure as Code?

### Probleem: Käsitsi Seadistamine

Kujuta ette olukorda: Sul on vaja luua 5 identset serverit AWS'is. Käsitsi seadistamine tähendab:

1. Logi sisse AWS Console
2. EC2 → Launch Instance
3. Vali AMI (Amazon Linux 2)
4. Vali instance type (t3.micro)
5. Seadista network (VPC, subnet, security group)
6. Seadista storage
7. Lisa tags
8. Käivita

Korda seda 5 korda. **Ajakulu:** 2-3 tundi.

**Probleemid:**
- Aeganõudev - iga server võtab 20-30 min
- Vigaderohke - inimene eksib, unustas pordi 443 avada
- Dokumenteerimata - 6 kuud hiljem ei tea keegi, mis seal oli
- Ei kordu - iga server veidi erinev ("snowflake")
- Koostöö raske - kaks inimest ei saa korraga töötada

### Lahendus: Infrastructure as Code

**IaC** tähendab: kirjuta infrastruktuuri koodina.

```hcl
# Lihtne näide - ära proovi veel käivitada!
resource "aws_instance" "web" {
  count         = 5
  ami           = "ami-12345"
  instance_type = "t3.micro"
  
  tags = {
    Name = "web-${count.index + 1}"
  }
}
```

Käivita: `terraform apply`

**Tulemus:** 5 identset serverit 3-5 minutiga.

### IaC Eelised

| Aspekt | Käsitsi | IaC (Terraform) |
|--------|---------|-----------------|
| **Kiirus** | 5 serverit = 2-3h | 5 serverit = 3-5 min |
| **Korratavus** | Iga kord erinev | Alati identne |
| **Versioonihaldus** | Confluence (aegunud) | Git (alati ajakohane) |
| **Dokumentatsioon** | Pole/aegunud | Kood ON dokumentatsioon |
| **Koostöö** | Konfliktid | Pull request + review |
| **Testimine** | Raske/võimatu | Dev → Staging → Prod |

### Kontrolli Ennast

<details>
<summary><strong>Küsimus 1:</strong> Miks on käsitsi seadistamine probleemne? (nimetada 3 põhjust)</summary>

**Vastus:**
1. **Aeganõudev** - iga server võtab kaua aega
2. **Vigaderohne** - inimene teeb vigu (unustab seadeid, valesti sisestab)
3. **Ei kordu** - iga kord tuleb natuke erinev ("snowflake servers")
4. **Dokumenteerimata** - mälu/Confluence ei ole piisav
5. **Koostöö raske** - kaks inimest korraga = kaos

(Iga kolm õige põhjus on OK vastus)
</details>

<details>
<summary><strong>Küsimus 2:</strong> Mis on IaC peamine idee?</summary>

**Vastus:**
Infrastructure as Code = infrastruktuur kirjutatakse **koodina** (fail), mitte klõbisedes UI'des.

Sarnaselt rakenduse koodiga:
- Versioonihaldus (Git)
- Review (pull request)
- Testimine (dev/staging/prod)
- Dokumentatsioon (kood ise on dok)
</details>

---

## 2. Mis on Terraform?

Terraform on HashiCorp'i loodud **Infrastructure as Code** tööriist.

**Loodud:** 2014 (üle 10 aasta kasutuses)  
**Keel:** Go  
**Litsents:** Open-source (tasuta)  
**Kasutajaid:** 1000+ ettevõtet (AWS, Microsoft, Google, GitLab, ...)

### Terraform Roll

Terraform **loob** infrastruktuuri. See ei konfigureeri rakendusi.

**Analoogi:**

```
Maja ehitamine:
├── Terraform ───> Ehitab maja (vundament, seinad, elekter)
├── Ansible ────> Sisekujundus (mööbel, värv, dekoratsioonid)
└── Kubernetes ─> Kolija (paigutab asjad õigetesse tubadesse)
```

**Näide:**

| Tööriist | Roll | Näide |
|----------|------|-------|
| Terraform | Loob serveri | AWS EC2 instance, 2GB RAM, Ubuntu 22.04 |
| Ansible | Seadistab serveri | Installib Nginx, MySQL, seadistab firewall |
| Kubernetes | Deploy'b rakenduse | Paigutab konteinerid serveritele |

**Tavaliselt koos:**
```
1. Terraform → loob 10 serverit AWS'is
2. Ansible → installib Nginx kõigile
3. Kubernetes → deploy'b rakenduse
```

### Terraform Tugevused

#### 1. Multi-Cloud

Sama kood töötab AWS'is, Azure'is, GCP's.

```hcl
# AWS
resource "aws_instance" "web" {
  ami           = "ami-12345"
  instance_type = "t3.micro"
}

# Azure (sama loogika!)
resource "azurerm_virtual_machine" "web" {
  name     = "web-vm"
  size     = "Standard_B1s"
}
```

**Miks oluline:** Täna kasutad AWS, homme võib vaja Azure. Terraform oskad juba.

#### 2. Deklaratiivne

Sa ütled **MIDA** tahad, mitte **KUIDAS**.

```
Imperatiivne (Bash):
1. create_server "web1"
2. wait_for_ready
3. attach_security_group
... (20 rida)

Deklaratiivne (Terraform):
resource "aws_instance" "web" {
  count = 3
}
```

Terraform arvutab ise, mida vaja teha.

#### 3. Suur Kogukond

**Terraform Registry:** [registry.terraform.io](https://registry.terraform.io/)

- 3000+ **providers** (AWS, Azure, Docker, Kubernetes, GitHub, ...)
- 10,000+ **mooduleid** (valmis lahendused)

### Terraform vs Ansible

| | Terraform | Ansible |
|---|-----------|---------|
| **Mis teeb** | Loob infrastruktuuri | Seadistab infrastruktuuri |
| **Näide** | "Loo 10 serverit" | "Installi Nginx kõigile" |
| **Keel** | HCL (deklaratiivne) | YAML (imperatiivne) |
| **State** | On (terraform.tfstate) | Ei ole |
| **Kasuta kui** | Vajad uut infrastruktuuri | Seadistad olemasolevat |

### Kontrolli Ennast

<details>
<summary><strong>Küsimus 3:</strong> Mis vahe on Terraform'il ja Ansible'il?</summary>

**Vastus:**

**Terraform:** Loob infrastruktuuri (serverid, võrgud, andmebaasid)  
**Ansible:** Seadistab/konfigureerib infrastruktuuri (installib tarkvara, muudab seadeid)

**Analoogi:**
- Terraform = ehitaja (ehitab maja)
- Ansible = sisekujundaja (paneb mööbli, värvi, dekoratsioonid)
</details>

<details>
<summary><strong>Küsimus 4:</strong> Miks Terraform on "multi-cloud"?</summary>

**Vastus:**

Terraform kasutab **providers** (pluginad), mis räägivad erinevate platvormidega:
- aws provider → Amazon Web Services
- azurerm provider → Microsoft Azure
- google provider → Google Cloud

Sama HCL süntaks, erinev provider. Õpid ühe korra, kasutad kõikjal.
</details>

---

## 3. Terraform Arhitektuur

Terraform = 3 komponenti:

```
┌─────────────────┐
│  Terraform Core │  ← Aju (planeerib, otsustab)
│     (Go)        │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼───┐  ┌──▼────┐
│AWS    │  │Azure  │  ← Käed (täidavad)
│Provider│  │Provider│
└───┬───┘  └──┬────┘
    │          │
┌───▼──────────▼───┐
│  State File      │  ← Mälu (mäletab)
│ terraform.tfstate│
└──────────────────┘
```

### 1. Terraform Core (Aju)

Core on Terraform'i peaprotsessor. Go keeles kirjutatud.

**Mis teeb:**
- Loeb `.tf` faile (sinu konfiguratsiooni)
- Võrdleb: **soovitud** (kood) vs **praegune** (state)
- Teeb plaani (mis muuta?)
- Täidab plaani (loob/muudab/kustutab)

**Analoogi:** Ehituse projektijuht. Vaatab joonist, vaatab mis ehitatud, planeerib järgmised sammud.

### 2. Providers (Käed)

Providers = pluginad, mis räägivad API'dega.

**Konfiguratsioon:**

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-north-1"  # Stockholm
}
```

**Kuidas töötab:**

```
Sina: "Tahan serveri"
  ↓
Core: "OK, kasutan AWS provider'it"
  ↓
AWS Provider: "CreateInstance API call..."
  ↓
AWS: "Valmis! ID: i-12345"
  ↓
Core: "Salvestan state'i"
```

**Populaarsed providers:**

| Provider | Kasutus |
|----------|---------|
| **aws** | Amazon Web Services |
| **azurerm** | Microsoft Azure |
| **google** | Google Cloud Platform |
| **docker** | Docker konteinerid |
| **kubernetes** | Kubernetes klaster |
| **local** | Lokaalsed failid (õppimiseks!) |

### 3. State File (Mälu)

State = `terraform.tfstate` fail. JSON vormingus.

**Miks oluline:**

```
Sina: "Tahan 3 serverit"
  ↓
Terraform: *vaatab state'i*
Terraform: "Praegu on 2, loon 1 juurde"
```

**Ilma state'ita:**

```
Terraform: "Loon 3 uut!"
AWS: "Aga sul on juba 2..."
Terraform: *loob ikka*
Tulemus: 5 serverit. Ootamatu arve.
```

**State sisaldab:**
- Kõik loodud ressursid
- ID'd (i-12345, sg-67890)
- Atribuudid (IP, subnet, jne)
- Sõltuvused

**KRIITILINE:** State võib sisaldada saladusi (paroolid, API key'd).

**ÄRA PANE GIT'I!**

```gitignore
# .gitignore
*.tfstate
*.tfstate.*
.terraform/
```

### Kontrolli Ennast

<details>
<summary><strong>Küsimus 5:</strong> Mis on Terraform Core, Provider ja State roll?</summary>

**Vastus:**

- **Core** = Aju (planeerib, otsustab, koordineerib)
- **Provider** = Käed (räägivad API'dega, täidavad käske)
- **State** = Mälu (mäletab, mis on loodud)

**Analoogi:** Projektijuht (Core) annab käsu ehitajatele (Provider) ja märgib päevikusse (State) mis on tehtud.
</details>

<details>
<summary><strong>Küsimus 6:</strong> Miks state fail on oluline?</summary>

**Vastus:**

State fail hoiab **päris infrastruktuuri seisu**. Ilma selleta Terraform ei tea:
- Mis ressursid on juba loodud
- Millised ID'd neil on
- Kas midagi on muutunud

Kui state kadub = Terraform on pime. Ta ei tea, mis AWS'is on, ja võib hakata looma duplikaate.

**Tähtis:** State sisaldab saladusi → ära pane Git'i!
</details>

---

## 4. Deklaratiivne vs Imperatiivne

See on Terraform'i **kõige olulisem** kontseptsioon. Kui mõistad seda, mõistad Terraform'i.

### Imperatiivne (KUIDAS?)

Kirjeldad **samme**. Annad täpsed instruktsionid.

**Näide - Bash:**

```bash
#!/bin/bash
# Imperatiivne: kirjeldad samme

echo "Loon security group..."
aws ec2 create-security-group --group-name web-sg

echo "Avan pordi 80..."
aws ec2 authorize-security-group-ingress \
  --group-name web-sg --port 80

echo "Loon 5 serverit..."
for i in {1..5}; do
    aws ec2 run-instances --instance-type t3.micro
done
```

**Probleem:** Käivita teist korda:

```bash
./create-servers.sh

# Tulemus: 10 serverit!
# Script ei tea, et 5 on juba olemas.
```

### Deklaratiivne (MIDA?)

Kirjeldad **tulemust**. Tööriist väljastab samme ise.

**Näide - Terraform:**

```hcl
# Deklaratiivne: kirjeldad tulemust

resource "aws_security_group" "web" {
  name = "web-sg"
  
  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
  }
}

resource "aws_instance" "web" {
  count         = 5
  instance_type = "t3.micro"
  
  vpc_security_group_ids = [aws_security_group.web.id]
}
```

**Käivita mitu korda:**

```bash
terraform apply  # 1. kord: loob 5 serverit
terraform apply  # 2. kord: ei tee midagi
terraform apply  # 3. kord: ei tee midagi
```

Terraform teab (tänu state'ile), mis on olemas. **Idempotent!**

### Võrdlus

| Aspekt | Imperatiivne | Deklaratiivne |
|--------|--------------|---------------|
| **Kirjeldad** | KUIDAS (sammud) | MIDA (tulemus) |
| **Näide** | "Loo server, siis võrk" | "Tahan 5 serverit" |
| **Kordamine** | Loob duplikaate | Idempotent (ei muuda 2. kord) |
| **State** | Sina pead meeles pidama | Tööriist mäletab |
| **Fail** | Kasvab pidevalt | Jääb lühikeseks |

### Update Stsenaarium

**Olukord:** Sul on 5 serverit. Tahad nüüd 7.

#### Imperatiivne:

```bash
#!/bin/bash
# Pead ise arvestama

# Lisa 2 serverit (5 + 2 = 7)
for i in {1..2}; do
    aws ec2 run-instances --instance-type t3.micro
done
```

Pead ise arvutama: "5 → 7 = 2 juurde".

#### Deklaratiivne:

```hcl
resource "aws_instance" "web" {
  count = 7  # Muutsime 5 → 7
  instance_type = "t3.micro"
}
```

```bash
terraform apply
# Terraform: "On 5, peab olema 7. Loon 2."
```

Sa ei pea arvutama. Terraform teeb ise.

### Kontrolli Ennast

<details>
<summary><strong>Küsimus 7:</strong> Mis vahe on imperatiivsel ja deklaratiivsel lähenemisel?</summary>

**Vastus:**

**Imperatiivne:** Kirjeldad **KUIDAS** (sammud)
- Näide: "Esmalt loo security group, siis ava port 80, siis loo 5 serverit"
- Probleem: Kordamine loob duplikaate

**Deklaratiivne:** Kirjeldad **MIDA** (tulemus)
- Näide: "Tahan 5 serverit"
- Eelis: Idempotent - 2. kord ei muuda midagi
</details>

<details>
<summary><strong>Küsimus 8:</strong> Miks Terraform on idempotent?</summary>

**Vastus:**

**Idempotent** = sama käsk mitu korda ei muuda tulemust.

Terraform kasutab **state faili** - ta teab, mis on juba loodud. Kui käivitad `terraform apply` uuesti:
1. Terraform loeb state'i
2. Võrdleb koodiga
3. Kui midagi pole muutunud → ei tee midagi

Tulemus: Turvaline käivitada mitu korda, ei teki duplikaate.
</details>

---

## 5. HCL Keel - HashiCorp Configuration Language

HCL on Terraform'i konfiguratsioonikeel. Disainitud inimestele loetavaks.

### Põhisüntaks

```hcl
<TYPE> "<LABEL>" "<LABEL>" {
  argument = value
}
```

**Näide:**

```hcl
resource "local_file" "greeting" {
  filename = "/tmp/hello.txt"
  content  = "Tere, Terraform!"
}
```

**Selgitus:**
- `resource` = block type
- `"local_file"` = ressursi tüüp (lokaalne fail)
- `"greeting"` = meie antud nimi (võid valida mis tahes)
- `filename`, `content` = argumendid

### Resources

Resource = miski, mida Terraform loob.

**Lokaalne fail:**

```hcl
resource "local_file" "config" {
  filename        = "app.conf"
  content         = "port=8080\ndebug=true"
  file_permission = "0644"
}
```

**Selgitus rea-haaval:**
1. `resource "local_file"` - ressursi tüüp (lokaalne fail)
2. `"config"` - meie nimi (viitamiseks)
3. `filename` - faili asukoht
4. `content` - faili sisu
5. `file_permission` - õigused (644 = rw-r--r--)

**AWS server:**

```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345"           # Amazon Machine Image
  instance_type = "t3.micro"            # Serveri suurus
  
  tags = {
    Name = "WebServer"
    Env  = "Dev"
  }
}
```

### Sõltuvused

Terraform loob automaatselt sõltuvusi.

```hcl
# 1. Esmalt security group
resource "aws_security_group" "web" {
  name = "web-sg"
}

# 2. Siis server (kasutab SG'd)
resource "aws_instance" "web" {
  ami                    = "ami-12345"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.web.id]
  # ↑ automaatne sõltuvus!
}
```

Terraform teab: "Teen SG enne, siis serveri."

```
aws_security_group.web → aws_instance.web
```

### Variables (Muutujad)

Muutujad = dünaamilised väärtused.

```hcl
variable "environment" {
  description = "Keskkond: dev või prod"
  type        = string
  default     = "dev"
}

resource "aws_instance" "app" {
  instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"
  
  tags = {
    Env = var.environment
  }
}
```

**Selgitus:**
- `variable` block - deklareerib muutuja
- `var.environment` - kasutab muutujat
- Ternary operator: `condition ? if_true : if_false`

**Kasutamine:**

```bash
terraform apply -var="environment=prod"
```

### Outputs (Väljundid)

Outputs = info pärast loomist.

```hcl
output "server_ip" {
  description = "Serveri avalik IP"
  value       = aws_instance.web.public_ip
}
```

Pärast `terraform apply`:

```
Outputs:
server_ip = "13.51.123.45"
```

### Funktsioonid

HCL sisaldab kasulikke funktsioone.

```hcl
# Faili sisu
content = file("config.json")

# JSON encode
metadata = jsonencode({
  name = "app"
  version = "1.0"
})

# String template
message = "Tere, ${var.name}!"

# Timestamp
created_at = timestamp()

# Format string
name = format("server-%03d", count.index + 1)
# Tulemus: server-001, server-002, ...
```

### ⚡ Praktiline Harjutus 1: Esimene Terraform Kood

**Eesmärk:** Loo lokaalne fail Terraform'iga.

**Sammud:**

1. **Loo kaust:**

```bash
mkdir ~/terraform-test && cd ~/terraform-test
```

2. **Loo fail `main.tf`:**

```hcl
resource "local_file" "hello" {
  filename = "/tmp/terraform-hello.txt"
  content  = "Tere, see on minu esimene Terraform fail!"
}

output "file_path" {
  value = local_file.hello.filename
}
```

3. **Salvesta fail** (Ctrl+O, Enter, Ctrl+X kui kasutad `nano`)

✅ **Checkpoint:** `ls -la` peaks näitama `main.tf` faili.

**Märkused:**
- `resource "local_file"` - lokaalne fail (ei vaja AWS/Azure)
- `"hello"` - meie nimi (võid muuta)
- `/tmp/terraform-hello.txt` - kuhu fail luuakse
- `output` - näitab meile faili teed

---

## 6. Terraform Workflow

Terraform'i kasutamine = 4 sammu tsükkel:

```
init → plan → apply → (destroy)
  ↑                         ↓
  └─────────────────────────┘
```

### 1. terraform init

Valmistab projekti ette.

```bash
terraform init
```

**Mis toimub:**
- Laeb provider'id (local, aws, azure, ...)
- Seadistab backend'i (kus state salvestatakse)
- Init-ib moodulid

**Output:**

```
Initializing the backend...
Initializing provider plugins...
- Finding latest version of hashicorp/local...
- Installing hashicorp/local v2.4.0...

Terraform has been successfully initialized!
```

**Millal käivita:**
- Esimest korda projektis
- Lisad uue provider'i
- Clone'id repo Git'ist

**Kui unustada:**

```bash
terraform plan
# Error: Could not load plugin
# Run: terraform init
```

### 2. terraform plan

Näitab, mis muutub. **EI MUUDA MIDAGI!**

```bash
terraform plan
```

**Sümbolid:**

| Sümbol | Tähendus | Näide |
|--------|----------|-------|
| `+` | Luuakse | Uus server |
| `-` | Kustutatakse | Vana server |
| `~` | Muudetakse | Port 80 → 443 |
| `-/+` | Replace | Instance type muutus |

**Output:**

```terraform
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
      + filename             = "/tmp/terraform-hello.txt"
      + id                   = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

**ALATI tee plan enne apply!** See näitab, mis juhtub.

### 3. terraform apply

Rakendab muudatused **PÄRISELT**.

```bash
terraform apply
```

Küsib kinnitust:

```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes
```

**Output:**

```
local_file.hello: Creating...
local_file.hello: Creation complete after 0s [id=abc123...]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:
file_path = "/tmp/terraform-hello.txt"
```

**Automaatne (ohtlik!):**

```bash
terraform apply -auto-approve
```

Kasuta ainult kui **100% kindel**!

### 4. terraform destroy

Kustutab **KÕIK** ressursid.

```bash
terraform destroy
```

**HOIATUS:** Pöördumatu!

**Output:**

```
local_file.hello: Destroying... [id=abc123...]
local_file.hello: Destruction complete after 0s

Destroy complete! Resources: 1 destroyed.
```

### ⚡ Praktiline Harjutus 2: Terraform Workflow

**Eesmärk:** Läbi kogu Terraform tsükkel.

**Sammud:**

1. **Init (kui pole veel teinud):**

```bash
cd ~/terraform-test
terraform init
```

✅ **Checkpoint:** Peaks ilmuma `.terraform/` kaust ja `terraform.lock.hcl` fail.

2. **Plan:**

```bash
terraform plan
```

✅ **Checkpoint:** Peaks näitama:
```
Plan: 1 to add, 0 to change, 0 to destroy.
```

3. **Apply:**

```bash
terraform apply
```

Sisesta: `yes`

✅ **Checkpoint:** Peaks näitama:
```
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

4. **Kontrolli:**

```bash
cat /tmp/terraform-hello.txt
```

✅ **Checkpoint:** Peaks näitama: `Tere, see on minu esimene Terraform fail!`

5. **Vaata state'i:**

```bash
cat terraform.tfstate
```

✅ **Checkpoint:** JSON fail, sisaldab `local_file.hello` infot.

6. **Apply uuesti (idempotence test):**

```bash
terraform apply
```

✅ **Checkpoint:** Peaks näitama:
```
No changes. Your infrastructure matches the configuration.
```

7. **Destroy:**

```bash
terraform destroy
```

Sisesta: `yes`

✅ **Checkpoint:** Fail `/tmp/terraform-hello.txt` on kustutatud.

```bash
ls -la /tmp/terraform-hello.txt
# ls: cannot access '/tmp/terraform-hello.txt': No such file or directory
```

### 🔧 Troubleshooting

**Probleem 1:** `terraform: command not found`

**Lahendus:** Terraform pole installitud või pole PATH'is.

```bash
# Kontrolli:
which terraform

# Kui puudub, installi:
# Ubuntu/Debian
sudo apt update
sudo apt install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update
sudo apt install terraform

# macOS
brew install terraform
```

**Probleem 2:** `Error: Could not load plugin`

**Lahendus:** Käivita `terraform init` uuesti.

```bash
rm -rf .terraform
terraform init
```

**Probleem 3:** `Error: Permission denied: /tmp/terraform-hello.txt`

**Lahendus:** Sul pole õigust `/tmp/` kirjutada (ebatavaline) või fail on olemas ja on read-only.

```bash
# Kontrolli:
ls -la /tmp/terraform-hello.txt

# Kui on read-only:
chmod 644 /tmp/terraform-hello.txt
rm /tmp/terraform-hello.txt

# Proovi uuesti:
terraform apply
```

**Probleem 4:** `Error: Unsupported block type`

**Lahendus:** Süntaksi viga `main.tf` failis. Kontrolli:
- Kas `resource` on õigesti kirjutatud?
- Kas kõik sulgud `{ }` on paarid?
- Kas stringid on jutumärkides `" "`?

```bash
# Kontrolli süntaksit:
terraform validate
```

---

## 7. State Haldamine

State fail on Terraform'i **kõige kriitilisem** komponent.

### State'i Sisemus

Ava `terraform.tfstate` fail:

```bash
cat terraform.tfstate
```

See on JSON. **Ära muuda käsitsi!**

**Struktuur:**

```json
{
  "version": 4,
  "terraform_version": "1.6.0",
  "serial": 1,
  "lineage": "abc-123-def",
  "resources": [
    {
      "mode": "managed",
      "type": "local_file",
      "name": "hello",
      "provider": "provider[\"registry.terraform.io/hashicorp/local\"]",
      "instances": [
        {
          "attributes": {
            "content": "Tere, see on minu esimene Terraform fail!",
            "filename": "/tmp/terraform-hello.txt",
            "id": "abc123...",
            "content_md5": "xyz789..."
          }
        }
      ]
    }
  ]
}
```

**Sisaldab:**
- `version` - state formaat
- `terraform_version` - Terraform versioon
- `serial` - inkrementeeruv number (iga apply suurendab)
- `resources` - kõik loodud ressursid

### State'i Elutsükkel

```
terraform apply
    ↓
Read current state
    ↓
Compare with config
    ↓
Differences?
    ↓
Yes → Make changes → Update state
No  → Do nothing
```

### State Lock

Kui kaks inimest käivitab `terraform apply` samaaegselt, tekib kaos.

**State lock** kaitseb selle eest:

```bash
# Terminal 1
$ terraform apply
Acquiring state lock. This may take a few moments...

# Terminal 2 (samaaegselt)
$ terraform apply
Error: Error acquiring the state lock
Lock ID: abc-123
```

Teine protsess **ootab**, kuni esimene lõpetab.

**Märkus:** Lokaalne state ei kasuta lock'i. Remote backend (S3 + DynamoDB) kasutab.

### State'i Ohud

**1. Saladused**

State fail sisaldab **kõike**, sh saladusi.

```hcl
resource "aws_db_instance" "main" {
  username = "admin"
  password = "SuperSecret123!"
}
```

Pärast `terraform apply` → `terraform.tfstate` sisaldab:

```json
{
  "resources": [{
    "attributes": {
      "username": "admin",
      "password": "SuperSecret123!"  ← PLAIN TEXT!
    }
  }]
}
```

**Lahendus:** Kasuta remote backend (S3) + encryption.

**2. State kaotsiminek**

Kui `terraform.tfstate` kustub → Terraform ei tea, mis on loodud.

**Stsenaarium:**

```bash
$ rm terraform.tfstate  # Kogemata
$ terraform apply
# Terraform: "Pole midagi, loon kõik uuesti!"
# AWS: Tulemus - duplikaadid
```

**Lahendus:** Alati backup! Kasuta remote backend (S3) + versioning.

### ⚡ Praktiline Harjutus 3: State Manipulatsioon

**Eesmärk:** Mõista, kuidas state mõjutab Terraform'i käitumist.

**Sammud:**

1. **Loo ressurss:**

```bash
cd ~/terraform-test

# main.tf peaks olemas olema
terraform apply -auto-approve
```

✅ **Checkpoint:** Fail `/tmp/terraform-hello.txt` on loodud.

2. **Vaata state'i:**

```bash
cat terraform.tfstate | grep "filename"
```

✅ **Checkpoint:** Peaks näitama: `"filename": "/tmp/terraform-hello.txt"`

3. **Muuda faili käsitsi (mitte Terraform'iga!):**

```bash
echo "Muudetud käsitsi!" > /tmp/terraform-hello.txt
```

4. **Käivita plan:**

```bash
terraform plan
```

✅ **Checkpoint:** Terraform **ei märka** muudatust!

**Miks?** Terraform võrdleb ainult:
- Config (`main.tf`) vs State (`terraform.tfstate`)

Ta **ei kontrolli** päris faili sisu!

5. **Force update:**

```bash
terraform apply -replace="local_file.hello"
```

✅ **Checkpoint:** Fail taastatud originaal sisuga.

6. **Kustuta state (TEST!):**

```bash
rm terraform.tfstate
rm terraform.tfstate.backup
```

7. **Käivita plan:**

```bash
terraform plan
```

✅ **Checkpoint:** Terraform arvab, et midagi pole loodud:

```
Plan: 1 to add, 0 to change, 0 to destroy.
```

Aga fail `/tmp/terraform-hello.txt` on **ikka olemas**!

8. **Apply (loob duplikaadi?):**

```bash
terraform apply -auto-approve
```

**Tulemus:** Fail üle kirjutatud (local_file ei saa duplikaate, aga AWS'is tekiks!).

9. **Cleanup:**

```bash
terraform destroy -auto-approve
```

### Kontrolli Ennast

<details>
<summary><strong>Küsimus 9:</strong> Mis on state fail ja miks see on oluline?</summary>

**Vastus:**

**State fail** (`terraform.tfstate`) = JSON fail, kus Terraform hoiab infot loodud ressursside kohta.

**Sisaldab:**
- Kõik ressursi ID'd
- Atribuudid (IP'd, nimesid, jne)
- Sõltuvused

**Miks oluline:**
- Ilma selleta Terraform ei tea, mis on loodud
- Kasutatakse võrdlemiseks: config vs tegelikkus
- Võimaldab idempotentsust

**HOIATUS:** Sisaldab saladusi → ära pane avalikku Git'i!
</details>

<details>
<summary><strong>Küsimus 10:</strong> Mida teeb Terraform, kui state fail kaob?</summary>

**Vastus:**

Kui state fail kaob:
1. Terraform arvab, et **midagi pole loodud**
2. `terraform plan` näitab: "Loon kõik ressursid"
3. `terraform apply` proovib **uuesti luua**

**Tulemus:**
- Lokaalsed ressursid (failid) → üle kirjutatud
- Cloud ressursid (AWS/Azure) → **duplikaadid**, konfliktid, vead

**Õppetund:** Alati backup state! Kasuta remote backend (S3) + versioning.
</details>

---

## 8. Kokkuvõte ja Järgmised Sammud

### Mida Sa Nüüd Oskad

✅ **IaC Kontseptsioon:**
- Infrastruktuur koodina
- Versioonihaldus, korratavus, dokumentatsioon

✅ **Terraform Arhitektuur:**
- Core (aju), Providers (käed), State (mälu)

✅ **Deklaratiivne Lähenemine:**
- Kirjelda MIDA, mitte KUIDAS
- Idempotentsus - turvaline käivitada mitu korda

✅ **HCL Keel:**
- `resource`, `variable`, `output`
- Sõltuvused, funktsioonid

✅ **Terraform Workflow:**
- `init` → `plan` → `apply` → (`destroy`)

✅ **State Haldamine:**
- Mis on state fail
- Miks see on kriitiline
- Kuidas seda kaitsta

### Praktiline Test (Testimiseks)

Proovi luua see ilma vaatamata:

**Ülesanne:** Loo Terraform konfiguratsioon, mis:
1. Loob 3 lokaalselt faili `/tmp/file-1.txt`, `/tmp/file-2.txt`, `/tmp/file-3.txt`
2. Iga fail sisaldab: "See on fail number X"
3. Kasuta `count` atribuuti

<details>
<summary><strong>Lahendus</strong></summary>

```hcl
resource "local_file" "test" {
  count    = 3
  filename = "/tmp/file-${count.index + 1}.txt"
  content  = "See on fail number ${count.index + 1}"
}

output "file_names" {
  value = local_file.test[*].filename
}
```

**Käivita:**

```bash
terraform init
terraform plan
terraform apply -auto-approve

# Kontrolli:
cat /tmp/file-1.txt
cat /tmp/file-2.txt
cat /tmp/file-3.txt

# Cleanup:
terraform destroy -auto-approve
```

**Selgitus:**
- `count = 3` → loob 3 instantsi
- `count.index` → 0, 1, 2
- `count.index + 1` → 1, 2, 3
- `local_file.test[*].filename` → kõik failide nimed
</details>

### Järgmised Sammud

**1. AWS/Azure Providers**

Järgmine samm: tee sama AWS/Azure'iga (päris cloud ressursid).

**Õppematerjalid:**
- [Terraform AWS Tutorial](https://developer.hashicorp.com/terraform/tutorials/aws-get-started)
- [Terraform Azure Tutorial](https://developer.hashicorp.com/terraform/tutorials/azure-get-started)

**2. Remote State**

Õpi salvestama state remote backend'is (S3, Azure Storage).

**Miks oluline:**
- Meeskonnatöö (state lock)
- Backup (versioning)
- Turvalisus (encryption)

**3. Moodulid**

Korduvkasutatavad komponendid.

```hcl
module "network" {
  source = "./modules/network"
  
  vpc_cidr = "10.0.0.0/16"
}
```

**4. Workspaces**

Erinevad keskkonnad (dev, staging, prod).

```bash
terraform workspace new dev
terraform workspace new prod
```

### Kasulikud Ressursid

**Dokumentatsioon:**
- [Terraform Docs](https://developer.hashicorp.com/terraform/docs)
- [HCL Syntax](https://developer.hashicorp.com/terraform/language/syntax)
- [Registry](https://registry.terraform.io/)
- [State Documentation](https://developer.hashicorp.com/terraform/language/state)

**Õppimine:**
- [HashiCorp Learn](https://developer.hashicorp.com/terraform/tutorials)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

**Kogukond:**
- [Terraform GitHub](https://github.com/hashicorp/terraform)
- [Terraform Discuss](https://discuss.hashicorp.com/c/terraform-core)

**Eesti:**
- DevOps Estonia meetup'id
- TalTech/Tartu Ülikool kursused

---

## Lisaküsimused (Self-Check)

Vastata pole vaja kirjalikult, aga mõtle läbi:

1. **Miks on IaC parem kui käsitsi seadistamine?**
   - Kiirus, korratavus, dokumentatsioon, versioonihaldus

2. **Mis vahe on Terraform'il ja Ansible'il?**
   - Terraform loob, Ansible seadistab

3. **Mis on Terraform Core, Provider ja State?**
   - Core = aju, Provider = käed, State = mälu

4. **Miks on deklaratiivne parem kui imperatiivne?**
   - Idempotentsus, lihtsam kood, automaatne planeerimine

5. **Mis on state fail ja miks see on kriitiline?**
   - Hoiab loodud ressursse, võimaldab võrdlust, sisaldab saladusi

6. **Mis juhtub, kui state fail kaob?**
   - Terraform loob duplikaate või tekivad vead

7. **Mis on Terraform workflow sammud?**
   - init → plan → apply → destroy

8. **Miks kasutada `terraform plan` enne `terraform apply`?**
   - Näed, mis muutub, vältid üllatusi

---

## Lõppmärkused

**Õnnitlused!** Oled läbinud Terraform alused.

**Eesti DevOps mantra:** "Plan enne Apply't, backup enne Destroy'd, kohv enne debugimist."

**Mis edasi?**

Nüüd oled valmis praktiseerima päris projektidega:
- Loo AWS/Azure ressursse
- Kasuta remote state (S3)
- Kirjuta mooduleid
- Töötavad meeskonnas (Git + Terraform)

**Küsimused?** Küsi õpetajalt või DevOps kogukonnast.

**Head programmeerimist!** 🚀