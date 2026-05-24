# 📝 RIWAYAT IMPLEMENTASI: ISSUE AI ECOSYSTEM MODULARIZATION

## 📅 Tanggal: 24 Mei 2026

## 🛠️ Status: SELESAI

## 🎯 Ringkasan singkat

Membangun reusable Issue AI ecosystem berbasis capability-isolated workflow dengan prompt terpisah per tugas (`summary`, `categorize`, `severity`, `tags`, `sentiment`) agar arsitektur tetap modular, scalable, dan contract-predictable.

---

## 🔍 Perubahan yang dilakukan

### 1) Workflow modular per capability
Menambahkan paket baru `workflows/issue/`:
- `summary.py`
- `categorize.py`
- `severity.py`
- `tags.py`
- `sentiment.py`

Setiap workflow:
- hanya orchestration
- memuat prompt dari file txt terpisah
- memanggil AI via centralized flow existing (`get_ai_service().generate_summary(...)`)
- menjaga parsing output simple dan deterministic

Khusus `summary`:
- tetap menyimpan history lewat `LocalStorage.save_record(...)`
- tetap memakai request_id lifecycle dari API boundary

### 2) Prompt management terstruktur
Menambahkan prompt baru di `prompts/issue/`:
- `summary.txt`
- `categorize.txt`
- `severity.txt`
- `tags.txt`
- `sentiment.txt`

Semua prompt dibuat:
- concise
- deterministic
- no markdown
- no JSON
- single responsibility

### 3) API contract alignment per endpoint
Refactor `api/routes.py` menjadi contract-driven endpoint:
- `POST /api/issue/summary` -> `{ "summary": "..." }`
- `POST /api/issue/categorize` -> `{ "category": "..." }`
- `POST /api/issue/severity` -> `{ "severity": "..." }`
- `POST /api/issue/tags` -> `{ "tags": ["..."] }`
- `POST /api/issue/sentiment` -> `{ "sentiment": "..." }`

Backward compatibility:
- tetap menyediakan alias lama `POST /api/issue-summary` dengan contract summary yang sama.

### 4) Cleanup artefak lama
- Menghapus `workflows/issue_summary.py` (digantikan oleh `workflows/issue/summary.py`).
- Menghapus `prompts/issue_summary.txt` (digantikan oleh `prompts/issue/summary.txt`).

---

## 📁 Berkas terpengaruh

- `api/routes.py`
- `workflows/__init__.py`
- `workflows/issue/__init__.py`
- `workflows/issue/summary.py`
- `workflows/issue/categorize.py`
- `workflows/issue/severity.py`
- `workflows/issue/tags.py`
- `workflows/issue/sentiment.py`
- `prompts/issue/summary.txt`
- `prompts/issue/categorize.txt`
- `prompts/issue/severity.txt`
- `prompts/issue/tags.txt`
- `prompts/issue/sentiment.txt`
- (deleted) `workflows/issue_summary.py`
- (deleted) `prompts/issue_summary.txt`

---

## ✅ Validasi singkat

- `python3 -m py_compile` sukses untuk seluruh file workflow/router baru.
- Uji helper normalizer (via `.venv/bin/python`) menunjukkan output deterministic untuk category, severity, tags, dan sentiment.

---

## 🔁 Update tambahan: 24 Mei 2026 (Legacy Compatibility Restore)

- Memulihkan backward compatibility endpoint legacy `POST /api/issue-summary`.
- Response contract legacy dikembalikan menjadi:
  - `{ "summary": "...", "request_id": "..." }`
- Endpoint modern `POST /api/issue/summary` tetap clean/simple:
  - `{ "summary": "..." }`
- Implementasi menggunakan lightweight compatibility adapter di router:
  - shared helper `_execute_issue_summary(...)`
  - tanpa duplicate workflow/orchestration path
  - request_id tetap dari lifecycle existing (generated di API boundary)

---

## 🔁 Update tambahan: 24 Mei 2026 (Deterministic Fallback Normalization)

- Menstabilkan fallback normalization pada workflow:
  - `workflows/issue/categorize.py`
  - `workflows/issue/severity.py`
  - `workflows/issue/sentiment.py`
  - (validasi konsistensi juga dilakukan untuk `workflows/issue/tags.py`)

Perubahan inti:
- Menghapus traversal classification berbasis `set` (unordered) pada fallback path.
- Mengganti dengan urutan eksplisit deterministic (`tuple`) untuk scan sequence.
- Menambahkan boundary-aware matching berbasis regex agar mengurangi partial collision.
- Menambahkan deterministic keyword priority map pada categorize untuk overlap-safe matching (contoh: `auth` diprioritaskan ke `authentication` sebelum token generik `api`).

Hasil validasi:
- Uji lintas proses dengan `PYTHONHASHSEED` berbeda menghasilkan output yang sama untuk input yang sama.
- Fallback result kini runtime-independent dan lebih mudah di-debug.

---

## 🔁 Update tambahan: 24 Mei 2026 (Request ID Observability Lifecycle Stabilization)

- Menstabilkan ownership `request_id` di boundary layer melalui middleware terpusat (`main.py`):
  - menerima `x-request-id` dari client jika tersedia
  - generate baru jika tidak ada
  - menyimpan ke `request.state.request_id` untuk propagasi antar layer
  - mengekspose konsisten ke response header `X-Request-ID`

- Menambahkan structured request access log ringan (centralized, non-duplicated):
  - event: `request_completed`
  - field: `request_id`, `method`, `path`, `status_code`, `duration_ms`

- Menyatukan propagasi request_id di route layer:
  - seluruh endpoint issue mengambil `request_id` dari context (`request.state.request_id`)
  - menghapus pola generate ulang `uuid` per endpoint
  - menjaga lifecycle continuity untuk tracing/correlation

- Menyesuaikan error context agar membaca `request_id` dari state terlebih dahulu:
  - fallback ke header jika state tidak tersedia
  - memastikan korelasi log error tetap konsisten dengan request lifecycle

---

## ✍️ Implementor

- BACKEND_EXECUTOR (otomatis)
