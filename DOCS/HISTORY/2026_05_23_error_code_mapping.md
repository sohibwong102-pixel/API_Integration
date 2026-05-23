# 📝 RIWAYAT IMPLEMENTASI: ERROR CODE MAPPING IMPROVEMENT

## 📅 Tanggal: 23 Mei 2026

## 🛠️ Status: SELESAI

## 🎯 Ringkasan singkat:

Menambahkan pemetaan semantic error yang lebih akurat untuk beberapa HTTP status code umum dan memperbaiki fallback agar `INTERNAL_SERVER_ERROR` hanya digunakan untuk unknown 5xx.

---

## 🔍 Perubahan yang dilakukan

- Menambah mapping eksplisit pada `core/error_handlers.py`:
  - `405` -> `METHOD_NOT_ALLOWED`
  - `408` -> `REQUEST_TIMEOUT`
  - `429` -> `RATE_LIMITED`
  - `503` -> `SERVICE_UNAVAILABLE`
- Mengubah fallback:
  - Jika kode 5xx tidak dikenali => `INTERNAL_SERVER_ERROR` (hanya untuk true unknown 5xx)
  - Jika kode lain tidak dikenali => gunakan label generik `HTTP_<code>` untuk predictable semantic
- Menambahkan komentar di file kode agar mudah dicari dan dipahami.

---

## 📁 Berkas terpengaruh

- `core/error_handlers.py` — update mapping dan komentar.

---

## ✅ Catatan pengujian singkat

- Memastikan handler mengembalikan response JSON dengan struktur:
  ```json
  {
    "success": false,
    "error": { "code": "<ERROR_CODE>", "message": "..." }
  }
  ```
- Uji manual disarankan: kirim response HTTP simulasi dengan status 405, 408, 429, 503, unknown 502, dan unknown 418 untuk verifikasi kode yang dikembalikan.

---

## 🧭 Alasan & Implikasi

- Membuat semantic error lebih akurat memudahkan client dan monitoring membedakan klasifikasi error (rate limit vs service unavailable vs method error).
- Fallback yang lebih spesifik membantu menghindari kebingungan ketika server mengembalikan 5xx yang sebenarnya bukan "unknown".

---

## ✍️ Implementor

- BACKEND_EXECUTOR (otomatis)

---

## 🔁 Update tambahan: 23 Mei 2026 (ValueError doc/comment)

- Menambahkan docstring dan komentar pada `core/error_handlers.py` yang menjelaskan
  bahwa handler `ValueError` hanya diperuntukkan untuk simple application errors.
- Menambahkan rekomendasi future untuk mengganti `ValueError` generik dengan
  custom exception (`AppError`/`BusinessValidationError`) agar mencegah misuse
  dan membuat handling error lebih eksplisit.

Catatan: perubahan ini bersifat dokumentasi inline dan tidak mengubah perilaku runtime.

---

## 🔁 Update tambahan: 23 Mei 2026 (5xx Structured Internal Logging)

- Menjaga response client untuk semua 5xx tetap tersanitasi:
  - `"message": "Internal server error"`
- Menambahkan structured internal logging untuk error 5xx di `core/error_handlers.py`:
  - Event: `http_exception_5xx` untuk `StarletteHTTPException` status 5xx
  - Event: `unexpected_exception_5xx` untuk exception tak terduga
- Menambahkan helper context `_build_error_context(request)` agar log berisi konteks penting:
  - `method`, `path`, `query`, `client_host`, `request_id`
- Menjaga detail exception asli tetap ada di log internal:
  - `exception_type`
  - `exception_detail` (untuk HTTPException 5xx)
  - `exception_message` + traceback (untuk exception tak terduga via `logger.exception`)

Catatan: perubahan ini meningkatkan kualitas root-cause debugging tanpa membuka detail internal ke client API.

---

## 🔁 Update tambahan: 23 Mei 2026 (Static Fallback Error Code Contract)

