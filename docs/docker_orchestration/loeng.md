# Docker Compose ja Mitme Konteineri Haldamine

**Eeldused:** Docker fundamentals, container concepts, basic YAML syntax  
**Platvorm:** Docker Engine 20.10+, Docker Compose v2

## Õpiväljundid

Pärast seda loengut oskate:
- Kirjutada ja käivitada Docker Compose faile
- Ehitada multi-container rakendusi
- Mõista teenuste vahelist suhtlust ja võrgustikku
- Hallata erinevaid keskkondi (development, production)
- Debugida ja tõrkeotsingut teha
- Mõista orkestreerimise põhimõtteid ja vajadust

---

Kaasaegne veebirakendus ei ole üks programm. See koosneb erinevatest komponentidest: andmebaas hoiab andmeid, API server käsitleb ärilogikat, frontend näitab kasutajaliidest, cache teeb süsteemi kiireks. Igaüks neist töötab eraldi konteineris. Iga komponent on teadlikult eraldatud, et saaks seda sõltumatult arendada, testida ja skaleerida - see on mikroteenuste arhitektuuri põhiprintsiip.

Küsimus on lihtne: kuidas neid kõiki koos hallata?

Docker Compose vastab sellele küsimusele. See on tööriist mis muudab mitme konteineri haldamise lihtsaks ja hallatavaks. Ilma Compose'ita peaksite iga konteineri käivitama eraldi käsuga, meelde jätma järjekorra, haldama IP aadresse ja võrgustikku - see muutub kiiresti kaootiliseks.

## 1. Käsitsi haldamise probleem

Vaatame näidet. Sul on kaks komponenti: PostgreSQL andmebaas ja Node.js API server.

Käivitad andmebaasi käsuga `docker run -d --name mydb postgres:13`. See töötab. Aga nüüd tahad API käivitada ja API vajab andmebaasi aadressi. Milline see on? Sa ei tea. Docker genereerib IP aadressi dünaamiliselt. Pead käsitsi välja uurima millise IP Docker andmebaasile andis (`docker inspect mydb | grep IPAddress`). Siis pead selle API käivitamise käsku kirjutama, lisades environment variable'i **DATABASE_URL** väärtusega mis sisaldab seda IP'd.

Järgmine päev käivitad uuesti - IP on erinev. Pead jälle käsitsi uurima ja muutma. Või veel hullem - kolleeg proovib sinu projekti käivitada oma arvutis ja IP'd on täiesti erinevad.

Lisaks sellele - kui API käivitub liiga kiiresti ja andmebaas ei ole veel valmis, saad errori. Pead ootama... aga kui kaua? 5 sekundit? 10? Raske öelda. Praktikas tähendab see et kirjutad bash skripti mis proovib käivitada, ootab, kontrollib, proovib uuesti - kõik käsitsi.

Kui sul on 5-6 erinevat komponenti, muutub see haldamatuks. Pead meeles pidama järjekorda, IP aadresse, ootama et asjad valmis saaksid. Ja kui tahad et kolleeg saaks sama projekti käivitada, pead kogu selle protsessi talle selgitama. Iga uus liige meeskonnas kulutab päeva projekti üles seadmisele.

## 2. Docker Compose lahendus

Compose'i põhiidee on lihtne: kirjelda kogu süsteem ühes failis. Ära ütle KUIDAS asjad teha, vaid ÜTLE MIDA sa tahad. See on deklaratiivne lähenemine - sa kirjeldad soovitud lõpptulemust, mitte samme sinna jõudmiseks.

Loome faili nimega `docker-compose.yml`. Selles failis kirjeldame meie kahe komponendiga süsteemi. Kirjutame et meil on kaks teenust: üks nimega "database" mis kasutab PostgreSQL'i, ja teine nimega "api" mis kasutab meie API koodi. Ütleme ka et API vajab andmebaasi, seega andmebaas peab enne käivituma.

Kui see fail on olemas, käivitame terve süsteemi ühe käsuga: `docker-compose up`. Compose loeb faili, mõistab mida me tahame, ja teeb kõik vajaliku: loob võrgu, käivitab teenused õiges järjekorras, seadistab et nad leiaksid üksteist. Kõik see juhtub automaatselt - te ei pea midagi käsitsi konfigureerima.

