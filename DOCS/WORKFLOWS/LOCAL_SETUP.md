# 💻 LOCAL_SETUP PLAYBOOK 😎🔥

> cara setup project tanpa ritual summon error 😭🔥

---

# 🧠 Tujuan

Supaya:
- onboarding gampang
- setup konsisten
- future self tidak tersesat 😭

---

# ⚙️ Requirement

Minimal:
- Python 3.10+
- pip
- git
- virtualenv

Optional:
- Docker
- WSL Ubuntu 😎🔥

---

# 📦 Clone Repo

```bash
git clone <repo-url>
cd API_Integration
```

---

# 🧪 Buat Virtual Environment

```bash
python -m venv .venv
```

Activate:

## Linux / WSL

```bash
source .venv/bin/activate
```

## Windows

```bash
.venv\Scripts\activate
```

---

# 📥 Install Dependency

```bash
pip install -r requirements.txt
```

Kalau belum ada:
```txt
future goblin wajib bikin 😭🔥
```

---

# 🔑 Setup Environment

Buat:

```txt
.env
```

Contoh:

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
OLLAMA_BASE_URL=
```

---

# 🚀 Jalankan App

```bash
python main.py
```

Atau:

```bash
uvicorn main:app --reload
```

---

# 🧠 Swagger Docs

```txt
http://127.0.0.1:8000/docs
```

---

# ⚠️ Common Chaos

## Module tidak ketemu

Coba:

```bash
export PYTHONPATH=.
```

---

## Port bentrok

Ganti port:

```bash
uvicorn main:app --reload --port 8001
```

---

## Env tidak kebaca

Checklist:

```txt
[ ] file .env ada?
[ ] nama variable benar?
[ ] config.py sudah load?
```

---

# 😭 Final Doctrine

```txt
kalau setup makan waktu 3 jam:

berarti docs kurang jelas 😭🔥
```
