# ⚡ API_USABILITY_RULES.md
> **Standar Ketergunaan API & Pengalaman Pengembang (Developer Experience - DX)**
>
> Dokumen ini mendefinisikan prinsip-prinsip ketergunaan (*usability*), desain response, serta standar dokumentasi OpenAPI untuk memastikan API Platform ini mudah diintegrasikan, andal, dan menyenangkan bagi pengembang frontend/pihak ketiga.

---

## 🎯 1. Pilar Utama Pengalaman Pengembang (DX Pillars)

Sebuah API yang baik bukan hanya yang berhasil mengembalikan response, melainkan yang didesain dengan memperhitungkan kemudahan pengembang (*developer*) yang akan mengonsumsinya:

1. **Clarity (Kejelasan)**: Nama rute (*endpoints*) dan struktur JSON harus intuitif dan konsisten.
2. **Predictability (Keterdugaan)**: Struktur data response untuk status sukses maupun error harus selalu seragam dan dapat diprediksi.
3. **Recoverability (Kemudahan Pemulihan)**: Saat terjadi kesalahan (*error*), API wajib mengembalikan pesan kesalahan yang informatif, bukan hanya kode HTTP mentah.
4. **Self-Documenting (Mandiri)**: API terdokumentasi secara otomatis dan interaktif melalui Swagger/ReDoc secara komprehensif.

---

## 🛠️ 2. Standar Desain Rute & Penamaan (Routing Standards)

* **Predictable HTTP Methods**:
  - `GET`: Digunakan hanya untuk membaca data, bebas dari efek samping (*safe & idempotent*). Contoh: `GET /api/history`
  - `POST`: Digunakan untuk membuat sumber daya baru atau memicu pengerjaan logika bisnis berat (workflow). Contoh: `POST /api/issue-summary`
* **Consistent URL Paths**: Gunakan format huruf kecil (*lowercase*), dipisahkan dengan tanda hubung jika terdiri dari beberapa kata (kebab-case), dan diawali dengan prefiks versi `/api/`.
* **Plural Naming for Resources**: Selalu gunakan kata benda jamak untuk rute yang mengambil daftar objek (misalnya `/api/history` untuk riwayat keluhan).

---

## 🛡️ 3. Format Penanganan Error & Respon Seragam (Error Shaping)

Saat client mengirimkan request yang tidak valid atau terjadi kegagalan server, API **DILARANG** membiarkan server hang atau mengembalikan traceback bahasa pemrograman. 

Setiap kegagalan wajib dibungkus menggunakan standardisasi FastAPI `HTTPException` dengan skema response berikut:

```json
{
  "detail": "Pesan kesalahan yang human-readable dalam Bahasa Indonesia menjelaskan akar masalah."
}
```

### 🚨 Aturan Pemetaan Status Code HTTP:

* **HTTP 400 (Bad Request)**: Digunakan saat data input dari client lolos validasi tipe data tetapi melanggar logika bisnis (misal: teks yang dikirim tidak relevan atau kosong).
* **HTTP 422 (Unprocessable Entity)**: Ditangani otomatis oleh Pydantic saat format data JSON tidak cocok atau field wajib (*required*) absen dari payload.
* **HTTP 500 (Internal Server Error)**: Penyelamat terakhir (*safeguard*). Digunakan untuk membungkus kegagalan tak terduga (database JSON terkunci, server AI eksternal mati) agar server tidak mati total.

---

## 📝 4. Dokumentasi Mandiri Melalui Pydantic & Swagger

Setiap endpoint wajib terdaftar dengan dokumentasi yang ramah di `/docs` (Swagger UI):

1. **Rich Metadata**: Sertakan parameter `summary`, `description`, dan `response_model` di setiap decorator APIRouter.
2. **Pydantic Field Descriptions**: Gunakan anotasi `Field` lengkap dengan `description` dan `examples` pada setiap skema Pydantic. Ini bertindak sebagai spesifikasi API yang langsung hidup di dalam dokumentasi.
3. **Bilingual Principle**: Gunakan bahasa Inggris untuk properti skema JSON teknis (`original_text`, `summary`), tetapi gunakan bahasa Indonesia untuk penjelasan deskripsi metadata bisnisnya agar mudah dipahami oleh tim lokal.

---

## 🔄 5. Kecepatan & Ketahanan Sistem (API Resiliency)

* **Mandatory Timeouts**: Setiap panggilan API keluar menuju pihak ketiga (seperti local Ollama API) **wajib** mencantumkan parameter `timeout` eksplisit (maksimal `30.0` detik) untuk mencegah starved threads yang dapat memacetkan server backend.
* **Stateless Operations**: Setiap request harus independen dan mandiri. Jangan menyimpan state percakapan di dalam RAM server API. Gunakan database persistensi atau biarkan client mengirimkan konteks riwayat jika diperlukan.
