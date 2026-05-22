# PROJECT_ARCHITECTURE.md - Arsitektur Proyek Kerja Cepat AI

Dokumen ini menjelaskan struktur tingkat tinggi dan pola arsitektur yang digunakan dalam proyek **Kerja Cepat AI**.

## 🚀 Tech Stack
- **Language**: Python 3.10+
- **Framework**: `aiogram` 3.x (Asynchronous Telegram Bot API)
- **AI Engine**: Google Gemini AI (Model: `gemini-1.5-flash`)
- **Database**: 
  - `user_data.json`: Penyimpanan profil & histori pengguna (ringan).
  - `analytics.db`: SQLite untuk pencatatan event/analitik.
- **State Management**: Aiogram FSM (Finite State Machine).

## 📁 Struktur Folder & Tanggung Jawab

| Folder | Tanggung Jawab |
| :--- | :--- |
| `handlers/` | **Controller Layer**. Menangani perintah, pesan, dan callback dari Telegram. |
| `services/` | **Service/Logic Layer**. Berisi logika bisnis (AI, Pembayaran, Analitik). |
| `keyboards/` | **View Layer**. Definisi tombol-tombol (inline/reply keyboards) untuk UI Telegram. |
| `states/` | Definisi state FSM untuk alur input pengguna yang kompleks. |
| `utils/` | Fungsi pembantu (helper), manajemen file JSON, dan fungsi pembersihan (cleanup). |
| `data/` | Tempat penyimpanan database lokal dan aset data. |

## 🔄 Alur Kerja Utama (Core Flow)

1. **User Interaction**: User menekan tombol atau mengirim pesan.
2. **Handler Processing**: Router di `handlers/` menangkap event berdasarkan filter (`Command`, `F.data`, `State`).
3. **Business Logic**: Handler memanggil fungsi di `services/` (misalnya `ai_service.py` untuk generate teks).
4. **Data Persistence**: Status user diperbarui melalui `utils/helpers.py`.
5. **UI Response**: Bot mengirimkan pesan baru atau memperbarui pesan lama menggunakan keyboard dari `keyboards/`.

## 🛠️ Aturan Engineering Penting

1. **Clean UI**: Gunakan `utils/cleanup.py` untuk menghapus pesan perintah/loading agar chat history tetap rapi.
2. **Asynchronous**: Semua operasi I/O (API call, File read/write) harus bersifat non-blocking (async/await).
3. **FSM Usage**: Selalu gunakan FSM saat membutuhkan input teks dari user untuk menghindari tabrakan input antar fitur.
4. **Error Handling**: Setiap call ke API eksternal (Gemini) wajib dibungkus dalam blok `try-except`.
