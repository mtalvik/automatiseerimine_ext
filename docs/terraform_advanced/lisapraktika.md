# Terraform Edasijõudnud Lisapraktika

Need harjutused on valikulised ja mõeldud neile, kes soovivad süvendada oma Terraform oskusi pärast põhilabori ja kodutöö tegemist.

**Eeldused:** Labor ja kodutöö lõpetatud, vähemalt 1 päeva paus ja reflektsioon vahepeal

---

## 1. Workspaces ja Keskkondade Haldamine

### 1.1 Probleem

Pärast kodutöö tegemist on teil üks keskkond. Aga päris elus on vaja mitut: development (katsetamiseks), staging (testimiseks) ja production (tõeline kasutamine). Kui loote iga keskkonna jaoks eraldi Terraform projekti, muutub kood duplikaadiks ja maintainance korraks.

### 1.2 Lahendus

Terraform workspaces võimaldavad sama koodi kasutada mitme eraldatud keskkonna loomiseks. Iga workspace'il on oma state fail, seega ressursid ei kattu.
```hcl
# variables.tf lisage:
variable "environment_config" {
  description = "Configuration per environment"
  type = map(object({
    instance_type = string
    instance_count = number
    enable_monitoring = bool
  }))
  
  default = {
    development = {
      instance_type     = "t2.micro"
      instance_count    = 1
      enable_monitoring = false
    }
    staging = {
      instance_type     = "t2.small"
      instance_count    = 1
      enable_monitoring = true
    }
    production = {
      instance_type     = "t2.medium"
      instance_count    = 2
      enable_monitoring = true
    }
  }
}

# main.tf-is kasutage:
locals {
  env_config = var.environment_config[terraform.workspace]
  
  common_tags = {
    Environment = terraform.workspace
    ManagedBy   = "Terraform"
    Project     = var.project_name
  }
}

resource "aws_instance" "app" {
  count = local.env_config.instance_count
  
  ami           = data.aws_ami.amazon_linux_2023.id
  instance_type = local.env_config.instance_type
  
  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-app-${count.index + 1}"
    }
  )
}

# Monitoring ainult kui lubatud
resource "aws_cloudwatch_metric_alarm" "cpu" {
  count = local.env_config.enable_monitoring ? local.env_config.instance_count : 0
  
  alarm_name          = "${var.project_name}-cpu-${count.index}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  
  dimensions = {
    InstanceId = aws_instance.app[count.index].id
  }
}
```

### 1.3 Harjutus: Multi-Environment Deployment

Võtke oma kodutöö projekt ja tehke sellest multi-environment:

**Nõuded:**

- [ ] Looge 3 workspace'i: `dev`, `staging`, `prod`
- [ ] Iga keskkond kasutab erinevat instance type'i (vaata configist ülalpool)
- [ ] Production on 2 instance'iga, teised 1'ga
- [ ] Ainult staging ja prod-il on CloudWatch alarms
- [ ] Kõik ressursid on taggeditud keskkonnaga
- [ ] VPC CIDR on erinev igale keskkonnale (dev: 10.0.x.x, staging: 10.1.x.x, prod: 10.2.x.x)

**Näpunäiteid:**

- Alustage workspace'ide loomisega: `terraform workspace new dev`
- Kasutage `terraform.workspace` muutujat CIDR valiku jaoks
- Kui workspace on "dev", kasutage 10.0.0.0/16, kui "staging", siis 10.1.0.0/16 jne
- Testige iga workspace'i eraldi: `terraform workspace select dev && terraform apply`

**Testimine:**
```bash
# Dev keskkond
terraform workspace select dev
terraform apply
terraform output

# Staging keskkond
terraform workspace select staging
terraform apply
terraform output

# Vaadake AWS konsoolist, et mõlemad eraldatud
```

**Boonus:**

- Lisage workspace-põhine DNS naming
- Kasutage erinevaid availability zone'e eri keskkondades
- Looge workspace-spetsiifilised S3 bucket'id

---

## 2. Remote State ja Team Collaboration

### 2.1 Probleem

Praegu on teie state fail arvutis. Kui töökolleeg tahab same projekti kallal tööd teha, ei tea ta, mis ressursid juba eksisteerivad. Kui mõlemad jooksutavad `terraform apply` samaaegselt, võib state korruptsiooni tekkida.

### 2.2 Lahendus

Remote state S3'is koos DynamoDB lockinguga lahendab need probleemid.
```hcl
# 1. Looge S3 bucket ja DynamoDB tabel (tehke see eraldi projektina!)
# s3-backend/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "minu-terraform-state-${random_string.suffix.result}"
  
  lifecycle {
    prevent_destroy = true
  }
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.terraform_state.bucket
}

output "dynamodb_table" {
  value = aws_dynamodb_table.terraform_locks.name
}

# 2. Nüüd oma põhiprojektis kasutage seda
# backend.tf põhiprojektis
terraform {
  backend "s3" {
    bucket         = "minu-terraform-state-abc12345"  # Asendage oma bucket'iga!
    key            = "myproject/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
  }
}
```

### 1.3 Harjutus: Shared State Setup

Seadistage remote state ja testige locking'ut.

**Nõuded:**

- [ ] Looge S3 bucket state'i jaoks (krüpteeritud!)
- [ ] Looge DynamoDB tabel locking'u jaoks
- [ ] Migreerige lokaalne state S3'i
- [ ] Testige, et kaks terminali ei saa samaaegselt apply'da
- [ ] Enable state versioning S3'is
- [ ] Lisage .gitignore, et state fails ei läheks Giti

