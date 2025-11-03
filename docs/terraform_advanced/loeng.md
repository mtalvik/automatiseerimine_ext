# Terraform Providerid ja Docker

**Eeldused:** Terraform põhitõed (loeng + labor), Docker põhiteadmised, Git

**Platvorm:** Docker (praktiline), cloud providers (kontseptuaalne ülevaade)

**Dokumentatsioon:** [registry.terraform.io](https://registry.terraform.io/)

## Õpiväljundid

Pärast seda loengut õpilane:

- Selgitab provider'i rolli Terraform'i arhitektuuris
- Kasutab Docker provider'it infrastruktuuri loomiseks
- Kirjeldab Docker ressursse: network, container, image, volume
- Võrdleb Docker ja cloud provider'ite põhimõtteid
- Mõistab, miks Docker sobib Terraform'i õppimiseks

---

## 1. Miks Local Provider Ei Piisa?

Terraform põhikursuses lõite faile - `local_file` resource kirjutas teksti kettale. See õpetas teile Terraform'i süntaksit ja workflow'i, aga see ei ole see, miks Terraform eksisteerib. Terraform loodi **infrastruktuuri haldamiseks** - serverid, võrgud, andmebaasid, load balancerid.

Local provider on nagu õppida autojuhtimist parklas. Kasulik alguses, aga mõttetu kui tahad tegelikult kuhugi sõita. Järgmine samm on päris infrastruktuur, ja me alustame Docker'iga - see annab teile päris infrastruktuuri kogemuse ilma cloud konto ja krediitkaarti vajamata.

---

## 2. Mis On Provider?

Provider on plugin, mis ühendab Terraform'i konkreetse platvormi API'ga. Terraform Core (see binaar, mille alla laadisite) ei tea midagi AWS'ist, Docker'ist ega ühestki teisest platvormist. Kogu platvormi-spetsiifiline teadmine tuleb provider'itest.

### Arhitektuur

```mermaid
graph TB
    A[Terraform Core<br/>HCL parser, state, planner] --> B[AWS Provider<br/>3000+ resources]
    A --> C[Azure Provider<br/>2000+ resources]
    A --> D[Docker Provider<br/>50+ resources]
    A --> E[Kubernetes Provider<br/>200+ resources]
    
    B --> F[AWS API]
    C --> G[Azure API]
    D --> H[Docker API]
    E --> I[Kubernetes API]
    
    F --> J[(AWS Cloud)]
    G --> K[(Azure Cloud)]
    H --> L[Docker Daemon]
    I --> M[K8s Cluster]
```

Terraform Core on orkestri dirigent - ta loeb teie konfiguratsioonifaili (noote), aga ta ise ei mängi ühtegi instrumenti. Instrumentide mängimise teevad provider'id, igaüks spetsialiseerunud ühele platvormile.

Kui käivitate `terraform init`, vaatab Terraform teie konfiguratsiooni ja laeb alla vajalikud provider'id **Terraform Registry'st**. Registry on avalik repositoorium üle 3000 erineva provider'iga - suurtest (AWS, Azure, GCP) kuni väikesteni (GitHub, Datadog, Discord).

### Provider Installimine

```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}
```

`source` määrab, kust provider tuleb. Formaat on `namespace/name` - kreuzwerker on kasutaja/organisatsioon, docker on provider'i nimi. `version = "~> 3.0"` tähendab "3.x, aga mitte 4.0" - automaatselt uueneb minor versioonidega (3.0 → 3.1 → 3.2), aga major versioon (4.0, mis võib koodi murda) ei uuene automaatselt.

`host` ütleb, kus Docker daemon asub. Linux'is on see tavaliselt `/var/run/docker.sock` socket fail.

[**Terraform Registry** - Browse 3000+ providers including AWS, Azure, GCP, Kubernetes](https://registry.terraform.io/browse/providers)

---

## 3. Docker Provider Põhjalikult

Docker provider on ideaalne Terraform'i õppimiseks ja arendamiseks. Kõik põhimõtted, mida siin õpite, töötavad täpselt samamoodi AWS'is, Azure'is või GCP's. Aga Docker on tasuta, kiire ja kohalik.

![Terraform workflow'i diagramm - näitab kuidas erinevad providerid töötavad sama workflow'iga](https://miro.medium.com/v2/resize:fit:1358/1*rojRn0kPfvk0fKnQElqbRQ.gif)

### Docker Image Resource

Image on template, millest tekivad containerid. Täpselt nagu AWS'is AMI (Amazon Machine Image) on template, millest tekivad EC2 serverid.

```hcl
resource "docker_image" "nginx" {
  name         = "nginx:alpine"
  keep_locally = false
}
```

`name` on Docker Hub'ist tulenud image. `nginx:alpine` tähendab nginx veebiserveri Alpine Linux baasil (väike, kiire). `keep_locally = false` tähendab, et kui Terraform kustutab selle resource'i, kustutatakse ka image kohalikust Docker'ist. Kui seatakse `true`, jääb image alles.

Terraform laeb image'i alla esimesel `terraform apply` käivitamisel. Kui image on juba kohalikult olemas, ei laadita uuesti alla.

```hcl
# Spetsiifiline versioon
resource "docker_image" "postgres" {
  name = "postgres:15.3"
}

# Latest (ohtlik production'is!)
resource "docker_image" "redis" {
  name = "redis:latest"
}
```

Production'is **mitte kunagi** `latest` tag'i. Täna võib `latest` olla versioon 7.0, homme 8.0 ja teie rakendus läheb katki. Alati spetsiifiline versioon.

### Docker Network Resource

Network loob isoleeritud võrgukeskkonna containeritele. Containerid samas network'is näevad üksteist DNS nime järgi, aga välised containerid ei näe.

```hcl
resource "docker_network" "app_network" {
  name   = "myapp-network"
  driver = "bridge"
  
  ipam_config {
    subnet  = "172.18.0.0/16"
    gateway = "172.18.0.1"
  }
}
```

`driver = "bridge"` on kõige levinum - see loob virtuaalse switch'i teie masinas. `subnet` määrab IP-aadresside vahemiku selles network'is. 172.18.0.0/16 tähendab 172.18.0.0 kuni 172.18.255.255 - kokku 65,536 aadressi. `gateway` on vaikimisi gateway aadress - läbi selle liiguvad paketid network'ist välja.

Network on nagu AWS'is VPC (Virtual Private Cloud) - isoleeritud võrgukeskkond, kus teie ressursid elavad.

```hcl
# Lihtne network ilma IPAM konfita
resource "docker_network" "simple" {
  name = "simple-network"
}
```

Kui te ei määra `ipam_config`, valib Docker automaatselt vaba IP vahemiku.

### Docker Container Resource

Container on "mini-server" - tal on oma protsessid, oma failisüsteem, oma võrguliides. AWS'is on analoogne EC2 instance.

```hcl
resource "docker_container" "web" {
  name  = "web-server"
  image = docker_image.nginx.image_id
  
  networks_advanced {
    name = docker_network.app_network.name
  }
  
  ports {
    internal = 80
    external = 8080
  }
  
  restart = "unless-stopped"
}
```

`image` viitab `docker_image.nginx.image_id`'le - see loob automaatse sõltuvuse. Terraform loob image enne container'it. `networks_advanced` ühendab container'i network'iga. `ports` mapib container'i pordi (80) host masina pordile (8080). Kui lähete http://localhost:8080, näete nginx'i.

`restart = "unless-stopped"` tähendab, et kui container crashib, käivitab Docker selle automaatselt uuesti. Kui te ise peatasite (`docker stop`), ei käivita uuesti.

**Keskkonnamuutujad:**

```hcl
resource "docker_container" "postgres" {
  name  = "database"
  image = docker_image.postgres.image_id
  
  env = [
    "POSTGRES_USER=myuser",
    "POSTGRES_PASSWORD=mypassword",
    "POSTGRES_DB=mydb"
  ]
  
  networks_advanced {
    name = docker_network.app_network.name
  }
}
```

Keskkonnamuutujad konfigureerivad container'i. PostgreSQL vajab kasutajanimme, parooli ja andmebaasi nime. Need antakse `env` listina.

**Volumes (püsiv salvestus):**

```hcl
resource "docker_volume" "postgres_data" {
  name = "postgres-data"
}

resource "docker_container" "postgres" {
  name  = "database"
  image = docker_image.postgres.image_id
  
  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }
  
  env = [
    "POSTGRES_USER=myuser",
    "POSTGRES_PASSWORD=mypassword"
  ]
}
```

Ilma volume'ita kaob PostgreSQL'i andmebaas, kui container kustutatakse. Volume on püsiv salvestusruum, mis jääb alles ka siis, kui container kustutatakse. AWS'is on analoogne EBS (Elastic Block Store) volume.

**Healthcheck:**

```hcl
resource "docker_container" "web" {
  name  = "web-server"
  image = docker_image.nginx.image_id
  
  healthcheck {
    test     = ["CMD", "curl", "-f", "http://localhost"]
    interval = "30s"
    timeout  = "3s"
    retries  = 3
  }
}
```

Healthcheck kontrollib, kas container töötab korralikult. Iga 30 sekundi tagant käivitab Docker `curl -f http://localhost`. Kui see ebaõnnestub 3 korda järjest, märgib container'i "unhealthy".

### Täielik Näide: Web + DB Stack

```hcl
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# Network
resource "docker_network" "app" {
  name = "app-network"
}

# Volume andmebaasile
resource "docker_volume" "db_data" {
  name = "postgres-data"
}

# Images
resource "docker_image" "postgres" {
  name = "postgres:15"
}

resource "docker_image" "nginx" {
  name = "nginx:alpine"
}

# Database container
resource "docker_container" "db" {
  name  = "postgres-db"
  image = docker_image.postgres.image_id
  
  networks_advanced {
    name = docker_network.app.name
  }
  
  volumes {
    volume_name    = docker_volume.db_data.name
    container_path = "/var/lib/postgresql/data"
  }
  
  env = [
    "POSTGRES_USER=dbuser",
    "POSTGRES_PASSWORD=dbpass",
    "POSTGRES_DB=appdb"
  ]
  
  restart = "unless-stopped"
}

# Web container
resource "docker_container" "web" {
  name  = "nginx-web"
  image = docker_image.nginx.image_id
  
  networks_advanced {
    name = docker_network.app.name
  }
  
  ports {
    internal = 80
    external = 8080
  }
  
  restart = "unless-stopped"
  
  # Web container sõltub DB'st
  depends_on = [docker_container.db]
}

# Outputs
output "web_url" {
  value = "http://localhost:${docker_container.web.ports[0].external}"
}

output "db_host" {
  value = docker_container.db.name
}
```

See loob täieliku web + database stack'i. Terraform teab automaatselt õige järjekorra:

1. Network
2. Volume
3. Images (paralleelselt)
4. DB container
5. Web container

`depends_on` on explicit dependency - isegi kui Terraform ei avasta automaatset sõltuvust, ütlete te: "Web vajab, et DB oleks valmis enne."

![Terraform template code example](https://www.opensourceforu.com/wp-content/uploads/2020/07/Figure-2-Terraform-template-code-for.jpg)

---

## 4. Docker vs Cloud Providerid

Kõik, mida Docker provider'iga õpite, töötab täpselt samamoodi cloud provider'ites. Ainult resource'ide nimed ja autentimine erinevad.

| Kontseptsioon | Docker | AWS | Azure | GCP |
|---------------|--------|-----|-------|-----|
| **Isoleeritud võrk** | `docker_network` | `aws_vpc` | `azurerm_virtual_network` | `google_compute_network` |
| **Arvutusressurss** | `docker_container` | `aws_instance` (EC2) | `azurerm_virtual_machine` | `google_compute_instance` |
| **Image/Template** | `docker_image` | `ami` (AMI ID) | `azurerm_image` | `google_compute_image` |
| **Püsiv salvestus** | `docker_volume` | `aws_ebs_volume` | `azurerm_managed_disk` | `google_compute_disk` |
| **Firewall** | Network policies | `aws_security_group` | `azurerm_network_security_group` | `google_compute_firewall` |

### Näide: Sama Loogika, Erinev Provider

**Docker:**
```hcl
resource "docker_network" "app" {
  name = "myapp-network"
}

resource "docker_container" "web" {
  name  = "web"
  image = "nginx:alpine"
  
  networks_advanced {
    name = docker_network.app.name
  }
}
```

**AWS (kui teil oleks konto):**
```hcl
resource "aws_vpc" "app" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "myapp-vpc"
  }
}

resource "aws_instance" "web" {
  ami           = "ami-0014ce3e52359afbd"
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public.id  # Viide subnet'ile
  
  tags = {
    Name = "web"
  }
}
```

Loogika on identne:
1. Loo isoleeritud võrk
2. Loo arvutusressurss võrku
3. Viita esimesele teisest (automaatne dependency)

Terraform workflow on identne:
```bash
terraform init    # Laeb provider'i
terraform plan    # Näitab, mis luuakse
terraform apply   # Loob ressursid
terraform destroy # Kustutab kõik
```

### Miks Docker On Õppimiseks Parem

**Kiirus.** AWS EC2 instance tekib 30-60 sekundiga. Docker container tekib 1-2 sekundiga. 30x kiirem iteratsioon.

**Tasuta.** AWS maksab raha (isegi Free Tier'il on piirangud ja vajab krediitkaarti). Docker on täiesti tasuta.

**Kohalik.** Kui internet kaob, Docker töötab endiselt. AWS mitte.

**Vigadest taastumine.** Kui kustutate kogemata Docker container'i, pole midagi hullu - `terraform apply` ja 2 sekundit hiljem on tagasi. Kui kustutate kogemata production EC2 instance'i AWS'is... see on "resume-generating event".

**Sama põhimõte.** Resources, state, dependencies, outputs, modules - kõik töötab täpselt samamoodi. Kui mõistate Terraform'i Docker'iga, oskate te kasutada seda AWS'iga.

---

## 5. Cloud Providerid - Kiire Ülevaade

Te ei saa täna neid kasutada (vajab krediitkaarti ja cloud kontot), aga te peaksite teadma, mis on olemas.

### Kolm Suurt

| Provider | Ressursse | Tugevus | Eesti Kasutus |
|----------|-----------|---------|---------------|
| **AWS** | 3000+ | Suurim, kõige rohkem teenuseid | Bolt, Wise, Pipedrive |
| **Azure** | 2000+ | Microsoft ökosüsteem, hybrid cloud | Playtech, pangad |
| **GCP** | 1500+ | ML/AI, analytics, data | Bolt (ML), startupid |

**AWS (Amazon Web Services)** on turuliider. Kui te ei tea, kumba valida, valige AWS. Dokumentatsioon on parim, kogukond on suurim, töökuulutused mainivad AWS'i kõige sagedamini.

**Azure (Microsoft)** on teine. Tugev kui kasutate Microsoft tooteid (Active Directory, Office 365, .NET). Paljud suured ettevõtted (pangad, valitsus) on juba Microsoft kliendinumber ja saavad Azure'i soodsalt.

**GCP (Google Cloud Platform)** on kolmas. Tugevad ML/AI tööriistad (TensorFlow, BigQuery). Bolt kasutab GCP'd machine learning'i jaoks, aga infrastruktuuri jaoks AWS'i.

### Autentimine (põgusalt)

Iga provider vajab credentials'eid. Need ei tohi **mitte kunagi** olla koodis.

```hcl
# VALE - credentials koodis
provider "aws" {
  access_key = "AKIAIOSFODNN7EXAMPLE"  # MITTE KUNAGI!
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

# ÕIGE - credentials keskkonnamuutujates
provider "aws" {
  region = "eu-north-1"
  # AWS_ACCESS_KEY_ID ja AWS_SECRET_ACCESS_KEY keskkonnast
}
```

Docker ei vaja credentials'eid, sest te jooksutate Terraform'i samas masinas, kus Docker daemon töötab. Cloud provider'ites on vaja tõestada, et te olete see, kes te väidate end olevat.

### Multi-Cloud

Terraform võib hallata mitut provider'it korraga. See on haruldane, aga võimalik.

```hcl
# AWS-is andmebaas
resource "aws_db_instance" "postgres" {
  engine         = "postgres"
  instance_class = "db.t3.micro"
}

# Azure'is veebirakendus
resource "azurerm_app_service" "web" {
  name     = "myapp"
  location = "West Europe"
}

# Docker'is arenduskeskkond
resource "docker_container" "dev" {
  image = "myapp:dev"
}
```

**Reaalsus:** 90%+ ettevõtetest kasutab single-cloud'i. Multi-cloud on keerukas, kallis ja nõuab spetsiaalset ekspertiisi. Aga Terraform **võimaldab** seda, kui vaja - kui alustate AWS'iga ja hiljem otsustate Azure'i lisada, ei pea te kõike ümber kirjutama.

**Bolt näide:** AWS põhiliselt, GCP machine learning'i jaoks. Kaks provider'it ühes Terraform projektis. Aga see pole norm - see on erand.

---

## 6. Järgmine Samm

Täna õppisime, kuidas Terraform töötab provider'itega ja süvenesime Docker provider'isse. Järgmises labor'is rakendame neid kontseptsioone praktiliselt:

**Te loote:**
- Docker network'i (isoleeritud võrk)
- Mitu container'it (web + database)
- Volume'id (püsiv andmesalvestus)
- Outputs (info resource'ide kohta)

**Te õpite:**
- Provider konfigureerimine
- Resource dependencies (automaatsed ja explicit)
- Multi-container aplikatsioonid
- State management päris ressurssidega
- Debugging (kui midagi läheb valesti)

Kui mõistate neid kontseptsioone Docker'iga, mõistate te neid AWS'iga, Azure'ga, GCP'ga - igaühe provider'iga Registry's.

---

## Kokkuvõte

**Provider on plugin**, mis ühendab Terraform'i konkreetse platvormi API'ga. Terraform Core ei tea midagi platvormidest - kogu teadmine tuleb provider'itest.

**Docker provider** annab teile päris infrastruktuuri kogemuse ilma cloud konto vajaduseta. Network, container, image, volume - need on samad kontseptsioonid, mida cloud provider'id kasutavad.

**Kõik provider'id järgivad sama pattern'i**: sama workflow (init → plan → apply → destroy), sama HCL süntaks, sama state management. Kui olete õppinud ühe provider'i, mõistate teisi.

**Cloud providerid** (AWS, Azure, GCP) on võimsad, aga kallid ja vajavad krediitkaarti. Õppige Docker'iga, rakendage cloud'is kui vaja.

---

## Ressursid

**Dokumentatsioon:**
- [Terraform Registry](https://registry.terraform.io/) - 3000+ provider'it
- [Docker Provider Docs](https://registry.terraform.io/providers/kreuzwerker/docker/latest/docs)
- [Docker Official Images](https://hub.docker.com/search?q=&type=image&image_filter=official)

**Õppimine:**
- [HashiCorp Learn - Docker](https://developer.hashicorp.com/terraform/tutorials/docker-get-started)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

**Tulevikuks (kui vajate cloud'i):**
- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

---

**Järgmine:** Labor - Docker provider hands-on praktika, loome päris infrastruktuuri