Kõige olulisem - me ei kirjuta IP aadresse. Kirjutame lihtsalt teenuse nime "database" ja Compose teab kuidas teenused ühendada. Kui teenused on samas Compose projektis, näevad nad üksteist automaatselt. Sisemiselt loob Compose DNS serveri, mis lahendab teenuste nimed IP aadressideks - täpselt nagu internet DNS lahendab domeeni nimed.

See on deklaratiivne lähenemine. Imperatiivselt sa ütleksid "tee samm üks, siis samm kaks, siis samm kolm". Deklaratiivselt sa ütled "ma tahan et lõpuks oleks selline süsteem" ja tööriist mõtleb välja kuidas sinna jõuda. See on sama erinevus mis Ansible ja shell skriptide vahel - üks kirjeldab tulemust, teine kirjeldab samme.

## 3. Compose faili struktuur

Compose fail on YAML formaadis tekstifail. YAML on lihtne formaat kus struktuur on määratud taandetega - täpselt nagu Python koodis. Kui midagi on rohkem taandatud, on see eelmise asja "sees". YAML valimine oli teadlik otsus - see on inimestele loetavam kui JSON või XML, aga piisavalt struktureeritud et masinad saaksid seda töödelda.

Iga Compose fail algab versiooniga. See number ütleb Compose'ile millise formaadiga on tegemist. Kasuta alati vähemalt `3.8` - see on piisavalt uus et kõik kasulikud võimalused oleksid olemas, aga piisavalt stabiilne et igal pool töötaks. Vanemad versioonid (2.x ja 1.x) on deprecated ja neil puuduvad olulised features nagu **secrets** ja **configs**.

Pärast versiooni tuleb `services` sektsioon. See on faili kõige olulisem osa. Siin sa kirjeldad oma rakenduse komponendid - igaüks neist saab oma konteineri. Iga komponendi all kirjeldad kuidas see käituma peab: millist Docker image't kasutada, millised pordid avada, millised seaded on vajalikud.

Kui su rakendus vajab et andmed jääksid alles isegi kui konteiner kustutatakse, lisad `volumes` sektsiooni. Siin defineerid püsivad andmehoidlad. Need on eraldi deklareeritud, sest sageli tahad ühte volume'd jagada mitme teenuse vahel, või luua volume enne teenuste käivitamist.

Kui vajad kontrolli võrkude üle - näiteks tahad et mõned teenused oleksid isoleeritud - võid lisada `networks` sektsiooni. Aga enamasti seda ei vaja, sest Compose loob automaatselt võrgu kõigile teenustele. Custom networks on kasulikud kui teil on frontend ja backend, ning te ei taha et frontend näeks andmebaasi otse - ainult läbi backend API.

## 4. Teenused

Teenus on sinu rakenduse üks komponent. Kui mõtled oma rakendusele kui firmale, siis teenused on osakonnad: üks vastutab andmete hoidmise eest, teine tegeleb äriloogikaga, kolmas näitab kasutajaliidet. Iga teenus on isoleeritud ja vastutab ainult oma ülesande eest - see on **separation of concerns** printsiip.

Kõige lihtsam teenus vajab ainult nime ja image't. Näiteks kui tahad Redis cache'i, kirjutad et sul on teenus nimega "cache" mis kasutab Redis'e. Compose tõmbab Redis image ja käivitab konteineri. See konteiner on kättesaadav teistele teenustele nimega "cache". Hostname on täpselt sama mis teenuse nimi - see on automaatne ja alati nii.

Aga tavaliselt vajad rohkem. Pead ütlema millised pordid avada - kui brauser peab su API'le ligi pääsema, pead pordi avama. Pead andma seadeid keskkonnamuutujate kaudu - paroolid, API võtmed, konfiguratsioon. Kui tahad et konteiner näeks sinu hosti faile - näiteks arenduses kui muudad koodi ja tahad et muudatused kohe näha oleksid - kasutad volumes'eid. Bind mount development'is tähendab, et muudad faili oma IDE's, salvestad Ctrl+S, ja server restartib automaatselt uue koodiga.

Ja väga oluline - kui üks teenus sõltub teisest, pead seda ütlema. Kui API vajab andmebaasi, kirjutad et API `depends_on` andmebaasist. Siis Compose käivitab andmebaasi enne API'd. Ilma selleta võivad teenused käivituda juhuslikult ja API võib proovida andmebaasiga ühenduda enne kui see on valmis.

## 5. Teenuste suhtlus

