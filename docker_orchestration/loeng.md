# Docker Compose ja Mitme Konteineri Haldamine

**Teemad:** Docker Compose põhialused, multi-container rakendused, keskkondade haldamine, orkestreerimise põhimõtted

---

##  Õpiväljundid

Pärast seda loengut oskate:
- Kirjutada ja käivitada Docker Compose faile
- Ehitada multi-container rakendusi
- Mõista teenuste vahelist suhtlust ja võrgustikku
- Hallata erinevaid keskkondi (development, production)
- Debuggida ja tõrkeotsingut teha
- Mõista orkestreerimise põhimõtteid ja vajadust

---

![Docker Compose](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*IzzwDYFNsfHxYexpgHqqSA.png)

## Sissejuhatus

Kaasaegne veebirakendus ei ole üks programm. See koosneb erinevatest komponentidest: andmebaas hoiab andmeid, API server käsitleb ärilogikat, frontend näitab kasutajaliidet, cache teeb süsteemi kiireks. Igaüks neist töötab eraldi konteineris.

Küsimus on lihtne: kuidas neid kõiki koos hallata?

Docker Compose vastab sellele küsimusele. See on tööriist mis muudab mitme konteineri haldamise lihtsaks ja hallatavaks.

---

## Miks me seda vajame?

### Käsitsi haldamise probleem

Vaatame näidet. Sul on kaks komponenti: PostgreSQL andmebaas ja Node.js API server.

Käivitad andmebaasi käsuga `docker run -d --name mydb postgres:13`. See töötab. Aga nüüd tahad API käivitada ja API vajab andmebaasi aadressi. Milline see on? Sa ei tea. Docker genereerib IP aadressi dünaamiliselt. Pead käsitsi välja uurima millise IP Docker andmebaasile andis. Siis pead selle API käivitamise käsku kirjutama.

Järgmine päev käivitad uuesti - IP on erinev. Pead jälle käsitsi uurima ja muutma.

Lisaks sellele - kui API käivitub liiga kiiresti ja andmebaas ei ole veel valmis, saad errori. Pead ootama... aga kui kaua? 5 sekundit? 10? Raske öelda.

Kui sul on 5-6 erinevat komponenti, muutub see haldamatuks. Pead meeles pidama järjekorda, IP aadresse, ootama et asjad valmis saaksid. Ja kui tahad et kolleeg saaks sama projekti käivitada, pead kogu selle protsessi talle selgitama.

---

## Docker Compose lahendus

Compose'i põhiidee on lihtne: kirjelda kogu süsteem ühes failis. Ära ütle KUIDAS asjad teha, vaid ÜtLE MIDA sa tahad.

Loome faili nimega `docker-compose.yml`. Selles failis kirjeldame meie kahe komponendiga süsteemi. Kirjutame et meil on kaks teenust: üks nimega "database" mis kasutab PostgreSQL'i, ja teine nimega "api" mis kasutab meie API koodi. Ütleme ka et API vajab andmebaasi, seega andmebaas peab enne käivituma.

Kui see fail on olemas, käivitame terve süsteemi ühe käsuga: `docker-compose up`. Compose loeb faili, mõistab mida me tahame, ja teeb kõik vajaliku: loob võrgu, käivitab teenused õiges järjekorras, seadistab et nad leiaksid üksteist.

Kõige olulisem - me ei kirjuta IP aadresse. Kirjutame lihtsalt teenuse nime "database" ja Compose teab kuidas teenused ühendada. Kui teenused on samas Compose projektis, näevad nad üksteist automaatselt.

See on deklaratiivne lähenemine. Imperatiivselt sa ütleksid "tee samm üks, siis samm kaks, siis samm kolm". Deklaratiivselt sa ütled "ma tahan et lõpuks oleks selline süsteem" ja tööriist mõtleb välja kuidas sinna jõuda.

**Viide:** https://docs.docker.com/compose/

---

## Kuidas Compose fail välja näeb

