# FEATURE_MAP.md

Peta fitur backend aktif dan berkas utama yang terlibat.

| Fitur | Tujuan | Berkas Utama | Endpoint | Risiko |
| :--- | :--- | :--- | :--- | :--- |
| **Health Check** | Memverifikasi server hidup dan menampilkan endpoint utama. | `main.py` | `GET /` | Rendah |
| **Legacy Issue Summary** | Menjaga contract lama summary plus `request_id`. | `api/routes.py`, `workflows/issue/summary.py` | `POST /api/issue-summary` | Sedang |
| **Issue Summary** | Menghasilkan ringkasan issue satu string. | `api/routes.py`, `workflows/issue/summary.py`, `prompts/issue/summary.txt` | `POST /api/issue/summary` | Sedang |
| **Issue Categorization** | Mengklasifikasikan issue ke kategori. | `api/routes.py`, `workflows/issue/categorize.py`, `prompts/issue/categorize.txt` | `POST /api/issue/categorize` | Sedang |
| **Issue Severity** | Menentukan tingkat keparahan issue. | `api/routes.py`, `workflows/issue/severity.py`, `prompts/issue/severity.txt` | `POST /api/issue/severity` | Sedang |
| **Issue Tags** | Mengekstrak tag penting dari issue. | `api/routes.py`, `workflows/issue/tags.py`, `prompts/issue/tags.txt` | `POST /api/issue/tags` | Sedang |
| **Issue Sentiment** | Mengklasifikasikan sentimen issue. | `api/routes.py`, `workflows/issue/sentiment.py`, `prompts/issue/sentiment.txt` | `POST /api/issue/sentiment` | Sedang |
| **History Retrieval** | Mengambil riwayat summary yang tersimpan. | `api/routes.py`, `storage/local_storage.py` | `GET /api/history` | Rendah |
