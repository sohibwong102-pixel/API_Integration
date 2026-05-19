# 📝 RIWAYAT IMPLEMENTASI: REFAKTORISASI ARSITEKTUR BACKEND (CONFIG & SERVICE ROUTER)

## 📅 Tanggal: 18 Mei 2026
## 🛠️ Status: SELESAI (SUKSES)
## 🎯 Pembahasan: Konsolidasi Lapisan Konfigurasi Terpusat & Router AI Multi-Provider

---

## 🔍 1. Ringkasan Perubahan Global
Pada hari ini, dilakukan refaktorisasi arsitektur berskala besar pada sistem konfigurasi (`core/`) dan layanan kecerdasan buatan (`services/`). Seluruh pembaruan ini bertujuan untuk mengeliminasi utang teknis (*structural debt*), meningkatkan kekokohan (*reliability*) melalui mekanisme *failover/fallback* otomatis, serta memastikan aplikasi gagal secara instan (*fail-fast*) saat startup jika konfigurasi tidak valid.

Seluruh refaktorisasi ini terbagi ke dalam lima (5) sub-pembahasan utama yang saling terintegrasi:
1. **Centralized Configuration Layer**: Mengonsolidasikan semua pembacaan `os.getenv()` ke dalam satu modul terpusat.
2. **Modular Multi-Provider AI Router**: Memecah layanan AI monolitik menjadi modul berbasis adapter (*config-driven*) dengan kemampuan *auto-failover*.
3. **Runtime-Based Instance Configuration**: Mengubah struktur konfigurasi statis menjadi berbasis instansiasi dinamis (*runtime instance*) demi isolasi testing dan fleksibilitas pemuatan ulang.
4. **Strict Provider Validation**: Menerapkan pencocokan pengenal penyedia AI dengan *whitelist* terdaftar untuk mencegah *typo* konfigurasi.
5. **Unified Core Package Interface**: Menyediakan batas masuk (*boundary*) paket `core` yang bersih dengan re-ekspor simbol terpadu via `core/__init__.py`.

---

## 📂 2. Peta Struktur Direktori Baru
Berikut adalah struktur folder hasil refaktorisasi terpadu:

```text
├── core/
│   ├── __init__.py          # Unified Core Interface (re-ekspor settings & BASE_DIR)
│   └── config.py            # Pengurus pemuatan .env manual & representasi Settings dinamis
├── services/
│   ├── ai/
│   │   ├── __init__.py      # Expose facade, router, & registry
│   │   ├── base.py          # Kontrak interface BaseAIService & BaseProvider
│   │   ├── facade.py        # Gateway terpadu (facade) steril untuk workflow
│   │   ├── models.py        # Normalisasi struktur output (AIResponse)
│   │   ├── registry.py      # Registri pemetaan string nama ke kelas adapter provider
│   │   ├── router.py        # Orkestrator utama perutean & fallback LLM
│   │   └── providers/       # Seluruh adapter API eksternal
│   │       ├── __init__.py
│   │       ├── mock_provider.py
│   │       ├── ollama_provider.py
│   │       ├── openai_provider.py
│   │       ├── gemini_provider.py
│   │       └── openrouter_provider.py
│   └── ai_service.py        # Gateway kompatibilitas mundur (backward-compatibility wrapper)
```

---

## 🛠️ 3. Rincian Modul & Berkas Terpengaruh

### A. Lapisan Konfigurasi & Inisialisasi (`core/`)
1. **`core/config.py`**:
   - **Tipe Dinamis**: Seluruh variabel konfigurasi diubah dari variabel statis tingkat kelas (*class-level*) menjadi variabel instansi (*instance-level*) di dalam `__init__(self)`. Pemuatan `.env` dipicu saat pembuatan objek.
   - **Whitelist Terpusat**: Ditetapkan daftar resmi `SUPPORTED_PROVIDERS = ["mock", "local_ollama", "openai", "google_gemini", "openrouter"]`.
   - **Validasi Fail-Fast**: 
     - Memastikan `PRIMARY_PROVIDER` dan `FALLBACK_PROVIDER` berada di dalam whitelist.
     - Memastikan API key wajib untuk provider cloud aktif (seperti `google_gemini`, `openai`, `openrouter`) terisi dengan benar di file `.env`.
   - **Kompatibilitas**: Mengekspos objek instansi tunggal `settings = Settings()` di baris paling bawah berkas.
2. **`core/__init__.py`**:
   - Menerapkan *Unified Package Interface* dengan mere-ekspor `settings` dan `BASE_DIR` secara eksplisit menggunakan properti `__all__`.

### B. Lapisan Layanan Kecerdasan Buatan (`services/`)
1. **`services/ai/base.py` & `models.py`**:
   - Mengisolasi kontrak integrasi dengan kelas abstrak `BaseAIService` dan `BaseProvider`.
   - Menghasilkan format respon terstandarisasi `AIResponse` yang seragam terlepas dari provider apa pun yang memprosesnya.
