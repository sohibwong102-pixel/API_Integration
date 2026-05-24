# 📜 DEVELOPMENT_PLAYBOOK.md
> **Panduan Keamanan Modifikasi & Aturan Kerja AI Coding Agent**
>
> Dokumen ini berisi aturan keamanan pengembangan, peta risiko berkas, dan instruksi wajib bagi AI Coding Agent dan Developer untuk menjaga stabilitas sistem.

---

## 🚦 1. Matriks Keamanan Berkas (Codebase Safety Matrix)

Sebelum melakukan modifikasi atau refactoring, periksa tingkat risiko berkas target Anda di bawah ini:

| Zona Risiko | Lokasi Berkas | Dampak Jika Rusak | Panduan Modifikasi |
| :--- | :--- | :--- | :--- |
| **🔴 CRITICAL** <br>(Dilarang Keras) | `storage/local_storage.py`<br>`storage/history.json` | Data loss total, korupsi data log riwayat, kegagalan operasional audit bisnis. | **HANYA** boleh diedit melalui instruksi eksplisit tertulis dari User. Wajib backup berkas `.json` sebelum mengedit kode logikanya. |
| **🟡 CAUTION** <br>(Perlu Kehati-hatian Tinggi) | `workflows/issue/*.py`<br>`api/routes.py`<br>`services/ai_service.py`<br>`main.py` | Kegagalan routing API, rusaknya orkestrasi bisnis, atau hilangnya integrasi model LLM. | Lakukan pengujian endpoint lokal setelah modifikasi. Pastikan schema Pydantic sinkron dengan format response. |
| **🟢 OPEN** <br>(Zona Eksperimen Aman) | `prompts/issue/*.txt`<br>`prompts/loader.py` | Kualitas output AI berubah atau loading template terganggu. | Aman untuk tuning prompt dan penambahan template baru selama kontrak output tetap dijaga. |

---

## 🚫 2. Larangan Mutlak (Absolute Prohibitions)

Untuk menghindari kerusakan pada integritas arsitektur backend, aturan-aturan ini bersifat **mutlak**:

1. **DILARANG BERINTERAKSI DENGAN STORAGE SECARA LANGSUNG**: Seluruh modul selain `storage/local_storage.py` dilarang keras membuka, membaca, atau menulis file JSON secara langsung menggunakan pustaka bawaan `json` atau `open()`.
2. **DILARANG MELEWATI VALIDASI PYDANTIC**: Setiap input request dan output response HTTP wajib tervalidasi menggunakan Pydantic BaseModel di dalam layer Routing API. Jangan pernah menggunakan data bertipe data mentah `dict` longgar di dalam parameter endpoint router.
3. **DILARANG MERUSAK KONTRAK INTERFACE**: Modifikasi pada `services/ai_service.py` dan subsystem `services/ai/` wajib menjaga kontrak interface provider/facade yang sudah ada.

---

## 🤖 3. Aturan Perilaku AI Coding Agent (Agent Behavior Rules)

Jika Anda adalah AI Coding Agent (seperti Antigravity) yang bertugas memodifikasi codebase ini, Anda **wajib** mematuhi aturan berikut:

### 🧩 A. Pola Komparasi Sebelum Modifikasi
Sebelum mengubah kode, lakukan analisis rantai dependensi untuk melihat dampak perubahan terhadap komponen API, Workflow, dan Storage:
- Analisa apakah perubahan tipe data di Router akan merusak Pydantic Schema.
- Pastikan perubahan parameter pada method Workflow diperbarui secara sinkron pada entry point di Router API.

### 📝 B. Disiplin Komentar & Kebersihan Kode
- **Preserve Comments**: Pertahankan komentar penjelas yang sudah ada, terutama penjelasan edukatif bagi pemula di awal berkas.
- **Action-Oriented Comments**: Jika menambahkan fungsi baru, gunakan komentar bahasa Indonesia yang bersih dan menjelaskan *kenapa* kode ditulis, bukan hanya *apa* yang dilakukan oleh kode tersebut.
- **No Spam**: Jangan tinggalkan sisa-sisa debug print atau komentar mati di dalam berkas produksi.

### ⚙️ C. Penanganan Error yang Tangguh (Robustness)
- Semua panggilan HTTP keluar ke provider AI wajib dibungkus dalam blok `try-except`.
- Jika panggilan API AI gagal, lemparkan exception yang bermakna atau gunakan fallback aman agar server backend tidak mati total (*crash*).

---

## 🧼 4. Panduan Naming & Kebersihan UI Swagger
Untuk menjaga konsistensi visual pada Swagger UI di `/docs`:
- **Naming Conventions**: Gunakan bahasa Inggris untuk nama kelas, fungsi, dan variabel (contoh: `get_ai_service`, `IssueResponse`).
- **Swagger Documentation**: Setiap endpoint di `api/routes.py` wajib dilengkapi parameter deskriptif seperti `summary`, `description`, `response_model`, dan skema input harus menyertakan anotasi `Field` lengkap dengan `examples`.
