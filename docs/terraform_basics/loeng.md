# Terraform Alused

**Eeldused:** Linux CLI, Git, teksteditor

**Platvorm:** Terraform (kohalik)

**Dokumentatsioon:** [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)

## Õpiväljundid

- Selgitad Infrastructure as Code eeliseid konkreetsete näidetega
- Eristad Terraform'i teistest IaC tööriistadest
- Kirjeldad Terraform'i arhitektuuri komponente
- Mõistad deklaratiivset lähenemist vs imperatiivne
- Kirjutad HCL koodi põhielemente
- Kasutad Terraform workflow'i: init, plan, apply

---

## 1. Miks Me Vajame Infrastructure as Code?

Eesti DevOps tõde: "Kui teed midagi käsitsi üle kahe korra, oled sa juba teinud seda liiga palju kordi."

### Käsitsi Seadistamise Õudusunenägu

Kujutage ette tüüpilist esmaspäeva Tallinna startup'is. CEO teatab kell üheksa hommikul, et test keskkonda on vaja reedeks. DevOps insener avab AWS Console'i, loeb dokumentatsiooni, klõbistab nuppudel ja valib seadeid. Kell kaksteist selgub, et valitud on vale instance type. Kustutada kõik, alustada uuesti. Kell kaks päeval on lõpuks valmis. Kell kolm teatatakse, et tegelikult on vaja viis serverit, mitte üks. Sisse hingamine.

See pole naljaasi. See on päris elu paljudes ettevõtetes, kus infrastruktuuri seadistamine toimub käsitsi graafilises kasutajaliideses.

### Probleemid

Käsitsi seadistamine toob kaasa mitmeid fundamentaalseid probleeme. Aeglane: iga server võtab 20-30 minutit käsitsi seadistada, viis serverit tähendavad tervet päeva tööd. Pipedrive kogemused näitavad, et käsitsi seadistamine võttis kaks päeva seal, kus Terraform lahendab sama küsimuse kümneks minutiks.

Vigaderohne: inimesed teevad vigu. Üks unustatud tulemüüri reegel, vale security group, vale instance type - ja kogu süsteem ei tööta ootuspäraselt. Uuringud näitavad, et käsitsi seadistatud keskkondades on kuni 40% infrastruktuurist erinev production ja staging vahel, sest keegi unustas midagi kopeerida või seadistas midagi teisiti.

Dokumenteerimata: 6 kuud hiljem ei tea keegi täpselt, mis seal AWS konsoolis tehti. Confluence dokumentatsioon on aegunud või puudulik. Algne insener on lahkunud. Uus inimene peab alustama nullist ja aimama.

Ei kordu: iga kord kui seadistad käsitsi, tekib natuke erinev tulemus. Need on nn "snowflake" serverid - iga server on unikaalne lumehelves, mitte standardiseeritud toode. Debuggimine muutub keeruliseks.

Koostöö raske: kaks inimest ei saa samaaegselt töötada AWS konsoolis sama keskkonna kallal. Konfliktid on paratamatud. Keegi kirjutab teise muudatused üle, keegi ei tea mida teine tegi.

| Probleem | Põhjus | Mõju | Päris Näide |
|----------|--------|------|-------------|
| Aeglane | Iga server käsitsi | 5 serverit = terve päev | Pipedrive: 2 päeva vs 10 min |
| Vigane | Inimesed eksivad | "Töötab minu masinas" | 40% infrastruktuur erinev |
| Dokumenteerimata | Keegi ei viitsi | 6 kuud hiljem ??? | Confluence 3 kuud vana |
| Ei kordu | Iga kord erinev | Unique snowflake | Iga server natuke teine |
| Koostöö raske | Kaks inimest = kaos | Konfliktid | "Kes seda muutis?!" |

### Päris Lugu: 30,000 Euro Viga

Tallinna fintech'is 2023. aastal seadistas DevOps insener production keskkonna käsitsi AWS'is. Kaks nädalat tööd. Kõik "dokumenteeritud" Confluence'is. Kolm kuud hiljem vajati staging keskkonda. Algne insener oli vahepeal lahkunud Bolt'i parema palga pärast.

Uus inimene proovis dokumentatsiooni järgida. Tulemus: staging oli 40% erinev production'ist. Bug'id, mis staging'us ei ilmnenud, plahvatasid production'is. Downtime. Kliendid vihased. CEO veel vihasem. Hind: 30,000 eurot + 200 tundi debuggimist + üks väga kurb DevOps insener. Õppetund: käsitsi seadistamine ei skaleeru.

