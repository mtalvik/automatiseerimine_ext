# Terraform Edasijõudnud: Pilve Infrastruktuur

**Eeldused:** Terraform põhitõed (resources, variables, state), Linux CLI, Git alused

**Platvorm:** AWS või Azure (pilve konto vajalik)

## Õpiväljundid

Pärast seda moodulit õpilane:

- Selgitab pilve provider'ite (AWS/Azure) tööpõhimõtteid ja eripära
- Loob VPC/Virtual Network infrastruktuuri võrgu isolatsiooniga
- Kasutab Terraform workspaces'eid keskkonnahalduseks (dev/prod)
- Rakendab remote state'i ja state locking'ut meeskonnatöös
- Kirjutab taaskasutatavaid Terraform module'eid

---

## 1. Pilve Providerid ja Ressursid

Terraform põhikursuses õppisime lokaalseid ressursse - faile, skripte, konfiguratsioone. Aga Terraform'i tegelik võimsus ilmneb siis, kui hakkame haldama pilve infrastruktuuri. Siin ei ole enam tegemist failide loomisega oma arvutis, vaid tõeliste serverite, võrkude ja andmebaaside loomisega AWS'is või Azure'is.

### Miks pilv ja miks Terraform?

Pilve infrastruktuur erineb põhimõtteliselt füüsilisest. Kui varem tähendas uue serveri saamine IT-osakonnas tellimuse tegemist, nädalaid ootamist ja seejärel mehhaanilise masina riiulisse paigaldamist, siis pilveteenustes võtab sama asi 30 sekundit. Aga see kiirus toob kaasa uue probleemi: kuidas hallata sadu või tuhandeid ressursse, mis võivad tekkida ja kaduda igal hetkel?

Käsitsi pilve konsoolist klikkimine on sama vale kui käsitsi serverite seadistamine. Esiteks, see ei ole korduvkasutatav - kui peate looma samasuguse keskkonna uuesti, peate meelde tuletama kõik sammud. Teiseks, see ei ole dokumenteeritud - kuus kuud hiljem ei tea keegi enam, miks mingi security group täpselt sellise reegli sai. Kolmandaks, see ei ole testitud - ei saa kindel olla, et tootmis- ja arenduskeskkond on identne.

Terraform lahendab need probleemid Infrastructure as Code lähenemisega. Kirjutate üks kord, kuidas infrastruktuur peaks välja nägema, ja Terraform loob selle alati täpselt samasugusena. Kood on dokumentatsioon, kood on test, kood on tõde.

### AWS Provider põhitõed

AWS (Amazon Web Services) on maailma suurim pilveteenuste pakkuja. Terraform suhtleb AWS'iga läbi API'de, kasutades AWS provider'it. Provider on justkui tõlk Terraform'i ja AWS'i vahel - Terraform ütleb "tahan serverit", provider tõlgib selle AWS API päringuteks.

AWS provideril on kaks olulist aspekti. Esiteks, autentimine. Terraform peab teadma, kellena ta AWS'i sisse logib. Selleks kasutatakse AWS credentials'eid - access key ja secret key, mis antakse Terraform'ile kas keskkonna muutujate või konfiguratsioonifaili kaudu. Turvakaalutlustel ei tohiks neid võtmeid kunagi kirjutada otse Terraform koodisse.

Teiseks, regioonid. AWS'il on kogu maailmas datacentrid, mida nimetatakse regioonideks - us-east-1 (Virginia), eu-west-1 (Iirimaa), ap-southeast-1 (Singapur) jne. Iga ressurss luuakse konkreetsesse regiooni ja need ei ole omavahel automaatselt ühendatud. Regiooni valik mõjutab nii latentsust (kui kiiresti kasutajad serverile ligi pääsevad) kui ka kulusid (eri regioonides on erinevad hinnad).
```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
  # Credentials tuleb anda AWS CLI kaudu või keskkonnamuutujatega
  # MITTE kunagi otse koodi!
}
```

### Azure Provider iseärasused

Azure erineb AWS'ist arhitektuuri poolest. Kui AWS'is luuakse ressursid otse, siis Azure nõuab alati ressursigrupi olemasolu. Ressursigrupp on loogiline konteiner, mis grupeerib seotud ressursse kokku. See võib tunduda algul tüütu lisasamm, aga tegelikult aitab see paremini organiseerida ja hallata suuri projekte.

