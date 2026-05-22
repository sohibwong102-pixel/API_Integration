# ⚡ QUICK_FIXES PLAYBOOK 😎🔥

> kumpulan solusi cepat saat system mulai bertingkah aneh 😭🔥

---

# 🧠 Tujuan

Supaya:
- debugging kecil tidak makan 3 jam
- future self tidak search error yang sama terus 😭

---

# 🔥 Common Quick Fix

## Module tidak ketemu

```bash
export PYTHONPATH=.
```

---

## Port sudah dipakai

```bash
uvicorn main:app --reload --port 8001
```

---

## Venv tidak aktif

Linux / WSL:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

---

## Dependency chaos

```bash
pip install -r requirements.txt
```

---

## Env tidak kebaca

Checklist:

```txt
[ ] .env ada?
[ ] variable benar?
[ ] config load jalan?
```

---

## Provider timeout

Cek:
- internet 😭
- endpoint
- timeout config
- model terlalu berat

---

## Routing tidak pilih provider

Biasanya:

```txt
lupa register 😭🔥
```

Cek:

```txt
services/ai/registry.py
```

---

# ⚠️ Rule Besar

```txt
kalau fix cuma "restart dulu"

berarti chaos belum dipahami 😭🔥
```

---

# 😭 Final Doctrine

```txt
quick fix boleh 😎

TAPI:
akar chaos tetap harus dicari 😭🔥
```
