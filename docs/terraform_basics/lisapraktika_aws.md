# Terraform AWS Lisapraktika

Need harjutused on mõeldud süvendama Terraform ja AWS integratsiooniga seotud oskusi. Iga harjutus keskendub ühele konkreetsele production-ready tehnikale, mida vajate päris projektides.

**Eeldused:** Terraform põhitööd läbitud, AWS konto seadistatud, AWS CLI ja Terraform installitud

---

## 1. Remote State ja State Locking

### 1.1 Probleem

Kohalikus arvutis olev `terraform.tfstate` fail on risk. Kui fail kaob või korrumpeerub, kaob ka info kogu infrastruktuuri kohta. Meeskonnatöös tekivad konfliktid, kui kaks inimest muudavad infrastruktuuri samaaegselt.

Real-world stsenaarium: kolmeliikmeline meeskond haldab AWS infrastruktuuri. State fail on Git'is, mis põhjustab pidevaid konflikte. Eile kustutati kogemata production database, sest kaks inimest käivitasid `terraform apply` samaaegselt ja nende state failid olid erinevad. Üks nägi database'i olemasolevana, teine mitte. Tulemus: andmekadu ja mitu tundi downtime'i.

Põhiprobleemid kohaliku state'iga:
- Ühel masinal olev fail - teised ei näe muudatusi
- Git'is hoidmine põhjustab merge konflikte
- Pole lukustust - kaks inimest võivad samaaegu muuta
- Backup puudub - kui disk crashib, kaob kõik
- Sisaldab tundlikku infot (paroolid, API võtmed)

### 1.2 Lahendus

Remote backend kasutab S3 bucketi state'i salvestamiseks ja DynamoDB tabelit lukustamiseks. S3 versioning võimaldab taastada vanu versioone, kui midagi läheb valesti. DynamoDB hoiab lukku - ainult üks operatsioon saab korraga state'i muuta.
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
  region = "eu-west-1"
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-${data.aws_caller_identity.current.account_id}"
  
  tags = {
    Name        = "Terraform State"
    Environment = "all"
    Purpose     = "Remote state storage"
  }
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
  
  tags = {
    Name = "Terraform State Locks"
  }
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.terraform_state.id
  description = "S3 bucket nimi state'i jaoks"
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.terraform_locks.name
  description = "DynamoDB tabeli nimi"
}
```

S3 bucket salvestab state faili krüpteeritult. Versioning hoiab kõiki varasemaid versioone, seega saab taastada, kui keegi teeb vea. Public access block tagab, et keegi ei pääse bucketi sisu vaatama. DynamoDB tabel kasutab LockID võtit lukustuse hoidmiseks. Billing mode PAY_PER_REQUEST tähendab, et maksate ainult kasutuse eest, mitte fikseeritud summat.

### 1.3 Harjutus: Remote Backend Seadistamine

**Nõuded:**
- [ ] Loo S3 bucket state'i jaoks unikaalse nimega
- [ ] Seadista bucket versioning ja encryption
- [ ] Loo DynamoDB tabel state locking'u jaoks
- [ ] Migreeri olemasolev kohalik state remote backend'i
- [ ] Testi, et lukustus töötab kahe paralleelse apply'ga

**Näpunäiteid:**
- Alusta ilma backend blokita, loo esmalt S3 ja DynamoDB ressursid
- Pärast ressursside loomist lisa backend konfiguratsioon
- Kasuta `terraform init -migrate-state` state'i migreerimiseks
- Kontrolli S3 konsoolist, et state fail on bucketi's
- Kui lukustus jääb kinni, kasuta `terraform force-unlock <LOCK_ID>`

**Testimine:**
```bash
# Loo backend ressursid
terraform init
terraform apply

# Lisa backend.tf oma projekti
# Migreeri state
terraform init -migrate-state

# Kontrolli S3's
aws s3 ls s3://terraform-state-ACCOUNT_ID/