- Menetapkan strategi final: **Option A - static fallback enum**.
- Menghapus fallback dynamic `HTTP_<status_code>` dari `core/error_handlers.py`.
- Menetapkan fallback contract stabil:
  - unknown `5xx` -> `INTERNAL_SERVER_ERROR`
  - unknown `4xx` -> `CLIENT_ERROR`
  - status non-4xx/5xx yang tidak terpetakan -> `INTERNAL_SERVER_ERROR`
- Mendokumentasikan behavior contract `error.code` di `README.md` agar API consumer memiliki referensi enum yang predictable dan stabil.

Alasan:
- Mencegah consumer bergantung pada enum dinamis yang berubah sesuai status code.
- Menjaga kompatibilitas contract lintas rilis.

---

## 🔁 Update tambahan: 23 Mei 2026 (Evidence Test Handler Contract)

- Menjalankan pembuktian behavior handler untuk skenario:
  - `405`
  - `429`
  - `503`
  - `validation error (422)`
  - `internal server error (500)`
- Menyimpan artefak evidence pada folder:
  - `DOCS/TEST_EVIDENCE/2026_05_23_handler_proof/`
- Artefak yang disimpan:
  - `*_curl_command.txt` (curl command ekuivalen)
  - `*_headers.txt` (status + headers)
  - `*_body.json` (sample response)
  - `summary.json` (ringkasan hasil)
  - `PROOF.md` (rekap readable)
  - `curl_result_terminal_capture.txt` (snapshot gaya terminal)

Hasil ringkas:
- `405` -> `METHOD_NOT_ALLOWED`
- `429` -> `RATE_LIMITED`
- `503` -> `SERVICE_UNAVAILABLE` dengan message tersanitasi (`Internal server error`)
- `422` -> `VALIDATION_ERROR`
- `500` -> `INTERNAL_SERVER_ERROR` dengan message tersanitasi (`Internal server error`)

---

## 🔁 Update tambahan: 23 Mei 2026 (Standardisasi Struktur TEST_EVIDENCE)

- Merapikan struktur evidence menjadi kategori:
  - `DOCS/TEST_EVIDENCE/CURL_TEST/`
- Menambahkan history test bulanan berbasis format `tahun_bulan`:
  - `DOCS/TEST_EVIDENCE/CURL_TEST/2026_05.md`
- Semua hasil test berbeda pada tanggal yang sama digabung rapi dalam file yang sama, dengan:
  - jarak antar blok
  - batas pemisah (`-----` dan `=====`) 
  - jam berbeda per case
- Memindahkan evidence mentah lama ke:
  - `DOCS/TEST_EVIDENCE/CURL_TEST/RAW/2026_05_23_handler_proof/`

---

## 🔁 Update tambahan: 23 Mei 2026 (Kategori Test Per Skenario)

- Menambahkan kategori evidence per jenis test dengan format yang sama seperti `CURL_TEST`:
  - `DOCS/TEST_EVIDENCE/405_TEST/`
  - `DOCS/TEST_EVIDENCE/429_TEST/`
  - `DOCS/TEST_EVIDENCE/503_TEST/`
  - `DOCS/TEST_EVIDENCE/VALIDATION_ERROR_TEST/`
  - `DOCS/TEST_EVIDENCE/500_TEST/`
- Masing-masing kategori memiliki:
  - history bulanan: `2026_05.md`
  - folder arsip raw: `RAW/2026_05_23_handler_proof/`
- Format history disamakan:
  - ada tanggal
  - ada jam
  - ada pemisah blok
  - ada command, headers, dan body response.

---

## 🔁 Update tambahan: 23 Mei 2026 (Cleanup Struktur Evidence Lama)

- Menghapus folder lama `DOCS/TEST_EVIDENCE/CURL_TEST/` karena seluruh bukti sudah dipisah per kategori test.
- Struktur akhir dibuat ringkas agar tidak duplikasi dan tidak membentuk folder yang tidak perlu.
