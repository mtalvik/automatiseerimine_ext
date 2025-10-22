# Terraform Alused

**Eeldused:** Linux CLI, Git, teksteditor

**Platvorm:** Terraform (kohalik)

**Dokumentatsioon:** [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)

## Õpiväljundid

Pärast seda loengut sa:
- Selgitad Infrastructure as Code eeliseid konkreetsete näidetega
- Eristad Terraform'i teistest IaC tööriistadest  
- Kirjeldad Terraform'i arhitektuuri komponente
- Mõistad deklaratiivset lähenemist vs imperatiivne
- Kirjutad HCL koodi põhielemente
- Kasutad Terraform workflow'i: init, plan, apply

---

## 1. Miks Me Vajame Infrastructure as Code?

Kujuta ette: Esmaspäev, kell 9:00 hommikul. CEO kirjutab Slackis: "Vajame test keskkonda, demo on reedel!"

Sa oled DevOps insener. Sul on 3 päeva. Sa avad AWS Console'i... ja seal on juba 47 tab'i eelmistest projektidest lahti.

**9:00** - Alustamine  
**10:00** - Ikka veel dokumentatsiooni lugemine  
**11:30** - Oops, vale instance type valitud  
**12:00** - "Kurat, pean kõik kustutama ja uuesti alustama"  
**14:00** - "LÕPUKS töötab!"  
**15:00** - CEO: "Aa jaa, tegelikult vajame 5 serverit, mitte üht..."

*Sügav sissehingamine.*

See pole ainult ühe halva päeva lugu. See on **reaalsus** paljudes ettevõtetes, kus infrastruktuuri seadistatakse käsitsi.

### Käsitsi Seadistamise Probleemid

Mõtle selle peale nagu videomängus:

**Level 1: Aeglus**  
Üks server = 30 minutit klõbistamist. Viis serverit = terve päev. Kümme serverit = kaks päeva. Sada serverit? Unusta ära.

Pipedrive näide: käsitsi seadistamine võttis kaks päeva. Terraform'iga? Kümme minutit.

**Level 2: Vead**  
Inimesed teevad vigu. Unustasid ühe tulemüüri reegli? Süsteem ei tööta. Vale security group? Häkkerid võivad sisse pääseda. Andmebaas vales subnet'is? Mitte keegi ei saa ühendust.

Uuringud näitavad: **40% infrastruktuurist on erinev** production ja staging vahel. Miks? Keegi unustas midagi kopeerida.

**Level 3: Dokumentatsioon puudub**  
Kuus kuud hiljem keegi ei mäleta, mida AWS konsoolis tehti. Confluence dokumentatsioon on aegunud. Algne insener? Läks Bolt'i (parem palk). Uus inimene peab kõike aimama.

**Level 4: Ei kordu**  
Iga kord kui seadistad käsitsi, tuleb natuke erinev tulemus. Need on "snowflake serverid" - iga server on unikaalne nagu lumehelves. Debuggimine muutub põrguks.

**Boss Level: Koostöö on võimatu**  
Kaks inimest ei saa AWS konsoolis samaaegselt töötada. Konfliktid on paratamatud. Üks kirjutab teise muudatused üle. "KES KUSTUTAS MU SERVERI?!"

| Probleem | Päris Näide |
|----------|-------------|
| Aeglane | Pipedrive: 2 päeva vs 10 minutit |
| Vigaderohne | 40% infrastruktuurist erinev |
| Dokumenteerimata | Confluence 3 kuud vana |
| Ei kordu | "Töötab minu masinas" |
| Koostöö raske | "Kes seda muutis?!" |

### Päris Lugu: 30,000 Euro Viga

**Tallinn, 2023. Fintech startup.**

DevOps insener seadistab production keskkonna käsitsi AWS'is. Kulub kaks nädalat. Kõik "dokumenteeritud" Confluence'is.