![Compose file](https://www.simplilearn.com/ice9/free_resources_article_thumb/docker-yaml.JPG)
Compose fail on YAML formaadis tekstifail. YAML on lihtne formaat kus struktuur on määratud taandetega - täpselt nagu Python koodis. Kui midagi on rohkem taandatud, on see eelmise asja "sees".

Iga Compose fail algab versiooniga. See number ütleb Compose'ile millise formaadiga on tegemist. Kasuta alati vähemalt `3.8` - see on piisavalt uus et kõik kasulikud võimalused oleksid olemas, aga piisavalt stabiilne et igal pool töötaks.

Pärast versiooni tuleb `services` sektsioon. See on faili kõige olulisem osa. Siin sa kirjeldad oma rakenduse komponendid - igaüks neist saab oma konteineri. Iga komponendi all kirjeldad kuidas see käituma peab: millist Docker image't kasutada, millised pordid avada, millised seaded on vajalikud.

Kui su rakendus vajab et andmed jääksid alles isegi kui konteiner kustutatakse, lisad `volumes` sektsiooni. Siin defineerid püsivad andmehoidlad.

Kui vajad kontrolli võrkude üle - näiteks tahad et mõned teenused oleksid isoleeritud - võid lisada `networks` sektsiooni. Aga enamasti seda ei vaja, sest Compose loob automaatselt võrgu kõigile teenustele.

**Viide:** https://docs.docker.com/compose/compose-file/

---

## Teenused - mis need on ja kuidas neid kirjeldada

Teenus on sinu rakenduse üks komponent. Kui mõtled oma rakendusele kui firmale, siis teenused on osakonnad: üks vastutab andmete hoidmise eest, teine tegeleb äriloogikaga, kolmas näitab kasutajaliidet.

Kõige lihtsam teenus vajab ainult nime ja image't. Näiteks kui tahad Redis cache'i, kirjutad et sul on teenus nimega "cache" mis kasutab Redis'e. Compose tõmbab Redis image ja käivitab konteineri. See konteiner on kättesaadav teistele teenustele nimega "cache".

Aga tavaliselt vajad rohkem. Pead ütlema millised pordid avada - kui brauser peab su API'le ligi pääsema, pead pordi avama. Pead andma seadeid keskkonnamuutujate kaudu - paroolid, API võtmed, konfiguratsioon. Kui tahad et konteiner näeks sinu hosti faile - näiteks arenduses kui muudad koodi ja tahad et muudatused kohe näha oleksid - kasutad volumes'eid.

Ja väga oluline - kui üks teenus sõltub teisest, pead seda ütlema. Kui API vajab andmebaasi, kirjutad et API `depends_on` andmebaasist. Siis Compose käivitab andmebaasi enne API'd.

**Viide:** https://docs.docker.com/compose/compose-file/05-services/

---

## Kuidas teenused üksteist leiavad

See on Compose'i kõige võimsam ja elegantne feature. Kui käivitad teenused Compose'iga, loob ta automaatselt sisemise võrgu. Selles võrgus töötab DNS server mis teab kõigi teenuste nimesid ja IP aadresse.

See tähendab et kui sul on teenus nimega "database", siis iga teine teenus samas võrgus saab sellega ühenduda kasutades lihtsalt nime "database". Mitte IP aadressi - lihtsalt nime. Docker lahendab selle automaatselt õigeks IP'ks.

Praktikas tähendab see et kui API vajab andmebaasiga ühendust, kirjutad ta konfiguratsioonifailis või keskkonnamuutujas lihtsalt "ühenda andmebaasiga nimega database". Pole vaja teada IP'd. Pole vaja muretseda et IP võib muutuda. Pole vaja konfiguratsiooni uuendada kui midagi muutub.

See on võimas sest muudab süsteemi paindlikuks. Saad teenuseid liigutada, uuesti käivitada, asendada - ja teised teenused leiavad nad ikka automaatselt.

Oluline mõista: see DNS töötab ainult Compose võrgu sees. Kui tahad et väljastpoolt (näiteks sinu brauser) saaks teenusele ligi, pead pordi avama `ports` sektsiooniga.

**Viide:** https://docs.docker.com/compose/networking/

---

## Andmete püsimine

Konteinerid on loodud olema ajutised. Kui kustutad konteineri, kaob ka kõik mis seal sees oli. See on disain - konteinerid peaksid olema "cattle not pets", nagu öeldakse. Saad igal ajal uue teha.

Aga andmebaas ei saa olla ajutine. Andmed peavad jääma alles. Siin tulevad mängu volumes.

Volume on nagu väline kõvaketas mille saad konteinerile külge ühendada. Kui konteiner kirjutab andmeid volume'i, jäävad need sinna püsivalt. Isegi kui konteiner kustutatakse ja tehakse uus, ühendatakse sama volume uuesti külge ja andmed on tagasi.

Compose'is defineerid volume kaks korda. Esiteks teenuse juures ütled KUHU konteineri failisüsteemis see ühendatakse. Näiteks PostgreSQL hoiab andmeid kaustas `/var/lib/postgresql/data`, seega ühendad volume sinna. Teiseks faili lõpus `volumes` sektsioonis deklareerid et see volume eksisteerib.

On ka teine variant - bind mount. See ei loo uut volume'd vaid ühendab otse sinu hosti kausta konteineriga. See on kasulik arenduses: kui kirjutad koodi oma arvutis ja tahad et konteiner näeks kohe muudatusi, mount'id koodi kausta sisse. Iga kord kui salvestad faili, on see kohe konteineris nähtav.

**Viide:** https://docs.docker.com/storage/volumes/

---

## Teenuste järjekord ja sõltuvused

Teenused ei saa kõik korraga käivituda. API ei saa töötada kui andmebaas ei ole veel käivitunud. Compose vajab teada õiget järjekorda.

Seda määrad `depends_on` võtmega. Kirjutad et API sõltub andmebaasist ja Compose käivitab andmebaasi enne.

Aga siin on oluline nüanss mis segab algajaid. `depends_on` ootab ainult kuni konteiner käivitub, mitte kuni teenus sees on päriselt valmis. PostgreSQL konteiner võib käivituda sekundiga, aga PostgreSQL ise võtab veel 5-10 sekundit et end seadistada ja valmis olla päringuid vastu võtma. Sel ajal API juba käivitub ja üritab ühenduda - saab errori.

Lahendus on health check. See on väike skript või käsk mida Compose regulaarselt käivitab et kontrollida kas teenus on päriselt valmis. Näiteks PostgreSQL'il on käsk `pg_isready` mis kontrollib kas andmebaas vastab. Compose käivitab seda iga mõne sekundi tagant. Kui see õnnestub, märgib teenuse "healthy". Ja kui ütled et API `depends_on` andmebaasi tingimuse "service_healthy", siis ootab Compose kuni andmebaas on päriselt valmis enne API käivitamist.

**Viide:** https://docs.docker.com/compose/startup-order/

---

## Keskkonnamuutujad ja konfiguratsioon

Konteinerid vajavad seadeid: andmebaasi paroole, API võtmeid, pordi numbreid. Need antakse keskkonnamuutujate kaudu.

Kõige lihtsam viis on kirjutada need otse Compose faili. Aga see ei ole hea idee sest siis on paroolid failis nähtavad ja kui commitid selle Git'i, on paroolid avalikud.

Parem viis on kasutada `.env` faili. See on lihtne tekstifail kus on muutujad ja väärtused. Compose loeb selle automaatselt ja saad Compose failis neid muutujaid kasutada. Näiteks kirjutad `.env` faili `DB_PASSWORD=minuparool` ja Compose failis kirjutad `${DB_PASSWORD}`. Compose asendab selle õige väärtusega.

Oluline: `.env` fail EI TOHI minna Git'i. See sisaldab saladusi. Pane see `.gitignore` faili. Aga tee `.env.example` fail kus on samad muutujad aga ilma väärtusteta - see näitab kolleegile millised muutujad on vajalikud.

**Viide:** https://docs.docker.com/compose/environment-variables/

---

## Põhilised käsud

Compose'i käsud on lihtsad. Kõik algavad `docker-compose` prefiksiga.

Kõige olulisem käsk on `up`. See käivitab kõik teenused. Kui käivitad lihtsalt `docker-compose up`, näed kõigi teenuste logisid reaalajas ühes aknas. See on hea arenduses. Kui lisad `-d` (detached), käivitab taustal - see on hea serverites.

Kui tahad näha mis töötab, kasuta `ps`. See näitab kõiki teenuseid ja nende staatust.

Kui midagi läheb valesti, vaata logisid: `docker-compose logs`. Lisades `-f` saad jälgida reaalajas, lisades teenuse nime näed ainult selle teenuse logisid.

Kui tahad kõik peatada, kasuta `stop`. See peatab konteinerid aga ei kustuta neid. Võid hiljem jätkata `start` käsuga.

Kui tahad kõik maha võtta ja puhastada, kasuta `down`. See kustutab konteinerid. Aga volumes jäävad alles - kui tahad ka need kustutada (ANDMED KAOVAD!), lisa `-v`.

Kui pead debugimiseks konteineri sisse minema, kasuta `exec`. Näiteks `docker-compose exec api sh` paneb su API konteineri shelli sisse.

**Viide:** https://docs.docker.com/compose/reference/

---

## Debugging

Kui midagi ei tööta, on süsteemne lähenemine.

Esiteks kontrolli kas kõik töötab: `docker-compose ps`. Kui mõni teenus on "Exit" staatuses või pidevalt restardib, on seal probleem.

Vaata logisid: `docker-compose logs teenuse_nimi`. Otsi sõnu nagu ERROR, FATAL, failed. Tavaliselt on seal selgitus mis valesti läks.

Kontrolli kas teenused näevad üksteist: mine teenuse sisse (`docker-compose exec teenus sh`) ja proovi teist teenust pingida. Kui ei saa vastust, on võrguprobleem.

Kontrolli keskkonnamuutujaid: kas kõik vajalikud muutujad on määratud? Kas väärtused on õiged?

Kui API ei käivitu või käitub imelikult, võib probleem olla volumes'ides - võib-olla on failid vales kohas või õigused on valed.

---

## Millal kasutada Compose

Compose on suurepärane väikeste ja keskmiste projektide jaoks. Kui arendad lokaalselt oma arvutis, on Compose ideaalne. Kui sul on üks server kuhu deploy'ida, piisab Compose'ist.

Aga Compose ei ole loodud suurte, jaotatud süsteemide jaoks. Kui vajad mitut serverit, automaatset skaleerimist (kui load kasvab, lisatakse automaatselt rohkem konteinereid), või keerukat failover'i, siis vaata Kubernetes'e või Docker Swarm'i poole.

Aga ausalt - 90% projektidest piisab Compose'ist. Ära mine Kubernetes'e ainult sellepärast et see on "cool" või et kõik räägivad sellest. Mine sinna kui sul on päris vajadus.

**Viide:** https://docs.docker.com/engine/swarm/

---

## Kokkuvõte

Docker Compose lahendab mitme konteineri haldamise probleemi. Sa kirjeldad oma rakenduse ühes failis - millised teenused on, kuidas nad omavahel suhtlevad, millised seaded on vajalikud. Compose hoolitseb ülejäänu eest: loob võrgu, käivitab teenused õiges järjekorras, seadistab DNS'i.

Peamised mõisted: teenused (services) on su rakenduse komponendid, volumes hoiavad andmeid püsivalt, võrgud võimaldavad teenustel omavahel suhelda, depends_on määrab järjekorra.

Järgmises labs ehitad ise terve mitme teenusega rakenduse kasutades Compose'i.

**Dokumentatsioon:** https://docs.docker.com/compose/
