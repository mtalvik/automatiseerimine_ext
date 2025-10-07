#  Terraform Lisapraktika

**Eeltingimused:** Terraform põhiteadmised, HCL süntaks

---

##  Ülevaade

See fail sisaldab lisapraktikaid Terraform mooduli jaoks, sealhulgas advanced HCL, count/for_each, data sources, ja real-world scenarios.

---

##  Õpiväljundid

Pärast lisapraktikat oskate:

- Kasutada `count` ja `for_each` dünaamiliste ressursside jaoks
- Data sources'idega olemasolevaid ressursse leida
- Conditional logic ja expressions HCL'is
- Terraform functions (lookup, merge, join, etc.)
- Complex variable structures (maps, objects)

---

##  Count ja For_Each

### Count - Lihtne Loop
```hcl
# Loo 5 faili
resource "local_file" "logs" {
  count    = 5
  filename = "log-${count.index}.txt"
  content  = "Log file #${count.index}"
}

# Access: local_file.logs[0], local_file.logs[1], ...
```

### For_Each - Map-Based
```hcl
variable "users" {
  type = map(object({
    role  = string
    email = string
  }))
  default = {
    alice = { role = "admin", email = "alice@example.com" }
    bob   = { role = "user", email = "bob@example.com" }
  }
}

resource "local_file" "user_configs" {
  for_each = var.users
  filename = "users/${each.key}.json"
  content = jsonencode({
    username = each.key
    role     = each.value.role
    email    = each.value.email
  })
}
```

### Ülesanne 1: Dünaamiline Infrastructure

Loo Terraform kood, mis genereerib:
- 3 kausta: `dev/`, `staging/`, `prod/`
- Igas kaustas: `config.yaml`, `secrets.txt` (encrypted), `README.md`
- Kasuta `for_each` ja variables

---

##  Data Sources

### Existing Resources
```hcl
# Leia olemasolev fail
data "local_file" "existing" {
  filename = "path/to/existing.txt"
}

# Kasuta sisu
resource "local_file" "derived" {
  filename = "derived.txt"
  content  = "Based on: ${data.local_file.existing.content}"
}
```

### External Data
```hcl
data "external" "git_info" {
  program = ["bash", "-c", <<-EOT
    echo "{\"commit\":\"$(git rev-parse HEAD)\",\"branch\":\"$(git branch --show-current)\"}"
  EOT
  ]
}

resource "local_file" "build_info" {
  filename = "build-info.json"
  content = jsonencode({
    commit = data.external.git_info.result.commit
    branch = data.external.git_info.result.branch
    time   = timestamp()
  })
}
```

---

##  Terraform Functions

### String Functions
```hcl
locals {
  upper_env = upper(var.environment)     # "PROD"
  formatted = format("app-%s-%03d", var.env, var.instance)  # "app-dev-001"
  joined    = join("-", ["web", "server", var.region])      # "web-server-eu"
}
```

### Collection Functions
```hcl
variable "ports" {
  default = [80, 443, 8080]
}

locals {
  # Merge lists
  all_ports = concat(var.ports, [9090, 3000])
  
  # Filter
  secure_ports = [for p in var.ports : p if p > 443]
  
  # Transform
  port_strings = [for p in var.ports : tostring(p)]
}
```

### Map/Object Functions
```hcl
locals {
  defaults = {
    region = "eu-west-1"
    env    = "dev"
  }
  
  overrides = {
    env = "prod"
  }
  
  # Merge (overrides win)
  config = merge(local.defaults, local.overrides)
  # Result: { region = "eu-west-1", env = "prod" }
  
  # Lookup with default
  timeout = lookup(var.settings, "timeout", 30)
}
```

### Ülesanne 2: Dynamic Configuration Generator

Loo Terraform kood, mis:
- Võtab map of services (name → config)
- Genereerib iga service jaoks nginx config
- Kasuta `for_each`, `templatefile()`, ja `merge()`

---

##  Conditional Logic

### Count Tricks
```hcl
variable "create_backup" {
  type    = bool
  default = false
}

resource "local_file" "backup" {
  count    = var.create_backup ? 1 : 0
  filename = "backup.txt"
  content  = "Backup enabled"
}
```

