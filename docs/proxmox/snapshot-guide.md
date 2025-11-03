# Proxmox Snapshot

## Ilma Shutdown'ita (Kiire)

**Kui "Include RAM" EI OLE märgitud:**

1. **Snapshots** tab
2. **Take Snapshot**
   - Name: `after-network-config`
   - **Include RAM:** ❌ EI
3. Done!

VM jookseb kogu aeg. Snapshot valmis 5-10 sek.

---

## Shutdown'iga (Harva)

Kui PEAB RAM'i kaasama:

1. **Shutdown** VM
2. **Snapshots** → **Take Snapshot**
   - **Include RAM:** ✅ jah
3. **Start** VM

Aeglane (~1-2 min), suur fail (~8GB).

---

## Restore

1. **Shutdown** VM (kohustuslik!)
2. **Snapshots** → vali snapshot
3. **Rollback**
4. **Start** VM
