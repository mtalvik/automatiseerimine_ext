# 📝 Terraform Edasijõudnud Kodutöö: Pilve Infrastruktuur

**Tähtaeg:** Järgmise nädala alguseks  
**Eesmärk:** Luua täielik pilve infrastruktuur Terraform'iga AWS või Azure'is  
**Aeg:** 3-4 tundi  
**Raskusaste:** Keskmine

---

## 🎯 Ülesande kirjeldus

Ehitage täielik pilve infrastruktuur Terraform'iga, mis sisaldab veebiserverit, andmebaasi ja failimajutust. Kasutage workspaces'eid erinevate keskkondade haldamiseks.

---

## 📋 Ülesanded

### 1. Infrastruktuuri Planeerimine (30 min)

**Mida ehitada:**
- VPC või Virtual Network
- Public ja private subnettid
- Internet Gateway või NAT Gateway
- Security Groups või Network Security Groups
- Load Balancer
- Veebiserver (EC2 või Virtual Machine)
- Andmebaas (RDS või Azure Database)
- Failimajutus (S3 või Blob Storage)

**Valige üks:**
- **AWS:** EC2, RDS, S3, Application Load Balancer
- **Azure:** Virtual Machine, Azure Database, Blob Storage, Load Balancer

---

## 🛠️ 2. Terraform Konfiguratsioon (2-3 tundi)

### 2.1 Põhistruktuur

Loo järgmine failide struktuur:
```
terraform_advanced_homework/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── production.tfvars
└── modules/
    ├── networking/
    ├── compute/
    └── database/
```

### 2.2 Nõuded

**Kohustuslikud ressursid:**
- [ ] VPC/Virtual Network
- [ ] Public subnet (veebiserver jaoks)
- [ ] Private subnet (andmebaas jaoks)
- [ ] Internet Gateway/NAT Gateway
- [ ] Security Groups/NSG (port 22, 80, 443)
- [ ] Load Balancer
- [ ] Veebiserver (t2.micro või B1s)
- [ ] Andmebaas (db.t3.micro või Basic)
- [ ] Failimajutus (S3 bucket või Storage Account)

**Täiendavad nõuded:**
- [ ] Kasutage muutujaid (variables.tf)
- [ ] Kasutage outputs'e (outputs.tf)
- [ ] Kasutage workspaces'eid (development, production)
- [ ] Kasutage tags'e kõigile ressurssidele
- [ ] Kasutage user data'd veebiserveri seadistamiseks

---

## 🎯 3. Spetsiifilised Ülesanded

### 3.1 Veebiserver

**Nõuded:**
- Apache või Nginx veebiserver
- Lihtne HTML leht, mis näitab serveri infot
- User data skript, mis seadistab serveri automaatselt
- Public IP või Load Balancer kaudu ligipääsetav

**Näide user data'st:**
```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Server: $(hostname)</h1><p>Environment: ${environment}</p>" > /var/www/html/index.html
```

### 3.2 Andmebaas

**Nõuded:**
- Private subnet'is (mitte public)
- MySQL või PostgreSQL
- Vähemalt 20GB salvestusruumi
- Backup'id lubatud
- Security group, mis lubab ühendust ainult veebiserverist

### 3.3 Failimajutus

**Nõuded:**
- S3 bucket või Storage Account
- Versioning lubatud
- Public read access (kui vaja)
- CORS seadistatud (kui vaja)

---

## 🛠️ 4. Workspaces ja Keskkonnad

### 4.1 Development Keskkond

```hcl
# terraform.tfvars
environment = "development"
instance_type = "t2.micro"
db_instance_class = "db.t3.micro"
```

### 4.2 Production Keskkond

```hcl
# production.tfvars
environment = "production"
instance_type = "t2.small"
db_instance_class = "db.t3.small"
```

### 4.3 Workspace'ide kasutamine

```bash
# Loo workspace'id
terraform workspace new development
terraform workspace new production

# Deploy development
terraform workspace select development
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"

# Deploy production
terraform workspace select production
terraform plan -var-file="production.tfvars"
terraform apply -var-file="production.tfvars"
```

---

## 📊 5. Dokumentatsioon

### 5.1 README.md

Loo README.md fail, mis sisaldab:
- Projekti kirjeldust
- Seadistamise juhendit
- Muutujate kirjeldust
- Deploy'imise juhendit
- Puhastamise juhendit

### 5.2 Arhitektuuridiagramm

Loo lihtne diagramm (tekst või pilt), mis näitab:
- VPC/Virtual Network struktuuri
- Subnet'ide paigutust
- Ressursside vahelisi ühendusi
- Security group'ide reegleid

---

## 🎯 6. Testimine ja Valideerimine

### 6.1 Funktsionaalsuse testid

- [ ] Veebiserver vastab HTTP päringutele
- [ ] Andmebaas on ligipääsetav veebiserverist
- [ ] Failimajutus on ligipääsetav
- [ ] Load Balancer töötab
- [ ] Security group'id blokeerivad ebasobivad ühendused

### 6.2 Terraform testid

```bash
# Valideeri konfiguratsioon
terraform validate

# Vaata planeeritud muudatusi
terraform plan

# Kontrolli state'i
terraform show

# Vaata outputs'e
terraform output
```

---

## 📋 7. Esitamine

### 7.1 GitHub Repository

Loo GitHub repository järgmise struktuuriga:
```
terraform_advanced_homework/
├── README.md
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── production.tfvars
├── modules/
│   ├── networking/
│   ├── compute/
│   └── database/
└── docs/
    └── architecture.md
```

### 7.2 Esitamise nõuded

- [ ] Kõik failid on GitHub'is
- [ ] README.md on täielik ja selge
- [ ] Kood on kommenteeritud
- [ ] Arhitektuuridiagramm on lisatud
- [ ] Deploy'imise juhend on töötav

---

## 🎯 8. Hindamiskriteeriumid

### Funktsionaalsus (40 punkti)
- [ ] Kõik ressursid on loodud (10p)
- [ ] Veebiserver töötab (10p)
- [ ] Andmebaas on ligipääsetav (10p)
- [ ] Failimajutus töötab (10p)

### Koodikvaliteet (30 punkti)
- [ ] Muutujad on kasutatud (10p)
- [ ] Outputs on määratletud (5p)
- [ ] Tags on kasutatud (5p)
- [ ] Kood on kommenteeritud (10p)

### Workspaces (20 punkti)
- [ ] Development workspace töötab (10p)
- [ ] Production workspace töötab (10p)

### Dokumentatsioon (10 punkti)
- [ ] README.md on täielik (5p)
- [ ] Arhitektuuridiagramm on olemas (5p)

---

## 🆘 Abi ja Näited

### Kasulikud lingid:
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Terraform Workspaces](https://www.terraform.io/docs/language/state/workspaces.html)

### Näidisressursid:
- [AWS EC2](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance)
- [AWS RDS](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance)
- [AWS S3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket)

---

## 🎯 Edu kodutöö tegemisel!

**Märkus:** Ärge unustage kustutada ressursid pärast kodutöö lõpetamist, et vältida kulusid!

```bash
terraform destroy
```