Kolm kuud hiljem: vaja staging keskkonda.

**Plot twist:** Algne insener on vahepeal lahkunud.

Uus inimene proovib dokumentatsiooni järgida:

```
Dokumentatsioon: "Lisa security group sg-abc123"
Reaalsus: See group kustutati 2 kuud tagasi

Dokumentatsioon: "Instance type: t2.medium"  
Reaalsus: Keegi upgraderis t3.large peale

Dokumentatsioon: "Database port: 5432"
Reaalsus: Muudeti 3306 peale (keegi ei mäleta miks)
```

**Tulemus:**  
Staging on 40% erinev production'ist. Bug'id, mis staging'us ei ilmnenud, plahvatasid production'is.

**Kahju:**
- 2 tundi downtime
- 1000+ vihast klienti  
- 30,000 eurot
- 200 tundi debuggimist
- Üks väga kurb DevOps insener

**Õppetund:** Käsitsi seadistamine ei skaleeru.

### Lahendus: Infrastructure as Code

**Lihtne vastus:** Kirjuta infrastruktuur koodina. Mitte klõpsamine, mitte nuppude vajutamine - **kood**.

```
Vana viis:
1. Ava AWS Console
2. Klõpsa 50 nuppu
3. Kulub 2-4 tundi
4. "Dokumenteeri" (või pigem mitte)
5. Unusta kuidas tegid

IaC viis:
1. Kirjuta kood (15 min)
2. terraform apply (3 min)
3. Kood ON dokumentatsioon
4. Git mäletab kõike
```

Võrdlus:

| Meetod | Aeg | Korratav? | Dokumenteeritud? | Vigade risk |
|--------|-----|-----------|------------------|-------------|
| Käsitsi | 2-4h | Ei | Vahel | Kõrge |
| Terraform | 3-10 min | Jah | Alati | Madal |

