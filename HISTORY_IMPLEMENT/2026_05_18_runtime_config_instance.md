# 📝 RIWAYAT IMPLEMENTASI: RUNTIME-BASED INSTANCE CONFIGURATION

## 📅 Tanggal: 18 Mei 2026 13:53

## 🛠️ Status: SELESAI (SUKSES)

---

## 🔍 1. Ringkasan Perubahan

Melakukan refaktorisasi arsitektur konfigurasi dari pembacaan _static/class-level_ variabel lingkungan menjadi instansiasi konfigurasi dinamis berbasis runtime (_runtime-based instance configuration_). Semua pembacaan `os.getenv()` dipindahkan sepenuhnya ke dalam metode inisialisasi `Settings.__init__()`.

---

## 🛠️ 2. Berkas yang Dibuat & Dimodifikasi

### A. Berkas Baru / Tambahan Riwayat

- **`HISTORY_IMPLEMENT/2026_05_18_runtime_config_instance.md`** _(Berkas ini)_

### B. Berkas Dimodifikasi

1. **`core/config.py`**
   - Menghapus semua deklarasi variabel statis/tingkat kelas (_class variables_).
   - Memindahkan fungsi pemuatan file `.env` (`load_dotenv()`) ke dalam `__init__(self)` agar dievaluasi secara dinamis saat objek dibuat.
   - Mengubah seluruh properti konfigurasi menjadi variabel instansi (_instance variables_) menggunakan awalan `self.`.
   - Tetap mengekspos instansi tunggal (_singleton_) `settings = Settings()` di bagian bawah modul demi menjaga kompatibilitas import 100% dengan modul konsumen lainnya.

---

## 🧪 3. Hasil Pengujian (Integration Testing)

### Skenario A: Kegagalan Instan Startup (Fail-Fast Validation)

Memastikan validasi runtime tetap mendeteksi kesalahan konfigurasi kritis secara instan pada startup.

- **Perintah**:
  ```bash
  PRIMARY_PROVIDER=google_gemini GEMINI_API_KEY= .venv/bin/python3 -c "import main"
  ```
- **Hasil**:
  ```text
  ValueError: GAGAL STARTUP: 'GEMINI_API_KEY' wajib diatur di file .env jika menggunakan google_gemini!
  ```

### Skenario B: Eksekusi Alur Normal (Ollama Lokal)

Menguji apakah modul konsumen (seperti workflow dan router) dapat memproses pemanggilan LLM secara lancar menggunakan shared settings instance baru.

- **Perintah**:
  ```bash
  .venv/bin/python3 -c "from services import get_ai_service; svc = get_ai_service(); print('RESULT:', svc.generate_summary('Test Issue Text: database error\n\nSummary:'))"
  ```
- **Hasil**:
  ```text
  RESULT: The summary is not provided...
  ```
  _(Berhasil dieksekusi dengan lancar via Ollama Lokal dengan status exit 0)._

---

## 🚀 4. Keuntungan Refaktorisasi

1. **Testing Isolation**: Memungkinkan isolasi pengetesan yang lebih aman karena instansi kelas `Settings` dapat di-mock atau dibuat ulang secara independen untuk tiap test case tanpa efek samping statis.
2. **Reloadable**: Memungkinkan pemuatan ulang konfigurasi secara dinamis di memori jika berkas `.env` berubah saat runtime tanpa perlu me-restart server.
3. **No Scattered Env Access**: Menjaga 100% disiplin pembatasan bahwa `os.getenv` hanya dieksekusi secara instan saat objek inisialisasi dibuat di memori.
