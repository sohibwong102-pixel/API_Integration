# SAFE_TO_EDIT.md - Panduan Keamanan Modifikasi

Dokumen ini membantu AI Agent dan Developer memahami area mana yang aman untuk dimodifikasi atau di-refactor, serta area mana yang sangat berisiko.

## 🟢 Low Risk (Aman untuk Modifikasi)
Area ini fokus pada tampilan dan informasi statis. Kesalahan di sini biasanya hanya menyebabkan typo atau UI yang kurang optimal.

- **`keyboards/`**: Sangat aman untuk eksperimen tata letak tombol (layout) atau mengubah label tombol.
- **`handlers/start.py`**: Aman untuk mengubah teks sambutan (onboarding).
- **`handlers/status.py`** & **`handlers/history.py`**: Aman untuk mengubah cara bot menampilkan informasi profil atau riwayat.
- **`utils/cleanup.py`**: Aman untuk di-refactor selama logika penghapusan pesan tetap bekerja.

## 🟡 Medium Risk (Perlu Hati-hati)
Area ini mengandung logika bisnis atau alur interaksi yang saling bergantung.

- **`services/ai_service.py`**: Aman untuk tweaking prompt, namun berisiko jika mengubah struktur output yang diharapkan oleh handler.
- **`handlers/tools.py`**: Berisiko tinggi karena menggunakan FSM. Perubahan kecil pada alur state dapat memutus seluruh fitur AI.
- **`config.py`**: Aman untuk menambah variabel baru, namun fatal jika mengubah nama variabel yang sudah ada.

## 🔴 High Risk (Sangat Berbahaya)
Area ini adalah pondasi sistem. Kesalahan di sini dapat menyebabkan data loss atau kegagalan transaksi.

- **`utils/helpers.py`**: Jantung dari manajemen data. Perubahan logika baca/tulis JSON di sini sangat berisiko merusak database `user_data.json`.
- **`services/payment_service.py`**: Mengelola instruksi pembayaran. Kesalahan di sini berakibat pada kerugian finansial atau ketidakpercayaan user.
- **`main.py`**: Mengatur inisialisasi bot. Perubahan pada konfigurasi router dapat menyebabkan bot tidak merespon pesan tertentu.

## 🧪 Zona Eksperimen UI
Jika Anda ingin mencoba gaya desain baru:
1. Modifikasi file di folder `keyboards/`.
2. Ubah pesan HTML di dalam `handlers/*.py`.
3. Gunakan emoji secara minimalis sesuai dengan [UX_PHILOSOPHY.md](file:///home/shobixlinuxdev/DEV_GLOBAL/Projects/TelegramBot/z_Docs/UX_PHILOSOPHY.md).

## ⚠️ Zona Refactor Berbahaya
- **Refactor FSM**: Jangan lakukan refactor pada `handlers/tools.py` kecuali Anda memahami setiap transisi state di `states/tool_states.py`.
- **Refactor JSON Handler**: Jangan mengubah cara `utils/helpers.py` bekerja kecuali Anda telah melakukan backup pada `user_data.json`.