**Näpunäiteid:**

- Alustage eraldi projektiga S3 + DynamoDB loomiseks
- Salvestage bucket nimi ja DynamoDB tabeli nimi
- Lisage backend konfiguratsioon põhiprojekti
- Käivitage `terraform init -migrate-state`
- Lokaalne state fail jääb alles backup'ina
- ärge kustutage kohe

**Testimine:**
```bash
# Terminalis 1
terraform plan
# Hoidke plani oodates...

# Terminalis 2 (sama kataloog)
terraform plan
# Peaks nägema: "Error locking state: state currently locked..."
```

**Boonus:**

- Kasutage erinevaid S3 key'sid erinevate workspace'ide jaoks
- Lisage lifecycle policy S3 state versioning'u jaoks (hoia 30 päeva)
- Looge IAM policy, mis lubab ainult read-only ligipääsu production state'ile

---

## 3. Terraform Modules ja Taaskasutatavus

### 3.1 Probleem

Teie kodutöö kood töötab, aga on spetsiifiline ühele projektile. Kui peaksite looma teise projekti sama VPC struktuuri-ga, peaksite kogu koodi kopeerima ja muutma. See on DRY (Don't Repeat Yourself) printsiibi rikkumine.

### 3.2 Lahendus

Terraform modules võimaldavad luua taaskasutatavaid infrastruktuuri komponente.
```
terraform-modules/
├── modules/
│   └── aws-vpc/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── README.md
└── projects/
    ├── project-a/
    │   └── main.tf
    └── project-b/
        └── main.tf
```

Module näide:
```hcl
# modules/aws-vpc/variables.tf
variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "cidr_block" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}

# modules/aws-vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = merge(
    {
      Name = "${var.project_name}-vpc"
    },
    var.tags
  )
}

resource "aws_subnet" "public" {
  count = length(var.public_subnets)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnets[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = merge(
    {
      Name = "${var.project_name}-public-${count.index + 1}"
      Type = "public"
    },
    var.tags
  )
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = merge(
    {
      Name = "${var.project_name}-igw"
    },
    var.tags
  )
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = merge(
    {
      Name = "${var.project_name}-public-rt"
    },
    var.tags
  )
}

resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public)
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# modules/aws-vpc/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.main.id
}

# Projekts kasutab module'it
# projects/project-a/main.tf
module "vpc" {
  source = "../../modules/aws-vpc"
  
  project_name       = "my-app"
  cidr_block         = "10.0.0.0/16"
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24"]
  availability_zones = ["eu-west-1a", "eu-west-1b"]
  
  tags = {
    Environment = "production"
    Team        = "platform"
  }
}

# Kasutage module outpute
resource "aws_instance" "web" {
  ami           = "ami-0d71ea30463e0ff8d"
  instance_type = "t2.micro"
  subnet_id     = module.vpc.public_subnet_ids[0]  # Esimene subnet
  
  tags = {
    Name = "web-server"
  }
}
```

### 3.3 Harjutus: VPC Module Creation

Looge taaskasutatav VPC module ja kasutage seda kahes erinevas projektis.

**Nõuded:**

- [ ] Module struktuur: `modules/aws-vpc/` koos `main.tf`, `variables.tf`, `outputs.tf`
- [ ] Module loob VPC, subnet'id, IGW, route table'id
- [ ] Module on parameetritega konfigureeritav (CIDR, subnet count, AZ'id)
- [ ] Looge 2 eraldatud projekti, mis kasutavad sama module'it
- [ ] Ühes projektis on 2 public subnet'i, teises 3
- [ ] Module README.md dokumentatsiooniga

**Näpunäiteid:**

- Alustage module failide loomisega eraldi kataloogis
- Testige module'it kõigepealt ühes projektis
- Lisage validation variable'itele (näiteks CIDR must be valid)
- Kasutage `count` või `for_each` subnet'ide loomiseks
- Dokumenteerige inputs, outputs ja kasutamisnäide README'sse

**Testimine:**
```bash
# Projekt A
cd projects/project-a
terraform init
terraform apply

# Projekt B
cd ../project-b
terraform init
terraform apply

# Kontrollige AWS konsoolist, et mõlemad VPC'd eksisteerivad
```

**Boonus:**

- Lisa module'ile private subnet'ide tugi koos NAT Gateway'ga
- Versiooni module (kasutades Git tag'e)
- Publish module Terraform Registry'sse (public või private)
- Lisa automated testing module'ile (Terratest või kitchen-terraform)

---

## Kasulikud Ressursid

**Dokumentatsioon:**

- [Terraform Workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)
- [Terraform Backend Configuration](https://developer.hashicorp.com/terraform/language/settings/backends/s3)
- [Terraform Modules](https://developer.hashicorp.com/terraform/language/modules)

**Tööriistad:**

- **terraform-docs**
- Generate module documentation: `brew install terraform-docs`
- **tflint**
- Linter for Terraform: `brew install tflint`
- **tfsec**
- Security scanner: `brew install tfsec`

**Näited:**

- [AWS VPC Terraform Module](https://github.com/terraform-aws-modules/terraform-aws-vpc)
- [Gruntwork Infrastructure Library](https://gruntwork.io/infrastructure-as-code-library/)

---

Need harjutused on mõeldud süvendama teie Terraform oskusi. Alustage esimesest ja liikuge järk-järgult keerulisemate poole.