# Testi lukustust - ava kaks terminali
# Terminal 1
terraform apply
# Terminal 2 peaks failima
terraform apply
```

**Boonus:**
- Lisa S3 lifecycle policy, mis kustutab state'i vanemad versioonid pärast 90 päeva
- Seadista CloudWatch alarm, mis hoiatab, kui state'i pole 7 päeva muudetud

---

## 2. Data Sources ja Existing Infrastructure

### 2.1 Probleem

Päris projektides ei loo te alati kõike nullist. Tihti peate kasutama olemasolevaid ressursse - VPC'd, subnette, AMI'sid, security gruppe. Neid ei saa hard-code'ida, sest ID'd muutuvad regiooniti ja keskkonniti. Kui kirjutate konkreetse AMI ID, siis kood töötab ainult ühes regioonis.

Real-world stsenaarium: teie ettevõttel on olemasolev võrk, mida haldab infrastruktuuri meeskond. Teil on vaja luua EC2 instance'e nende võrku, aga te ei tohi võrku ise muuta ega selle Terraform koodi omaneda. Teie kood peab leidma olemasoleva VPC ja subnet'id, kasutama neid, aga mitte neid haldama.

Probleemid hard-code'imisega:
- AMI ID erinevad regiooniti - kood pole portable
- VPC ja subnet ID'd muutuvad keskkonniti
- Security group'id on erinevad
- Ei saa kasutada uusimaid AMI versioone automaatselt
- Kood muutub aegunuks, kui ressursse uuendatakse

### 2.2 Lahendus

Data source'd pärivad infot olemasolevate ressursside kohta runtime'il. Need ei loo uusi ressursse, vaid otsivad ja loevad olemasolevaid. Saate filtreerida tag'ide, nimede või muude atribuutide järgi.
```hcl
data "aws_vpc" "existing" {
  filter {
    name   = "tag:Name"
    values = ["company-main-vpc"]
  }
}

data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.existing.id]
  }
  
  filter {
    name   = "tag:Type"
    values = ["public"]
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_security_group" "existing_web" {
  filter {
    name   = "tag:Name"
    values = ["web-sg"]
  }
  
  vpc_id = data.aws_vpc.existing.id
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t3.micro"
  subnet_id              = tolist(data.aws_subnets.public.ids)[0]
  vpc_security_group_ids = [data.aws_security_group.existing_web.id]
  
  tags = {
    Name = "app-server"
  }
}
```

VPC data source otsib tag'i järgi VPC'd nimega "company-main-vpc". Subnets data source leiab kõik selle VPC subnet'id, millel on tag Type=public. AMI data source võtab uusima Amazon Linux 2 AMI. Security group data source leiab olemasoleva web-sg grupi. Instance kasutab kõiki neid leitud ressursse, aga ei loo ega muuda neid.

### 2.3 Harjutus: Olemasolevate Ressursside Kasutamine

**Nõuded:**
- [ ] Loo käsitsi AWS konsoolist VPC tag'iga Name=lab-vpc
- [ ] Kirjuta Terraform kood, mis leiab selle VPC data source'iga
- [ ] Leia kõik subnet'id selles VPC's
- [ ] Leia uusim Ubuntu 22.04 AMI Canonical'ilt
- [ ] Loo EC2 instance leitud ressurssidega
- [ ] Väljasta instance'i public IP

**Näpunäiteid:**
- Kasuta `terraform console` data source'ide testimiseks
- Ubuntu Canonical owner ID on `099720109477`
- Kui VPC'd pole, kasuta default VPC't: `data "aws_vpc" "default" { default = true }`
- `tolist()` funktsioon konverteerib set'i listiks indekseerimiseks
- Filtreeri AMI'd nime pattern'i järgi: `ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*`

**Testimine:**
```bash
# Testi data source'e console'is
terraform console
> data.aws_vpc.existing.id
> data.aws_subnets.public.ids
> data.aws_ami.amazon_linux.id

# Loo instance
terraform apply

# Kontrolli, et instance on õiges subnet's
aws ec2 describe-instances \
  --instance-ids $(terraform output -raw instance_id) \
  --query 'Reservations[0].Instances[0].SubnetId'
