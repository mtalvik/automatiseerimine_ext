# Terraform ja Cloud Platvormid: Konto Seadistamise Juhend

**Eeldused:** Selles juhendis käsitleme, kuidas seadistada erinevaid cloud platvorme Terraform'i kasutamiseks. Valik platvormi sõltub sellest, kas sul on krediitkaart ning milliseid ressursse vajad.

---

## Ülevaade: Cloud Platvormide Võrdlus

| Platvorm | Krediitkaart | Free Tier | Parim Kasutus | Keerukus |
|----------|--------------|-----------|---------------|----------|
| **GitHub Codespaces** | ❌ Ei | 60h/kuu | Development, testimine | ⭐ Väga lihtne |
| **Railway.app** | ❌ Ei | $5/kuu | Väikesed API'd, web apps | ⭐ Lihtne |
| **Render.com** | ❌ Ei | 512MB RAM | Web services, PostgreSQL | ⭐ Lihtne |
| **Fly.io** | ❌ Ei | 3 CPU, 256MB | Microservices, low-latency | ⭐⭐ Keskmine |
| **Azure for Students** | ❌ Ei | $100 credit | Microsoft ecosystem | ⭐⭐ Keskmine |
| **DigitalOcean** | ✅ Jah | $200/60 päeva | VPS, Droplets | ⭐⭐ Keskmine |
| **AWS** | ✅ Jah | 12 kuud | Enterprise, õppimine | ⭐⭐⭐ Keeruline |
| **Google Cloud** | ✅ Jah | $300/90 päeva | Big Data, ML | ⭐⭐⭐ Keeruline |
| **Azure** | ✅ Jah | $200/30 päeva | Windows, .NET | ⭐⭐⭐ Keeruline |
| **Oracle Cloud** | ✅ Jah | Always Free | 4 CPU, 24GB RAM | ⭐⭐⭐ Väga keeruline |

---

## Variant 1: GitHub Student Pack (SOOVITATUD ÕPILASTELE!)

**Miks see variant?**
- ❌ Krediitkaart pole vaja
- 🎁 Kõige rohkem tasuta ressursse
- 🎓 Spetsiaalselt õpilastele
- 💰 DigitalOcean $200 + Azure $100 + palju muud

### Samm 1: GitHub Student Pack taotlemine

**Nõuded:**
- Kool/ülikooli email (.edu või .edu.ee)
- VÕI õpilastunnistus/isikutunnistus

**Taotlus:**