Azure'i autentimine on samuti erinev. Kui AWS kasutab lihtsalt võtmepaari, siis Azure kasutab Service Principal'eid, mis on põhimõtteliselt robotkasutajad. Service Principal'il on tenant ID (mis Azure Active Directory'ga ühendatakse), subscription ID (mis maksmise konto määrab) ja client ID koos client secret'iga (mis autentimiseks).
```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
  
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  # Client credentials tuleks anda keskkonnamuutujatega
}

resource "azurerm_resource_group" "main" {
  name     = "terraform-rg"
  location = "West Europe"
}
```

### Võrgu põhikontseptsioonid pilves

Nii AWS kui Azure kasutavad virtuaalseid võrke (Virtual Private Cloud või Virtual Network), mis on isoleeritud võrgukeskkonnad pilves. Need võimaldavad luua võrguarhitektuuri, mis sarnaneb füüsilise datacentri omale, aga kõik on tarkvaraliselt defineeritud.

Virtuaalse võrgu põhielement on CIDR block - IP-aadresside vahemik, mida see võrk kasutab. Näiteks 10.0.0.0/16 tähendab, et võrgul on kasutada IP-aadressid 10.0.0.0 kuni 10.0.255.255 - kokku 65,536 aadressi. See vahemik tuleb valida nii, et see ei kattuks teiste võrkudega, millega hiljem võib vaja olla ühendust luua.

Võrk jagatakse subnet'ideks - alamvõrkudeks, mis on väiksemad IP vahemikud. Subnet'id võivad olla public (ligipääsetav internetist) või private (ligipääsetav ainult seesmiselt). Public subnet'is olevad ressursid saavad otse internetiga suhelda, private subnet'is olevad peavad kasutama NAT Gateway'd või muid vahendusservereid.
```hcl
# AWS VPC näide
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "eu-west-1a"
  
  tags = {
    Name = "public-subnet"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-west-1a"
  
  tags = {
    Name = "private-subnet"
    Type = "private"
  }
}
```

Igal ressursil on ID, mida saab kasutada teistes ressurssides viitamiseks. Siin on oluline mõista Terraform'i dependency graafi - Terraform teab, et subnet sõltub VPC'st, sest kasutab `aws_vpc.main.id` viitamist. See tähendab, et Terraform loob alati VPC enne subnet'e.

## 2. Security Groups ja Võrguturve

Pilves ei ole füüsilisi firewalle, mida saaks riiulisse panna. Kogu võrguturve on tarkvaraline ja realiseeritud security groupide ja network ACL'ide kaudu. Need määravad, milline liiklus võib ressursside juurde jõuda ja milline mitte.

### Security Groupide loogikaecurity Groups on stateful firewall'id, mis kontrollivad sissetulevat (ingress) ja väljaminevat (egress) liiklust. Stateful tähendab, et kui lubate sissetuleva liikluse mingilt portilt, siis vastus sellele lubatakse automaatselt välja - ei pea eraldi väljaminevat reeglit looma.

Näiteks kui loote veebiserveri, vajate tavaliselt kolme asja: SSH ligipääs (port 22), et saaksite serverisse sisse logida ja seda seadistada; HTTP ligipääs (port 80), et kasutajad saaksid veebilehte vaadata; ja HTTPS ligipääs (port 443) turvaliseks ühenduseks. Kõik muu liiklus blokeeritakse vaikimisi.

Oluline on mõista, et security group'id pole seotud ühe konkreetse ressursiga, vaid neid saab rakendada mitmele ressursile. Kui teil on viis veebiserveri, võivad kõik kasutada sama security group'i. See teeb haldamise lihtsamaks - kui peate muutma firewall reegleid, muudate ühes kohas ja mõjutab kõiki.
```hcl
resource "aws_security_group" "web" {
  name_prefix = "web-"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id
  
  # Sisse: HTTP
  ingress {
    description = "HTTP from internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Sisse: HTTPS
  ingress {
    description = "HTTPS from internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Sisse: SSH (ainult teie IP'st!)
  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["85.253.123.45/32"]  # Asenda oma IP'ga!
  }
  
  # Välja: kõik
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "web-security-group"
  }
}
```

CIDR notatsioonis `/32` tähendab täpselt ühte IP-aadressi, `/0` tähendab kõiki IP-aadresse. Port 0 ja protokoll "-1" tähendavad kõiki porte ja protokolle. Seega egress reegel ülalpool ütleb: "luba välja kõik".

### Network ACL'id ja kaitsekihid

Network ACL (Access Control List) on teine turvakiht, mis töötab subnet tasemel. Kui security group'id on ressursi tasemel ja stateful, siis NACL'id on subnet tasemel ja stateless. Stateless tähendab, et peate eraldi defineerima nii sissetulevad kui väljaminevad reeglid, isegi vastustele.