2. **`services/ai/router.py`**:
   - Menjalankan logika orkestrasi perutean utama. Memanggil provider utama (`PRIMARY_PROVIDER`), mendeteksi adanya kegagalan jaringan atau kegagalan API, lalu otomatis mengalihkan panggilan LLM ke penyedia cadangan (`FALLBACK_PROVIDER`) jika opsi `ENABLE_FALLBACK` bernilai `True`.
3. **`services/ai/facade.py`**:
   - Kelas `AIFacade` bertindak sebagai *gatekeeper* tunggal untuk dikonsumsi oleh lapisan *workflow* (`workflows/issue_summary.py`) sehingga alur logika bisnis tetap steril dari detail internal routing.
4. **`services/ai_service.py`**:
   - Ditulis ulang menjadi modul ringkas pembungkus (*compatibility gateway*) yang mengarahkan method lama `get_ai_service()` ke `AIFacade()` demi menjamin 100% kompatibilitas mundur dengan sistem lama.

### C. Lapisan Konsumen Lainnya
1. **`main.py`**:
   - Mengimpor `settings` langsung dari paket `core` dan memicu `settings.validate()` di fase terawal modul startup untuk menggagalkan jalannya server jika ada kesalahan konfigurasi kritis.
   - Membaca properti inisialisasi Uvicorn (`host`, `port`, `reload`) secara dinamis dari `settings`.
2. **`storage/local_storage.py`**:
   - Mengubah model import menjadi `from core import settings, BASE_DIR`.
   - Membaca absolute path database lokal dari properti `settings.DB_STORAGE_PATH` secara dinamis.

---

## 🧪 4. Skenario & Hasil Pengujian Integrasi

Seluruh skenario pengujian di bawah ini dijalankan langsung via terminal untuk memastikan tidak ada kesalahan integrasi.

### Skenario A: Kegagalan Instan Typo Nama Provider (Strict Validation)
*Sistem menolak startup saat nama provider utama diatur dengan nilai typo.*
- **Perintah**:
  ```bash
  PRIMARY_PROVIDER=invalid_ollama_typo .venv/bin/python3 -c "import main"
  ```
- **Hasil**:
  ```text
  ValueError: GAGAL STARTUP: PRIMARY_PROVIDER 'invalid_ollama_typo' tidak valid/didukung!
  Pilihan yang tersedia: ['mock', 'local_ollama', 'openai', 'google_gemini', 'openrouter']
  ```

### Skenario B: Kegagalan Instan Kehilangan API Key (Fail-Fast Cloud Validation)
*Sistem menggagalkan inisialisasi ketika API key cloud provider aktif kosong.*
- **Perintah**:
  ```bash
  PRIMARY_PROVIDER=google_gemini GEMINI_API_KEY= .venv/bin/python3 -c "import main"
  ```
- **Hasil**:
  ```text
  ValueError: GAGAL STARTUP: 'GEMINI_API_KEY' wajib diatur di file .env jika menggunakan google_gemini!
  ```

### Skenario C: Failover Otomatis (Ollama Offline -> Mock Fallback)
*Sistem otomatis mengalihkan tugas summary ketika provider utama (Ollama) offline.*
- **Perintah**:
  ```bash
  PRIMARY_PROVIDER=local_ollama FALLBACK_PROVIDER=mock ENABLE_FALLBACK=True .venv/bin/python3 -c "from services import get_ai_service; svc = get_ai_service(); print('RESULT:', svc.generate_summary('Test Issue Text: database error\n\nSummary:'))"
  ```
- **Hasil**:
  ```text
  [WARNING] local_ollama provider failed: Connection refused. Attempting failover to mock...
  RESULT: Database connection timeout preventing successful service startup.
  ```

### Skenario D: Inisialisasi dan Pemrosesan Normal (Sukses)
*Sistem berjalan normal menggunakan provider Mock yang valid.*
- **Perintah**:
  ```bash
  PRIMARY_PROVIDER=mock .venv/bin/python3 -c "from services import get_ai_service; svc = get_ai_service(); print('RESULT:', svc.generate_summary('Test Issue Text: auth middleware failed\n\nSummary:'))"
  ```
- **Hasil**:
  ```text
  RESULT: Deployment issue related to auth middleware conflict.
  ```

---

## 🚀 5. Keuntungan Arsitektur Terpadu
1. **Kebersihan Kode (No Scattered os.getenv)**: Pembacaan variabel lingkungan terisolasi 100% di dalam `core/config.py`.
2. **Kekokohan Sistem (Resiliency)**: Auto-failover menjaga sistem backend selalu aktif secara mandiri jika penyedia LLM utama mengalami gangguan (*downtime*).
3. **Isolasi Unit Testing**: Instansi konfigurasi dinamis mempermudah pembuatan *test suite* independen dengan *mocking configuration* yang aman tanpa efek samping statis.
4. **Batas Impor Bersih (Unified Boundary)**: Pengembang lain hanya perlu melakukan impor satu pintu `from core import settings, BASE_DIR`, mengabstraksikan struktur direktori internal `core/`.
5. **Kemudahan Skalabilitas**: Penambahan provider baru di masa mendatang cukup dengan membuat adapter di `providers/` dan meregistrasikannya di `registry.py` tanpa mengganggu alur routing maupun kode API luar.
