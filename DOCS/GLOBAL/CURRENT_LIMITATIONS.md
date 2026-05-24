# CURRENT_LIMITATIONS.md

Dokumen ini mencatat keterbatasan teknis backend saat ini untuk membantu prioritas pengembangan berikutnya.

## Data & Storage

| Batasan | Dampak | Risiko | Rekomendasi |
| :--- | :--- | :--- | :--- |
| **JSON File Storage** | `storage/history.json` tidak ideal untuk skala besar atau konkurensi tinggi. | Tinggi | Migrasi ke database transaksional saat kebutuhan scale naik. |
| **Local File I/O** | Potensi race condition saat banyak request menulis history bersamaan. | Tinggi | Tambahkan locking strategy atau ganti ke database nyata. |

## AI & Provider Routing

| Batasan | Dampak | Risiko | Rekomendasi |
| :--- | :--- | :--- | :--- |
| **Provider Dependency Runtime** | Provider aktif bisa gagal jika API key atau local engine tidak siap. | Sedang | Pertahankan startup validation dan fallback policy yang jelas. |
| **Quality Variance** | Output antar provider dapat berbeda walau prompt sama. | Sedang | Perkuat normalisasi output di workflow dan tambah coverage test. |

## API & Contract

| Batasan | Dampak | Risiko | Rekomendasi |
| :--- | :--- | :--- | :--- |
| **Legacy Compatibility Surface** | Endpoint legacy perlu dipertahankan agar client lama tidak putus mendadak. | Sedang | Dokumentasikan lifecycle endpoint dan rencana deprecation. |
| **Input Length Limit** | Input dibatasi `max_length=4000`, request lebih panjang ditolak. | Rendah | Pertahankan limit atau tambahkan preprocessing chunking jika use case berubah. |

## Maintainability

- **Documentation Drift**: Sebagian dokumen lama sempat membawa narasi Telegram bot, padahal repo sekarang adalah backend FastAPI workflow-first.
- **History File Growth**: Riwayat lokal akan terus membesar jika tidak ada strategi rotasi atau archival.
- **Workflow Expansion Risk**: Semakin banyak fitur issue-classification, semakin penting menjaga pemisahan tanggung jawab antar workflow.
