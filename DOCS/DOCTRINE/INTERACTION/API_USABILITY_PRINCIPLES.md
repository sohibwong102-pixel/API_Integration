# ⚡ API_USABILITY_PRINCIPLES.md
> **Prinsip Ketergunaan REST API & Standar Desain Skema JSON - `summary_endpoint`**
>
> Dokumen ini mendefinisikan prinsip-prinsip usabilitas antarmuka program (API), hierarki tindakan (*endpoints*), penyederhanaan skema JSON, dan standar semantik penamaan untuk memastikan integrasi yang mudah dan andal.

---

## 🎯 1. Pilar Utama Usabilitas API (REST Usability Pillars)

Interaksi pada API Platform tidak terjadi lewat penekanan tombol fisik di layar, melainkan lewat pertukaran dokumen mesin-ke-mesin. Desain API yang baik harus meminimalkan gesekan integrasi (*integration friction*) melalui 4 pilar usabilitas:

1. **Clarity (Kejelasan)**: Rute API dan kunci JSON harus langsung menceritakan fungsinya tanpa perlu menebak-nebak.
2. **Flatness (Kesederhanaan)**: Hindari struktur JSON bersarang (*nested object*) yang dalam. Jaga agar payload tetap datar (*flat*) untuk mempermudah parsing.
3. **Consistency (Konsistensi)**: Menggunakan pola penamaan, tipe data, dan format waktu standar (ISO 8601) yang seragam di seluruh rute.
4. **Performance Budgets (Kecepatan)**: API harus memberikan umpan balik instan. Operasi pemrosesan AI harus dibatasi oleh anggaran latensi (*latency budget*) yang ketat.

---

## 🗂️ 2. Hierarki Tindakan API (Endpoint Priority Tiering)

Untuk merancang rute API yang bersih, kelompokkan tindakan berdasarkan prioritas fungsionalitas bisnis:

```
                  ┌────────────────────────────────────────┐
                  │          HIERARKI ENDPOINT API         │
                  └────────────────────────────────────────┘
                                      │
             ┌────────────────────────┴────────────────────────┐
             ▼                                                 ▼
   [Primary Endpoints]                               [Secondary Endpoints]
     - Mutating POST                                   - Querying GET
     - Trigger Alur Kerja                              - Membaca Log/Riwayat
     - Beban Komputasi AI                              - Ringan, Cepat, Idempotent
     - Contoh: POST /api/issue-summary                 - Contoh: GET /api/history
```

### A. Primary Endpoints (Tindakan Utama)
* **Karakteristik**: Memodifikasi state data, memicu orkestrasi alur kerja (*workflows*), atau melakukan panggilan berat ke kecerdasan buatan (LLM).
* **HTTP Method**: Wajib menggunakan `POST`.
* **Desain Payload**: Payload input harus seminimal mungkin untuk meminimalkan beban kognitif developer. Contoh:
  ```json
  {
    "text": "Konten teks masalah operasional..."
  }
  ```

### B. Secondary Endpoints (Tindakan Pendukung)
* **Karakteristik**: Bersifat membaca (*read-only*), mengambil daftar log/riwayat transaksi untuk kebutuhan audit, aman, dan idempotent.
* **HTTP Method**: Wajib menggunakan `GET`.
* **Desain Payload**: Tidak menggunakan JSON request body. Pencarian/filter dikirim via Query Parameters.

---

## 📝 3. Desain Skema JSON & Aturan Semantik (JSON Schema Standards)

### A. Aturan Penamaan Rute URL
* Gunakan huruf kecil (*lowercase*) dan gunakan tanda hubung jika terdiri dari beberapa kata (kebab-case). Contoh: `/api/issue-summary` (BUKAN `/api/issueSummary` atau `/api/Issue_Summary`).
* Gunakan kata benda jamak (*plural*) untuk endpoint sumber daya yang mengembalikan daftar objek. Contoh: `/api/history` atau `/api/issues`.

### B. Semantik Kunci JSON (JSON Key Wording)
* **Action-Oriented**: Nama properti wajib menggunakan deskripsi fungsionalitas yang jelas dan universal. 
  - 🟢 **GOOD**: `original_text`, `summary`, `timestamp`, `record_id`.
  - 🔴 **BAD**: `data1`, `isi_issue`, `summaryText`, `output_ai`.
* **Bilingual Rules**: Properti skema JSON wajib menggunakan Bahasa Inggris teknis agar kompatibel dengan library pemrograman global, tetapi dokumentasi deskripsi penjelasannya di Swagger wajib menggunakan Bahasa Indonesia.

---

## ⚡ 4. Anggaran Latensi & Penanganan Beban Kerja (Performance & Latency)

* **LLM Latency Budget**: Operasi sinkronus pemanggilan LLM lokal dibatasi oleh waktu maksimal **30 detik** (timeout). 
* **Worker Queue Transition**: Jika di masa depan waktu generate melebihi 30 detik (misalnya untuk perangkuman dokumen log server berukuran besar), rute wajib berevolusi menjadi asinkronus menggunakan sistem *task queue* (seperti Celery/Redis) dan mengembalikan HTTP 202 (Accepted) lengkap dengan URL status pengerjaan.
