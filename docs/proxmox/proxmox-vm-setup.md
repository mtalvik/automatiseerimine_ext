# Proxmox VM Võrgu Seadistamine

**Kestus:** ~20 min

---

## 1. Proxmox Ligipääs

**Kooli sisevõrgus:**
- https://10.231.231.2:8006 (HKHKPROX)

**Väljastpoolt:**
- https://proxmox.hkhk.edu.ee:8006

**Login:**
- User: sinu kasutajanimi
- Password: sinu parool
- **Realm: `hkhk.edu.ee`** (MITTE "Linux PAM"!)

⚠️ **HOIATUS:** Kui valid vale Realm, ei saa sisse!

**Kui HSTS viga:** kirjuta `thisisunsafe`

---

## 2. Oma Võrgu Leidmine

1. Kliki suvalise oma VM peale
2. **Hardware** tab
3. Vaata **Network Device** → näed `vmbr208` (näiteks)

**Reegel:** `vmbr[X]` → võrk on `10.0.[X].0/24`, gateway `10.0.[X].1`

| vmbr | Võrk | Gateway |
|------|------|---------|
| vmbr208 | 10.0.208.0/24 | 10.0.208.1 |
| vmbr82 | 10.0.82.0/24 | 10.0.82.1 |
| vmbr26 | 10.0.26.0/24 | 10.0.26.1 |

**IP plaan (täida):**

```
Võrk:     10.0.___.0/24
Gateway:  10.0.___.1
DNS:      8.8.8.8, 1.1.1.1

Masin         | IP            
--------------+---------------
WinKlient     | 10.0.___.10   
Ubuntu-1      | 10.0.___.20   
Ubuntu-2      | 10.0.___.21   
Alma-1        | 10.0.___.30   
Alma-2        | 10.0.___.31   
```

---

## 3. Vaikimisi Paroolid

| OS | Kasutaja | Parool |
|----|----------|--------|
| Linux | kasutaja | Passw0rd |
| Linux | root | Passw0rd |
| Windows | kasutaja | Passw0rd |

⚠️ **HOIATUS:** Number `0` (null), MITTE suurtäht O!

---

## 4. Ubuntu Netplan

### 1. Kontrolli Interface

```bash
ip a
```

Otsi: `ens18`, `enp0s3`, `eth0` (ignoreeri `lo`)

### 2. Netplan Config

```bash
cd /etc/netplan
ls -la

# Kopeeri vana fail
cp 50-cloud-init.yaml static.yaml
# või
cp 00-installer-config.yaml static.yaml

# Muuda
nano static.yaml
```

**YAML:**

⚠️ **2 TÜHIKUT, MITTE TAB!**

```yaml
network:
  version: 2
  ethernets:
    ens18:
      addresses:
        - 10.0.208.20/24
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
      routes:
        - to: default
          via: 10.0.208.1
```

**Muuda:**
- `ens18` → oma interface
- IP'd vastavalt oma võrgule

**Salvesta:** Ctrl+O → Enter → Ctrl+X

### 3. Rakenda

```bash
netplan generate static.yaml
netplan apply static.yaml

# Vana fail ümber
mv 50-cloud-init.yaml 50-cloud-init.yaml.bak

# Test
ip a
ping 8.8.8.8
```

---

## 5. Alma Linux

```bash
nmtui
```

1. **Edit a connection** → vali adapter
2. **IPv4 CONFIGURATION** → `<Manual>` → `<Show>`
3. Sisesta:
   - Addresses: `10.0.208.30/24`
   - Gateway: `10.0.208.1`
   - DNS: `8.8.8.8, 1.1.1.1`
4. `[X] Automatically connect`
5. **`<OK>`** → **Activate** → Deactivate/Activate

**Test:**

```bash
ping 8.8.8.8
```

---

## 6. Windows

**Login:** `kasutaja` / `Passw0rd`

**Settings** → **Network** → **Ethernet** → **IPv4** → **Properties**

| Väli | Väärtus |
|------|---------|
| IP address | 10.0.208.10 |
| Subnet mask | 255.255.255.0 |
| Gateway | 10.0.208.1 |
| DNS | 8.8.8.8 |

**Test:**

```powershell
ping 8.8.8.8
```

---

## 7. Snapshot

**Ilma shutdown'ita (kui RAM EI OLE märgitud):**

1. **Snapshots** tab
2. **Take Snapshot**
   - Name: `after-network-config`
   - **Include RAM:** ❌ EI
3. Done! VM jookseb edasi.

**Restore:**

1. **Shutdown** VM
2. **Snapshots** → vali → **Rollback**
3. **Start**

---

## 8. Kontroll

- [ ] Tean oma vmbr numbrit
- [ ] Ubuntu võrk töötab
- [ ] Alma võrk töötab
- [ ] Windows võrk töötab
- [ ] Snapshot tehtud

```bash
ip a
ping 8.8.8.8
```
