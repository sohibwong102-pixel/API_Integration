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
