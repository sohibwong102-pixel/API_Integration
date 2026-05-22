# FEATURE_MAP.md - Peta Fitur Kerja Cepat AI

Daftar fitur yang tersedia beserta file terkait dan tingkat risikonya.

| Fitur | Deskripsi | File Terkait | Entry Point | Risiko |
| :--- | :--- | :--- | :--- | :--- |
| **Onboarding** | Sambutan awal & pendaftaran user baru. | `handlers/start.py`, `utils/helpers.py` | `/start` | Rendah |
| **AI Rewrite** | Menulis ulang teks agar lebih segar. | `handlers/tools.py`, `services/ai_service.py` | `tool_rewrite` | Sedang |
| **Customer Reply** | Membalas pesan pelanggan secara otomatis. | `handlers/tools.py`, `services/ai_service.py` | `tool_customer_reply` | Sedang |
| **Caption Gen** | Membuat caption media sosial + hashtag. | `handlers/tools.py`, `services/ai_service.py` | `tool_caption` | Sedang |
| **Translate** | Terjemahan antar bahasa (EN <-> ID). | `handlers/tools.py`, `services/ai_service.py` | `tool_translate` | Sedang |
| **Summarize** | Merangkum teks panjang menjadi poin. | `handlers/tools.py`, `services/ai_service.py` | `tool_summarize` | Sedang |
| **Email Writer** | Draft email bisnis profesional. | `handlers/tools.py`, `services/ai_service.py` | `tool_email_writer` | Sedang |
| **Premium Sub** | Upgrade akun ke akses tanpa batas. | `handlers/premium.py`, `services/payment_service.py` | `btn_premium` | **Tinggi** |
| **Work History** | Melihat 10 hasil pengerjaan terakhir. | `handlers/history.py`, `utils/helpers.py` | `btn_history` | Rendah |
| **User Status** | Cek limit harian dan tipe plan. | `handlers/status.py`, `utils/helpers.py` | `btn_status` | Rendah |
| **Analytics** | Tracking event penggunaan untuk admin. | `services/service_analytics.py` | Internal calls | Sedang |

## 🛠️ Detail Fitur Utama: AI Tools
Setiap tool mendukung 6 gaya penulisan:
1. **Formal**: Bahasa baku & resmi.
2. **Friendly**: Santai & bersahabat (Kak/Sobat).
3. **Selling**: Persuasif & Call to Action.
4. **Singkat**: Padat & To-the-point.
5. **Profesional**: Kompeten & Dunia Kerja.
6. **Rapihin Text**: Hanya memperbaiki typo & format.

## 🚀 Alur Premium (Risk Point)
- User pilih Paket -> Pilih Metode (OVO/DANA/QRIS) -> Dapatkan Instruksi -> Kirim Bukti ke Admin.
- *Catatan*: Aktivasi akun premium masih dilakukan secara manual oleh Admin setelah verifikasi bukti transfer (semi-otomatis).
