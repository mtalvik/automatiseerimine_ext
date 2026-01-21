# Terraform Alused

**Eeldused:** Linux CLI, Git, teksteditor, IaC põhimõtted (Ansible kursusest)

**Platvorm:** Terraform (kohalik)

**Dokumentatsioon:** [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)

## Õpiväljundid

Pärast seda loengut sa:

- Eristad Terraform'i Ansible'ist ja teistest IaC tööriistadest
- Kirjeldad Terraform'i arhitektuuri komponente (Core, Providers, State)
- Mõistad deklaratiivset lähenemist ja idempotentsust
- Tunned HCL süntaksit ja põhielemente
- Tead Terraform workflow'd: init, plan, apply, destroy

---

## 1. Terraform ja teised tööriistad

Ansible'iga olete juba tuttavad - see konfigureerib olemasolevat infrastruktuuri. Installid pakette, kopeerid faile, käivitad teenuseid. Aga kust tulevad need serverid, mida Ansible konfigureerib? Keegi peab need enne looma. Siin tuleb mängu Terraform.

Terraform on infrastruktuuri loomise tööriist. Kui Ansible on "sisekujundaja", kes paneb majja mööbli ja värvib seinad, siis Terraform on "ehitaja", kes ehitab maja ise - vundamendi, seinad, katuse. Praktikas töötavad need tööriistad koos: Terraform loob serverid pilves, seejärel Ansible konfigureerib need serverid, ja lõpuks Kubernetes jooksutab neil rakendustel.