### Lahendus: Infrastructure as Code

IaC tähendab, et infrastruktuur kirjutatakse koodina. Mitte klõpsamine, mitte nuppude vajutamine - kood. Sama nagu rakenduse kood elab Git'is ja läbib code review protsessi, peaks ka infrastruktuur elama koodina.

Traditsiooniline lähenemine: ava AWS Console, klõpsa 50 nuppu, kulub 2-4 tundi, dokumenteeri (või pigem ära dokumenteeri). IaC lähenemine: kirjuta kood, käivita terraform apply, kulub 3-10 minutit, kood ON dokumentatsioon.

Sama ülesanne kahe meetodiga:

| Meetod | Aeg | Tulemus | Korratav? | Dokumenteeritud? |
|--------|-----|---------|-----------|------------------|
| Käsitsi AWS Console | 2-4h | "Unique snowflake" | Ei | Vahel |
| Terraform | 3-10 min | Identne iga kord | Jah | Alati |


![How Does IaC Work?](https://cdn.servermania.com/images/w_1024,h_494,c_scale/f_webp,q_auto:best/v1744146107/kb/2_351821c347/2_351821c347.png?_i=AA)


### IaC Eelised

Kiirus on ilmne. Käsitsi: 10 serverit võtab 1-2 päeva. Terraform: 10 serverit võtab 5 minutit. Matemaatika on lihtne. See pole ainult aja kokkuhoid - see on võimalus eksperimenteerida, katsetada, kiirelt itereerida.

Korratavus on võib-olla kõige väärtuslikum omadus. Sama kood annab alati sama tulemuse. Käivita 100 korda, saad 100 identset keskkonda. Ei ole "töötab minu masinas" probleemi. Development, staging ja production on identsed, ainult parameetrid erinevad. See tähendab, et bug'id ilmnevad development'is, mitte production'is.

Versioonihaldus tuleneb sellest, et kood elab Git'is. `git log` näitab täpselt kes mida muutis ja millal. Keegi kustutas production'i kell 3 öösel? Git teab täpselt mida tehti. Saab rollback'ida. Saab vaadata ajalugu. Saab blame'ida (konstruktiivselt).

Dokumentatsioon muutub iseenesestmõistetavaks: kood ON dokumentatsioon. Alati up-to-date, sest kui kood ei ole ajakohane, süsteem ei tööta. Confluence ei vaja (tänu taevale). See on reaalne, töötav dokumentatsioon, mitte "loosely based on actual events" versioon mis kirjutati 6 kuud tagasi.

Meeskonnatöö muutub võimalikuks: pull request'id infrastruktuurile, code review enne production'i, nagu normaalne tarkvaraarendus. Kolm inimest saavad samaaegselt töötada erinevatel osadel. Konfliktid lahendatakse Git'is, mitte "viimane kirjutab üle" põhimõttel AWS konsoolis.

Testimine lihtsustub: Dev -> Staging -> Prod. Sama kood, erinevad parameetrid. Testi julgelt, prod ei purune. Kui midagi läheb valesti staging'us, ei jõua see kunagi production'ini.

![How Terraform Helps in DevOps](https://media.geeksforgeeks.org/wp-content/uploads/20241212151316849879/How-does-Terraform-work.webp)
*Example: How Terraform Helps in DevOps*

### Pipedrive Näide

Pipedrive kogemus Terraform'iga illustreerib hästi väärtust. Enne Terraform'i 2018. aastal võttis uue keskkonna loomine kaks päeva. Dokumentatsioon elas Confluence'is ja oli sageli aegunud. Vead olid tavalised, sest iga keskkond oli pisut erinev. Meeskond ei teadnud täpselt, mis production'is oli.

Pärast Terraform'i kasutuselevõttu 2019. aastal võtab uue keskkonna loomine 10 minutit. Dokumentatsioon elab Git'is. Vigu on 90% vähem. Meeskond näeb `git log` kaudu kõike. ROI: 10x kiirem, 100,000+ eurot säästu aastas, üks väga õnnelik DevOps meeskond.

---

## 2. Mis on Terraform?

"Terraform on nagu LEGO infrastruktuurile - ehitad samme koos ja saad täis süsteemi."

Terraform on HashiCorp'i loodud Infrastructure as Code tööriist. Loodud 2014. aastal, kirjutatud Go keeles, open-source ja täiesti tasuta. Üle 10 aasta praktilist kasutust tootmiskeskkondades, 1000+ ettevõtet (AWS, Microsoft, Google, GitLab kasutavad ise Terraform'i oma infrastruktuurile).

### Terraform Roll

Terraform loob infrastruktuuri. See ei konfigureeri rakendusi. See on oluline vahe, mida algajad sageli ei mõista. Terraform ehitab maja - loob serveri, seadistab võrgu, avab tulemüüri reeglid. Terraform ei pane mööblit majja - see on Ansible'i või teiste konfigureerimistööriistade töö.

Analoogi: maja ehitamine jaguneb osadeks. Terraform ehitab maja (vundament, seinad, katus, elektri juhtmestik). Ansible teeb sisekujunduse (installib mööbli, värvib seinad, paigaldab dekoratsioonid). Kubernetes on kolija (paigutab asjad õigetesse tubadesse ja haldab nende paigutust dünaamiliselt).

| Roll | Tööriist | Mis ta teeb |
|------|----------|-------------|
| Maja ehitaja | Terraform | Vundament, seinad, katus |
| Sisekujundaja | Ansible | Mööbel, värvid, elekter |
| Kolija | Kubernetes | Paigutab asjad õigetesse tubadesse |

See on oluline: Terraform ei deploy rakendusi. See loob serveri, kus rakendus jookseb. Nagu ehitaja ei pane tuppa diivanit - see on sisekujundaja töö. Paljud algajad proovivad Terraform'iga teha asju, mis on mõeldud Ansible'ile või Kubernetes'ele.

### Terraform Tugevused

Esimene suur tugevus on multi-cloud tugi. Sama süntaks töötab kõigile platvormidele. AWS, Azure, GCP - kõik kasutavad HCL keelt. Õpid ühe korra, kasutad kõikjal.

Näiteks sama server AWS'is ja Azure'is:

```hcl
# AWS
resource "aws_instance" "web" {
  ami           = "ami-12345"
  instance_type = "t3.micro"
}

# Azure (sama loogika!)
resource "azurerm_virtual_machine" "web" {
  name     = "web-vm"
  size     = "Standard_B1s"
}

# GCP
resource "google_compute_instance" "web" {
  name         = "web-instance"
  machine_type = "f1-micro"
}
```

![Multi-Cloud Support](https://miro.medium.com/v2/resize:fit:1400/1*QlqZdh6-8WXFzbVRWKLZSw.png)
*Terraform Multi-Cloud Architecture*

Sama loogika, erinevad provider'id. See tähendab, et täna kasutad AWS'i, homme kui tarvis on Azure'i, sa ei pea õppima täiesti uut süsteemi. Terraform oskused on portaalsed.

Teine tugevus on deklaratiivne lähenemine. Ütled MIDA tahad, mitte KUIDAS. Imperatiivne kood Bash'is: create_server "web1", wait_for_ready, attach_security_group, ja veel 20 sammu. Deklaratiivne kood Terraform'is: resource "aws_instance" "web" { count = 3 }. Terraform väljastab samme ise. Sa ei pea muretsema järjekorra pärast, sõltuvuste pärast, ootamise pärast.

Kolmas tugevus on suur kogukond. Terraform Registry sisaldab 3000+ provider'it ja 10,000+ moodulit. AWS, Azure, GCP, Docker, Kubernetes, GitHub, ja veel sadade platvormide toetus. See tähendab, et tõenäoliselt ei pea sa kirjutama ise provider'it või moodulit - keegi teine on seda juba teinud ja jagab avalikult.

### Terraform vs Teised

Terraform vs Ansible on üks sagedasemaid segadusi. Need tööriistad teevad erinevaid asju, kuigi mõlemat sageli kutsutakse "IaC" nime all. Terraform loob infrastruktuuri. Ansible seadistab infrastruktuuri. Näide: Terraform ütleb "Loo 10 serverit". Ansible ütleb "Installi Nginx kõigile neile 10 serverile". Keel: Terraform kasutab HCL'd (deklaratiivne), Ansible kasutab YAML'i (imperatiivne). Kasuta Terraform'i kui vajad uut infrastruktuuri, kasuta Ansible'i kui seadistad olemasolevat.

| | Terraform | Ansible |
|---|-----------|---------|
| Peamine ülesanne | Loo infrastruktuur | Seadista infrastruktuur |
| Näide | Loo 10 serverit | Installi Nginx kõigile |
| Keel | HCL (deklaratiivne) | YAML (imperatiivne) |
| Kasuta kui | Vajad uut infrastruktuuri | Seadistad olemasolevat |

![Ansible vs Terraform Differences](https://i.pinimg.com/originals/c4/49/5e/c4495ece1697f3f7e499e7ef719276ff.png)
*Ansible vs Terraform: Understanding the Differences*

Praktikas kasutatakse neid koos: Terraform loob 10 serverit AWS'is, Ansible installib Nginx kõigile, Kubernetes deploy'b rakenduse. Wise (endine TransferWise) kasutab mõlemat. Terraform loob infrastruktuuri, Ansible seadistab. Koos nad on võimsad, eraldi poolik töö.

Terraform vs CloudFormation on teine oluline võrdlus. CloudFormation on Amazon'i enda IaC tööriist. Platvormid: Terraform töötab AWS'is, Azure'is, GCP's, ja 100+ teises platvormis. CloudFormation töötab ainult AWS'is. Süntaks: Terraform kasutab HCL'd (loetav ja kompaktne). CloudFormation kasutab JSON'i või YAML'i (verbose ja keeruline). Kogukond: Terraform'il on suur multi-cloud kogukond. CloudFormation on AWS-keskne.

| | Terraform | CloudFormation |
|---|-----------|----------------|
| Platvormid | AWS, Azure, GCP, 100+ | Ainult AWS |
| Süntaks | HCL (loetav) | JSON/YAML (verbose) |
| Kogukond | Suur, multi-cloud | AWS-kesksed |
| Kasuta kui | Multi-cloud või tulevikukindlus | 100% AWS forever |

Eesti valik: 95% ettevõtteid valib Terraform. Isegi kui praegu ainult AWS, homme võib-olla Azure. Paindlikkus on kuningas. Terraform oskused on väärtuslikumad tööturul kui CloudFormation oskused.

### Bolt Näide

Bolt infrastruktuur 2024. aastal: 1000+ mikroteenust, 50+ riiki, AWS + GCP + Azure. Ilma Terraform'ita oleks see võimatu. Vajaks sadu DevOps insenere iga platvormi jaoks. Terraform'iga: väike meeskond haldab kõike. 1 moodul kirjutatakse korra, rakendatakse kõikjal. See on skaleeritavuse näide - Terraform võimaldab väiksel meeskonnal hallata tohutut infrastruktuuri.

---

## 3. Terraform Arhitektuur

"Kolm osa: Aju, Käed, Mälu."

![Terraform Architecture Components](https://media.geeksforgeeks.org/wp-content/uploads/20230529185228/git-merge-dev.png)
*Components of Terraform Architecture*

Terraform koosneb kolmest põhikomponendist: Core (aju), Providers (käed), State (mälu). Iga komponent täidab spetsiifilist rolli ja nende koostöö võimaldab Terraform'i töötada.

Core on Terraform'i peaprotsessor, kirjutatud Go keeles. Core loeb .tf faile (sinu konfiguratsioon), võrdleb soovitud seisundit praeguse seisundiga (state failist), teeb plaani (mis ressursse luua/muuta/kustutada), ja täidab plaani (kasutades provider'eid). Analoogi: ehituse projektijuht vaatab joonist (kood), vaatab mis on ehitatud (state), planeerib järgmised sammud, ja koordineerib ehitajaid (provider'eid).

### Terraform Core (Aju)

Core teeb kõik "mõtlemise". See ei räägi ühegi platvormi API'ga otse - see on provider'ite töö. Core ainult:

- Parsib HCL koodi
- Ehitab sõltuvuste graafi (mis peab olema enne mida)
- Arvutab mis muutub (diff)
- Genereerib plaani
- Täidab plaani järjestikku

Core on platvormist sõltumatu. Sama Core töötab AWS'i, Azure'i, GCP, Docker'i jaoks. See on Terraform'i võlu - üks tööriist, palju platvorme.

### Providers (Käed)

Providers on pluginad, mis räägivad platvormide API'dega. Provider on nagu tõlk. Sina räägid HCL't, AWS räägib REST API't, provider tõlgib.

Näiteks AWS provider konfiguratsioon:

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
  region = "eu-north-1"  # Stockholm
}
```

Populaarsed provider'id:

| Provider | Ressursse | Kasutus |
|----------|-----------|---------|
| aws | 3000+ | Amazon Web Services |
| azurerm | 2000+ | Microsoft Azure |
| google | 1500+ | Google Cloud |
| docker | 50+ | Containerid |
| kubernetes | 200+ | K8s klastrid |
| local | 5 | Failid (õppimiseks!) |

Kuidas töötab: sina ütled "Tahan serveri", Core ütleb "OK, kasutan AWS provider'it", AWS Provider teeb CreateInstance API call'i, AWS vastab "Valmis! ID: i-12345", Core salvestab state'i. Provider on vahendaja Core ja platvormi vahel.

Iga provider laetakse alla terraform init käsuga. Provider'id elavad `.terraform/` kataloogis. Neid EI PANDA Git'i - nad on suuremad ja genereeritavad.

### State File (Mälu)

State on `terraform.tfstate` fail JSON vormingus. See on Terraform'i päevik - mäletab kõike, mis on loodud.

![Terraform State Management](https://spacelift.io/wp-content/uploads/2022/02/TerraformStateFile2.png)
*Terraform State File Management*

Miks oluline: sina ütled "Tahan 3 serverit". Terraform vaatab state'i, näeb et praegu on 2, loob 1 juurde. Ilma state'ita Terraform ei tea mis on loodud. Terraform arvaks "Pole midagi, loon 3 uut!" ja AWS vastaks "Aga sul on juba 2..." ja tulemus on 5 serverit. Ootamatu arve. CEO on vihane.

State sisaldab: kõik loodud ressursid (serverid, võrgud, andmebaasid), nende ID'd (i-12345, sg-67890), atribuudid (IP aadressid, nimed, portid), sõltuvused (server sõltub võrgust).

Kriitiline hoiatus: state võib sisaldada saladusi. Kui kirjutad koodis:

```hcl
resource "aws_db_instance" "main" {
  username = "admin"
  password = "SuperSecret123!"
}
```

Siis pärast terraform apply sisaldab terraform.tfstate:

```json
{
  "resources": [{
    "attributes": {
      "username": "admin",
      "password": "SuperSecret123!"
    }
  }]
}
```

Parool on plain text'is! Seetõttu: ÄRA PANE STATE FAILI GIT'I. Lisa .gitignore:

```gitignore
*.tfstate
*.tfstate.*
.terraform/
```

Hiljem õpid kasutama remote backend'i (S3 + encryption), kuid algajana õppides lokaalselt: hoia state privaatsena, tee backup'i regulaarselt, ära jaga kedagi.

State kaotsimineku lugu: üks Eesti startup developer kustutas kogemata `terraform.tfstate`. Meeskond ei teadnud, mis production'is on. 4 tundi downtime. 20,000 eurot kahju. Üks väga kurb developer. Alati backup state! See pole valikuline soovitus.

---

## 4. Deklaratiivne vs Imperatiivne

"Imperatiivne: ütled KUIDAS. Deklaratiivne: ütled MIDA."

![Declarative vs Imperative](https://spacelift.io/wp-content/uploads/2021/02/declarative-vs-imperative.png)
*Declarative vs Imperative Infrastructure as Code*

See on Terraform'i kõige olulisem kontseptsioon. Mõista seda ja sa mõistad Terraform'i. Mõista valesti ja sa võitad Terraform'iga igavesti.

### Imperatiivne (KUIDAS?)

Imperatiivne kood kirjeldab samme. Annad täpsed instruktsionid, sammhaaval, järjekorras. Nagu retsept: võta muna, purusta, sega, küpseta.

Näide Bash'is:

```bash
#!/bin/bash
# Imperatiivne: kirjeldad samme

echo "Loon security group..."
aws ec2 create-security-group --group-name web-sg

echo "Avan pordi 80..."
aws ec2 authorize-security-group-ingress \
  --group-name web-sg --port 80

echo "Loon viis serverit..."
for i in {1..5}; do
    aws ec2 run-instances --instance-type t3.micro
done
```

Probleem: käivita teist korda ja script loob 10 serverit! Script ei tea, et 5 on juba olemas. Sa pead ise meeles pidama seisundit. Sa pead ise kontrollima "kas see on juba olemas?". Sa pead ise kirjutama cleanup loogikat. Sa pead ise tegelema vigadega (mida teha kui security group juba eksisteerib?).

### Deklaratiivne (MIDA?)

Deklaratiivne kood kirjeldab lõpptulemust. TÃ¶Ã¶riist väljastab sammud. Sina ütled "Tahan 5 serverit" ja Terraform arvutab ise kuidas selleni jõuda.

Näide Terraform'is:

```hcl
# Deklaratiivne: kirjeldad tulemust

resource "aws_security_group" "web" {
  name = "web-sg"
  
  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
  }
}

resource "aws_instance" "web" {
  count         = 5
  instance_type = "t3.micro"
  
  vpc_security_group_ids = [aws_security_group.web.id]
}
```

Käivita mitu korda: terraform apply esimesel korral loob 5 serverit. terraform apply teisel korral ei tee midagi (juba on 5). terraform apply kolmandal korral ei tee midagi (ikka 5). Terraform teab (tänu state'ile), mis on olemas. Idempotent! Turvaline käivitada mitu korda.

### Update Stsenaarium

Olukord: sul on 5 serverit. Tahad nüüd 7 serverit + uus firewall reegel + uued õigused.

Imperatiivne Bash:

```bash
#!/bin/bash
# Pead ise arvestama

# Lisa 2 serverit (5 + 2 = 7)
for i in {1..2}; do
    aws ec2 run-instances --instance-type t3.micro
done

# Lisa firewall reegel
aws ec2 authorize-security-group-ingress \
  --group-name web-sg --port 443

# Lisa õigused
aws iam attach-user-policy \
  --user-name deploy --policy-arn ...
```

Pead ise arvutama: "5 -> 7 = 2 juurde". Kui eksid, on probleeme. Kui käivitad uuesti, on duplikaadid. Sa pead ise tegelema idempotentsusega.

Deklaratiivne Terraform:

```hcl
resource "aws_instance" "web" {
  count = 7  # Muutsime 5 -> 7
  instance_type = "t3.micro"
}

resource "aws_security_group" "web" {
  name = "web-sg"
  
  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
  }
}

resource "aws_iam_user_policy_attachment" "deploy" {
  user       = "deploy"
  policy_arn = "..."
}
```

Terraform: "On 5, peab olema 7. Loon 2." Terraform: "Firewall puudub. Lisan." Terraform: "Õigus puudub. Lisan." Sa ei pea arvutama. Terraform teeb ise.

### Konfiguratsiooni Puhtus

Imperatiivne fail pärast päevi kasutamist:

```bash
# Day 1
create_server 1
create_server 2
create_server 3
create_server 4
create_server 5

# Day 3
add_firewall_rule 80

# Day 7
add_firewall_rule 443

# Day 10
remove_server 1
remove_server 2

# Day 14
add_server 6
add_server 7

# ... (200+ rida ajalugu)
```

Fail muutub pidevalt pikemaks. See on ajalugu, mitte seisund. Debuggimine nõuab kogu ajaloo mõistmist.

Deklaratiivne fail (alati):

```hcl
resource "aws_instance" "web" {
  count = 7
}

resource "aws_security_group" "web" {
  # Rules here
}

# See on KÕIK!
```

Fail jääb alati puhtaks. See näitab PRAEGUST seisu, mitte ajalugu. Git log näitab ajalugu. Konfiguratsioon näitab seisundit.

| Aspekt | Imperatiivne | Deklaratiivne |
|--------|--------------|---------------|
| Kirjeldad | KUIDAS (sammud) | MIDA (tulemus) |
| Näide | "Loo server, siis võrk" | "Tahan 5 serverit" |
| Kordamine | Loob duplikaate | Idempotent |
| State | Sina pead meeles pidama | Tööriist mäletab |
| Fail | Kasvab pidevalt | Jääb lühikeseks |
| Debuggimine | Raske | Lihtsam |

Eesti DevOps'ija ütlus: "Imperatiivne on nagu juhendada koerale, kuidas istuda. Deklaratiivne on nagu öelda 'Istu!' ja koer väljastab ise."

---

## 5. HCL Keel

"HCL on nagu JSON, aga inimestele."

HashiCorp Configuration Language on Terraform'i konfiguratsioonikeel. See on deklaratiivne, loetav, ja spetsiaalselt disainitud infrastruktuuri kirjeldamiseks.

### Põhisüntaks

HCL struktuur:

```hcl
<TYPE> "<LABEL>" "<LABEL>" {
  argument = value
}
```

Näiteks lihtne fail:

```hcl
resource "local_file" "greeting" {
  filename = "/tmp/hello.txt"
  content  = "Tere, Terraform!"
}
```

Elemendid: resource on block type (mis liiki asi see on), "local_file" on ressursi tüüp (provider + ressurss), "greeting" on meie antud nimi (identifier), filename ja content on argumendid (parameetrid).

### Resources

Resource on miski, mida Terraform loob. Resource on Terraform'i põhielement. Kõik mis tahad luua, on resource.

![Terraform Resource Syntax](https://k21academy.com/wp-content/uploads/2024/06/AWSResource.webp)
*Terraform Resource Syntax*

Lokaalne fail:

```hcl
resource "local_file" "config" {
  filename = "app.conf"
  content  = "port=8080"
  
  file_permission = "0644"
}
```

AWS server:

```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345"
  instance_type = "t3.micro"
  
  tags = {
    Name = "WebServer"
    Env  = "Dev"
  }
}
```

Iga provider defineerib oma ressursse. AWS provider pakub aws_instance, aws_s3_bucket, aws_db_instance. Azure provider pakub azurerm_virtual_machine, azurerm_storage_account. Dokumentatsioon on Terraform Registry's.

### Sõltuvused

Terraform loob automaatselt sõltuvusi. Kui kasutad ühe ressursi atribuuti teises ressursis, Terraform teab järjekorda.

```hcl
# 1. Esmalt security group
resource "aws_security_group" "web" {
  name = "web-sg"
}