See on Compose'i kõige võimsam ja elegantne feature. Kui käivitad teenused Compose'iga, loob ta automaatselt sisemise võrgu. Selles võrgus töötab DNS server mis teab kõigi teenuste nimesid ja IP aadresse. See DNS server on Docker Engine osa ja töötab täiesti automaatselt - te ei pea seda konfigureerima ega installima.

See tähendab et kui sul on teenus nimega "database", siis iga teine teenus samas võrgus saab sellega ühenduda kasutades lihtsalt nime "database". Mitte IP aadressi - lihtsalt nime. Docker lahendab selle automaatselt õigeks IP'ks. Tehniliselt: Docker Engine embedded DNS server kuulab pordi 127.0.0.11 peal igas konteineris ja vastab DNS päringutele.

Praktikas tähendab see et kui API vajab andmebaasiga ühendust, kirjutad ta konfiguratsioonifailis või keskkonnamuutujas lihtsalt "ühenda andmebaasiga nimega database". Pole vaja teada IP'd. Pole vaja muretseda et IP võib muutuda. Pole vaja konfiguratsiooni uuendada kui midagi muutub. See töötab isegi kui kustutad konteineri ja teed uue - DNS entry uuendatakse automaatselt uue IP'ga.

See on võimas sest muudab süsteemi paindlikuks. Saad teenuseid liigutada, uuesti käivitada, asendada - ja teised teenused leiavad nad ikka automaatselt. Saad ka skaleerida teenuseid (`docker-compose up --scale api=3`) ja DNS teeb round-robin load balancing'u automaatselt.

Oluline mõista: see DNS töötab ainult Compose võrgu sees. Kui tahad et väljastpoolt (näiteks sinu brauser) saaks teenusele ligi, pead pordi avama `ports` sektsiooniga. Ports loob mapping'u host'i ja konteineri vahel - näiteks `8080:80` tähendab "host'i port 8080 suunab konteineri port 80 peale".

## 6. Andmete püsimine

Konteinerid on loodud olema ajutised. Kui kustutad konteineri, kaob ka kõik mis seal sees oli. See on disain - konteinerid peaksid olema "cattle not pets", nagu öeldakse. Saad igal ajal uue teha. See printsiip tuleb cloud computing'ust: server'id (virtuaalmasinad, konteinerid) peaksid olema kergesti asenvatavad, mitte unikaalsed lumehelvakesed mida kardetakse puudutada.

Aga andmebaas ei saa olla ajutine. Andmed peavad jääma alles. Siin tulevad mängu volumes. Volume on Docker'i abstrakt andmehoidla - see on eraldatud konteineri failisüsteemist ja elab kauem kui konteiner ise.

Volume on nagu väline kõvaketas mille saad konteinerile külge ühendada. Kui konteiner kirjutab andmeid volume'i, jäävad need sinna püsivalt. Isegi kui konteiner kustutatakse ja tehakse uus, ühendatakse sama volume uuesti külge ja andmed on tagasi. Tehniliselt Docker hoiab volume'id host'i failisüsteemis spetsiaalses kaustas (tavaliselt `/var/lib/docker/volumes/`), aga te ei peaks kunagi otse sinna puutuma - kasutage Docker käske.

Compose'is defineerid volume kaks korda. Esiteks teenuse juures ütled KUHU konteineri failisüsteemis see ühendatakse. Näiteks PostgreSQL hoiab andmeid kaustas `/var/lib/postgresql/data`, seega ühendad volume sinna. Teiseks faili lõpus `volumes` sektsioonis deklareerid et see volume eksisteerib. See kahekordne deklaratsioon võimaldab sama volume'd kasutada mitmes teenuses, kui vaja.

On ka teine variant - bind mount. See ei loo uut volume'd vaid ühendab otse sinu hosti kausta konteineriga. See on kasulik arenduses: kui kirjutad koodi oma arvutis ja tahad et konteiner näeks kohe muudatusi, mount'id koodi kausta sisse. Iga kord kui salvestad faili, on see kohe konteineris nähtav. Aga bind mount'id on ohtlikud produktsioonis - need sõltuvad host'i failisüsteemi struktuurist ja õigustest, mis võib olla erinev eri serverites.

## 7. Teenuste järjekord

Teenused ei saa kõik korraga käivituda. API ei saa töötada kui andmebaas ei ole veel käivitunud. Compose vajab teada õiget järjekorda. Ilma selleta võib juhtuda et API käivitub esimesena, proovib andmebaasiga ühendust, saab "connection refused" errori ja crashib.

