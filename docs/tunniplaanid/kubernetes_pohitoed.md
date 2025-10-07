# Tunnikava: Kubernetes – Konteinerite Orkestreerim (4×45 min) + 1.5h kodutöö

**Tase:** Keskmine (eelteadmised: Docker, YAML, võrgustik basics)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`, `lisa_labor.md`, `lisapraktika.md`

---

## 🎯 Õpiväljundid
- ÕV1: Selgitab, mis probleemi Kubernetes lahendab; eristab Pod, Deployment, Service
- ÕV2: Seadistab kohaliku klastri (Minikube/Kind) ja käivitab esimese Pod'i
- ÕV3: Kirjutab YAML manifeste ja kasutab `kubectl` käske ressursside haldamiseks
- ÕV4: Loob Deployment'e ja Service'eid rakenduste deploy'imiseks
- ÕV5: Skaleerib rakendusi ja kasutab põhilisi troubleshooting meetodeid

---

## 📚 Pedagoogiline raamistik

1. **Eelteadmised:** Õpilased teavad Docker'i – ehita Kubernetes sellele
2. **Arusaamine:** Õpeta MIKS orkestreerim ine on vajalik (mitte ainult käsud)
3. **Metakognitsioon:** Refleksioonid, kontrollküsimused, peer review

---

## 🛠️ Õpetamismeetodid

| Meetod | Kirjeldus | Millal |
|--------|-----------|--------|
| **Passiivne** | Loeng, demo | Blokk 1 (≤15 min) |
| **Aktiivne** | Guided practice | Lab (3×45 min) |
| **Interaktiivne** | Paaristöö | Iga blokk lõpus |

---

## 👨‍🏫 Näpunäited

### Enne tundi:
- [ ] Minikube/Kind installeeritud ja testitud
- [ ] `kubectl` töötab (`kubectl version`)
- [ ] Näidis YAML'id valmis

### Tunni ajal:
- **Minikube start võtab aega:** 2-3 min esimesel korral
- **YAML indentation:** Sama probleem kui Ansible!
- **Pods vs Deployments:** Õpilased segivad – selgita erinevust
- **Services:** Port mapping on keeruline – joonis on vajalik!

### Troubleshooting:
- **"ImagePullBackOff":** Vale image nimi või pole internetis
- **"CrashLoopBackOff":** Container crashib – vaata `kubectl logs`
- **"Pending":** Pole piisavalt ressursse või vale node selector

---

## 1. Kubernetes põhitõed ja esimene Pod

- **Eesmärk:** Mõista orkestreerimise vajadust, seadistada klaster, käivitada esimene Pod
- **Meetodid:** mini-loeng (≤15 min), demo, juhendatud praktika
- **Minutiplaan:**
  - 0–5: "Kui raske on 100 Docker container'it hallata?"
  - 5–15: Kubernetes arhitektuur (master, nodes, pods)
  - 15–25: Demo: `minikube start`, `kubectl get nodes`, esimene pod
  - 25–45: Lab: õpilased käivitavad Minikube ja esimese Pod'i

**Kontrollnimekiri:**

  - [ ] Minikube/Kind töötab
  - [ ] `kubectl` ühendub klastrile
  - [ ] Esimene Pod käivitatud
- **Refleksioon:** "Kuidas Kubernetes erineb Docker Compose'ist?"

---

## 2. Deployments ja skaleerim ine

- **Eesmärk:** Luua Deployment'e, mõista replica'sid, skaleerida rakendusi
- **Minutiplaan:**
  - 0–10: Deployment YAML demo
  - 10–35: Lab: loo Deployment, muuda replicas, vaata pod'e
  - 35–45: Paariskontroll + refleksioon
- **Kontrollküsimused:** "Mis vahe on Pod ja Deployment vahel?"

---

## 3. Services ja networking

- **Eesmärk:** Kasutada Service'eid rakenduste expose'imiseks
- **Minutiplaan:**
  - 0–15: Service types demo (ClusterIP, NodePort, LoadBalancer)
  - 15–40: Lab: loo Service, testi port-forward, curl rakendust
  - 40–45: Refleksioon
- **Kontrollküsimused:** "Millal NodePort vs LoadBalancer?"

---

## 4. Troubleshooting ja best practices

- **Eesmärk:** Debugida probleeme, rakendada best practices
- **Minutiplaan:**
  - 0–20: `kubectl logs`, `describe`, `exec` demo
  - 20–40: Lab: troubleshoot crashivad pods, resource limits
  - 40–45: Quiz + kodutöö
- **Kontrollküsimused:** "Kuidas debugida crashivat pod'i?"

---

## Kodutöö (1.5h)

- **Ülesanne:** Deploy'i 3-tier app (frontend + backend + db) Kubernetes'es
- **Kriteeriumid:**
  - [ ] 3 Deployment'i (nginx, API, MySQL)
  - [ ] Service'id iga komponendi jaoks
  - [ ] Rakendus töötab ja on ligipääsetav
  - [ ] README refleksiooniga

---

## 📖 Viited

- **Kubernetes Docs**: https://kubernetes.io/docs/
- **K8s Best Practices**: https://kubernetes.io/docs/concepts/configuration/overview/
- **Pedagoogika**: NRC (2000) *How People Learn*

---

## 🎓 Kokkuvõte

**Teha:**
- ✅ Alusta Docker'i teadmistega
- ✅ Selgita MIKS orkestreerim ine
- ✅ Minikube/Kind (mitte real cluster!)
- ✅ YAML demo koos vigadega

**Mitte teha:**
- ❌ Helm, Operators, Ingress kohe
- ❌ Cloud clusters (liiga kallis!)
- ❌ 50 resource tüüpi