Enamasti piisab security groupidest ja NACL'e ei ole vaja kohe alguses konfigureerida - vaikimisi lubavad need kõike. Aga suuremas organisatsioonis või rangema turvalisusega projektides on NACL'id oluline lisaturvakiht. Neid kasutatakse tavaliselt subnet taseme blokeerimiseks - näiteks kui soovite blokeerida kogu liikluse teatud IP vahemikust.

## 3. Workspaces ja Keskkonnahaldus

Reaalsetes projektides ei ole kunagi ainult üks keskkond. Teil on vähemalt development (arendus), staging (testimine) ja production (toodang). Iga keskkond peaks olema eraldatud, aga samas peaks neil olema sama konfiguratsioon - muidu ei ole testimine usaldusväärne.

### Workspaces'ide kontseptsioon

Terraform workspaces lahendavad selle probleemi. Workspace on eraldi state fail samale konfiguratsioonile. Igal workspace'il on oma state, aga nad jagavad sama Terraform koodi. See tähendab, et saate kirjutada konfiguratsiooni üks kord ja luua sellest mitu eraldatud instantsi.

Kui käivitate `terraform workspace new development`, loob Terraform uue state faili nimega `terraform.tfstate.d/development/terraform.tfstate`. Kui käivitate `terraform workspace new production`, luuakse eraldi state fail `terraform.tfstate.d/production/terraform.tfstate`. Need kaks state faili on täiesti eraldatud - ressursid ühes ei mõjuta teist.
```bash
# Loo uus workspace
terraform workspace new development
terraform workspace new staging
terraform workspace new production

# Vaata kõiki workspace'e
terraform workspace list

# Vaheta workspace'i
terraform workspace select development

# Vaata praegust workspace'i
terraform workspace show
```

### Keskkonna-spetsiifilised konfiguratsioonid

Kuigi kood on sama, peavad keskkonnad erinema. Production vajab võimsamaid servereid kui development. Production vajab backup'e, development ei pruugi. Production on mitmes availability zone's, development võib olla ühes.

Neid erinevusi hallatakse muutujate kaudu. Võite luua eraldi `.tfvars` faile igale keskkonnale või kasutada `terraform.workspace` built-in muutujat, et koodis vahet teha.
```hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
}

variable "instance_size" {
  description = "Server size per environment"
  type        = map(string)
  default = {
    development = "t3.micro"
    staging     = "t3.small"
    production  = "t3.medium"
  }
}

variable "enable_backups" {
  description = "Enable automated backups"
  type        = map(bool)
  default = {
    development = false
    staging     = false
    production  = true
  }
}

# main.tf
resource "aws_instance" "app" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.instance_size[terraform.workspace]
  
  tags = {
    Name        = "app-server-${terraform.workspace}"
    Environment = terraform.workspace
  }
}

resource "aws_db_instance" "postgres" {
  count = var.enable_backups[terraform.workspace] ? 1 : 0
  
  allocated_storage    = 20
  engine              = "postgres"
  instance_class      = "db.t3.micro"
  backup_retention_period = 7
}
```

Siin kasutatakse mitut tehnikat. `var.instance_size[terraform.workspace]` valib map'ist õige võtme workspace nime järgi. `count` kasutamine conditionally ressursi loomiseks - kui `enable_backups` on false, siis `count = 0` ja ressurssi ei looda üldse.

### Deployment strateegia workspaces'iga

Tüüpiline deployment workflow workspace'idega näeb välja nii: arendaja teeb muudatuse koodis development workspace'is ja testib seda. Kui töötab, mergeeb ta koodi main branchi ja CI/CD süsteem deploy'ib automaatselt staging workspace'i. Pärast testimist staging'us saab käsitsi deploy'ida production workspace'i.
```bash
# Development deployment
terraform workspace select development
terraform plan -var="environment=development"
terraform apply -var="environment=development"

# Production deployment (käsitsi)
terraform workspace select production
terraform plan -var="environment=production"
# Kontrolli plaani põhjalikult!
terraform apply -var="environment=production"
```

Oluline on mõista, et workspaces ei asenda proper keskkondade eraldamist. Production peaks ikka olema eraldi AWS accountis või Azure subscription'is. Workspaces on hea dev ja staging jaoks samas accountis, aga production vajab täielikku eraldamist.

## 4. Remote State ja Meeskonnatöö

Kohalik state fail töötab üksikule arendajale, aga meeskonnas on see katastroof. Kui kaks inimest teevad samaaegselt muudatusi ja kumbki kasutab oma local state faili, tekib kiiresti olukord, kus keegi ei tea enam, mis tegelikult pilves eksisteerib.