### Conditional Expressions
```hcl
locals {
  environment = var.env == "prod" ? "production" : "development"
  
  log_level = (
    var.debug ? "DEBUG" :
    var.env == "prod" ? "ERROR" :
    "INFO"
  )
}
```

### Dynamic Blocks
```hcl
variable "enable_https" {
  type = bool
}

resource "something" "example" {
  name = "example"
  
  dynamic "https_config" {
    for_each = var.enable_https ? [1] : []
    content {
      cert_path = "/path/to/cert"
      key_path  = "/path/to/key"
    }
  }
}
```

---

##  Real-World Scenario: Web Stack
```hcl
# variables.tf
variable "environments" {
  type = map(object({
    replicas    = number
    memory_mb   = number
    enable_https = bool
    domains     = list(string)
  }))
  default = {
    dev = {
      replicas     = 1
      memory_mb    = 512
      enable_https = false
      domains      = ["dev.example.local"]
    }
    prod = {
      replicas     = 3
      memory_mb    = 2048
      enable_https = true
      domains      = ["example.com", "www.example.com"]
    }
  }
}

# main.tf
resource "local_file" "nginx_configs" {
  for_each = var.environments
  
  filename = "nginx/${each.key}.conf"
  content = templatefile("templates/nginx.tpl", {
    env          = each.key
    replicas     = each.value.replicas
    memory       = each.value.memory_mb
    domains      = each.value.domains
    enable_https = each.value.enable_https
  })
}

# Output upstream servers
output "upstreams" {
  value = {
    for env, config in var.environments :
    env => [
      for i in range(config.replicas) :
      "server-${env}-${i}"
    ]
  }
}
```

### Ülesanne 3: Multi-Environment Setup

Loo terraform projekt, mis genereerib:
- Dev, staging, prod environments
- Igal: nginx config, app config, database init script
- Conditional: prod'is SSL, dev'is debug mode
- Kasuta `for_each`, `dynamic`, `templatefile()`

---

##  Lifecycle Rules
```hcl
resource "local_file" "important" {
  filename = "important.txt"
  content  = var.content
  
  lifecycle {
    # Ära kunagi kustuta (even if removed from code)
    prevent_destroy = true
    
    # Ignoreeri content muudatusi
    ignore_changes = [content]
    
    # Loo uus enne vana kustutamist
    create_before_destroy = true
  }
}
```

---

##  Modules Advanced

### Module with Conditional Resources
```hcl
# modules/webserver/main.tf
variable "enable_monitoring" {
  type    = bool
  default = false
}

resource "local_file" "app_config" {
  filename = "config.yaml"
  content  = "..."
}

resource "local_file" "monitoring_config" {
  count    = var.enable_monitoring ? 1 : 0
  filename = "monitoring.yaml"
  content  = "..."
}

# Usage
module "web_dev" {
  source            = "./modules/webserver"
  enable_monitoring = false
}

module "web_prod" {
  source            = "./modules/webserver"
  enable_monitoring = true
}
```

### Module Outputs as Inputs
```hcl
module "network" {
  source = "./modules/network"
}

module "servers" {
  source     = "./modules/servers"
  network_id = module.network.network_id  # Chaining!
}
```

---

##  Challenge: Infrastructure Generator

**Ülesanne:** Loo "Infrastructure as Data" generaator

**Input** (`infrastructure.yaml`):
```yaml
projects:
  - name: web-app
    environments:
      - name: dev
        services:
          - name: api
            port: 8080
            replicas: 1
          - name: db
            port: 5432
            replicas: 1
      - name: prod
        services:
          - name: api
            port: 8080
            replicas: 3
          - name: db
            port: 5432
            replicas: 2
```

**Output:** Terraform genereerib:
- Directory structure
- Docker Compose files
- Nginx configs
- Init scripts
- README'ed

**Nõuded:**
- [ ] Parse YAML (`yamldecode()`)
- [ ] Nested `for_each` loops
- [ ] Templates
- [ ] Conditional logic
- [ ] Outputs summary



---

##  Kasulikud Ressursid

- **HCL Syntax**: https://developer.hashicorp.com/terraform/language/syntax
- **Functions**: https://developer.hashicorp.com/terraform/language/functions
- **Expressions**: https://developer.hashicorp.com/terraform/language/expressions
- **Modules**: https://developer.hashicorp.com/terraform/language/modules

---

**Edu advanced Terraform'iga!** 