# 2. Siis server (kasutab SG'd)
resource "aws_instance" "web" {
  ami                    = "ami-12345"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.web.id]
  # → automaatne sõltuvus!
}
```

Terraform teab: "Teen SG enne, siis serveri." Ei pea ütlema depends_on. Terraform näeb, et server kasutab security group'i ID'd, järelikult peab security group olema enne.

### Variables

Muutujad võimaldavad dünaamilisi väärtusi. Muutujad teevad koodi taaskasutavaks.

```hcl
variable "environment" {
  description = "Keskkond: dev või prod"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Peab olema dev või prod!"
  }
}

resource "aws_instance" "app" {
  instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"
  
  tags = {
    Env = var.environment
  }
}
```

Kasutamine: terraform apply -var="environment=prod". Või loo terraform.tfvars fail:

```hcl
environment = "prod"
```

### Outputs

Outputs näitavad infot pärast loomist. Outputs on kasulikud teiste moodulite jaoks või lihtsalt info näitamiseks.

```hcl
output "server_ip" {
  description = "Serveri IP"
  value       = aws_instance.web.public_ip
}
```

Pärast terraform apply:

```
Outputs:
server_ip = "13.51.123.45"
```

### Funktsioonid

HCL sisaldab kasulikke built-in funktsioone:

```hcl
# Faili sisu lugemine
content = file("config.json")