![Kuidas Terraform töötab](https://media.geeksforgeeks.org/wp-content/uploads/20241212151316849879/How-does-Terraform-work.webp)

### Miks mitte kasutada Ansibled infrastruktuuri loomiseks?

Ansible saab tehniliselt ka infrastruktuuri luua - olemas on `amazon.aws.ec2_instance` moodul ja sarnased. Aga Terraform on selleks tööks parem mitmel põhjusel.

Esiteks, state management. Terraform peab arvet, mis ressursid on juba loodud. Kui kirjutad konfiguratsiooni "tahan 5 serverit" ja 3 on juba olemas, loob Terraform ainult 2 juurde. Ansible seevastu loob 5 uut serverit, sest tal puudub mälu varasematest käivitustest. Tulemuseks on 8 serverit ja ootamatult suur arve.

Teiseks, planeerimine. Terraform'i `plan` käsk näitab ette, mis täpselt muutub, enne kui midagi tehakse. Sa näed, et "luuakse 2 serverit, kustutatakse 1, muudetakse 3 security groupi". Ansible'il sellist sisseehitatud funktsionaalsust pole - sa käivitad playbooki ja loodad parimat.

Kolmandaks, sõltuvuste graaf. Terraform mõistab automaatselt, et VPC tuleb luua enne subnetti ja subnet enne serverit. Ta ehitab sõltuvuste graafi ja paralleliseerib kõik, mis võimalik. Ansible'is pead sa ise järjekorra määrama ja kui unustad midagi, siis playbook kukub läbi.

Neljandaks, elutsükli haldus. Terraform teab vahet, millal ressurss vajab uuesti loomist (replace) versus millal piisab uuendamisest (update). Näiteks kui muudad EC2 instance'i AMI'd, siis Terraform teab, et vana tuleb kustutada ja uus luua. Ansible'is pead selle loogika ise kirjutama.

### Terraform versus CloudFormation

CloudFormation on AWS-i enda IaC tööriist. Kui su ettevõte kasutab ainult AWS-i ja plaanib seda teha igavesti, siis CloudFormation on täiesti mõistlik valik - AWS haldab state'i sinu eest ja integratsioon on sügav.

Aga enamik ettevõtteid ei ole 100% ühes pilves. Täna AWS, homme võib-olla Azure'i või GCP projekt. Terraform töötab kõigi nendega sama süntaksiga. Õpid ühe korra ja kasutad kõikjal. See on Terraformi peamine eelis - sa ei ole lukustatud ühe pilveteenuse pakkuja külge.

![Multi-Cloud](https://miro.medium.com/v2/resize:fit:627/1*OiA514LNzKtDij8cSVrKeA.png)

![Terraform Key Features](https://nxos-devops.ciscolive.com/lab/static/images/terraform/terraform-1.jpg)

---

## 2. Terraform arhitektuur

Terraformi arhitektuur koosneb kolmest põhikomponendist, mida on oluline mõista enne praktilise tööga alustamist.

```
┌─────────────────────────────────────────────────────────┐
│                    TERRAFORM CORE                       │
│    Loeb .tf faile, võrdleb state'iga, teeb plaani      │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ AWS Provider│  │Azure Provider│  │Local Provider│
│  (plugin)   │  │   (plugin)  │  │   (plugin)  │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       ▼                ▼                ▼
     [AWS]           [Azure]      [Local Files]

┌─────────────────────────────────────────────────────────┐
│              terraform.tfstate (JSON)                   │
│         Mis ressursid on loodud + nende ID'd            │
└─────────────────────────────────────────────────────────┘
```

### Core

Core on Terraformi "aju" - see on `terraform` binaar, mille sa installid. Core loeb sinu `.tf` konfiguratsioonifaile, loeb state faili (kui see eksisteerib), võrdleb neid omavahel ja koostab plaani. Oluline on mõista, et Core ise ei tea midagi AWS-ist, Azure'ist ega ühestki teisest platvormist. Ta on üldotstarbeline mootor, mis delegeerib konkreetse töö provideritele.

### Providers

Provider on plugin, mis räägib konkreetse platvormi API-ga. Kui sa kirjutad `resource "aws_instance"`, siis Core saab aru, et see ressurss kuulub AWS providerile, ja delegeerib töö sinna. Provider teab, kuidas AWS API-ga suhelda, milliseid parameetreid vaja on, ja kuidas vastuseid tõlgendada.

Providerid ei ole Terraformi osad - need on eraldi binarid, mille `terraform init` alla laeb. Terraform Registry's on üle 3000 provideri: AWS, Azure, GCP, Kubernetes, Docker, GitHub, Cloudflare, ja palju muud. Laboris kasutame `local` providerit, mis loob kohalikke faile - see ei vaja kontot ega maksekaarti, ideaalne õppimiseks.

### State

State on `terraform.tfstate` fail, mis on Terraformi mälu. See JSON fail sisaldab infot kõigi loodud ressursside kohta: nende ID-d, IP-aadressid, omavahelised sõltuvused, ja muu metadata.

Miks on state nii kriitiline? Ilma selleta ei suuda Terraform teha vahet, kas ressurss on juba olemas või mitte. Kui ütled "tahan 3 serverit" ja käivitad `apply` kaks korda, siis ilma state'ita saaksid 6 serverit. State'iga teab Terraform, et 3 on olemas ja ei tee midagi.

State'iga tuleb olla ettevaatlik, sest see võib sisaldada tundlikku infot - paroole, API võtmeid, andmebaasi connection string'e. Seetõttu ei tohi state faili kunagi Git'i panna. Lisa `.gitignore` faili read `*.tfstate`, `*.tfstate.*` ja `.terraform/`. Production keskkonnas kasutatakse remote backend'i nagu S3 või Azure Blob Storage, kus state on krüpteeritud ja versioonitud, aga seda käsitleme hilisemates tundides.

---

## 3. Deklaratiivne versus imperatiivne

Ansible'iga töötades kirjutasid sa task'e, mis kirjeldasid samme: "installi pakett", "kopeeri fail", "käivita teenus". See on imperatiivne lähenemine - sa ütled, KUIDAS midagi teha. Terraform kasutab deklaratiivset lähenemist - sa kirjeldad, MIDA tahad saada, ja Terraform väljastab sammud ise.

Vaatame konkreetset näidet. Ansible'is viie faili loomiseks kirjutaksid midagi sellist:

```yaml
- name: Loo failid
  file:
    path: "/tmp/file{{ item }}.txt"
    state: touch
  loop: [1, 2, 3, 4, 5]
```

Terraformis sama tulemus:

```hcl
resource "local_file" "files" {
  count    = 5
  filename = "/tmp/file${count.index + 1}.txt"
  content  = "File ${count.index + 1}"
}
```

Esmapilgul tunduvad need sarnased, aga erinevus tuleb välja muudatuste tegemisel. Kui muudad Ansible playbooki `loop: [1, 2, 3]` peale, siis Ansible lihtsalt jätab failid 4 ja 5 alles - ta ei tea, et need tuleks kustutada. Pead ise kirjutama eraldi cleanup task'i. Terraformis muudad `count = 3` peale ja Terraform ütleb: "On 5 faili, peab olema 3, kustutan 2." See on deklaratiivse lähenemise võlu - sa kirjeldad soovitud lõppseisu ja tööriist väljastab, kuidas sinna jõuda.

### Idempotentsus

Mõlemad tööriistad on idempotentsed, aga erineval viisil. Ansible'is kontrollib iga task ise, kas muudatus on vajalik - `state: present` versus `state: absent`. Terraformis teeb seda tööd state fail. Kui käivitad `terraform apply` sada korda järjest, tehakse muudatusi ainult esimesel korral. Ülejäänud 99 korda ütleb Terraform "No changes needed" ja ei tee midagi.

See käitumine on oluline mõista, sest see tähendab, et sa võid julgelt käivitada `terraform apply` ka siis, kui pole kindel, kas muudatusi on vaja. Terraform kontrollib ise ja teeb ainult seda, mis vajalik.

---

## 4. HCL süntaks

HCL (HashiCorp Configuration Language) on Terraformi konfiguratsioonikeel. See on loodud olema inimloetav ja -kirjutatav, JSON-i alternatiiv, mis on vähem verbose.

### Põhistruktuur

HCL koosneb plokkidest. Iga plokk algab tüübiga, millele järgnevad sildid ja loogelistes sulgudes sisu. Põhistruktuur on `<BLOCK_TYPE> "<LABEL1>" "<LABEL2>" { ... }`. Kõige olulisem ploki tüüp on `resource`, mis defineerib midagi, mida Terraform loob ja haldab. Ressursil on kaks silti: tüüp (mis provideri ressurss) ja nimi (sinu valitud identifikaator).

```hcl
resource "local_file" "greeting" {
  filename = "/tmp/hello.txt"
  content  = "Tere, Terraform!"
}
```

Selles näites on `local_file` ressursi tüüp (local provideri file ressurss) ja `greeting` on nimi, mida kasutad viitamiseks teistes kohtades. `filename` ja `content` on argumendid, mis määravad, mida täpselt luuakse.

### Viitamine teistele ressurssidele

Ressursid saavad viidata teiste ressursside atribuutidele. Süntaks on `<TYPE>.<NAME>.<ATTRIBUTE>`. Kui kasutad viitamist, mõistab Terraform automaatselt, et tekib sõltuvus - viidatav ressurss tuleb luua enne viitavat.

```hcl
resource "local_file" "config" {
  filename = "/tmp/config.txt"
  content  = "port=8080"
}

resource "local_file" "readme" {
  filename = "/tmp/readme.txt"
  content  = "Config asub: ${local_file.config.filename}"
}
```

Terraform teab nüüd, et `config` tuleb luua enne `readme`'d, sest `readme` viitab `config`'i atribuudile.

### Muutujad

Muutujad teevad konfiguratsiooni dünaamiliseks. Deklareerid muutuja `variable` plokiga ja kasutad seda `var.<nimi>` süntaksiga.

```hcl
variable "environment" {
  description = "Keskkond (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "file_count" {
  description = "Mitu faili luua"
  type        = number
  default     = 3
}

resource "local_file" "app" {
  count    = var.file_count
  filename = "/tmp/${var.environment}-${count.index}.txt"
  content  = "Environment: ${var.environment}"
}
```

Muutuja väärtust saad anda mitmel viisil: käsurealt (`terraform apply -var="environment=prod"`), failist `terraform.tfvars` (mida Terraform loeb automaatselt), või keskkonnamuutujast (`TF_VAR_environment=prod`).

### Väljundid

Väljundid (outputs) võimaldavad kuvada infot pärast ressursside loomist. See on kasulik näiteks serveri IP-aadressi või URL-i kuvamiseks.

```hcl
output "file_paths" {
  description = "Loodud failide teed"
  value       = local_file.app[*].filename
}
```

### Tüübid ja andmestruktuurid

HCL toetab mitmeid andmetüüpe. Primitiivsed tüübid on `string`, `number` ja `bool`. Komplekssed tüübid on `list` (järjestatud kogum), `set` (unikaalsete väärtuste kogum), `map` (võti-väärtus paarid) ja `object` (kindla struktuuriga objekt).

```hcl
variable "ports" {
  type    = list(number)
  default = [80, 443, 8080]
}

variable "tags" {
  type = map(string)
  default = {
    env   = "dev"
    owner = "team-a"
  }
}
```

### Tingimuslik loogika ja tsüklid

Tingimuslik loogika kasutab ternary operaatorit: `condition ? true_value : false_value`. Näiteks `filename = var.environment == "prod" ? "/etc/app.conf" : "/tmp/app.conf"`.

Tsükliteks on kaks võimalust. `count` on lihtne - määrad arvu ja kasutad `count.index` väärtust. `for_each` on paindlikum - saad itereerida üle map'i või set'i, kasutades `each.key` ja `each.value` väärtusi.

```hcl
# count näide
resource "local_file" "files" {
  count    = 3
  filename = "/tmp/file-${count.index}.txt"
  content  = "File number ${count.index}"
}

# for_each näide
resource "local_file" "configs" {
  for_each = {
    "web"    = "port=80"
    "api"    = "port=8080"
    "worker" = "threads=4"
  }
  filename = "/tmp/${each.key}.conf"
  content  = each.value
}
```

---

## 5. Terraform workflow

Terraformi kasutamine järgib kindlat töövoogu: `init`, `plan`, `apply`, ja vajadusel `destroy`. Seda tsüklit korratakse iga muudatuse tegemisel.

![Terraform workflow](https://assets.bytebytego.com/diagrams/0225-how-terraform-creates-infra-at-scale.png)

### terraform init

Esimene käsk, mida uues projektis käivitad. See valmistab projekti ette: laeb alla vajalikud providerid, initsialiseerib backend'i (kuhu state salvestatakse), ja loob `.terraform/` kausta. Seda käsku tuleb käivitada iga kord, kui kloonid repo, lisad uue provideri, või muudad backend konfiguratsiooni.

### terraform plan

See käsk on sinu parim sõber. Ta näitab, mis täpselt muutub, ilma et midagi päriselt teeks. Väljundis näed sümboleid: `+` tähendab loomist, `-` kustutamist, `~` muutmist, ja `-/+` kustutamist ja uuesti loomist. Hea praktika on alati käivitada `plan` enne `apply` - nii ei tule üllatusi.

Veelgi parem praktika on salvestada plan faili: `terraform plan -out=tfplan`. Seejärel saad teha `terraform apply tfplan` ja oled kindel, et rakendatakse täpselt see, mida nägid.

### terraform apply

See käsk rakendab muudatused päriselt. Terraform näitab plaani ja küsib kinnitust. Kui oled kindel, et tead, mida teed (näiteks CI/CD pipeline'is), võid kasutada `-auto-approve` lippu, mis jätab kinnituse küsimata.

### terraform destroy

See käsk kustutab kõik ressursid, mida Terraform haldab. Kasuta ettevaatlikult - see on pöördumatu. Production ressursside kaitseks saad kasutada `lifecycle` plokki koos `prevent_destroy = true` argumendiga.

---

## 6. Failide struktuur

Terraform loeb kõik `.tf` laiendiga failid kataloogist ja käsitleb neid ühe konfiguratsioonina. Failide nimed ei ole olulised - võid kogu koodi panna ühte `main.tf` faili või jagada mitmeks failiks.

![Terraform projekti struktuur](https://miro.medium.com/v2/resize:fit:720/format:webp/1*4hswCxEEkkZtU6-ddp_riA.png)

Tüüpiline projekti struktuur suuremate projektide puhul jagab koodi loogiliselt: `main.tf` põhiliste ressursside jaoks, `variables.tf` muutujate deklaratsioonide jaoks, `outputs.tf` väljundite jaoks, `providers.tf` providerite konfiguratsiooni jaoks, ja `terraform.tfvars` muutujate väärtuste jaoks. Väikeste projektide puhul on täiesti OK hoida kõike ühes `main.tf` failis.

Oluline on `.gitignore` - lisa sinna `*.tfstate`, `*.tfstate.*` ja `.terraform/`. State failid ei tohi Git'i minna, sest need võivad sisaldada tundlikku infot.

---

## Kokkuvõte

Terraform on infrastruktuuri loomise tööriist, mis täiendab Ansibled - Terraform loob serverid, Ansible konfigureerib need. Terraformi arhitektuur koosneb Core'ist (mis loeb konfiguratsiooni ja teeb plaane), Provideritest (mis räägivad platvormide API'dega), ja State'ist (mis mäletab, mis on loodud).

Terraform kasutab deklaratiivset lähenemist - sa kirjeldad soovitud lõppseisu ja Terraform väljastab sammud sinna jõudmiseks. State fail tagab idempotentsuse: sama konfiguratsiooni korduv rakendamine ei loo duplikaate.

HCL on Terraformi konfiguratsioonikeel, mis sisaldab ressursse, muutujaid, väljundeid, ja toetab tingimuslikku loogikat ning tsükleid. Töövoog on lihtne: `init` valmistab ette, `plan` näitab muudatusi, `apply` rakendab need.

---

## Kasulikud ressursid

- [Terraform Docs](https://developer.hashicorp.com/terraform/docs) - ametlik dokumentatsioon
- [Terraform Registry](https://registry.terraform.io/) - providerid ja moodulid
- [Local Provider Docs](https://registry.terraform.io/providers/hashicorp/local/latest/docs) - laboris kasutame seda

Järgmisena: **Labor** - loome päris ressursse local provideriga.
