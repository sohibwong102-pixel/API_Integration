# DO_NOT_TOUCH.md - File Sensitif & Berisiko Tinggi

Daftar file yang tidak boleh dimodifikasi secara sembarangan karena dapat merusak stabilitas sistem atau integritas data.

## 🔴 Critical: Business Logic & Data
1. **`services/payment_service.py`**
   - **Alasan**: Berisi instruksi pembayaran dan credential merchant. 
   - **Risiko**: Salah modifikasi bisa menyebabkan user gagal bayar atau uang masuk ke akun yang salah.
   
2. **`utils/helpers.py`**
   - **Alasan**: Menangani baca/tulis ke `user_data.json` secara sinkron/asinkron.
   - **Risiko**: Kesalahan logika di sini bisa menyebabkan korupsi data seluruh pengguna bot.

3. **`data/user_data.json`**
   - **Alasan**: Database utama user.
   - **Risiko**: Penghapusan atau pengeditan manual yang tidak sesuai skema JSON akan menyebabkan bot crash total saat startup.

## 🟡 High Risk: Architecture & Flow
1. **`main.py`**
   - **Alasan**: Konfigurasi startup dan registrasi router.
   - **Risiko**: Perubahan urutan router atau konfigurasi polling dapat menyebabkan bot gagal menerima pesan atau error *TelegramConflictError*.

2. **`services/ai_service.py`**
   - **Alasan**: Berisi system prompt yang telah dioptimasi untuk Gemini.
   - **Risiko**: Perubahan pada prompt bisa merusak kualitas output AI atau membuat AI menjadi terlalu bertele-tele (melanggar filosofi "Kerja Cepat").

3. **`handlers/tools.py`**
   - **Alasan**: Mengelola FSM State yang kompleks.
   - **Risiko**: Kesalahan transisi state akan membuat user terjebak di satu menu dan tidak bisa menggunakan fitur lain.

## 💡 Panduan Modifikasi
- Selalu lakukan **Backup** `user_data.json` sebelum melakukan refactor pada `utils/helpers.py`.
- Jika ingin mengubah prompt AI, lakukan testing secara terpisah sebelum di-commit ke `ai_service.py`.
