# Terraform Edasijõudnud Lisapraktika

Täiendavad ülesanded Terraform'i enterprise patterns'i õppimiseks.

**Eeldused:** Põhilabor läbitud, Terraform resources/variables/state selged

---

## Enne alustamist

Need ülesanded on valikulised ja mõeldud neile, kes:

- Lõpetasid põhilabori ära
- Mõistavad Terraform põhitõdesid (resources, variables, state)
- Tahavad õppida advanced Terraform patterns
- Valmistuvad päris cloud infrastructure haldamiseks

** OLULINE:** Need harjutused kasutavad päris pilve (AWS/Azure). **Ära unusta `terraform destroy`!**

---

## Väljakutse 1: Terraform Modules Library


### Mida õpid?
- Module design patterns
- Input/output variables
- Module composition
- Versioning

### Projekt struktuur:
```
terraform-modules/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── ec2-instance/
│   ├── rds-postgres/
│   └── s3-bucket/
└── examples/
    ├── simple-vpc/
    └── full-stack/
```

### VPC Module näide:
```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support

  tags = merge(
    var.tags,
    {
      Name = var.name
    }
  )
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(
    var.tags,
    {
      Name = "${var.name}-public-${count.index + 1}"
      Type = "public"
    }
  )
}

# modules/vpc/variables.tf
variable "name" {
  description = "Name prefix for VPC resources"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string
  validation {
    condition     = can(cidrhost(var.cidr_block, 0))
    error_message = "Must be valid IPv4 CIDR."
  }
}

variable "public_subnet_cidrs" {
  description = "List of public subnet CIDRs"
  type        = list(string)
  default     = []
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
```

### Module kasutamine:
```hcl
# examples/simple-vpc/main.tf
module "vpc" {
  source = "../../modules/vpc"

  name       = "my-app"
  cidr_block = "10.0.0.0/16"
  
  public_subnet_cidrs = [
    "10.0.1.0/24",
    "10.0.2.0/24"
  ]
  
  availability_zones = [
    "us-east-1a",
    "us-east-1b"
  ]

  tags = {
    Environment = "dev"
    Project     = "myapp"
  }
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
```

###  Boonus:
- Publish modules to Terraform Registry
- Loo automated module testing (Terratest)
- Lisa module versioning (Git tags)
- Loo module documentation generator

---

## Väljakutse 2: Remote State Management


### Mida õpid?
- Remote backends (S3, Azure Blob)
- State locking
- State collaboration
- State migration