### Remote backend'i vajadus

Remote state tähendab, et state fail ei ole enam teie arvutis, vaid kusagil kesksel serveris - tavaliselt S3 bucket'is (AWS) või Azure Blob Storage'is. Nüüd kõik meeskonnaliikmed loevad ja kirjutavad sama state faili. Kui keegi teeb muudatuse, näevad teised seda kohe.

Aga see toob uue probleemi: mis juhtub kui kaks inimest proovivad samaaegselt `terraform apply` käivitada? Võivad tekkida konfliktsed muudatused või pool-lõpetatud operatsioonid. Siin tuleb appi state locking.

State locking lukustab state faili operatsiooni ajaks. Kui üks inimene käivitab `terraform apply`, pane Terraform lukku state faili. Kui teine inimene proovib samaaegselt, näeb ta viga: "State locked by user X". Pärast esimese operatsiooni lõppu võetakse lukk maha ja teine saab jätkata.

### S3 backend konfiguratsioon

AWS'is kasutatakse state'i jaoks S3 bucket'it ja locking'uks DynamoDB tabelit. S3 on objekt storage - ideaalne failide hoidmiseks. DynamoDB on NoSQL andmebaas - kiire võtme-väärtus paar'ide hoidmiseks, ideaalne lock'ide jaoks.
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# State bucket'i loomine (tehke see eraldi enne!)
resource "aws_s3_bucket" "terraform_state" {
  bucket = "mycompany-terraform-state"
  
  lifecycle {
    prevent_destroy = true  # Ei lase kogemata kustutada!
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  versioning_configuration {
    status = "Enabled"  # Versioonihaldus - saab tagasi võtta!
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"  # Krüpteeritud!
    }
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
}
```

Pange tähele `prevent_destroy` lifecycle reeglit. See on turvamehhanism, mis takistab state bucket'i kogemata kustutamist. State fail on teie infrastruktuuri ainuke tõeallikas - kui see kaob, ei tea Terraform enam, mis pilves eksisteerib.

Versioning lubamine on samuti kriitiline. Kui keegi teeb vea ja state fail corrups, saate alati tagasi võtta eelmise versiooni. S3 hoiab kõiki vanu versioone.

### State'i migratsioon

Kui olete alustanud kohaliku state'iga ja nüüd soovite remote state'i kasutada, peate state'i migreerima. Terraform teeb selle lihtsamaks `terraform init -migrate-state` käsuga.
```bash
# 1. Lisa backend konfiguratsioon
# (backend.tf fail ülalpool)

# 2. Initsiiseeri uuesti ja migreeri
terraform init -migrate-state

# Terraform küsib kinnitust ja kopeerib state'i S3'i
# Kohalik fail jääb alles backup'ina
```

Pärast migratsiooni võite kohaliku state faili kustutada, aga hoidke see esialgu alles turvakoopiana. Kui remote state on töökorras, siis enam ei pea sellest muretsema.

## 5. Terraform Modules

Modules on Terraform'i võimsaim feature korduvkasutatavas koodis. Module on nagu funktsioon programmeerimises - võtab sisendid (variables), teeb midagi (creates resources), ja tagastab väljundid (outputs).

### Miks modules on vajalikud

Kujutage ette, et teil on 10 erinevat projekti ja igaüks vajab VPC'd koos subnet'ide, internet gateway, route table'ite jms. Kas kirjutate selle koodi 10 korda? Kui peate hiljem midagi muutma, muudate 10 kohas?

Module võimaldab kirjutada VPC konfiguratsioon üks kord ja kasutada seda 10 projektis. Kui peate muutma, muudate ühes kohas ja kõik projektid saavad uuenduse.
```
project/
├── modules/
│   └── vpc/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── main.tf
```

VPC module võiks näha välja selline:
```hcl
# modules/vpc/variables.tf
variable "name" {
  description = "Name prefix for VPC resources"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
}

variable "azs" {
  description = "Availability zones"
  type        = list(string)
}

# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.name}-vpc"
  }
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.azs[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.name}-public-${count.index + 1}"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.name}-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${var.name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# modules/vpc/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}
```

### Module'i kasutamine

Nüüd saate seda module'it kasutada erinevates projektides:
```hcl
# main.tf
module "vpc" {
  source = "./modules/vpc"
  
  name                = "myapp"
  cidr_block         = "10.0.0.0/16"
  public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
  azs                = ["eu-west-1a", "eu-west-1b"]
}

