# Terraform Edasijõudnud

**Teemad:** Pilve ressursid, AWS/Azure integratsioon, workspaces, turvalisus, moodulid

---

##  Õpiväljundid

Pärast seda loengut oskate:
- Mõista pilve ressursid ja provider'id
- Luua AWS/Azure infrastruktuuri Terraform'iga
- Kasutada Terraform workspaces'eid ja keskkondi
- Rakendada turvalisuse parimaid praktikaid
- Kasutada Terraform mooduleid ja taaskasutatavaid komponente

---

##  Pilve Ressursid ja Provider'id

## ⏰ Ajaplaneerimine

- **Kontaktõpe:** 5 tundi
- **Iseseisev õppimine:** 7.5 tundi
- **Kokku:** 12.5 tundi

##  Teoreetiline Taust

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

AWS'is saab Terraform'iga hallata:
- **VPC** (Virtual Private Cloud) - isoleeritud võrk
- **Subnets** - alamvõrgud (public/private)
- **EC2 Instances** - virtuaalsed serverid
- **S3 Buckets** - failimajutus
- **RDS** - hallatavad andmebaasid

**Näide struktureeritud ressurssidest:**
 Vaata [labor.md - Samm 1: AWS VPC ja ressursid](labor.md#-samm-1-aws-provider-seadistamine)

**Põhiprintsiibid:**
- Ressursid viitavad üksteisele (nt subnet kasutab VPC ID'd)
- Tag'id aitavad ressursse organiseerida
- CIDR blokid määravad IP vahemikud

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

##  Turvalisus ja IAM

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

##  Terraform Workspaces

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

##  State'i Haldamine

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

##  Testimine ja Valideerimine

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

##  Kasulikud Ressursid

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)
- [Terraform Testing with Terratest](https://terratest.gruntwork.io/)

---

##  Järgmised sammud

**Lab'is täna:**
- Loome AWS/Azure ressursse
- Seadistame workspaces
- Implementeerime remote state
- Rakendame turvalisuse best practices

**Õpi rohkem:**
- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)

---

**Edu ja head IaC'itamist!** 
