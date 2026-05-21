# 🎯 API_RETENTION_RULES.md
> **Panduan Developer Experience (DX) & Retensi Integrasi API Platform**
>
> Dokumen ini mendefinisikan prinsip-prinsip untuk menjaga retensi pengembang (developer retention) dengan meminimalkan gesekan integrasi (*integration friction*), mendeteksi sinyal kelelahan pengembang (*developer fatigue*), dan menjamin penyampaian nilai (*value delivery*) secara instan.

---

## 🏗️ 1. Prinsip Utama Retensi API (DX Retention Principles)

Pada API Platform, "User" adalah **Developer** atau **Sistem Pihak Ketiga** yang mengintegrasikan layanan Anda. Retensi mereka sepenuhnya ditentukan oleh kualitas **Developer Experience (DX)**:

### ⚡ A. Low Friction First (Integrasi Kilat)
* **Target**: Pengembang baru harus bisa melakukan panggilan API pertama menggunakan `curl` dan mendapatkan hasil sukses dalam waktu kurang dari **10 detik**.
* **Cara Mencapai**:
  - Dokumentasi interaktif Swagger `/docs` harus selalu up-to-date dan menyertakan contoh data riil.
  - Skema data input/output harus sederhana, menggunakan tipe data standar, dan divalidasi ketat oleh Pydantic.
  - Bebas dari setup environment yang rumit atau autentikasi multi-step yang tidak perlu di masa awal integrasi.

### 🎁 B. Instant Value Reward (Hasil Cepat & Akurat)
* Setiap request yang berhasil dikirimkan harus langsung mengembalikan data yang memiliki kegunaan bisnis tinggi (misal: ringkasan keluhan sistem satu kalimat yang sangat akurat dari AI).
* Hindari proses asinkronus yang memaksa developer membuat sistem polling kompleks jika pengerjaan aslinya bisa diselesaikan dalam rentang waktu sinkronus yang wajar.

### 🧠 C. Eliminasi Beban Kognitif (Cognitive Load Minimization)
* Jangan memaksa developer memikirkan struktur data yang rumit. 
* Jaga agar payload JSON input seminimal mungkin (seperti skema `IssueRequest` yang hanya membutuhkan satu field wajib `text`).
* Gunakan penamaan field yang intuitif dan baku.

---

## 🚨 2. Sinyal Kelelahan Integrasi (Developer Fatigue Signals)

Developer tidak tiba-tiba berhenti menggunakan API Anda; mereka perlahan merasa frustrasi karena akumulasi gesekan teknis kecil sebelum akhirnya memutuskan melakukan *silent churn* (pindah ke API kompetitor).

Berikut adalah indikator utama kelelahan integrasi yang wajib dipantau dalam log sistem:

### 1. Tingginya Rasio HTTP 422 (Unprocessable Entity)
* **Arti Sinyal**: Pengembang terus-menerus mengirimkan format data yang salah.
* **Akar Masalah**: Dokumentasi skema Pydantic tidak jelas, deskripsi field membingungkan, atau tidak ada contoh skema (*examples*) yang representatif di Swagger UI.

### 2. Lonjakan Latency & Timeout API
* **Arti Sinyal**: Panggilan API memakan waktu terlalu lama atau terputus tengah jalan akibat timeout.
* **Akar Masalah**: Antrean pada local AI model (Ollama Qwen) yang macet atau tidak adanya batasan ukuran karakter input pada API router.

### 3. Kebocoran Error 500 (Unhandled Exceptions)
* **Arti Sinyal**: Server mengembalikan status code 500 dengan traceback mentah bahasa pemrograman (Python traceback).
* **Akar Masalah**: Panggilan ke database JSON lokal crash atau integrasi API AI mati tanpa dibungkus *error handler* yang aman di tingkat API routing.

### 4. Silent Integration Churn
* **Arti Sinyal**: Penurunan tajam frekuensi panggilan API harian dari client yang sebelumnya aktif tanpa adanya laporan error. Hal ini menandakan developer menyerah karena integrasi terasa tidak andal atau lambat.

---

## 🛡️ 3. Prinsip Pemulihan & Ketahanan API (API Recovery & Resiliency)

Untuk mengembalikan momentum pengembang yang mulai frustrasi akibat kendala integrasi, sistem wajib menerapkan prinsip-prinsip pemulihan ini secara otomatis:

### 🟢 A. Informative Error Shaping
Jangan biarkan developer menebak mengapa request mereka ditolak. Setiap error HTTP 4xx wajib menjelaskan secara spesifik:
* Field mana yang menyebabkan kesalahan.
* Apa aturan batasan yang dilanggar (misal: "Teks issue tidak boleh kosong").
* Bagaimana cara memperbaikinya.

### 🟢 B. LLM Failover Resiliency
Jika server kecerdasan buatan lokal (Ollama Qwen) mengalami kegagalan koneksi atau beban kerja berlebih (timeout):
* Sistem harus dapat secara otomatis mengalihkan panggilan ke model fallback eksternal (seperti Google Gemini API).
* Proses peralihan ini wajib terisolasi di dalam [services/ai_service.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/services/ai_service.py) tanpa disadari oleh client integrator dan tanpa mengubah format output response API.

### 🟢 C. Graceful Timeout Management
* Selalu tetapkan batas waktu (*timeout*) maksimal 30 detik pada panggilan layanan pihak ketiga.
* Jika batas terlampaui, segera kembalikan respon HTTP 504 (Gateway Timeout) yang terformat rapi, daripada membiarkan koneksi menggantung tanpa batas waktu yang berisiko memacetkan server utama.