# Kasuta module'i outpute teistes ressurssides
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  subnet_id     = module.vpc.public_subnet_ids[0]
  
  tags = {
    Name = "web-server"
  }
}
```

Module outputs on ligipääsetavad `module.<name>.<output>` kaudu. Terraform teab, et `aws_instance.web` sõltub `module.vpc`'st, sest kasutab selle outputi. Seega loob Terraform alati VPC enne serveri loomist.

### Public modules Terraform Registry'st

Te ei pea isegi ise module'eid kirjutama - Terraform Registry sisaldab tuhandeid valmis module'eid. Need on community poolt testitud ja kasutusel paljudes ettevõtetes.
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "myapp-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["eu-west-1a", "eu-west-1b"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.11.0/24", "10.0.12.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = {
    Environment = "dev"
  }
}
```

Versioning on oluline - `version = "5.0.0"` tagab, et saate alati sama module'i versiooni. Kui module uueneb, ei muutu teie infrastruktuur ootamatult.

## 6. Parimad Praktikad ja Levinud Vead

Pilve infrastruktuuri haldamine Terraform'iga nõuab distsipliini. Väikesed vead võivad põhjustada suuri probleeme või kulusid.

### Kulude kontroll

Pilveressursid maksavad raha ja kulud kasvavad kiiresti, kui ei ole ettevaatlik. EC2 instance't3.micro Free Tier'is on tasuta, aga t3.large maksab $0.08 tunnis - see on $60 kuus. RDS andmebaas võib maksta $50-200 kuus. Load balancer maksab $20+ kuus.

Alati seadke AWS Budgets alerts või Azure Cost Management alerts. Määrake budget (nt $10 kuus) ja saate hoiatuse, kui kulude lävi ületatakse. Terraform ei hoiata teid kulude eest - see on teie vastutus.

Kõige olulisem: alati käivitage `terraform destroy` kui ressursse enam ei vaja. Unustatud test server't võib maksta sadu dollareid kuus.

### State'i turvalisus

State fail sisaldab kogu teie infrastruktuuri detaile, sealhulgas sageli tundlikku informatsiooni - IP aadressid, ressursi ID'd, mõnikord isegi salasõnu. Kui kasutate remote state'i, veenduge et:

1. S3 bucket on krüpteeritud (server-side encryption)
2. S3 bucket ei ole avalik (public access blocked)
3. DynamoDB table on kaetud IAM õigustega
4. State faile pole Git repositories (lisa .gitignore)
```
# .gitignore
*.tfstate
*.tfstate.*
.terraform/
terraform.tfvars  # Kui sisaldab salasõnu
```

### Tagging standardid

Tags on metadata, mida saate lisada igale ressursile. Need on kriitilise tähtsusega suurtes organisatsioonides. Tags võimaldavad:

- Jälgida kulusid projekti või meeskonna kaupa
- Tuvastada ressursside omanikke
- Automaatselt peatada või kustutada ressursse
- Rakendada security policy'sid
```hcl
locals {
  common_tags = {
    Project     = "myapp"
    Environment = terraform.workspace
    ManagedBy   = "Terraform"
    Owner       = "platform-team"
    CostCenter  = "engineering"
  }
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  
  tags = merge(
    local.common_tags,
    {
      Name = "web-server"
      Role = "webserver"
    }
  )
}
```

`merge()` funktsioon kombineerib kaks map'i. Nii saate defineerida ühised tag'id ühes kohas ja lisada ressursi-spetsiifilisi tag'e vajadusel.

### Sensitive data haldamine

MITTE KUNAGI pane salasõnu või API võtmeid Terraform koodi. Kasuta alati:

1. Keskkonna muutujaid (`TF_VAR_db_password`)
2. AWS Secrets Manager või Azure Key Vault
3. Terraform Cloud variables (kui kasutate)
```hcl
# VALE - salasõna koodis
resource "aws_db_instance" "postgres" {
  password = "SuperSecret123"  # ÄRA TEE SEDA!
}

# ÕIGE - salasõna muutujast
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true  # Ei näita plan/apply väljundis
}

resource "aws_db_instance" "postgres" {
  password = var.db_password
}

# Käivitamine
# export TF_VAR_db_password="SuperSecret123"
# terraform apply
```

Või veelgi parem - kasuta Secrets Manager:
```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "myapp/database/password"
}

resource "aws_db_instance" "postgres" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

---

See loeng andis teile foundation pilve infrastruktuuri haldamiseks Terraform'iga. Järgmises labs hakkame neid kontseptsioone praktikas rakendama, luues tõelise AWS VPC'ga koos serverite, võrgu ja turvalisusega.