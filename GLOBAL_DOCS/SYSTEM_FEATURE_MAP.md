# 🗂️ SYSTEM_FEATURE_MAP.md
> **Peta Fitur, Indeks Kode & Batasan Teknis Sistem**
>
> Dokumen ini memetakan fitur-fitur operasional sistem ke berkas implementasi aslinya, serta mendokumentasikan batasan teknis saat ini dan rencana pengembangan skala besar (roadmap).

---

## 🗺️ 1. Peta Fitur & Pemetaan Berkas (Feature-to-Code Mapping)

Berikut adalah katalog endpoint API aktif yang dapat dikonsumsi oleh client saat ini:

| Nama Fitur / Endpoint | Jenis Request | Tujuan & Alur Bisnis | Berkas Utama yang Terlibat | Tingkat Risiko |
| :--- | :--- | :--- | :--- | :--- |
| **Welcome / Health Check** | `GET /` | Memverifikasi status online server backend, menampilkan daftar endpoint aktif, dan tautan dokumentasi OpenAPI. | [main.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/main.py) | **🟢 Rendah** |
| **Issue Summarization** | `POST /api/issue-summary` | Menerima teks keluhan sistem panjang, memprosesnya melalui AI, dan mengembalikan ringkasan satu kalimat. | [api/routes.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/api/routes.py)<br>[workflows/issue_summary.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/workflows/issue_summary.py)<br>[services/ai_service.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/services/ai_service.py) | **🟡 Sedang** |
| **Audit Logs / Work History** | `GET /api/history` | Mengambil dan menampilkan seluruh daftar riwayat keluhan beserta ringkasan AI yang telah sukses tersimpan di database lokal. | [api/routes.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/api/routes.py)<br>[storage/local_storage.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/storage/local_storage.py) | **🟢 Rendah** |

---

## 📁 2. Indeks Berkas Pendukung (Supporting Files Index)

Di luar kode utama, berikut adalah indeks berkas konfigurasi penting sistem:

* **[prompts/loader.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/prompts/loader.py)**: Mengatur pembacaan teks file instruksi prompt LLM secara non-blocking.
* **`prompts/issue_summary.txt`**: Teks template prompt LLM yang berisi instruksi tegas agar AI meringkas keluhan menjadi satu kalimat bahasa Inggris yang padat tanpa basa-basi.
* **[storage/history.json](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/storage/history.json)**: Berkas database log JSON lokal yang mencatat `id`, `timestamp`, `original_text`, dan `summary` untuk setiap keluhan yang diproses.

---

## 🛠️ 3. Batasan Sistem Saat Ini (Current Technical Limitations)

Untuk membantu perencanaan arsitektur di masa depan, berikut adalah analisis keterbatasan teknis backend saat ini:

| Keterbatasan Sistem | Dampak Negatif | Risiko | Rekomendasi Solusi |
| :--- | :--- | :--- | :--- |
| **Database File JSON** <br>(`storage/history.json`) | Kinerja pembacaan/penulisan akan melambat drastis saat ukuran log mencapai ribuan catatan. | **Kuning (Sedang)** | Migrasi ke database relasional seperti **PostgreSQL** atau database dokumen seperti **MongoDB**. |
| **Local File I/O Synchronous** | Potensi terjadinya *race condition* (data tabrakan/tertimpa) saat banyak client memproses keluhan secara bersamaan. | **Merah (Tinggi)** | Gunakan library file asinkron (seperti `aiofiles`) atau gunakan database transaksional ACID. |
| **Single Active AI Service** | Sangat bergantung pada local Ollama (`qwen2.5:1.5b`). Jika engine mati atau overload, server mengembalikan error 500. | **Kuning (Sedang)** | Implementasi mekanisme fallback otomatis (seperti beralih ke **Google Gemini API** atau **OpenAI API** jika local Ollama mati). |
| **No Character Validation** | Mengirim keluhan dengan ukuran karakter yang luar biasa panjang dapat membebani local model dan menyebabkan timeout server. | **Kuning (Sedang)** | Pasang validasi panjang karakter input maksimal (misal: 4000 karakter) di skema Pydantic. |

---

## 🚀 4. Roadmap & Rencana Skalabilitas (Scaling Roadmap)

Jika API Backend ini ingin dideploy ke server produksi untuk melayani ribuan request harian secara stabil, lakukan langkah-langkah peningkatan arsitektur berikut:

```mermaid
graph LR
    Step1[1. Validasi Input & Fallback LLM] --> Step2[2. Asynchronous File / PostgreSQL]
    Step2 --> Step3[3. caching & Rate Limiting Redis]
```

1. **Tahap 1 (Stability & Resiliency)**:
   - Pasang validasi `max_length` pada field `text` di skema `IssueRequest` di [api/routes.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/api/routes.py).
   - Buat helper fallback di [services/ai_service.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/services/ai_service.py) yang secara otomatis mengalihkan beban kerja ke Google Gemini API jika server local Ollama gagal dihubungi.
2. **Tahap 2 (Data Integrity)**:
   - Ganti mock `storage/local_storage.py` dengan adaptor database nyata. Gunakan SQLAlchemy atau Tortoise-ORM untuk berkomunikasi secara asinkron dengan database PostgreSQL.
3. **Tahap 3 (Performance Optimization)**:
   - Integrasikan Redis untuk melakukan caching ringkasan keluhan (jika teks keluhan identik dikirim berulang kali) untuk menghemat sumber daya komputasi AI.
   - Gunakan Redis juga untuk membatasi jumlah request harian per IP/Client (Rate-Limiter).