### S3 Backend setup:
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "myapp-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# Create S3 bucket for state
resource "aws_s3_bucket" "terraform_state" {
  bucket = "myapp-terraform-state"

  lifecycle {
    prevent_destroy = true
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

# DynamoDB for state locking
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

### State operations:
```bash
# Initialize with backend
terraform init

# View current state
terraform state list

# Show specific resource
terraform state show aws_instance.web

# Move resource
terraform state mv aws_instance.web aws_instance.app

# Remove from state (but don't destroy)
terraform state rm aws_instance.old

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Pull remote state
terraform state pull > terraform.tfstate.backup

# Push local state to remote
terraform state push terraform.tfstate
```

###  Boonus:
- Loo automated state backup
- Implementeeri state file encryption
- Lisa state access logging
- Loo state disaster recovery plan

---

## Väljakutse 3: Dynamic Infrastructure


### Mida õpid?
- `for_each` vs `count`
- Dynamic blocks
- Conditional resources
- Data sources

### Dynamic blocks näide:
```hcl
# Dynamic security group rules
variable "ingress_rules" {
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = [
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTP"
    },
    {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTPS"
    }
  ]
}

resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }
}

# for_each with maps
variable "instances" {
  type = map(object({
    instance_type = string
    ami           = string
    subnet_id     = string
  }))
  default = {
    web = {
      instance_type = "t3.micro"
      ami           = "ami-12345678"
      subnet_id     = "subnet-abc123"
    }
    api = {
      instance_type = "t3.small"
      ami           = "ami-12345678"
      subnet_id     = "subnet-abc123"
    }
  }
}

resource "aws_instance" "app" {
  for_each = var.instances

  ami           = each.value.ami
  instance_type = each.value.instance_type
  subnet_id     = each.value.subnet_id

  tags = {
    Name = each.key
  }
}

# Conditional resources
variable "enable_monitoring" {
  type    = bool
  default = false
}

resource "aws_cloudwatch_dashboard" "main" {
  count = var.enable_monitoring ? 1 : 0

  dashboard_name = "my-dashboard"
  dashboard_body = jsonencode({
    widgets = []
  })
}
```

###  Boonus:
- Loo environment-specific resources
- Implementeeri feature flags
- Lisa cost optimization conditionals
- Loo self-documenting infrastructure

---

## Väljakutse 4: Testing ja Validation


### Mida õpid?
- Terratest
- Pre-commit hooks
- Policy as code (OPA/Sentinel)
- Cost estimation

### Terratest näide (Go):
```go
// test/vpc_test.go
package test

import (
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestVPCModule(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../examples/simple-vpc",
		Vars: map[string]interface{}{
			"name":       "test-vpc",
			"cidr_block": "10.0.0.0/16",
		},
	})

	defer terraform.Destroy(t, terraformOptions)

	terraform.InitAndApply(t, terraformOptions)

	vpcID := terraform.Output(t, terraformOptions, "vpc_id")
	assert.NotEmpty(t, vpcID)
}
```

### Pre-commit hooks (.pre-commit-config.yaml):
```yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_docs
      - id: terraform_tflint
      - id: terraform_tfsec
      - id: terraform_checkov
```

### OPA Policy näide:
```rego
# policy/require_tags.rego
package terraform.required_tags

import input as tfplan

required_tags = ["Environment", "Project", "Owner"]

deny[msg] {
  resource := tfplan.resource_changes[_]
  resource.type == "aws_instance"
  
  tags := object.get(resource.change.after, "tags", {})
  missing_tags := {tag | tag := required_tags[_]; not tags[tag]}
  
  count(missing_tags) > 0
  
  msg := sprintf(
    "Instance %s is missing required tags: %v",
    [resource.address, missing_tags]
  )
}
```

### Infracost integration:
```yaml
# .gitlab-ci.yml
cost_estimate:
  stage: plan
  script:
    - terraform init
    - terraform plan -out=plan.cache
    - terraform show -json plan.cache > plan.json
    - infracost breakdown --path plan.json
    - infracost diff --path plan.json --compare-to latest
```

###  Boonus:
- Loo automated security scanning
- Lisa compliance checking (CIS benchmarks)
- Implementeeri drift detection
- Loo cost budget alerts

---

## Väljakutse 5: Multi-Cloud Deployment


### Mida õpid?
- Multi-cloud strategies
- Provider abstraction
- Cross-cloud resources
- Disaster recovery

### Multi-provider setup:
```hcl
# providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "azurerm" {
  features {}
}

# main.tf
variable "cloud_provider" {
  type    = string
  default = "aws"
  
  validation {
    condition     = contains(["aws", "azure", "both"], var.cloud_provider)
    error_message = "Must be 'aws', 'azure', or 'both'"
  }
}

# AWS resources
resource "aws_instance" "app" {
  count = var.cloud_provider == "aws" || var.cloud_provider == "both" ? 1 : 0

  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
}

# Azure resources
resource "azurerm_linux_virtual_machine" "app" {
  count = var.cloud_provider == "azure" || var.cloud_provider == "both" ? 1 : 0

  name                = "app-vm"
  resource_group_name = azurerm_resource_group.main[0].name
  location            = azurerm_resource_group.main[0].location
  size                = "Standard_B1s"

  admin_username = "adminuser"

  network_interface_ids = [
    azurerm_network_interface.main[0].id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}
```

###  Boonus:
- Loo abstraction layer modules
- Implementeeri cross-cloud networking (VPN)
- Lisa multi-cloud monitoring
- Loo failover strategy

---

## Väljakutse 6: Terraform Cloud/Enterprise


### Mida õpid?
- Terraform Cloud workspaces
- Remote execution
- Private registry
- Team collaboration

### Terraform Cloud setup:
```hcl
# backend.tf
terraform {
  cloud {
    organization = "myorg"
    
    workspaces {
      tags = ["app:myapp", "env:prod"]
    }
  }
}

# Workspace variables via API
resource "tfe_workspace" "myapp_prod" {
  name         = "myapp-prod"
  organization = "myorg"

  vcs_repo {
    identifier     = "myorg/myapp-infrastructure"
    oauth_token_id = var.oauth_token_id
  }

  auto_apply = false  # Manual approval for prod
}

resource "tfe_variable" "database_url" {
  key          = "database_url"
  value        = "postgres://..."
  category     = "terraform"
  workspace_id = tfe_workspace.myapp_prod.id
  sensitive    = true
}
```

### Sentinel Policy:
```hcl
# policies/enforce-instance-types.sentinel
import "tfplan/v2" as tfplan

allowed_types = ["t3.micro", "t3.small", "t3.medium"]

main = rule {
  all tfplan.resource_changes as _, rc {
    rc.type is "aws_instance" implies
      rc.change.after.instance_type in allowed_types
  }
}
```

###  Boonus:
- Loo private module registry
- Implementeeri policy sets
- Lisa cost estimation policies
- Loo team-based access controls

---

## Täiendavad ressursid

### Dokumentatsioon:
- [Terraform Docs](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Cloud](https://www.terraform.io/cloud)
- [Terratest](https://terratest.gruntwork.io/)

### Tööriistad:
- **terraform-docs:** Generate documentation
- **tflint:** Linter for Terraform
- **tfsec:** Security scanner
- **checkov:** Policy as code scanner
- **Infracost:** Cost estimation

### Näited:
- [Gruntwork Infrastructure Library](https://gruntwork.io/)
- [Terraform AWS Modules](https://github.com/terraform-aws-modules)
- [Azure Verified Modules](https://aka.ms/avm)

---

## Näpunäited

1. ** ALWAYS destroy resources:** `terraform destroy` pärast testing'u!
2. **Use version constraints:** Pin provider versions production'is
3. **Never commit secrets:** Kasuta variables ja secrets management
4. **Test changes:** Alati `terraform plan` enne `apply`
5. **Document modules:** Hea README on pool võitu

---

**Edu ja head IaC'itamist!** 