Seda määrad `depends_on` võtmega. Kirjutad et API sõltub andmebaasist ja Compose käivitab andmebaasi enne. See on deklaratiivne viis öelda "need asjad on seotud".

Aga siin on oluline nüanss mis segab algajaid. Depends_on ootab ainult kuni konteiner käivitub, mitte kuni teenus sees on päriselt valmis. PostgreSQL konteiner võib käivituda sekundiga, aga PostgreSQL ise võtab veel 5-10 sekundit et end seadistada ja valmis olla päringuid vastu võtma. Sel ajal API juba käivitub ja üritab ühenduda - saab errori. See on klassikaline race condition distributed süsteemides.

Lahendus on health check. See on väike skript või käsk mida Compose regulaarselt käivitab et kontrollida kas teenus on päriselt valmis. Näiteks PostgreSQL'il on käsk `pg_isready` mis kontrollib kas andmebaas vastab. Compose käivitab seda iga mõne sekundi tagant. Kui see õnnestub, märgib teenuse "healthy". Ja kui ütled et API depends_on andmebaasi tingimuse "service_healthy", siis ootab Compose kuni andmebaas on päriselt valmis enne API käivitamist. See on korrektne viis käsitleda teenuste sõltuvusi.

## 8. Keskkonnamuutujad

Konteinerid vajavad seadeid: andmebaasi paroole, API võtmeid, pordi numbreid. Need antakse keskkonnamuutujate kaudu. See on 12-factor app metodoloogia põhiprintsiip - konfiguratsioon peaks olema keskkonnas, mitte koodis.

Kõige lihtsam viis on kirjutada need otse Compose faili. Aga see ei ole hea idee sest siis on paroolid failis nähtavad ja kui commitid selle Git'i, on paroolid avalikud. Paljudes ettevõtetes on juhtunud turvaintsidente just seetõttu - keegi committis kogemata `.env` või config faili kus olid production andmebaasi paroolid, ja see läks GitHubi public repo'sse.

Parem viis on kasutada `.env` faili. See on lihtne tekstifail kus on muutujad ja väärtused. Compose loeb selle automaatselt ja saad Compose failis neid muutujaid kasutada. Näiteks kirjutad `.env` faili `DB_PASSWORD=minuparool` ja Compose failis kirjutad `${DB_PASSWORD}`. Compose asendab selle õige väärtusega. See toimib täpselt nagu template engine - muutujad asendatakse väärtustega enne kui Compose faili parsitakse.

Oluline: `.env` fail EI TOHI minna Git'i. See sisaldab saladusi. Pane see `.gitignore` faili. Aga tee `.env.example` fail kus on samad muutujad aga ilma väärtusteta või placeholder väärtustega - see näitab kolleegile millised muutujad on vajalikud. Näiteks `.env.example` võib sisaldada `DB_PASSWORD=changeme` ja `.env` sisaldab päris parooli.

## 9. Põhilised käsud

Compose'i käsud on lihtsad. Kõik algavad `docker-compose` prefiksiga (uuemates versioonides võib kasutada ka `docker compose` ilma sidekriipsuta - see on Docker CLI native integratsioon).

Kõige olulisem käsk on `up`. See käivitab kõik teenused. Kui käivitad lihtsalt `docker-compose up`, näed kõigi teenuste logisid reaalajas ühes aknas. See on hea arenduses - näed kõike mis juhtub. Kui lisad `-d` (detached), käivitab taustal - see on hea serverites. Detached mode'is jooksevad teenused taustal ja te saate terminali tagasi kasutada.

Kui tahad näha mis töötab, kasuta `ps`. See näitab kõiki teenuseid ja nende staatust - running, exited, restarting. Kui mõni teenus pidevalt restartib, on seal probleem.

Kui midagi läheb valesti, vaata logisid: `docker-compose logs`. Lisades `-f` saad jälgida reaalajas (follow), lisades teenuse nime näed ainult selle teenuse logisid. Flag `-f` töötab sarnaselt `tail -f` käsule UNIX'is - see jääb terminali kinni ja näitab uusi logiridu nagu nad tulevad.

Kui tahad kõik peatada, kasuta `stop`. See peatab konteinerid aga ei kustuta neid. Võid hiljem jätkata `start` käsuga. Konteinerite failisüsteem jääb alles, ainult protsessid peatuvad.

