# DO_NOT_TOUCH.md

Daftar area sensitif yang tidak boleh dimodifikasi sembarangan karena berisiko merusak stabilitas backend atau kontrak publiknya.

## Critical

1. **`core/error_handlers.py`**
   - **Alasan**: Sumber utama kontrak error response publik.
   - **Risiko**: Perubahan sembarangan dapat merusak stabilitas `error.code` untuk consumer.

2. **`storage/local_storage.py`**
   - **Alasan**: Satu-satunya adapter resmi untuk history JSON lokal.
   - **Risiko**: Kesalahan logika dapat menyebabkan data history korup atau hilang.

3. **`storage/history.json`**
   - **Alasan**: Berkas persistensi lokal aktif.
   - **Risiko**: Edit manual yang tidak valid dapat membuat pembacaan history gagal.

## High Risk

1. **`main.py`**
   - **Alasan**: Entry point aplikasi, inisialisasi config, middleware, router, dan error handler.
   - **Risiko**: Salah modifikasi bisa membuat server gagal start atau observability rusak.

2. **`api/routes.py`**
   - **Alasan**: Memegang kontrak endpoint, schema request/response, dan compatibility alias.
   - **Risiko**: Perubahan tanpa sinkronisasi bisa mematahkan client existing.

3. **`services/ai/router.py`** dan **`services/ai/registry.py`**
   - **Alasan**: Mengatur routing provider dan fallback provider.
   - **Risiko**: Salah konfigurasi dapat membuat seluruh panggilan AI gagal.

## Panduan Modifikasi

- Jangan ubah file di atas tanpa memahami dampaknya ke API consumer.
- Jika kontrak error berubah, `README.md` dan `DOCS/HISTORY/` harus ikut diperbarui.
- Jika storage disentuh, validasi hasil baca/tulis setelah perubahan.