1. Mine [education.github.com/pack](https://education.github.com/pack)
2. Logi sisse GitHub'i (loo konto, kui pole)
3. Vajuta "Get student benefits"
4. Vali "Student"
5. Sisesta kooli email
6. Kui kooli emaili pole, lae üles õpilastunnistus
7. Oota kinnitust (tavaliselt 1-3 päeva)

**Mida saad:**

| Teenus | Väärtus | Kasutus |
|--------|---------|---------|
| **DigitalOcean** | $200 credit / 1 aasta | VPS, Terraform labs |
| **Azure** | $100 credit | Cloud services, Windows |
| **Heroku** | Credits | Web app hosting |
| **Name.com** | Tasuta domain | DNS, veebileht |
| **JetBrains** | IDE'd tasuta | Development |
| **Canva** | Pro tasuta | Design |

### Samm 2: DigitalOcean aktiveerimine (Student Pack kaudu)

**Pärast Student Pack kinnitust:**

1. Mine [digitalocean.com](https://www.digitalocean.com)
2. Loo konto (kasuta sama emaili mis GitHub'is)
3. Logi sisse
4. Mine "Billing" → "Promo Code"
5. Sisesta Student Pack promo kood (saad GitHub'ist)
6. Vajuta "Apply"
7. Näed $200 credit'it!

**DigitalOcean CLI installimine:**

```bash
# Linux / macOS / Codespaces
curl -sL https://github.com/digitalocean/doctl/releases/download/v1.98.0/doctl-1.98.0-linux-amd64.tar.gz | tar -xzv
sudo mv doctl /usr/local/bin

# Kontrolli
doctl version
```

**DigitalOcean autentimine:**

```bash
# Loo API token
# Mine DO konsool → API → Generate New Token
# Name: terraform-labs
# Märgi: Read & Write
# Kopeeri token (näed ainult ühe korra!)

# Autendi
doctl auth init
# Sisesta token

# Testi
doctl account get
```

---

## Variant 2: AWS Setup (Krediitkaart vajalik)

**Miks AWS?**
- 🏢 Kõige populaarsem (CV jaoks hea)
- 📚 Kõige rohkem õppematerjale
- 🌍 12 kuud free tier
- ⚠️ Keerulisem kui teised

### AWS Konto Loomine

**Samm-sammult:**

| Samm | Tegevus | Detail |
|------|---------|--------|
| 1 | Mine [aws.amazon.com](https://aws.amazon.com) | Vajuta "Create an AWS Account" |
| 2 | Email ja nimi | Email, konto nimi, tugev parool |
| 3 | Konto tüüp | Vali "Personal" |
| 4 | Makseinfo | Krediitkaart (teevad $1 testi) |
| 5 | Telefon | SMS kinnituskood |
| 6 | Support | Vali "Basic Support - Free" |

**OLULINE:** Pärast konto loomist seadista MFA (Multi-Factor Authentication)!

### IAM Kasutaja Loomine

**Miks mitte root kasutajat?**
Root kasutaja on nagu "admin" - liiga võimas igapäevaseks tööks. Loome turvalisema kasutaja.

**IAM kasutaja:**

| Samm | Tegevus | Seaded |
|------|---------|--------|
| 1 | AWS konsool → IAM → Users | "Create user" |
| 2 | Username | `terraform-user` |
| 3 | Access type | Console + Programmatic |
| 4 | Permissions | `AdministratorAccess` (labs'ideks OK) |
| 5 | Download credentials | CSV fail - HOIA TURVALISELT! |

**Access Keys loomine:**

```bash
# AWS konsool → IAM → Users → terraform-user
# Security credentials tab → Create access key
# Vali "Command Line Interface (CLI)"
# Kopeeri:
# - Access Key ID: AKIAIOSFODNN7EXAMPLE
# - Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### AWS CLI Installimine ja Seadistamine

**Installimine:**

| OS | Käsk |
|----|------|
| **Linux/macOS/Codespaces** | `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install` |
| **Windows** | Lae alla [AWS CLI MSI](https://awscli.amazonaws.com/AWSCLIV2.msi) |

**Seadistamine:**

```bash
# Configure
aws configure

# Sisesta:
# AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region: eu-west-1
# Default output: json

# Testi
aws sts get-caller-identity
```

**Oodatav väljund:**
```json
{
    "UserId": "AIDAI...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/terraform-user"
}
```

---

## Variant 3: GitHub Codespaces (Arenduskeskkond)

**Miks Codespaces?**
- ❌ Krediitkaart pole vaja
- 💻 VS Code brauseris
- 🎁 60 tundi kuus tasuta
- ⚡ Terraform ja Git juba installitud

### Codespace Loomine

**Kiire start:**

| Samm | Tegevus |
|------|---------|
| 1 | Mine [github.com](https://github.com) |
| 2 | Loo repo: `terraform-labs` |
| 3 | Vajuta "Code" → "Codespaces" |
| 4 | "Create codespace on main" |
| 5 | Oota 30 sek... Valmis! |

**Kontrolli tööriistu:**

```bash
# Terraform
terraform version
# Terraform v1.5.x ✓

# Git
git --version
# git version 2.x.x ✓

# Kui AWS CLI pole
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### AWS Credentials Codespaces'is

**Variant A: aws configure**

```bash
aws configure
# Sisesta Access Key ID ja Secret
```

**Variant B: Käsitsi failid**

```bash
# Loo AWS konfiguratsiooni kaustad
mkdir -p ~/.aws

# Credentials fail
cat > ~/.aws/credentials << 'EOF'
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
EOF

# Config fail
cat > ~/.aws/config << 'EOF'
[default]
region = eu-west-1
output = json
EOF

# Testi
aws sts get-caller-identity
```

**TURVALISUS:**
- ⚠️ Ära pane credentials Git'i!
- ⚠️ Ära jaga Codespace'i avalikult!
- ✅ Credentials kustutatakse codespace'i sulgemisel

---

## SSH Key Setup (EC2 jaoks)

**Miks vaja?**
EC2 instancesse ühendumiseks vajad SSH key'i. See on nagu "võti serveri ukse jaoks".

### SSH Key Loomine

**Kohalik arvuti või Codespaces:**

```bash
# Loo SSH key paar
ssh-keygen -t rsa -b 4096 -f ~/.ssh/terraform-key -N ""

# Kontrolli faile
ls -la ~/.ssh/
# terraform-key       <- Private key (HOIA SALADUSES!)
# terraform-key.pub   <- Public key (läheb AWS'i)
```

**Faili õigused (Linux/macOS):**

```bash
chmod 600 ~/.ssh/terraform-key
chmod 644 ~/.ssh/terraform-key.pub
```

### Key Import AWS'i

**Variant A: AWS CLI**

```bash
aws ec2 import-key-pair \
  --key-name "terraform-key" \
  --public-key-material fileb://~/.ssh/terraform-key.pub \
  --region eu-west-1
```

**Variant B: AWS Konsool**

| Samm | Tegevus |
|------|---------|
| 1 | Mine EC2 → Key Pairs |
| 2 | "Actions" → "Import key pair" |
| 3 | Name: `terraform-key` |
| 4 | Kopeeri `~/.ssh/terraform-key.pub` sisu |
| 5 | Paste ja "Import" |

**Kontrolli:**

```bash
aws ec2 describe-key-pairs --key-names terraform-key
```

---

## Terraform Projekti Struktuur

### Põhiline Kausta Struktuur

```
terraform-labs/
├── .gitignore              # Mida EI pane Git'i
├── README.md               # Projekti kirjeldus
├── backend.tf              # Remote state konfiguratsioon
├── main.tf                 # Põhiline infrastruktuur
├── variables.tf            # Muutujad
├── outputs.tf              # Väljundid
├── terraform.tfvars        # Muutujate väärtused (SECRET!)
└── modules/                # Taaskasutatavad moodulid
    ├── networking/
    ├── compute/
    └── database/
```

### .gitignore (KRIITILISELT OLULINE!)

```bash
cat > .gitignore << 'EOF'
# Terraform
.terraform/
*.tfstate
*.tfstate.*
.terraform.lock.hcl

# Secrets
terraform.tfvars
*.auto.tfvars
*.tfvars.json

# AWS
.aws/
*.pem

# SSH keys
*.pem
id_rsa
id_rsa.pub
terraform-key
terraform-key.pub

# OS
.DS_Store
Thumbs.db
EOF
```

**Miks see oluline?**
- 🔒 Ei pane paroole Git'i
- 🔒 Ei pane AWS credentials Git'i
- 🔒 Ei pane SSH võtmeid Git'i
- 🔒 Ei pane state faile Git'i (võivad sisaldada paroole)

---

## Kiire Kontroll: Kas Kõik Valmis?

| Kontrollpunkt | Käsk | Oodatav Tulemus |
|---------------|------|-----------------|
| **Terraform installitud** | `terraform version` | `Terraform v1.x.x` |
| **AWS CLI installitud** | `aws --version` | `aws-cli/2.x.x` |
| **AWS credentials** | `aws sts get-caller-identity` | Näitab sinu Account ID |
| **AWS regioon** | `aws configure get region` | `eu-west-1` või muu |
| **SSH key** | `ls ~/.ssh/terraform-key` | Fail eksisteerib |
| **SSH key AWS'is** | `aws ec2 describe-key-pairs` | Näitab key nime |
| **.gitignore** | `cat .gitignore` | Sisaldab `.terraform/` jne |

**Kui kõik ✅, oled valmis Terraform labs'ideks!**

---

## Järgmised Sammud

Nüüd kui keskkond on seadistatud, saad alustada harjutustega:

1. **Remote State ja Locking** - S3 + DynamoDB setup
2. **Data Sources** - Olemasolevate ressursside kasutamine
3. **Zero-Downtime Updates** - Lifecycle rules

**Vali oma variant:**

| Kui sul on... | Kasuta... | Harjutus |
|---------------|-----------|----------|
| GitHub Student Pack | DigitalOcean | Lihtsamad labs'id |
| Krediitkaart + huvi AWS vastu | AWS | Kõik 3 harjutust |
| Ainult Codespaces | Lokaalse failisüsteemi | Terraform põhitõed |

---

## Probleemide Lahendamine

### "aws: command not found"

```bash
# Installi AWS CLI uuesti
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Lisa PATH'i (Codespaces)
export PATH="/usr/local/bin:$PATH"
```

### "Error: No valid credential sources found"

```bash
# Kontrolli credentials faili
cat ~/.aws/credentials

# Kui tühi, configure uuesti
aws configure
```

### "Permission denied (publickey)"

```bash
# Kontrolli SSH key õigusi
chmod 600 ~/.ssh/terraform-key

# Kontrolli, et key on AWS'is
aws ec2 describe-key-pairs --key-names terraform-key
```

### "Access Denied" AWS'is

```bash
# Kontrolli IAM kasutaja õigusi
# AWS konsool → IAM → Users → terraform-user → Permissions
# Peaks olema AdministratorAccess või EC2FullAccess
```

**Valmis alustama? Lähme harjutuste juurde! 🚀**