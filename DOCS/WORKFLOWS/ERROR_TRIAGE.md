# 🚨 ERROR_TRIAGE PLAYBOOK 😎🔥

> panduan identifikasi error sebelum goblin menyalahkan semesta 😭🔥

---

# 🧠 Tujuan

Supaya:
- error cepat dikenali
- recovery lebih jelas
- debugging ga random

---

# 🔥 Kategori Error

## 4xx → Client Problem

Contoh:
```txt
400 bad request
401 unauthorized
403 forbidden
404 not found
429 rate limit
```

Biasanya:
- input salah
- auth salah
- request aneh 😭

---

## 5xx → Internal Chaos

Contoh:
```txt
500 internal server error
502 bad gateway
503 service unavailable
```

Biasanya:
- provider mati
- workflow rusak
- routing chaos
- dependency ngamuk 😭🔥

---

# 🔄 Alur Triage

```txt
cek log
→ identifikasi layer
→ cek provider
→ cek routing
→ cek fallback
→ cek config
```

---

# ⚠️ Rule Besar

```txt
jangan langsung nyalahin provider 😭🔥
```

Kadang:
- env salah
- config typo
- routing lupa update
- async chaos 😭

---

# 😭 Emergency Doctrine

```txt
panic tidak memperbaiki stack trace 😎🔥
```
