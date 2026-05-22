# CURRENT_LIMITATIONS.md - Batasan Sistem Saat Ini

Dokumen ini mencatat keterbatasan teknis dan produk untuk membantu perencanaan pengembangan di masa depan.

## 📁 Data & Storage
| Batasan | Dampak | Risiko | Rekomendasi |
| :--- | :--- | :--- | :--- |
| **JSON Database** | `user_data.json` akan melambat saat jumlah user mencapai ribuan. | Sedang | Migrasi ke PostgreSQL atau MongoDB. |
| **Local File I/O** | Potensi *race condition* saat banyak user menulis data secara bersamaan. | Tinggi | Gunakan sistem antrian atau database transaksional. |
| **Max History (10)** | User tidak bisa melihat riwayat kerja yang sudah lama. | Rendah | Implementasi fitur "Archive" atau pencarian histori. |

## 🚀 Fitur & Operasional
| Batasan | Dampak | Risiko | Rekomendasi |
| :--- | :--- | :--- | :--- |
| **Manual Payment** | Admin harus mengecek bukti transfer secara manual sebelum aktivasi Premium. | Tinggi | Integrasi Payment Gateway (Midtrans/Xendit) untuk aktivasi otomatis. |
| **Single AI Model** | Hanya bergantung pada `gemini-1.5-flash`. Jika API down, bot mati total. | Sedang | Implementasi fallback ke OpenAI atau Anthropic. |
| **Daily Limit Reset** | Reset limit harian mungkin tidak presisi jika bot mati saat pergantian hari. | Rendah | Gunakan *cron job* eksternal atau Redis untuk manajemen limit. |

## 🎨 UX & Interface
| Batasan | Dampak | Risiko | Rekomendasi |
| :--- | :--- | :--- | :--- |
| **No Input Validation** | Teks yang sangat panjang (>4000 karakter) dapat menyebabkan error pada Telegram/AI. | Sedang | Tambahkan validasi panjang karakter pada input user. |
| **Limited Feedback** | Tidak ada fitur bagi user untuk memberi rating pada hasil AI. | Rendah | Tambahkan tombol Like/Dislike pada hasil output. |

## 🛠️ Pemeliharaan (Maintainability)
- **Monolithic Handlers**: `handlers/tools.py` mulai membengkak. Perlu dipecah menjadi sub-modul berdasarkan kategori alat jika fitur ditambah lagi.
- **Minimal Logging**: Logging saat ini hanya di konsol. Sulit melakukan debugging jika terjadi error pada user spesifik di masa lalu.