# JSON encode
metadata = jsonencode({
  name = "app"
})

# String interpolation
message = "Tere, ${var.name}!"

# Timestamp
created = timestamp()
```

Terraform dokumentatsioonis on kõik funktsioonid kirjeldatud. Näiteks faili lugemine võimaldab hoidda suuremad JSON/YAML failid eraldi ja laadida need Terraform'i.

---

## 6. Terraform Workflow

"4 käsku: init, plan, apply, destroy"

![Terraform Workflow Lifecycle](https://spacelift.io/wp-content/uploads/2023/08/Terraform-Workflow.png)
*Terraform Workflow: Write → Init → Plan → Apply → Destroy*

Terraform'i kasutamine järgib standardset workflow'd. Need käsud käivad alati samas järjekorras. Mõista workflow'd ja sa mõistad kuidas Terraform töötab.

### terraform init

Esimene samm: terraform init. See valmistab projekti ette.

```bash
terraform init
```

Mis toimub: Terraform laeb provider'id (.terraform/ kataloogi), seadistab backend'i (state'i salvestuskohta), init'ib moodulid (kui kasutad).

Output:

```
Initializing provider plugins...
- Finding hashicorp/local v2.4.0...
- Installing hashicorp/local v2.4.0...

Terraform has been successfully initialized!
```

Millal käivita: esimest korda projektis, kui lisad uue provider'i, kui clone'id repo uuest kohast.

Kui unustad init'i:

```bash
terraform plan
# Error: Could not load plugin
# Run: terraform init
```

Terraform ütleb selgelt, et init on vaja. Provider'id ei ole laetud, seega Terraform ei saa töötada.

### terraform plan

Teine samm: terraform plan. See näitab mis muutub. KRIITILINE: EI MUUDA MIDAGI!

```bash
terraform plan
```

Sümbolid:

| Sümbol | Tähendus | Näide |
|--------|----------|-------|
| + | Luuakse | Uus server |
| - | Kustutatakse | Vana server |
| ~ | Muudetakse | Port 80 -> 443 |
| -/+ | Replace | Instance type muutus |

Output:

```terraform
Terraform will perform the following actions:

  # local_file.greeting will be created
  + resource "local_file" "greeting" {
      + content  = "Tere!"
      + filename = "/tmp/test.txt"
      + id       = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

ALATI tee plan enne apply! Plan on sinu kindlus. Näed täpselt mis muutub. Näed kas tuleb üllatusi. Näed kas kustutad kogemata production serveri. Plan on tasuta, apply on kallis.

Eelistatavalt salvesta plan:

```bash
terraform plan -out=tfplan
terraform apply tfplan
```

See tagab, et apply teeb täpselt seda, mida plan näitas. Vahepealsed muudatused (näiteks keegi teine tegi midagi) ei mõjuta.

### terraform apply

Kolmas samm: terraform apply. See rakendab muudatused PÄRISELT. Nüüd tehakse päris tööd. Nüüd luuakse päris ressursid. Nüüd tulevad päris arved.

```bash
terraform apply
```

Terraform küsib kinnitust:

```
Do you want to perform these actions?
  Enter a value: yes
```

Automaatne (ohtlik):

```bash
terraform apply -auto-approve
```

Kasuta ainult kui 100% kindel! Development'is OK, production'is MITTE KUNAGI ilma plan'ita.

Output:

```
local_file.greeting: Creating...
local_file.greeting: Creation complete after 0s

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:
file_path = "/tmp/test.txt"
```

### terraform destroy

Neljas samm: terraform destroy. See kustutab KÕIK ressursid. See on pöördumatu. See on nagu rm -rf / - ohtlik ja võimas.

```bash
terraform destroy
```

HOIATUS: Pöördumatu! Kõik ressursid kustutatakse. Kõik andmed kaovad. Kõik serverid lähevad maha. Kõik andmebaasid kustutatakse.

Õuduslugu: Juunior developer production'is käivitas terraform destroy. Vajutas "yes" ilma mõtlemata. 5 minutit hiljem: 150 serverit kadunud, kliendid offline, CEO helistab. Kahjusumma umbes 500,000 eurot. Tulemus: "resume-generating event".

Õppetund: Kontrolli 3x, kus oled. Lisa production'i prevent_destroy lifecycle policy. Kasuta workspace'e. Ära kunagi tee destroy production'is ilma backup'ita. Ära kunagi tee destroy enne kui oled 100% kindel.

---

## Kokkuvõte

### Õppisime

Infrastructure as Code: kood vs käsitsi seadistamine. Kood on kiirem, korratavam, dokumenteeritum, testitavam.

Terraform: provisioning tööriist infrastruktuuri loomiseks. Multi-cloud, deklaratiivne, suur kogukond.

Arhitektuur: Core (aju loeb koodi ja planeerib), Providers (käed räägivad platvormidega), State (mälu mäletab mis on loodud).

Deklaratiivne lähenemine: MIDA vs KUIDAS. Kirjelda tulemust, mitte samme. Idempotentne, turvaline, lihtne.

HCL keel: konfiguratsioonikeel ressursside kirjeldamiseks. Resources, variables, outputs, functions.

Workflow: init (valmista ette) -> plan (vaata mis muutub) -> apply (rakenda) -> destroy (kustuta kõik).

### Terraform Võtmepunktid

Miks Terraform: Multi-cloud (AWS, Azure, GCP kõik ühe tööriista all). Deklaratiivne (ütle MIDA, mitte KUIDAS). Suur kogukond (3000+ providers, 10,000+ mooduleid). State haldamine (mäletab mis on loodud, võimaldab idempotentsust).

Kuidas töötab: Core loeb config faile ja state faili. Teeb plaani (mis muutub). Provider täidab plaani (kutsub API'sid). Uuendab state'i (salvestab mis loodi).

Millal kasutada: Lood uut infrastruktuuri (serverid, võrgud, andmebaasid). Haldad olemasolevat (muudad, skaleeri, kustutad). Replitseerid keskkondi (dev, staging, prod identsed). Tahad koodi kui dokumentatsiooni (Git log näitab ajalugu).

### Järgmine Samm

Järgmine tund: Labor - praktiline töö Terraform'iga. Loome päris ressursse. Käivitame päris käske. Teeme päris vigu (ohutult) ja õpime nendest.

### Ressursid

Dokumentatsioon: Terraform ametlik dokumentatsioon sisaldab kõike. developer.hashicorp.com/terraform/docs on peamine allikas. HCL süntaks on kirjeldatud developer.hashicorp.com/terraform/language/syntax. Terraform Registry registry.terraform.io sisaldab kõik providers ja mooduleid.

Õppimine: HashiCorp Learn developer.hashicorp.com/terraform/tutorials pakub interaktiivseid õpetusi. Terraform Best Practices terraform-best-practices.com kogub kogukonna parimad praktikad.

Kogukond: Terraform GitHub github.com/hashicorp/terraform on avatud. DevOps Estonia meetup'id toimuvad regulaarselt Tallinnas.

---

Eesti DevOps mantra: "Plan enne Apply't, backup enne Destroy'd, kohv enne debugimist."
