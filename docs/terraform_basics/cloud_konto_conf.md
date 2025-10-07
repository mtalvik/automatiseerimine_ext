# Terraform Cloud Seadistamine

**Eeldused:** Terraform installitud, Git põhiteadmised  
**Platvorm:** AWS, DigitalOcean või GitHub Codespaces

Selles juhendis seadistad cloud platvormi Terraform'i kasutamiseks. Valik platvormi sõltub sellest, kas sul on krediitkaart ning milliseid ressursse vajad.

---

## Cloud Platvormide Võrdlus

| Platvorm | Krediitkaart | Free Tier | Parim Kasutus | Keerukus |
|----------|--------------|-----------|---------------|----------|
| **GitHub Codespaces** | Ei | 60h/kuu | Development, testimine | Väga lihtne |
| **Railway.app** | Ei | $5/kuu | Väikesed API'd, web apps | Lihtne |
| **Render.com** | Ei | 512MB RAM | Web services, PostgreSQL | Lihtne |
| **Fly.io** | Ei | 3 CPU, 256MB | Microservices, low-latency | Keskmine |
| **Azure for Students** | Ei | $100 credit | Microsoft ecosystem | Keskmine |
| **DigitalOcean** | Jah | $200/60 päeva | VPS, Droplets | Keskmine |
| **AWS** | Jah | 12 kuud | Enterprise, õppimine | Keeruline |
| **Google Cloud** | Jah | $300/90 päeva | Big Data, ML | Keeruline |
| **Azure** | Jah | $200/30 päeva | Windows, .NET | Keeruline |
| **Oracle Cloud** | Jah | Always Free | 4 CPU, 24GB RAM | Väga keeruline |

---

## 1. GitHub Student Pack Seadistamine

**Soovitatud õpilastele** - ei vaja krediitkaarti ja annab kõige rohkem tasuta ressursse.

### 1.1 Miks Student Pack?

GitHub Student Pack annab õpilastele juurdepääsu paljudele tasuta tööriistadele:
- DigitalOcean $200 credit (1 aasta)
- Azure $100 credit
- Heroku credits
- JetBrains IDE'd tasuta
- Canva Pro tasuta
- Tasuta domain Name.com'ist

### 1.2 Student Pack Taotlemine

Vajad kooli või ülikooli emaili (lõppeb .edu või .edu.ee) VÕI õpilastunnistust.

Mine https:
- //education.github.com/pack ja logi sisse GitHub'i. Kui kontot pole, loo uus. Vajuta "Get student benefits" ja vali "Student". Sisesta oma kooli email või lae üles õpilastunnistus (foto või PDF). Oota kinnitust
- tavaliselt võtab 1-3 päeva.

**Kontrolli:**```bash
# Kontrolli kas Student Pack aktiivne
# Mine github.com/settings/billing
# Peaks näitama "GitHub Student Developer Pack"```

### 1.3 DigitalOcean Aktiveerimine

Pärast Student Pack kinnitust mine https://www.digitalocean.com ja loo konto. Kasuta sama emaili mis GitHub'is. Mine "Billing" sektsiooni ja vajuta "Promo Code". Sisesta Student Pack promo kood mis said GitHub'ist. Peaksid nägema $200 credit'it oma kontol.

Installi DigitalOcean CLI:```bash
# Linux / macOS / Codespaces
curl -sL https://github.com/digitalocean/doctl/releases/download/v1.98.0/doctl-1.98.0-linux-amd64.tar.gz | tar -xzv
sudo mv doctl /usr/local/bin

# Kontrolli
doctl version```

Loo API token DigitalOcean konsoolil:```bash
# DO konsool → API → Generate New Token
# Name: terraform-labs
# Märgi: Read & Write
# Kopeeri token (näed ainult ühe korra!)

# Autendi CLI
doctl auth init
# Sisesta token

# Testi
doctl account get```

**Validation:**
- [ ] Student Pack aktiivne GitHub'is
- [ ] DigitalOcean konto loodud
- [ ] $200 credit nähtav
- [ ] doctl CLI töötab
- [ ] doctl account get näitab sinu kontot

---

