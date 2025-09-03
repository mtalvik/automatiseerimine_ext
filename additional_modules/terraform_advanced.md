# 🚀 Terraform Edasijõudnud - Moodul 8

## 📋 Ülevaade

See moodul keskendub Terraform'i edasijõudnud funktsioonidele, sealhulgas pilve ressursid, AWS/Azure integratsioon, Workspaces ja turvalisus.

## 🎯 Õpieesmärgid

- Mõista pilve ressursid ja providerid
- Oskama luua AWS/Azure infrastruktuuri
- Kasutada Terraform Workspaces ja keskkondi
- Rakendada turvalisuse parimaid praktikaid

## ⏰ Ajaplaneerimine

- **Kontaktõpe:** 5 tundi
- **Iseseisev õppimine:** 7.5 tundi
- **Kokku:** 12.5 tundi

## 📚 Teoreetiline Taust

### Pilve Ressursid ja Providerid

Terraform võimaldab hallata erinevaid pilve ressursse läbi providerite:

```hcl
# AWS Provider
provider "aws" {
  region = "eu-west-1"
  profile = "default"
}

# Azure Provider
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}
```

### AWS Põhilised Ressursid

```hcl
# VPC ja alamvõrgu
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "main-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  
  tags = {
    Name = "public-subnet"
  }
}

# EC2 Instance
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public.id
  
  tags = {
    Name = "web-server"
  }
}
```

### Azure Põhilised Ressursid

```hcl
# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# Virtual Network
resource "azurerm_virtual_network" "vnet" {
  name                = "vnet"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  address_space       = ["10.0.0.0/16"]
}

# Subnet
resource "azurerm_subnet" "subnet" {
  name                 = "subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}
```

## 🛠️ Praktilised Harjutused

### Harjutus 1: AWS VPC Loomine

Loo AWS VPC koos avaliku ja privaatse alamvõrguga:

```hcl
# main.tf
provider "aws" {
  region = "eu-west-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  
  tags = {
    Name = "public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  
  tags = {
    Name = "private-subnet"
  }
}
```

### Harjutus 2: Azure Web App

Loo Azure Web App koos vajalike ressursidega:

```hcl
# main.tf
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "webapp-rg"
  location = "West Europe"
}

resource "azurerm_app_service_plan" "plan" {
  name                = "webapp-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  kind                = "Linux"
  reserved            = true
  
  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "webapp" {
  name                = "webapp-12345"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  app_service_plan_id = azurerm_app_service_plan.plan.id
}
```

## 🔐 Turvalisus ja IAM

### AWS IAM Rollid

```hcl
# IAM Role
resource "aws_iam_role" "ec2_role" {
  name = "ec2_role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy
resource "aws_iam_policy" "ec2_policy" {
  name = "ec2_policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "arn:aws:s3:::my-bucket/*"
      }
    ]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "ec2_policy_attachment" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.ec2_policy.arn
}
```

### Azure RBAC

```hcl
# Azure AD Application
resource "azuread_application" "app" {
  name = "terraform-app"
}

# Service Principal
resource "azuread_service_principal" "sp" {
  application_id = azuread_application.app.application_id
}

# Role Assignment
resource "azurerm_role_assignment" "role" {
  scope                = azurerm_resource_group.rg.id
  role_definition_name = "Contributor"
  principal_id         = azuread_service_principal.sp.object_id
}
```

## 🌍 Terraform Workspaces

### Workspace'ide Kasutamine

```bash
# Loo uus workspace
terraform workspace new development
terraform workspace new staging
terraform workspace new production

# Vaheta workspace'i
terraform workspace select development

# Vaata kõiki workspace'e
terraform workspace list
```

### Keskkonna-spetsiifilised Konfiguratsioonid

```hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  
  default = {
    development = "t3.micro"
    staging     = "t3.small"
    production  = "t3.medium"
  }
}

# main.tf
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = lookup(var.instance_type, var.environment, "t3.micro")
  
  tags = {
    Name        = "web-server"
    Environment = var.environment
  }
}
```

## 📊 State'i Haldamine

### Remote State

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "global/s3/terraform.tfstate"
    region = "eu-west-1"
  }
}
```

### State'i Jagamine

```hcl
# data.tf
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "terraform-state-bucket"
    key    = "vpc/terraform.tfstate"
    region = "eu-west-1"
  }
}

# main.tf
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  subnet_id     = data.terraform_remote_state.vpc.outputs.public_subnet_id
}
```

## 🧪 Testimine ja Valideerimine

### Terraform Validate

```bash
# Valideeri konfiguratsioon
terraform validate

# Vaata planeeritud muudatusi
terraform plan

# Kontrolli süntaksit
terraform fmt -check
```

### Testimise Tööriistad

```hcl
# test/terraform_test.go
package test

import (
  "testing"
  "github.com/gruntwork-io/terratest/modules/terraform"
)

func TestTerraformBasicExample(t *testing.T) {
  terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
    TerraformDir: "../",
  })
  
  defer terraform.Destroy(t, terraformOptions)
  terraform.InitAndApply(t, terraformOptions)
}
```

## 📝 Kodutööd

### Ülesanne 1: Pilve Infrastruktuur

Loo AWS või Azure infrastruktuur, mis sisaldab:
- VPC/Virtual Network
- Avalik ja privaatne alamvõrk
- Security Groups/Network Security Groups
- Load Balancer
- Auto Scaling Group/VM Scale Set

### Ülesanne 2: Turvalisus ja IAM

Rakenda turvalisuse parimad praktikad:
- IAM rollid ja poliitikad
- Security Groups/NSG reeglid
- VPC endpoints
- Krypto võtmed ja saladused

### Lisapraktika: Mitme Keskkonna Konfiguratsioon

Loo Terraform konfiguratsioon, mis toetab:
- Development, Staging, Production keskkondi
- Workspace'ide kasutamist
- Keskkonna-spetsiifilisi ressursse
- Remote state haldamist

## 🔍 Kasulikud Ressursid

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)
- [Terraform Testing with Terratest](https://terratest.gruntwork.io/)

## 📊 Hindamine

- **Praktiline töö (60%):** Pilve infrastruktuuri loomine ja konfigureerimine
- **Teoreetiline mõistmine (25%):** Turvalisuse ja IAM kontseptsioonid
- **Lisapraktika (15%):** Mitme keskkonna konfiguratsioon ja optimeerimine

---

**🎯 Edu mooduli läbimisel!**
