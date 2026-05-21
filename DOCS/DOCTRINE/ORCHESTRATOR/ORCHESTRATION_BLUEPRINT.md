# 📜 ORCHESTRATION_BLUEPRINT.md
> **Panduan Orkestrasi AI & Pembagian Peran Pengembang - `summary_endpoint`**
>
> Dokumen ini mendefinisikan cakupan operasional, tanggung jawab spesifik, dan aturan perutean tugas (*task routing*) bagi seluruh AI Agent dalam ekosistem pengembangan **Operational Workflow API Backend**.

---

## 🏛️ 1. Doktrin Pembagian Peran (Role Separation)

Untuk mencegah kekacauan koordinasi (*role drift*) dan menjaga kebersihan arsitektur, sistem ini mematuhi prinsip **Satu Agent, Satu Domain Keahlian Utama**.

Jika sebuah agent mendeteksi tugas di luar domain keahliannya, ia wajib melakukan eskalasi ke **MANAGER_ORCHESTRATOR** untuk dirutekan ulang ke spesialis yang tepat.

---

## 👥 2. Matriks Tanggung Jawab Agent (Unified Agent Matrix)

Proyek backend ini didukung oleh **6 peran spesialis** yang bekerja dalam harmoni:

### 1. MANAGER_ORCHESTRATOR
* **Tanggung Jawab**: Pengawas alur kerja global dan pengambil keputusan strategis.
* **Fokus Utama**: Membagi task kompleks menjadi sub-task, mengarahkan sub-task ke agent spesialis, memvalidasi hasil akhir, dan mengelola eskalasi ke USER.
* **🚫 Batasan**: DILARANG menulis kode teknis secara langsung atau melakukan tuning prompt mendalam.

### 2. TASK_AGENT_OPTIMIZER
* **Tanggung Jawab**: Penjaga efisiensi eksekusi workflow AI.
* **Fokus Utama**: Menganalisis kegagalan alur kerja agent, merapikan instruksi kerja (*sistem prompt* pengembang), dan mengotomatisasi tugas-tugas operasional yang berulang.
* **🚫 Batasan**: DILARANG mendesain arsitektur database atau mengubah logika bisnis backend.

### 3. ARCHITECTURE_GUARDIAN
* **Tanggung Jawab**: Penjaga integritas struktur dan standar kualitas sistem.
* **Fokus Utama**: Meninjau perubahan struktur folder, memastikan kepatuhan terhadap [DEVELOPMENT_PLAYBOOK.md](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/DOCS/GLOBAL_DOCS/DEVELOPMENT_PLAYBOOK.md), memvalidasi keamanan dependensi, serta menjaga keterpeliharaan kode jangka panjang.
* **🚫 Batasan**: DILARANG merancang logika bisnis internal workflow atau memformat teks prompt.

### 4. BACKEND_SPECIALIST (The Thinker)
* **Tanggung Jawab**: Otak perancang algoritma dan logika bisnis backend.
* **Fokus Utama**: Merancang alur kerja ([workflows/](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/workflows/)), merancang skema validasi Pydantic ([api/routes.py](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/api/routes.py)), mendesain skema penyimpanan JSON/database ([storage/](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/summary_endpoint/storage/)), dan melakukan Root Cause Analysis (RCA) saat terjadi bug logika.
* **🚫 Batasan**: DILARANG menulis kode implementasi massal (boilerplate), menulis unit test teknis, atau mengonfigurasi uvicorn.

### 5. BACKEND_EXECUTOR (The Executor)
* **Tanggung Jawab**: Tangan pelaksana teknis implementasi backend.
* **Fokus Utama**: Menulis kode rute API berdasarkan rancangan Specialist, mengimplementasikan method database, menulis unit test, memperbaiki bug teknis (syntax, type-error, missing imports), dan mengelola variabel lingkungan (`.env`).
* **🚫 Batasan**: DILARANG mengambil keputusan strategis logika bisnis atau mengubah arsitektur global tanpa persetujuan Specialist.

### 6. PROMPT_SPECIALIST
* **Tanggung Jawab**: Arsitek komunikasi LLM dan optimalisasi token.
* **Fokus Utama**: Merancang berkas prompt (`prompts/*.txt`), melakukan penyusutan token (kompresi prompt), menyelaraskan persona AI, serta menyusun parameter inferensi (seperti temperature dan top_p).
* **🚫 Batasan**: DILARANG memanipulasi routing FastAPI atau berinteraksi langsung dengan database storage.

---

## 🔀 3. Doktrin Perutean Backend: Thinker vs. Executor

Orchestrator wajib menerapkan pemisahan yang tegas antara fase **"Berpikir"** dan **"Melakukan"** pada setiap tugas pengembangan:

```
[Permintaan Fitur API Baru]
           │
           ▼
┌──────────────────────┐      Rekomendasi Skema
│  BACKEND_SPECIALIST  │ ───────────────────────────┐
│     (The Thinker)    │                            ▼
└──────────────────────┘                 ┌────────────────────┐
                                         │  BACKEND_EXECUTOR  │ ──► [Kode Siap]
                                         │   (The Executor)   │
                                         └────────────────────┘
```

---

## 📊 4. Aturan Matriks Perutean Tugas (Task Routing Rules)

| Kondisi / Jenis Tugas | Agent Utama | Agent Pendukung |
| :--- | :--- | :--- |
| **Pembuatan Fitur/Workflow Baru** | BACKEND_SPECIALIST | BACKEND_EXECUTOR |
| **Penyusunan Skema Validasi (Pydantic)** | BACKEND_SPECIALIST | BACKEND_EXECUTOR |
| **Bug Logika (Salah Output/Aliran Bisnis)** | BACKEND_SPECIALIST | BACKEND_EXECUTOR |
| **Bug Teknis (Crash, Type Error, Missing Import)** | BACKEND_EXECUTOR | - |
| **Optimalisasi Kinerja Jaringan/Timeout** | BACKEND_EXECUTOR | ARCHITECTURE_GUARDIAN |
| **Perubahan Template Prompt (`.txt`)** | PROMPT_SPECIALIST | - |
| **Audit Struktur File & Standardisasi Kode** | ARCHITECTURE_GUARDIAN | TASK_AGENT_OPTIMIZER |

---

## 🛡️ 5. Prinsip Pencegahan Tumpang Tindih (Overlap Prevention)

1. **Context Hand-off Policy**: Perpindahan tugas antar agent wajib menyertakan konteks rancangan secara lengkap (desain logis dari Specialist harus disertakan saat diserahkan ke Executor).
2. **Single Ownership Rule**: Satu berkas kode tidak boleh dimodifikasi oleh dua agent berbeda secara bersamaan dalam satu iterasi pengerjaan.
3. **No Double-Thinking**: Executor dilarang mengubah keputusan arsitektur atau logika bisnis rancangan Specialist di tengah pengerjaan tanpa konfirmasi ulang.