## 2. AWS Konto Seadistamine

AWS on kõige populaarsem cloud platvorm. Vajad krediitkaarti, aga free tier kehtib 12 kuud.

### 2.1 Miks AWS?

AWS on:
- Kõige populaarsem (hea CV jaoks)
- Kõige rohkem õppematerjale
- 12 kuud free tier
- Keerulisem kui teised (aga õppimine tasub ära)

### 2.2 Konto Loomine

Mine https:
- //aws.amazon.com ja vajuta "Create an AWS Account". Sisesta email, konto nimi ja tugev parool. Vali konto tüübiks "Personal". Sisesta krediitkaart info
- AWS teeb $1 test'i mille tagastavad. Kinnita telefon SMS koodiga. Vali support plaan "Basic Support
- Free".

**OLULINE:** Kohe pärast konto loomist seadista MFA (Multi-Factor Authentication) turvalisuse jaoks.

**Validation:**```bash
# Pea saama sisse logida
# Mine https://console.aws.amazon.com
# Näed AWS konsool'i```

### 2.3 IAM Kasutaja Loomine

Root kasutaja on liiga võimas igapäevaseks tööks. Loome turvalisema kasutaja.

Mine AWS konsool'i → IAM → Users ja vajuta "Create user". Sisesta username "terraform-user". Vali access type "Console + Programmatic". Lisa õigused - vali "AdministratorAccess" (labs'ideks OK, produktsioonis kasuta kitsama

id õiguseid). Lae alla credentials CSV fail ja HOIA TURVALISELT.

Loo Access Keys:

Mine IAM → Users → terraform-user → Security credentials → Create access key. Vali "Command Line Interface (CLI)". Kopeeri Access Key ID ja Secret Access Key - näed neid ainult ühe korra.

**Validation:**
- [ ] IAM kasutaja loodud
- [ ] Credentials CSV alla laetud
- [ ] Access keys loodud ja salvestatud

### 2.4 AWS CLI Installimine

Installi AWS CLI oma masinas:```bash
# Linux / macOS / Codespaces
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Windows
# Lae alla MSI: https://awscli.amazonaws.com/AWSCLIV2.msi

# Kontrolli
aws --version```

Seadista credentials:```bash
aws configure
# AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region: eu-west-1
# Default output: json

# Testi
aws sts get-caller-identity```

Peaksid nägema JSON'i oma account ID'ga.

**Validation:**
- [ ] AWS CLI installitud
- [ ] aws configure tehtud
- [ ] aws sts get-caller-identity töötab

---

## 3. GitHub Codespaces Arenduskeskkond

Codespaces on brauseripõhine VS Code - ei vaja kohalikku installatsiooni.

### 3.1 Codespace Loomine

Mine https://github.com ja loo uus repository "terraform-labs". Vajuta "Code" → "Codespaces" → "Create codespace on main". Oota umbes 30 sekundit kuni keskkond valmis. Nüüd on sul VS Code brauseris töötamas.

Kontrolli et tööriistad on olemas:```bash
# Terraform
terraform version
# Peaks näitama: Terraform v1.5.x

# Git
git --version

# Kui AWS CLI pole, installi
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install```

### 3.2 AWS Credentials Codespaces'is

Codespaces'is saad AWS credentials seadistada kahel viisil.

**Variant A - aws configure:**```bash
aws configure
# Sisesta Access Key ID ja Secret```

**Variant B - Käsitsi failid:**```bash
mkdir -p ~/.aws

cat > ~/.aws/credentials << 'EOF'
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
EOF

cat > ~/.aws/config << 'EOF'
[default]
region = eu-west-1
output = json
EOF

# Testi
aws sts get-caller-identity```

**TURVALISUS:**
- Ära pane credentials Git'i
- Ära jaga Codespace'i avalikult
- Credentials kustutatakse codespace'i sulgemisel

**Validation:**
- [ ] Codespace töötab
- [ ] Terraform installitud
- [ ] AWS CLI töötab
- [ ] aws sts get-caller-identity näitab sinu kontot

---

## 4. SSH Key Setup

EC2 instancesse ühendumiseks vajad SSH key'i - see on nagu võti serveri ukse jaoks.

