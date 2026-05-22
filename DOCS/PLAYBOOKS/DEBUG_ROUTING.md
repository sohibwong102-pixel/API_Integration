# 🔍 DEBUG_ROUTING PLAYBOOK 😎🔥

> cara debug routing sebelum goblin kehilangan kewarasan 😭🔥

---

# 🧠 Tujuan

Playbook ini dibuat supaya:
- routing chaos bisa ditelusuri
- fallback gampang dicek
- provider error cepat ketahuan

---

# 🔄 Alur Routing

```txt
request
→ router
→ pilih provider
→ execute
→ fallback jika gagal
→ return response
```

---

# 🚨 Checklist Debug

```txt
[ ] provider ter-register?
[ ] config kebaca?
[ ] API key valid?
[ ] endpoint hidup?
[ ] timeout terlalu kecil?
[ ] fallback aktif?
[ ] router pilih provider yang benar?
```

---

# ⚠️ Error Umum

## Provider tidak kepilih

Cek:

```txt
services/ai/registry.py
```

Biasanya:
```txt
lupa register 😭🔥
```

---

## Fallback tidak jalan

Cek:
- retry logic
- exception handling
- fallback order

---

## Timeout random

Cek:
- koneksi provider
- timeout config
- model terlalu berat 😭

---

# 😭 Emergency Doctrine

```txt
kalau routing mulai aneh:

jangan panik 😎
trace flow dulu 😎🔥
```
