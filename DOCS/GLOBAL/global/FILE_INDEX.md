# FILE_INDEX.md - Indeks File Proyek (Enhanced)

Daftar file penting dengan informasi risiko, dependensi, dan panduan untuk AI Agent.

## 🎨 UX / User Interface (Keyboards)
- **`keyboards/main_menu.py`**
  - **Tujuan**: Menu utama bot.
  - **Risiko**: Rendah.
  - **AI Notes**: Aman diubah untuk menambah navigasi baru.
- **`keyboards/tools_menu.py`**
  - **Tujuan**: Daftar 6 fitur AI.
  - **Risiko**: Rendah.
  - **AI Notes**: Gunakan label yang scannable.
- **`keyboards/styles_menu.py`**
  - **Tujuan**: Opsi gaya bahasa.
  - **Risiko**: Sedang (Dependensi pada callback tools).
  - **AI Notes**: Perubahan callback data di sini harus sinkron dengan `handlers/tools.py`.

## 🎮 Handlers (Controllers)
- **`handlers/start.py`**
  - **Tujuan**: Onboarding & Command `/start`.
  - **Risiko**: Rendah.
  - **AI Notes**: Tempat terbaik untuk eksperimen teks sambutan.
- **`handlers/tools.py`**
  - **Tujuan**: Alur inti FSM Fitur AI.
  - **Risiko**: **Sangat Tinggi**.
  - **Dependensi**: `ai_service.py`, `states/tool_states.py`.
  - **AI Notes**: Hindari mengubah alur callback/state tanpa testing menyeluruh. Sangat sensitif terhadap breakage.
- **`handlers/premium.py`**
  - **Tujuan**: Alur pembelian premium.
  - **Risiko**: Tinggi.
  - **Dependensi**: `payment_service.py`.
  - **AI Notes**: Pastikan instruksi pembayaran tidak berubah secara tidak sengaja.

## 🧠 Core Services (Business Logic)
- **`services/ai_service.py`**
  - **Tujuan**: Integrasi Gemini AI.
  - **Risiko**: Sedang.
  - **AI Notes**: Modifikasi prompt di sini mempengaruhi kualitas seluruh fitur.
- **`services/payment_service.py`**
  - **Tujuan**: Logika instruksi pembayaran.
  - **Risiko**: **Sangat Tinggi**.
  - **AI Notes**: Berisi data rekening/QRIS. DILARANG keras mengubah data tanpa instruksi spesifik.

## 🛠️ Utilities & Storage
- **`utils/helpers.py`**
  - **Tujuan**: CRUD Data JSON.
  - **Risiko**: **Sangat Tinggi**.
  - **AI Notes**: Semua akses ke database harus melalui file ini. Jangan buat fungsi baca file sendiri di handler.
- **`utils/cleanup.py`**
  - **Tujuan**: UX Polish (Hapus pesan).
  - **Risiko**: Rendah.
  - **AI Notes**: Selalu gunakan fungsi di sini untuk menghapus pesan perintah/loading.

## ⚙️ Konfigurasi & Entry
- **`main.py`**: Inisialisasi Bot & Router. (Risiko: Tinggi)
- **`config.py`**: Load ENV. (Risiko: Sedang)
- **`.env`**: API Keys (Rahasia). (Risiko: Kritis)