### 4.1 SSH Key Loomine

Loo SSH key paar:```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/terraform-key -N ""

# Kontrolli faile
ls -la ~/.ssh/
# terraform-key       <- Private key (HOIA SALADUSES!)
# terraform-key.pub   <- Public key (läheb AWS'i)```

Seadista õigused:```bash
chmod 600 ~/.ssh/terraform-key
chmod 644 ~/.ssh/terraform-key.pub```

### 4.2 Key Import AWS'i

**Variant A - AWS CLI:**```bash
aws ec2 import-key-pair \
  --key-name "terraform-key" \
  --public-key-material fileb://~/.ssh/terraform-key.pub \
  --region eu-west-1```

**Variant B - AWS Konsool:**

Mine EC2 konsool'i → Key Pairs → Actions → Import key pair. Name "terraform-key". Kopeeri ~/.ssh/terraform-key.pub sisu ja paste. Vajuta "Import".

Kontrolli:```bash
aws ec2 describe-key-pairs --key-names terraform-key```

**Validation:**
- [ ] SSH key paar loodud
- [ ] Private key õigused 600
- [ ] Key AWS'is nähtav

---

## 5. Terraform Projekti Struktuur

### 5.1 Kausta Loomine

Loo projektile kaust ja failid:```bash
mkdir terraform-labs
cd terraform-labs```

### 5.2 .gitignore Loomine

KRIITILISELT OLULINE - ei pane paroole ja võtmeid Git'i:```bash
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
terraform-key
terraform-key.pub

# OS
.DS_Store
Thumbs.db
EOF```

Miks see oluline:
- Ei pane AWS credentials Git'i
- Ei pane SSH võtmeid Git'i
- Ei pane terraform.tfvars Git'i (sisaldab tundlikku infot)
- Ei pane state faile Git'i (võivad sisaldada paroole)

### 5.3 Põhiline Struktuur

Loo failid:```bash
touch main.tf
touch variables.tf
touch outputs.tf
touch terraform.tfvars
touch README.md```

Sinu projekti struktuur peaks välja nägema:```
terraform-labs/
├── .gitignore
├── README.md
├── main.tf
├── variables.tf
├── outputs.tf
└── terraform.tfvars```

**Validation:**
- [ ] Kaust loodud
- [ ] .gitignore on olemas
- [ ] Põhifailid loodud
- [ ] README.md on olemas

---

## 6. Kontrollnimekiri

Enne labori alustamist kontrolli:

**Terraform:**
- [ ] terraform version töötab
- [ ] Näitab versiooni 1.5+

**Cloud Platform (vali üks):**
- [ ] DigitalOcean: doctl account get töötab
- [ ] AWS: aws sts get-caller-identity töötab
- [ ] Codespaces: Codespace töötab ja AWS CLI seadistatud

**SSH:**
- [ ] SSH key paar loodud
- [ ] Private key õigused 600
- [ ] Key AWS'is (kui kasutad AWS'i)

**Projekt:**
- [ ] terraform-labs kaust loodud
- [ ] .gitignore on olemas ja õige
- [ ] Põhifailid loodud

**Turvalisus:**
- [ ] Credentials pole Git'is
- [ ] .gitignore sisaldab *.tfvars
- [ ] SSH private key pole Git'is

---

## Probleemide Lahendamine

### aws command not found```bash
# Installi AWS CLI uuesti
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Lisa PATH'i
export PATH="/usr/local/bin:$PATH"```

### No valid credential sources found```bash
# Kontrolli credentials faili
cat ~/.aws/credentials

# Kui tühi, configure uuesti
aws configure```

### Permission denied publickey```bash
# Kontrolli SSH key õigusi
chmod 600 ~/.ssh/terraform-key

# Kontrolli et key on AWS'is
aws ec2 describe-key-pairs --key-names terraform-key```

### Access Denied AWS'is```bash
# Kontrolli IAM kasutaja õigusi
# AWS konsool → IAM → Users → terraform-user → Permissions
# Peaks olema AdministratorAccess```

---

Valmis alustama Terraform lab'idega!