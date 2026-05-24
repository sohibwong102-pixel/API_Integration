# SAFE_TO_EDIT.md

Dokumen ini membantu developer memahami area mana yang relatif aman dimodifikasi dan area mana yang perlu kehati-hatian tinggi.

## Low Risk

- **`prompts/issue/*.txt`**: Aman untuk tuning instruksi AI selama kontrak output tetap dijaga.
- **`DOCS/HISTORY/`**: Aman untuk menambah catatan perubahan setelah implementasi selesai.
- **`DOCS/TEST_EVIDENCE/`**: Aman untuk menambah evidence validasi.

## Medium Risk

- **`workflows/issue/*.py`**: Aman diubah jika tetap menjaga kontrak input/output tiap workflow.
- **`services/ai/providers/*.py`**: Aman untuk perbaikan provider spesifik, tetapi wajib menjaga interface yang sama.
- **`core/config.py`**: Aman untuk menambah config baru, tetapi berisiko bila mengubah nama env existing.

## High Risk

- **`api/routes.py`**: Memegang public contract. Perubahan kecil bisa berdampak langsung ke client.
- **`main.py`**: Menyangkut startup, middleware, dan router registration.
- **`core/error_handlers.py`**: Mengatur seluruh bentuk response error publik.
- **`storage/local_storage.py`**: Menyangkut integritas data riwayat.

## Panduan Aman

1. Mulai dari perubahan paling kecil yang menyelesaikan masalah.
2. Jika menyentuh layer `api/`, cek dampaknya ke workflow dan documentation contract.
3. Jika menyentuh storage atau error handler, lakukan validasi lebih ketat.
4. Hindari mengubah banyak layer sekaligus tanpa alasan yang jelas.