![How Does IaC Work?](https://cdn.servermania.com/images/w_1024,h_494,c_scale/f_webp,q_auto:best/v1744146107/kb/2_351821c347/2_351821c347.png?_i=AA)

### Miks IaC Päriselt Töötab?

**1. Kiirus = Superpower**

Käsitsi: 10 serverit = 1-2 päeva  
Terraform: 10 serverit = 5 minutit

Aga see pole ainult kiirus. See on **võimalus eksperimenteerida**. "Mis juhtub kui teen 100 serverit? Vaatame!" Testi, kustuta, testi uuesti. Käsitsi see oleks hullumeelne.

**2. Korratavus = Clone Magic**

Sama kood = alati sama tulemus.

```hcl
resource "aws_instance" "web" {
  count = 100  # Boom! 100 identset serverit
}
```

Käivita 100 korda → saad 100 identset keskkonda. "Töötab minu masinas" probleem kaob.

Development = täpne koopia production'ist (ainult väiksem).  
Bug ilmneb dev'is? Fiksid dev'is.  
Fix töötab dev'is? Töötab ka production'is.

**3. Versioonihaldus = Time Machine**

Kood elab Git'is:

```bash
git log     # Näed kõike
git blame   # Kes seda muutis?
git revert  # Tagasi minevikku!
```

Keegi kustutas production'i kell 3 öösel?  
Git teab **täpselt** mida tehti. Rollback võtab 2 minutit.

**4. Dokumentatsioon = Self-Updating**

Kood **ON** dokumentatsioon.

Confluence:
```
Viimati uuendatud: 6 kuud tagasi
Autor: lahkunud töötaja
Õigsus: ~40%
```

Terraform fail:
```
Viimati uuendatud: täna (git log)
Autor: sina (git blame)
Õigsus: 100% (muidu ei tööta)
```

**5. Meeskonnatöö = Multiplayer Mode**

```
Käsitsi AWS:
Mängija 1: "Teen serveri..."
Mängija 2: "Ma ka..."
*konflikt*
"KES KUSTUTAS MU SERVERI?!"

Terraform + Git:
Mängija 1: git commit "Add server"
Mängija 2: git commit "Add database"  
git merge
Code review
Kõik õnnelikud
```

Pull request'id infrastruktuurile. Code review enne production'i. Nagu normaalne tarkvaraarendus.

**6. Testimine = Safe Zone**

```
Dev keskkond (test siin)
    ↓
Staging (test veel kord)
    ↓  
Production (100% kindel)
```

Sama kood, erinevad parameetrid:

```hcl
# dev.tfvars
instance_type = "t3.micro"  # odav

# prod.tfvars  
instance_type = "t3.large"  # võimas
```

Kui midagi läheb valesti staging'us → see ei jõua production'ini.

![How Terraform Helps](https://media.geeksforgeeks.org/wp-content/uploads/20241212151316849879/How-does-Terraform-work.webp)

### Pipedrive Success Story

**Enne Terraform (2018):**
- Uus keskkond: 2 päeva
- Dokumentatsioon: Confluence (aegunud)
- Vead: iga keskkond erinev
- Meeskond: stress level 9000+

**Pärast Terraform (2019):**
- Uus keskkond: 10 minutit
- Dokumentatsioon: Git (alati õige)
- Vead: 90% vähem
- Meeskond: chill

**Tulemused:**
- 10x kiirem
- 100,000+ eurot säästu aastas
- Õnnelik DevOps meeskond
- CEO rahul

---

## 2. Mis on Terraform?

Terraform on **infrastruktuuri ehitaja**. Mitte rakenduste installer - **maja ehitaja**.

```
         TERRAFORM
             ↓
Ehitab infrastruktuuri
     ↓           ↓
Serverid     Võrgud
     ↓           ↓  
Andmebaasid  Firewall
```

Loodud: 2014  
Autor: HashiCorp  
Keel: Go  
Litsents: Open-source (tasuta!)  
Kasutajad: AWS, Microsoft, Google, GitLab, Pipedrive, Bolt...

### Analoogia: Maja Ehitamine

| Roll | Tööriist | Mis teeb | Näide |
|------|----------|----------|-------|
| Ehitaja | Terraform | Loob infrastruktuuri | "Tee 10 serverit" |
| Sisekujundaja | Ansible | Installib tarkvara | "Pane Nginx kõigile" |
| Kolija | Kubernetes | Deploy rakendused | "Käivita 50 pod'i" |

**OLULINE:** Terraform ei deploy rakendusi. See loob **koha**, kus rakendus jookseb. Nagu ehitaja ei pane tuppa diivanit - see on sisekujundaja töö.

### Terraform Superpowerid

**1. Multi-Cloud**

Õpid ühes kohas → töötad kõikjal:

```hcl
# AWS
resource "aws_instance" "web" {
  ami           = "ami-12345"
  instance_type = "t3.micro"
}

# Azure (sama loogika!)
resource "azurerm_virtual_machine" "web" {
  name = "web-vm"
  size = "Standard_B1s"
}

# Google Cloud
resource "google_compute_instance" "web" {
  name         = "web-instance"
  machine_type = "f1-micro"
}
```

![Multi-Cloud](https://miro.medium.com/v2/resize:fit:627/1*OiA514LNzKtDij8cSVrKeA.png)

**Miks see on cool?**
- Täna: AWS
- Homme: Azure  
- Sa ei pea õppima uut süsteemi
- Terraform skills on portable

**2. Deklaratiivne**

```
Imperatiivne (Bash):
1. create_server "web1"
2. wait_for_ready  
3. attach_security_group
... (20 sammu)

Deklaratiivne (Terraform):
resource "aws_instance" "web" {
  count = 3
}
# Terraform teab kuidas!
```

**3. Suur Kogukond**

Terraform Registry:
- 3000+ provider'it
- 10,000+ moodulit  
- Aktiivne kogukond
- Hulk tutorial'e

Tõenäoliselt ei pea sa kunagi ise provider'it kirjutama - keegi on seda juba teinud.

### Terraform vs Ansible

See on kõige sagedasem küsimus:

| | Terraform | Ansible |
|---|-----------|---------|
| **Peamine töö** | Loo infrastruktuur | Seadista infrastruktuur |
| **Näide** | "Tee 10 serverit" | "Installi Nginx kõigile" |
| **Keel** | HCL (deklaratiivne) | YAML (imperatiivne) |
| **Kasuta kui** | Vajad uut infrastruktuuri | Seadistad olemasolevat |

**Praktikas koos:**

```
Terraform → loob 10 serverit
    ↓
Ansible → installib Nginx kõigile  
    ↓
Kubernetes → deploy'b rakenduse
```

Wise (TransferWise) kasutab mõlemat. Terraform loob, Ansible seadistab. Koos nad on võimsad.

### Terraform vs CloudFormation

| | Terraform | CloudFormation |
|---|-----------|----------------|
| **Platvormid** | AWS + Azure + GCP + 100+ | Ainult AWS |
| **Süntaks** | HCL (loetav) | JSON/YAML (verbose) |
| **Kogukond** | Suur, multi-cloud | AWS-focused |

**Eesti valik:** 95% ettevõtteid valib Terraform.

Miks? Isegi kui praegu ainult AWS, homme võib-olla Azure. **Paindlikkus > vendor lock-in**.

### Bolt Näide

**Bolt infrastruktuur (2024):**
- 1000+ mikroteenust
- 50+ riiki
- AWS + GCP + Azure

**Ilma Terraform'ita:** Võimatu. Vajaks sadu insenere.

**Terraform'iga:** Väike meeskond haldab kõike. 1 moodul → rakenda kõikjal.

---

## 3. Terraform Arhitektuur

Terraform = 3 komponenti: **Core** (aju), **Providers** (käed), **State** (mälu).

```
      TERRAFORM CORE
           (Aju)
      Loeb faile
      Teeb plaane
           ↓
    ┌──────┴──────┐
    ↓             ↓
PROVIDERS     STATE FILE
  (Käed)        (Mälu)
Räägivad    Mäletab mis
API'dega    on loodud
    ↓
AWS, Azure...
```

### 1. Core = Aju

Core on peaprotsessor. Kirjutatud Go keeles.

**Mis teeb:**
1. Loeb `.tf` faile (sinu kood)
2. Loeb `terraform.tfstate` (mis on olemas)
3. Võrdleb: "mida tahan" vs "mis on"
4. Teeb plaani
5. Täidab plaani
6. Uuendab state'i

**Analoogia:** Ehituse projektijuht.
- Vaatab joonist (config)
- Vaatab ehitust (state)
- Planeerib järgmised sammud

### 2. Providers = Käed

Provider = plugin, mis räägib platvormi API'ga.

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
Core: "Kasutan AWS provider'it"
  ↓
Provider: API call → AWS
  ↓
AWS: "OK! ID: i-12345"
  ↓
Core: Salvestan state'i
```

Provider on tõlk:
- **Sina** räägid HCL't
- **AWS** räägib API't
- **Provider** tõlgib

**Populaarsed:**

| Provider | Ressursse | Kasutus |
|----------|-----------|---------|
| aws | 3000+ | Amazon Web Services |
| azurerm | 2000+ | Microsoft Azure |
| google | 1500+ | Google Cloud |
| docker | 50+ | Containerid |
| kubernetes | 200+ | K8s klastrid |
| local | 5 | Failid (õppimiseks!) |

### 3. State = Mälu

State = `terraform.tfstate` fail. JSON vormingus.

**Näide:**

```json
{
  "version": 4,
  "resources": [
    {
      "type": "aws_instance",
      "name": "web",
      "instances": [{
        "id": "i-1234567890abcdef0",
        "public_ip": "13.51.123.45"
      }]
    }
  ]
}
```

**Miks KRIITILINE:**

```
ILMA State'ita:
Sina: "Tahan 3 serverit"
Terraform: "Loon 3!"
AWS: "Sul on juba 2..."
Terraform: *loob ikka 3*
→ 5 serverit, suur arve, vihane CEO

State'iga:
Sina: "Tahan 3 serverit"  
Terraform: *vaatab state'i*
Terraform: "On 2, loon 1 juurde"
→ 3 serverit, õige arve, õnnelik CEO
```

**State sisaldab:**
- Kõik ressursid
- ID'd
- IP aadressid
- Sõltuvused

**KRIITILINE HOIATUS:**

State võib sisaldada saladusi!

```gitignore
# .gitignore
*.tfstate
*.tfstate.*
.terraform/
```

**ÄRA PANE GIT'I!**

**Õppetund:**

Üks startup kustutas kogemata state'i. 150 serverit AWS'is, keegi ei tea millised. 4 tundi downtime. 20,000 eurot kahju.

**Õppetund:** ALATI backup state!

---

## 4. Deklaratiivne vs Imperatiivne

**Kõige olulisem** kontseptsioon. Mõista seda = mõistad Terraform'i.

### Imperatiivne = KUIDAS

Kirjeldad samme. Täpsed instruktsioonid.

```bash
#!/bin/bash
# Imperatiivne

echo "Samm 1: Security group..."
aws ec2 create-security-group --group-name web-sg

echo "Samm 2: Port 80..."
aws ec2 authorize-security-group-ingress \
  --group-name web-sg --port 80

echo "Samm 3: 5 serverit..."
for i in {1..5}; do
    aws ec2 run-instances --instance-type t3.micro
done
```

**Probleem:**

```bash
# 1. kord:
./script.sh  # 5 serverit ✓

# 2. kord (kogemata):
./script.sh  # 5 VEEL serverit  
# Kokku: 10 serverit, 2x arve
```

Script ei tea mis juba olemas on.

### Deklaratiivne = MIDA

Kirjeldad tulemust. Tööriist väljastab samme.

```hcl
# Deklaratiivne

resource "aws_security_group" "web" {
  name = "web-sg"
  
  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
  }
}

resource "aws_instance" "web" {
  count                  = 5
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.web.id]
}
```

**Maag:**

```bash
terraform apply  # 1. kord: loob 5 ✓
terraform apply  # 2. kord: ei tee midagi ✓
terraform apply  # 100. kord: ikka ei tee midagi ✓
```

Terraform **teab** (tänu state'ile) mis olemas on. **Idempotent!**

### Võrdlus

```
IMPERATIIVNE           DEKLARATIIVNE

create server 1        Desired: 3 servers
     ↓                       ↓
create server 2        Check state
     ↓                   ┌───┴───┐
create server 3      Has 0?  Has 3?
     ↓                   ↓       ↓
Run again?          Create 3  Do nothing
     ↓
Creates 3 MORE!
(total: 6)
```

### Update Stsenaarium

**Olukord:** Sul on 5 serverit. Tahad:
- 7 serverit
- HTTPS (port 443)
- IAM õigus

#### Imperatiivne:

```bash
# Pead ise arvutama
current=$(aws ec2 describe-instances ...)
needed=$((7 - current))

# Loo juurde  
for i in $(seq 1 $needed); do
    aws ec2 run-instances ...
done

# Port (kontrolli kas olemas?)
aws ec2 authorize... || echo "Exists"

# IAM (kontrolli kas...)
aws iam attach... || echo "Exists"
```

Pead:
- Ise arvutama
- Kontrollima
- Error handling
- Käsitsi kirjutama

#### Deklaratiivne:

```hcl
resource "aws_instance" "web" {
  count = 7  # Oli 5, nüüd 7
}

resource "aws_security_group" "web" {
  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
  }
}

