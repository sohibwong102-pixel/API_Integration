# 🚀 PANDUAN LENGKAP: SETUP & TEST OPENROUTER PROVIDER

Panduan ini memberikan **roadmap menyeluruh** dari awal hingga berhasil test endpoint OpenRouter di Swagger & OpenWebUI.

---

## 📋 DAFTAR ISI

0. [⚡ Quick Start - 5 Menit Setup](#-quick-start---5-menit-setup)
1. [Prerequisites](#prerequisites)
2. [Langkah 1: Dapatkan OpenRouter API Key](#langkah-1-dapatkan-openrouter-api-key)
3. [Langkah 2: Setup File .env](#langkah-2-setup-file-env)
4. [Langkah 3: Validasi Konfigurasi](#langkah-3-validasi-konfigurasi)
5. [Langkah 4: Jalankan Server](#langkah-4-jalankan-server)
6. [Langkah 5: Test di Swagger](#langkah-5-test-di-swagger)
7. [Langkah 6: Test di OpenWebUI](#langkah-6-test-di-openwebui)
8. [🆘 Troubleshooting - Antisipasi Error](#troubleshooting---antisipasi-error)
9. [🔧 Quick Reference](#quick-reference)

---

## ⚡ Quick Start - 5 Menit Setup

**TL;DR**: Setup `.env` saja, langsung test! Tidak perlu ubah file lain.

### Ringkas Steps:

```bash
# 1. Dapatkan API Key dari https://openrouter.ai/
# (Copy: sk-or-v1-xxxxx)

# 2. Edit file .env
echo "PRIMARY_PROVIDER=openrouter" >> .env
echo "OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE" >> .env
echo "OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct:free" >> .env

# 3. Jalankan server
python main.py

# 4. Test di browser
# Buka: http://127.0.0.1:8000/docs
# Cari endpoint: POST /api/issue/summary
# Isi: {"text": "Database error"}
# Click Execute!
```

### ✅ Hanya 3 File Yang Perlu Disentuh:

| File      | Aksi                              |
| --------- | --------------------------------- |
| `.env`    | ✏️ Edit (tambahin 3 baris config) |
| `main.py` | ▶️ Run (tidak diubah)             |
| (Swagger) | 🧪 Test (tidak diubah)            |

### ❌ Tidak Perlu Ubah:

```
services/ai/providers/openrouter_provider.py  ← Sudah ready!
services/ai/router.py                         ← Sudah implement fallback!
services/ai/registry.py                       ← Sudah register provider!
api/routes.py                                 ← Sudah valid input!
```

**Semua provider logic sudah built-in, tinggal set .env dan GO! 🚀**

---

---

## Prerequisites

Pastikan Anda memiliki:

✅ Python 3.9+ terinstal
✅ Git terinstal
✅ Akses ke OpenRouter (https://openrouter.ai/)
✅ Virtual environment sudah aktif (atau siap diaktifkan)
✅ IDE/Editor dengan terminal (VS Code/PyCharm/dll)

Periksa versi Python:

```bash
python --version   # Pastikan >= 3.9
```

---

## LANGKAH 1: Setup File .env

### 2.1 Cek Struktur File .env

File konfigurasi `.env` berada di **root project** (sejajar dengan `main.py`):

```
API_CIVIL_GROUP/
├── main.py
├── .env              ← File yang akan kita setup
├── .env.example      ← Template referensi
├── README.md
└── ...
```

### 2.2 Buat atau Edit File .env

Jika belum ada `.env`, buat file baru:

**Option A: Copy dari template**

```bash
cp .env.example .env
```

**Option B: Buat manual**

```bash
touch .env
```

### 2.3 Konfigurasi Minimal untuk OpenRouter

Edit file `.env` dan tambahkan konfigurasi berikut:

```bash
# ============================================================
# 🖥️ KONFIGURASI SERVER UTAMA
# ============================================================
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000

# ============================================================
# 🤖 KONFIGURASI PENYEDIA AI (OPENROUTER CONFIG)
# ============================================================

# PRIMARY_PROVIDER: Provider utama yang akan digunakan
# Opsi: 'openrouter', 'local_ollama', 'openai', 'google_gemini', 'mock'
PRIMARY_PROVIDER=openrouter

# FALLBACK_PROVIDER: Provider cadangan jika primary gagal
# Opsi: 'mock', 'local_ollama', dll
FALLBACK_PROVIDER=mock

# ENABLE_FALLBACK: Aktifkan auto-failover ke fallback provider (true/false)
ENABLE_FALLBACK=true

# ============================================================
# OPENROUTER SPESIFIK CONFIG
# ============================================================

# OPENROUTER_API_KEY: API Key Anda dari https://openrouter.ai/
# ⚠️ PENTING: Ganti 'your_openrouter_api_key_here' dengan API key yang sebenarnya!
# Format: sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENROUTER_API_KEY=your_openrouter_api_key_here

# OPENROUTER_MODEL: Model yang akan digunakan
# Recommended model (free tier):
# - meta-llama/llama-3-8b-instruct:free    (CEPAT & GRATIS)
# - meta-llama/llama-3-70b-instruct:free   (LEBIH POWERFUL, tapi lebih lambat)
#
# Paid models (lebih berkualitas):
# - gpt-4o-mini          (OpenAI GPT-4 mini version)
# - google/gemini-2.0-flash-exp  (Google Gemini)
# - mistralai/mistral-large      (Mistral)
#
# List model lengkap: https://openrouter.ai/docs#models
OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct:free

# ============================================================
# 💾 KONFIGURASI PENYIMPANAN DATA
# ============================================================
DB_STORAGE_PATH=storage/history.json
```

### 2.4 Verifikasi File .env

Setelah selesai, file `.env` Anda harus terlihat seperti ini:

```bash
cat .env
```

Output yang diharapkan:

```
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000
PRIMARY_PROVIDER=openrouter
FALLBACK_PROVIDER=mock
ENABLE_FALLBACK=true
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct:free
DB_STORAGE_PATH=storage/history.json
```

✅ **Pastikan tidak ada typo atau spasi berlebih!**

---

## LANGKAH 3: Validasi Konfigurasi

Sebelum menjalankan server, validasi setup Anda:

### 3.1 Cek Environment Variables

Buka terminal di root project dan jalankan:

```bash
# Verifikasi .env dapat dibaca Python
python -c "
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.env')
if env_path.exists():
    load_dotenv()
    print('✅ .env file found and loaded')
    print(f'  PRIMARY_PROVIDER: {os.getenv(\"PRIMARY_PROVIDER\")}')
    print(f'  OPENROUTER_API_KEY: {os.getenv(\"OPENROUTER_API_KEY\", \"NOT SET\")[:20]}...')
    print(f'  OPENROUTER_MODEL: {os.getenv(\"OPENROUTER_MODEL\")}')
else:
    print('❌ .env file not found at', env_path.resolve())
"
```

### 3.2 Jalankan Validasi Settings

```bash
python -c "
from core import settings
print('✅ Settings loaded successfully!')
print(f'  App Environment: {settings.APP_ENV}')
print(f'  Primary Provider: {settings.PRIMARY_PROVIDER}')
print(f'  OpenRouter API Key Set: {bool(settings.OPENROUTER_API_KEY)}')
print(f'  OpenRouter Model: {settings.OPENROUTER_MODEL}')
"
```

**Jika error muncul**, lihat section [Troubleshooting](#troubleshooting---antisipasi-error).

### 3.3 Test Koneksi ke OpenRouter (Optional)

Untuk test koneksi tanpa menjalankan server:

```bash
python -c "
import requests
import os
from core import settings

api_key = settings.OPENROUTER_API_KEY
if not api_key:
    print('❌ OPENROUTER_API_KEY tidak diset!')
    exit(1)

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

payload = {
    'model': settings.OPENROUTER_MODEL,
    'messages': [{'role': 'user', 'content': 'Say hello'}],
    'max_tokens': 10
}

try:
    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        json=payload,
        headers=headers,
        timeout=10
    )
    if response.status_code == 200:
        print('✅ OpenRouter API connection successful!')
        print(f'   Response: {response.json()[\"choices\"][0][\"message\"][\"content\"]}')
    else:
        print(f'❌ OpenRouter API error: {response.status_code}')
        print(f'   {response.text}')
except Exception as e:
    print(f'❌ Connection error: {e}')
"
```

---

## LANGKAH 4: Jalankan Server

### 4.1 Aktivasi Virtual Environment (Jika Belum)

```bash
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 4.2 Install Dependencies (Jika Belum)

```bash
pip install -r requirements.txt
```

Atau manual:

```bash
pip install fastapi uvicorn requests pydantic python-dotenv
```

### 4.3 Jalankan Server

```bash
python main.py
```

**Output yang diharapkan:**

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

✅ **Server berhasil berjalan!**

---

## LANGKAH 5: Test di Swagger

### 5.1 Buka Swagger UI

Setelah server berjalan, buka browser dan kunjungi:

```
http://127.0.0.1:8000/docs
```

**Atau gunakan link langsung:**

- Local: http://localhost:8000/docs
- Remote: http://your_server_ip:8000/docs

### 5.2 Cari Endpoint Issue Summary

Di Swagger UI:

1. Cari endpoint `/api/issue/summary` (POST)
2. Klik untuk membuka detail endpoint

### 5.3 Test Request

1. Klik tombol **"Try it out"**
2. Isi request body JSON:

```json
{
  "text": "Database connection failed after migration to new server. Error: timeout on port 5432"
}
```

3. Klik **"Execute"**

### 5.4 Verifikasi Response

**Response yang diharapkan (status 200):**

```json
{
  "summary": "Database connection timeout after server migration on port 5432",
  "request_id": "abc123def456"
}
```

**Response yang diharapkan dari OpenRouter:**

- ✅ Summary berisi ringkasan dari prompt Anda
- ✅ Status code: 200 (OK)
- ✅ Time: beberapa detik (tergantung model & latency)

### 5.5 Test Endpoint Lainnya

Provider yang sama (OpenRouter) digunakan untuk endpoint lain:

| Endpoint                | Method | Deskripsi          |
| ----------------------- | ------ | ------------------ |
| `/api/issue/summary`    | POST   | Ringkasan issue    |
| `/api/issue/categorize` | POST   | Kategori issue     |
| `/api/issue/severity`   | POST   | Level severity     |
| `/api/issue/tags`       | POST   | Tag extraction     |
| `/api/issue/sentiment`  | POST   | Sentiment analysis |

Coba setiap endpoint dengan test input.

---

## LANGKAH 6: Test di OpenWebUI

### 6.1 Pra-syarat OpenWebUI

OpenWebUI adalah interface untuk test provider yang kompatibel dengan OpenAI API format.

**Option A: Gunakan OpenWebUI Online (Recommended untuk testing)**

1. Buka https://openwebui.com/
2. Tidak perlu instalasi lokal

**Option B: Install OpenWebUI Lokal**

```bash
# Install via Docker (recommended)
docker run -d -p 3000:8080 --name open-webui ghcr.io/open-webui/open-webui:latest

# Atau install via pip
pip install open-webui
open-webui serve
```

### 6.2 Setup Connection ke API Anda

Di OpenWebUI:

1. **Settings** → **Connections** (atau **Models**)
2. Tambah **New Connection** / **New Provider**
3. Isi konfigurasi:

```
Provider Name: OpenRouter (Civil)
API Base URL: http://127.0.0.1:8000/v1
API Key: (optional - bisa kosong jika public)
Model Name: meta-llama/llama-3-8b-instruct:free
```

### 6.3 Test Chat

1. Di halaman chat OpenWebUI
2. Pilih model yang baru ditambah
3. Kirim pesan test: "Summarize: Database error after migration"
4. Tunggu response dari provider Anda

✅ Jika response muncul, OpenWebUI integration berhasil!

---

## 🆘 TROUBLESHOOTING - ANTISIPASI ERROR

### ❌ ERROR 1: "OPENROUTER_API_KEY belum diatur!"

**Penyebab:**

- File `.env` tidak ditemukan
- Variable `OPENROUTER_API_KEY` tidak diset
- Typo nama variable

**Solusi:**

1. Verifikasi file `.env` ada:

```bash
ls -la .env
```

2. Pastikan format correct:

```bash
grep "OPENROUTER_API_KEY" .env
```

3. Reload settings:

```bash
# Restart server
# (CTRL+C kemudian jalankan ulang)
python main.py
```

---

### ❌ ERROR 2: "OPENROUTER_API_KEY tidak valid" (401 Unauthorized)

**Penyebab:**

- API Key salah/tidak valid
- API Key expired
- API Key diberi typo

**Solusi:**

1. Verifikasi API Key di OpenRouter dashboard:
   - Login: https://openrouter.ai/
   - Cek di Settings → API Keys

2. Re-generate key jika diperlukan:
   - Delete key yang lama
   - Create key baru
   - Copy ke `.env` dengan benar

3. Test API Key secara manual:

```bash
curl -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer sk-or-v1-YOUR_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/llama-3-8b-instruct:free",
    "messages": [{"role": "user", "content": "hello"}],
    "max_tokens": 10
  }'
```

---

### ❌ ERROR 3: "Connection timeout" / "Failed to connect to OpenRouter API"

**Penyebab:**

- Internet connection bermasalah
- OpenRouter server down
- Firewall memblokir koneksi

**Solusi:**

1. Test koneksi internet:

```bash
ping openrouter.ai
curl -I https://openrouter.ai/
```

2. Cek firewall/proxy:

```bash
# Test koneksi dengan timeout yang lebih lama
curl --max-time 30 https://openrouter.ai/api/v1/models
```

3. Gunakan fallback provider (mock) sementara:

```bash
# Edit .env
PRIMARY_PROVIDER=mock
```

4. Restart server dan test ulang

---

### ❌ ERROR 4: "PRIMARY_PROVIDER 'openrouter' tidak valid/didukung!"

**Penyebab:**

- Typo nama provider (misalnya: `openroute`, `open-router`)
- Provider tidak terdaftar di registry

**Solusi:**

1. Verifikasi nama provider di `services/ai/registry.py`:

```bash
grep "PROVIDER_REGISTRY" services/ai/registry.py
```

2. Provider yang valid:

```
mock
local_ollama
openai
google_gemini
openrouter  ← Pastikan ini
```

3. Perbaiki `.env`:

```bash
# ❌ SALAH
PRIMARY_PROVIDER=open-router
PRIMARY_PROVIDER=openroute

# ✅ BENAR
PRIMARY_PROVIDER=openrouter
```

---

### ❌ ERROR 5: "Application startup failed" / "ModuleNotFoundError"

**Penyebab:**

- Dependencies tidak terinstall
- Virtual environment tidak aktif
- Python version tidak compatible

**Solusi:**

1. Aktivasi virtual environment:

```bash
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Verifikasi imports:

```bash
python -c "import fastapi, requests, pydantic; print('✅ All dependencies installed')"
```

---

### ❌ ERROR 6: "Swagger UI tidak bisa diakses" (http://127.0.0.1:8000/docs blank)

**Penyebab:**

- Server tidak running
- Port sudah terpakai
- Firewall memblokir

**Solusi:**

1. Verifikasi server running:

```bash
curl -I http://127.0.0.1:8000/docs
```

2. Ganti port jika port 8000 sudah terpakai:

```bash
# Edit .env
APP_PORT=8001

# Atau run dengan port berbeda:
python -c "import uvicorn; uvicorn.run('main:app', port=8001, reload=True)"
```

3. Restart server:

```bash
python main.py
```

---

### ❌ ERROR 7: Rate Limit / "429 Too Many Requests"

**Penyebab:**

- Terlalu banyak request ke OpenRouter dalam waktu singkat
- API quota habis

**Solusi:**

1. Tunggu beberapa menit sebelum test ulang
2. Cek quota OpenRouter:
   - Login: https://openrouter.ai/
   - Settings → Billing / Usage

3. Gunakan model gratis (jika masih ada):

```bash
OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct:free
```

4. Cek rate limit limit info:

```bash
# Response header akan menunjukkan:
# RateLimit-Limit-Requests: 100
# RateLimit-Remaining-Requests: 99
```

---

### ❌ ERROR 8: "FALLBACK_PROVIDER validation error"

**Penyebab:**

- Fallback provider tidak valid
- Fallback provider kehilangan kredensial

**Solusi:**

1. Jika tidak perlu fallback, disable:

```bash
ENABLE_FALLBACK=false
```

2. Atau set fallback ke mock (selalu ada):

```bash
FALLBACK_PROVIDER=mock
```

3. Pastikan nama fallback provider valid:

```bash
# Valid options:
FALLBACK_PROVIDER=mock
FALLBACK_PROVIDER=local_ollama
```

---

### ❌ ERROR 9: "Empty Response" / "Response content is empty"

**Penyebab:**

- Model tidak merespons dengan benar
- Prompt terlalu kompleks untuk model
- Token limit terlampaui

**Solusi:**

1. Test dengan prompt yang lebih sederhana:

```json
{
  "text": "Server error"
}
```

2. Cek model support di OpenRouter:
   - List model: https://openrouter.ai/docs#models
   - Verify model masih tersedia

3. Ganti ke model yang lebih powerful (jika perlu):

```bash
# Free tier:
OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct:free

# Atau paid:
OPENROUTER_MODEL=gpt-4o-mini
```

---

### ❌ ERROR 10: ".env file tidak ditemukan" saat import settings

**Penyebab:**

- Working directory tidak tepat
- Path .env tidak absolute

**Solusi:**

1. Jalankan server dari root project:

```bash
# ✅ BENAR
cd /home/shobixlinuxdev/CIVIL_GROUP/Projects/API_CIVIL_GROUP
python main.py

# ❌ SALAH
cd /home/shobixlinuxdev/
python CIVIL_GROUP/Projects/API_CIVIL_GROUP/main.py
```

2. Verifikasi working directory:

```bash
python -c "import os; print('Current dir:', os.getcwd())"
```

3. Gunakan absolute path jika diperlukan:

```bash
# Edit core/config.py
BASE_DIR = "/home/shobixlinuxdev/CIVIL_GROUP/Projects/API_CIVIL_GROUP"
```

---

## 🔧 QUICK REFERENCE

### Checklist Setup Cepat

```
[ ] 1. API Key dari https://openrouter.ai/ didapat
[ ] 2. File .env dibuat dan dikonfigurasi dengan benar
[ ] 3. OPENROUTER_API_KEY diisi dengan value yang correct
[ ] 4. PRIMARY_PROVIDER=openrouter di .env
[ ] 5. pip install -r requirements.txt sudah dijalankan
[ ] 6. Virtual environment sudah aktif
[ ] 7. Server berjalan (python main.py)
[ ] 8. Swagger UI accessible (http://127.0.0.1:8000/docs)
[ ] 9. Test endpoint di Swagger berhasil
[ ] 10. OpenWebUI connection configured (optional)
```

### Command Shortcuts

```bash
# Start server
python main.py

# Test OpenRouter API connection
python -c "from services.ai.providers import OpenRouterProvider; p = OpenRouterProvider(); print(p.generate('hello'))"

# Validate config
python -c "from core import settings; print(f'Provider: {settings.PRIMARY_PROVIDER}')"

# Check .env loaded
grep "OPENROUTER_API_KEY" .env | head -c 50

# Restart server dengan reload
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Kill server di background
pkill -f "uvicorn main:app"
```

### Environment Variables Summary

| Variable             | Required | Default       | Example                               |
| -------------------- | -------- | ------------- | ------------------------------------- |
| `PRIMARY_PROVIDER`   | ✅       | -             | `openrouter`                          |
| `OPENROUTER_API_KEY` | ✅       | -             | `sk-or-v1-...`                        |
| `OPENROUTER_MODEL`   | ✅       | -             | `meta-llama/llama-3-8b-instruct:free` |
| `FALLBACK_PROVIDER`  | ❌       | `mock`        | `mock`                                |
| `ENABLE_FALLBACK`    | ❌       | `true`        | `true`                                |
| `APP_ENV`            | ❌       | `development` | `development`                         |
| `APP_HOST`           | ❌       | `127.0.0.1`   | `127.0.0.1`                           |
| `APP_PORT`           | ❌       | `8000`        | `8000`                                |

### Recommended Free Models (OpenRouter)

```
meta-llama/llama-3-8b-instruct:free
→ Cepat, gratis, cocok untuk testing

meta-llama/llama-3-70b-instruct:free
→ Lebih powerful, tapi lebih lambat

mixtral-8x7b-instruct:free
→ Alternative gratis dengan kualitas baik
```

### Paid Models (Lebih baik, tapi ada cost)

```
gpt-4o-mini          → OpenAI (recommended)
google/gemini-2.0-flash-exp  → Google
mistralai/mistral-large      → Mistral
```

---

## 📞 Bantuan Lebih Lanjut

Jika masalah belum terselesaikan:

1. **Cek dokumentasi OpenRouter**: https://openrouter.ai/docs
2. **Cek project docs**: Lihat folder `DOCS/GUIDE_PROJECT/`
3. **Debug logs**: Enable debug mode di `.env`:
   ```bash
   APP_ENV=debug
   ```
4. **Test manual dengan curl**:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/issue/summary \
     -H "Content-Type: application/json" \
     -d '{"text": "Database error"}'
   ```

---

**Dibuat**: 2026-05-30
**Status**: ✅ Tested & Ready to Use
**Last Updated**: 2026-05-30

---

## 🎯 Kesimpulan

Setelah mengikuti panduan ini, Anda seharusnya:

✅ Memahami cara setup OpenRouter provider
✅ Bisa test endpoint di Swagger
✅ Bisa integrate dengan OpenWebUI
✅ Tahu cara troubleshoot error umum
✅ Punya fallback provider (mock) untuk testing offline

**Happy Testing! 🚀**