Kui tahad kõik maha võtta ja puhastada, kasuta `down`. See kustutab konteinerid. Aga volumes jäävad alles - kui tahad ka need kustutada (ANDMED KAOVAD!), lisa `-v`. Käsk `docker-compose down -v` on ohtlik - kasuta seda ainult arenduses, mitte kunagi produktsioonis ilma varunduseta.

Kui pead debugimiseks konteineri sisse minema, kasuta `exec`. Näiteks `docker-compose exec api sh` paneb su API konteineri shelli sisse. Sealt saad failisüsteemi uurida, käske käivitada, logisid vaadata. See on nagu SSH konteineri sisse, ainult et kasutab Docker API'd, mitte SSH'd.

## 10. Debugging

Kui midagi ei tööta, on süsteemne lähenemine. Debugging võib tunduda keeruline, aga kui lähed samm-sammult, leiad probleemi alati.

Esiteks kontrolli kas kõik töötab: `docker-compose ps`. Kui mõni teenus on "Exit" staatuses või pidevalt restardib, on seal probleem. "Exit 0" tähendab et teenus lõpetas edukalt (mis on imelik teenuse puhul mis peaks töötama), "Exit 1" või muu number tähendab viga.

Vaata logisid: `docker-compose logs teenuse_nimi`. Otsi sõnu nagu ERROR, FATAL, failed, exception. Tavaliselt on seal selgitus mis valesti läks. PostgreSQL'i logid ütlevad näiteks "FATAL: password authentication failed" - selge, et parool on vale. Node.js logid võivad öelda "ECONNREFUSED" - ei saa andmebaasiga ühendust.

Kontrolli kas teenused näevad üksteist: mine teenuse sisse (`docker-compose exec teenus sh`) ja proovi teist teenust pingida või `nslookup` käsuga lahendada. Kui ei saa vastust, on võrguprobleem - kas teenused pole samas võrgus või DNS ei tööta.

Kontrolli keskkonnamuutujaid: kas kõik vajalikud muutujad on määratud? Kas väärtused on õiged? Kasuta `docker-compose config` et näha kuidas Compose tõlgendas YAML faili - see näitab ka kõiki asendatud muutujaid.

Kui API ei käivitu või käitub imelikult, võib probleem olla volumes'ides - võib-olla on failid vales kohas või õigused on valed. Linuxis võivad file permissions põhjustada kummalisi probleeme kui host user ID ei kattu konteineri user ID'ga.

## 11. Millal kasutada Compose

Compose on suurepärane väikeste ja keskmiste projektide jaoks. Kui arendad lokaalselt oma arvutis, on Compose ideaalne. Kui sul on üks server kuhu deploy'ida, piisab Compose'ist. Enamik startup'e ja väiksemaid projekte töötavad edukalt ainult Compose'iga ilma Kubernetes'i vajamata.

Aga Compose ei ole loodud suurte, jaotatud süsteemide jaoks. Kui vajad mitut serverit, automaatset skaleerimist (kui load kasvab, lisatakse automaatselt rohkem konteinereid), või keerukat failover'i, siis vaata Kubernetes'e või Docker Swarm'i poole. Compose töötab ainult ühel host'il - sa ei saa jaotada teenuseid mitme serveri vahel.

Aga ausalt - 90% projektidest piisab Compose'ist. Ära mine Kubernetes'e ainult sellepärast et see on "cool" või et kõik räägivad sellest. Mine sinna kui sul on päris vajadus. Kubernetes toob kaasa märkimisväärse keerukuse - YAML failid on palju keerulisemad, vajad eraldi cluster'it, õppekulg on järsem. Hinda kas see keerukus on õigustatud sinu kasutusprobleemiga.

## Kokkuvõte

Docker Compose lahendab mitme konteineri haldamise probleemi. Sa kirjeldad oma rakenduse ühes failis - millised teenused on, kuidas nad omavahel suhtlevad, millised seaded on vajalikud. Compose hoolitseb ülejäänu eest: loob võrgu, käivitab teenused õiges järjekorras, seadistab DNS'i. Üks YAML fail asendab kümneid `docker run` käske ja bash skripte.

Peamised mõisted: teenused (services) on su rakenduse komponendid, volumes hoiavad andmeid püsivalt, võrgud võimaldavad teenustel omavahel suhelda, depends_on määrab järjekorra. Kõik need kontseptsioonid töötavad koos, et luua terviklik, hallatav süsteem.

Järgmises labs ehitad ise terve mitme teenusega rakenduse kasutades Compose'i. Näed praktikas kuidas YAML fail muutub töötavaks rakenduseks.