resource "aws_iam_user_policy_attachment" "deploy" {
  user       = "deploy"
  policy_arn = "..."
}
```

```bash
terraform plan
# "On 5, peab 7, loon 2"
# "Port 443 puudub, lisan"
# "IAM puudub, lisan"

terraform apply
# *teeb kõik automaatselt*
```

### Faili Puhtus

**Imperatiivne (aja jooksul):**

```bash
# Day 1
create_server 1
create_server 2
...
# Day 3
add_firewall 80
# Day 7  
add_firewall 443
# Day 10
remove_server 1
...
# 200+ rida ajalugu
# Mis praegu olemas? 🤷
```

**Deklaratiivne (alati):**

```hcl
resource "aws_instance" "web" {
  count = 7
}

resource "aws_security_group" "web" {
  # ...
}

# 20 rida
# Näitab PRAEGUST seisu
```

Ajalugu elab Git'is: `git log`

### Tabel

| | Imperatiivne | Deklaratiivne |
|---|--------------|---------------|
| **Kirjeldad** | KUIDAS (sammud) | MIDA (tulemus) |
| **Näide** | "Loo server, siis võrk..." | "Tahan 5 serverit" |
| **Kordamine** | Loob duplikaate | Idempotent |
| **State** | Sina mäletad | Tööriist mäletab |
| **Fail** | Kasvab (200+ rida) | Jääb lühikeseks (20 rida) |

---

## 5. HCL Keel

HCL = HashiCorp Configuration Language. Terraform'i keel.

**Lihtne selgitus:** HCL on nagu JSON, aga loetavam.

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

- `resource` = block type
- `"local_file"` = ressursi tüüp
- `"greeting"` = meie nimi
- `filename`, `content` = argumendid

### Resources

Resource = miski, mida Terraform loob.

**Fail:**

```hcl
resource "local_file" "config" {
  filename        = "app.conf"
  content         = "port=8080"
  file_permission = "0644"
}
```

**AWS server:**

```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345"
  instance_type = "t3.micro"
  
  tags = {
    Name = "WebServer"
    Env  = "Dev"
  }
}
```

### Sõltuvused

Terraform loob automaatselt sõltuvusi.

```hcl
# 1. Security group esmalt
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

