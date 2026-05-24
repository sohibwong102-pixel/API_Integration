# FILE_INDEX.md

Daftar file penting dengan konteks fungsi, risiko, dan catatan singkat untuk pengembang.

## API Layer

- **`main.py`**
  - **Tujuan**: Entry point FastAPI, middleware, router registration, dan startup validation.
  - **Risiko**: Tinggi.

- **`api/routes.py`**
  - **Tujuan**: Endpoint issue summary, categorize, severity, tags, sentiment, dan history.
  - **Risiko**: Tinggi.
  - **AI Notes**: Jangan campurkan business logic berat ke sini.

- **`api/openwebui_routes.py`**
  - **Tujuan**: Adapter sederhana untuk format request chat compatibility.
  - **Risiko**: Sedang.

## Core Layer

- **`core/config.py`**
  - **Tujuan**: Pemuatan env, whitelist provider, dan startup validation.
  - **Risiko**: Tinggi.

- **`core/error_handlers.py`**
  - **Tujuan**: Centralized exception handling dan stable error contract.
  - **Risiko**: Tinggi.

## Workflow Layer

- **`workflows/issue/summary.py`**
  - **Tujuan**: Menjalankan issue summarization flow dan menyimpan history.
  - **Risiko**: Sedang.

- **`workflows/issue/categorize.py`**
  - **Tujuan**: Klasifikasi kategori issue.
  - **Risiko**: Sedang.

- **`workflows/issue/severity.py`**
  - **Tujuan**: Normalisasi tingkat severity issue.
  - **Risiko**: Sedang.

- **`workflows/issue/tags.py`**
  - **Tujuan**: Ekstraksi tag issue.
  - **Risiko**: Sedang.

- **`workflows/issue/sentiment.py`**
  - **Tujuan**: Klasifikasi sentimen issue.
  - **Risiko**: Sedang.

## Prompt Layer

- **`prompts/loader.py`**
  - **Tujuan**: Memuat dan memformat template prompt.
  - **Risiko**: Rendah.

- **`prompts/issue/*.txt`**
  - **Tujuan**: Template prompt per fitur issue.
  - **Risiko**: Rendah sampai Sedang tergantung kontrak output.

## Service Layer

- **`services/ai_service.py`**
  - **Tujuan**: Backward compatibility gateway ke subsystem AI modular.
  - **Risiko**: Sedang.

- **`services/ai/router.py`**
  - **Tujuan**: Menentukan provider aktif dan fallback path.
  - **Risiko**: Tinggi.

- **`services/ai/providers/*.py`**
  - **Tujuan**: Adapter tiap provider AI.
  - **Risiko**: Sedang.

## Storage Layer

- **`storage/local_storage.py`**
  - **Tujuan**: Adapter resmi baca/tulis history JSON.
  - **Risiko**: Tinggi.

- **`storage/history.json`**
  - **Tujuan**: Penyimpanan history lokal.
  - **Risiko**: Tinggi.