```

**Boonus:**
- Kasuta `data "aws_availability_zones"` leidmaks kõik AZ'd ja loo instance igasse
- Lisa `data "aws_ssm_parameter"` leidmaks AMI ID Systems Manager'ist

---

## 3. Lifecycle Rules ja Zero-Downtime Deployments

### 3.1 Probleem

Terraform'i default käitumine on kustutada ressurss enne uue loomist. See tähendab downtime'd - vahepeal pole serverit üldse. Production keskkonnas on see vastuvõetamatu. Kasutajad näevad viga, teenus ei ole kättesaadav.

Real-world stsenaarium: peate uuendama web serveri AMI'd security patch'ide tõttu. Vana AMI sisaldab vulnerabilit

y'd, uus on turvaline. Kui kasutate default käitumist, Terraform kustutab vana instance'i, siis loob uue. Vahepeal on 2-3 minutit downtime'd. Veebileht ei ole kättesaadav, kasutajad näevad vigu.

Probleemid default käitumisega:
- Instance kustutamine põhjustab downtime'i
- Load balancer näeb instance'i unhealthy
- Kasutajad näevad 503 Service Unavailable
- Mõned ressursid ei saa uuesti luua (nt Elastic IP)
- Blue-green deployment pole võimalik

### 3.2 Lahendus

Lifecycle rule `create_before_destroy` muudab järjekorda - loob uue enne vana kustutamist. See võimaldab zero-downtime uuendusi. Kombineerides Auto Scaling Group'iga ja instance refresh'iga saab uuendada servereid järk-järgult.
```hcl
resource "aws_launch_template" "web" {
  name_prefix   = "web-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    app_version = var.app_version
  }))
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  lifecycle {
    create_before_destroy = true
  }
  
  tags = {
    Name = "web-launch-template"
  }
}

resource "aws_autoscaling_group" "web" {
  name                = "web-asg"
  min_size            = 2
  max_size            = 4
  desired_capacity    = 2
  vpc_zone_identifier = data.aws_subnets.private.ids
  target_group_arns   = [aws_lb_target_group.web.arn]
  
  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }
  
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
      instance_warmup        = 60
    }
  }
  
  tag {
    key                 = "Name"
    value               = "web-server"
    propagate_at_launch = true
  }
}

resource "aws_lb" "web" {
  name               = "web-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = data.aws_subnets.public.ids
}

resource "aws_lb_target_group" "web" {
  name     = "web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.main.id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    timeout             = 5
    unhealthy_threshold = 2
  }
}
```

Launch template määrab, kuidas instance'd luuakse. Create before destroy tagab, et uus template luuakse enne vana kustutamist. Auto Scaling Group haldab instance'ite arvu. Instance refresh strateegia Rolling tähendab järkjärgulist uuendamist. Min healthy percentage 50 tähendab, et alati vähemalt pool servereid töötab. Load balancer suunab liiklust ainult healthy instance'itele.

### 3.3 Harjutus: Zero-Downtime Update Setup

**Nõuded:**
- [ ] Loo launch template create_before_destroy lifecycle'iga
- [ ] Loo Auto Scaling Group vähemalt 2 instance'iga
- [ ] Loo Application Load Balancer ja target group
- [ ] Seadista health check target group'ile
- [ ] Uuenda AMI'd ja vaata, kuidas instance'id uuendatakse ilma downtime'ita
- [ ] Verifitseeri, et load balancer IP jääb samaks

**Näpunäiteid:**
- Alusta 2 instance'iga - lihtsam jälgida
- Health check path peaks vastama 200 OK
- Instance warmup määrab, kui kaua oodatakse enne healthy märkimist
- Vaata AWS konsoolist Auto Scaling Activity History
- Kasuta `curl` loopis load balancer'i testimiseks uuenduse ajal

**Testimine:**
```bash
# Loo infrastruktuur
terraform apply

# Testi load balancer'it
while true; do curl -s http://$(terraform output -raw lb_dns_name) | grep Version; sleep 1; done

# Muuda app_version variables.tf'is
# Uuenda infrastruktuuri
terraform apply

# Jälgi, et curl jätkab töötamist ilma errorita
# Peaks nägema versioonide muutumist järk-järgult
```

**Boonus:**
- Lisa lifecycle ignore_changes user_data'le, et väiksed skripti muudatused ei tekita instance'ite uuendamist
- Kasuta blue-green deployment strateegia weighted target groups'iga

---

## Kasulikud Ressursid

**Dokumentatsioon:**
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Backend Configuration](https://www.terraform.io/language/settings/backends/s3)
- [AWS Auto Scaling Groups](https://docs.aws.amazon.com/autoscaling/ec2/userguide/)

**Tööriistad:**
- **terraform console** - interaktiivne REPL testimiseks: `terraform console`
- **aws-vault** - AWS credentials turvaliseks haldamiseks: `aws-vault exec profile -- terraform apply`
- **tflint** - Terraform koodi linter: `tflint --init && tflint`

**Näited:**
- [Terraform Best Practices](https://github.com/antonbabenko/terraform-best-practices)

Need harjutused on mõeldud süvendama teie Terraform AWS integratsiooniga seotud oskusi. Alustage esimesest ja liikuge järk-järgult keerulisemate poole.