```
aws_security_group.web
        ↓
aws_instance.web
```

Terraform teab: "Teen SG enne, siis serveri."

### Variables

```hcl
variable "environment" {
  description = "dev või prod"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Peab olema 'dev' või 'prod'!"
  }
}

resource "aws_instance" "app" {
  instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"
  
  tags = {
    Env = var.environment
  }
}
```

**Kasutamine:**

```bash
terraform apply -var="environment=prod"
```

### Outputs

```hcl
output "server_ip" {
  description = "Serveri IP"
  value       = aws_instance.web.public_ip
}
```

Pärast apply't:

```
Outputs:
server_ip = "13.51.123.45"
```

### Funktsioonid

```hcl
# Faili sisu
content = file("config.json")

# JSON
metadata = jsonencode({
  name = "app"
})

# String template
message = "Tere, ${var.name}!"

# Conditional  
instance_type = var.env == "prod" ? "t3.large" : "t3.micro"
```

---

## 6. Terraform Workflow

4 käsku: init, plan, apply, destroy.

```
┌─────────────┐
│ terraform   │ Valmista ette
│   init      │
└──────┬──────┘
       ↓
┌──────┴──────┐
│ terraform   │ Vaata mis muutub
│   plan      │
└──────┬──────┘
       ↓
┌──────┴──────┐
│ terraform   │ Rakenda
│   apply     │
└──────┬──────┘
       ↓
┌──────┴──────┐
│ terraform   │ Kustuta kõik
│   destroy   │
└─────────────┘
```

### 1. terraform init

Valmistab projekti.

```bash
terraform init
```

**Mis toimub:**
- Laeb provider'id
- Seadistab backend'i
- Init'ib moodulid

**Output:**

```
Initializing provider plugins...
- Finding hashicorp/aws v5.31.0...
- Installing hashicorp/aws v5.31.0...

Terraform has been successfully initialized!
```

**Millal:**
- Esimest korda
- Lisasid provider'i
- Clone'isid repo

### 2. terraform plan

Näitab mis muutub. **EI MUUDA MIDAGI!**

```bash
terraform plan
```

**Sümbolid:**

| Sümbol | Tähendus |
|--------|----------|
| `+` | Luuakse |
| `-` | Kustutatakse |
| `~` | Muudetakse |
| `-/+` | Replace |

**Output:**

```terraform
Terraform will perform the following actions:

  # local_file.greeting will be created
  + resource "local_file" "greeting" {
      + content  = "Tere!"
      + filename = "/tmp/test.txt"
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

**ALATI tee plan enne apply!**

Salvesta plan:

```bash
terraform plan -out=tfplan
terraform apply tfplan
```

### 3. terraform apply

Rakendab **PÄRISELT**.

```bash
terraform apply
```

Küsib kinnitust:

```
Do you want to perform these actions?
  Enter a value: yes
```

**Automaatne (ohtlik!):**

```bash
terraform apply -auto-approve
```

Kasuta ainult kui **100% kindel**!

### 4. terraform destroy

Kustutab **KÕIK**. Pöördumatu!

```bash
terraform destroy
```

**HOIATUS:**
- Pöördumatu
- Kõik kaob
- Andmed kaovad

**Õuduslugu:**

Juunior developer production'is:

```bash
$ terraform destroy
  Enter a value: yes  # ilma mõtlemata

5 min hiljem:
- 150 serverit kadunud
- Kliendid offline
- CEO helistab
- Kahju: ~500,000 eurot
```

**Kuidas vältida:**

```hcl
resource "aws_instance" "web" {
  lifecycle {
    prevent_destroy = true
  }
}
```

---

## Kokkuvõte

### Õppisime

**IaC:** Kood vs käsitsi. 10x kiirem, korratav, dokumenteeritud.

**Terraform:** Multi-cloud provisioning. Deklaratiivne. Suur kogukond.

**Arhitektuur:**
- Core = aju
- Providers = käed  
- State = mälu

**Deklaratiivne:** MIDA vs KUIDAS. Idempotent, turvaline, lihtne.

**HCL:** Resources, variables, outputs, functions.

**Workflow:** init → plan → apply → (destroy)

### Võtmepunktid

**Miks Terraform?**
- Multi-cloud
- Deklaratiivne
- Suur kogukond
- State haldamine

**Kuidas töötab?**
1. Core loeb config + state
2. Teeb plaani
3. Provider täidab
4. Uuendab state'i

**Millal kasutada?**
- Lood infrastruktuuri
- Haldad olemasolevat
- Replitseerid keskkondi
- Tahad koodi kui dokumentatsiooni

### Järgmine Samm

**Labor:** Praktiline töö. Loome päris ressursse.

**Vaja:**
- Terraform
- Teksteditor
- Terminal
- Uudishimu

### Ressursid

**Dokumentatsioon:**
- [Terraform Docs](https://developer.hashicorp.com/terraform/docs)
- [HCL Syntax](https://developer.hashicorp.com/terraform/language/syntax)
- [Registry](https://registry.terraform.io/)

**Õppimine:**
- [HashiCorp Learn](https://developer.hashicorp.com/terraform/tutorials)
- [Best Practices](https://www.terraform-best-practices.com/)

**Kogukond:**
- [Terraform GitHub](https://github.com/hashicorp/terraform)
- DevOps Estonia meetup'id

---

**Eesti DevOps mantra:** "Plan enne Apply't, backup enne Destroy'd, kohv enne debugimist."
