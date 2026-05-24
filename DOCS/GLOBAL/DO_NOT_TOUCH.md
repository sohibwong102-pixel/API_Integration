🚫 DO_NOT_TOUCH.md

«area sacred yang jangan disentuh sembarangan 😭🔥

file-file disini punya dampak besar terhadap:

- stability
- public contract
- orchestration lifecycle
- observability
- compatibility»

---

🔴 CRITICAL AREA

⚠️ "core/error_handlers.py"

Kenapa Sensitif?

File ini adalah:

sumber utama kontrak error response publik 😭🔥

Kalau diubah sembarangan:

- "error.code" bisa drift
- automation client bisa gagal parsing
- observability mulai tidak konsisten
- API consumer mulai chaos diam diam 😭🔥

---

⚠️ "storage/local_storage.py"

Kenapa Sensitif?

Satu-satunya adapter resmi untuk history JSON lokal.

Kesalahan kecil bisa menyebabkan:

- history korup
- data hilang
- debugging kehilangan jejak
- workflow tracing mulai gelap 😭🔥

---

⚠️ "storage/history.json"

Kenapa Sensitif?

Berkas persistensi lokal aktif.

Edit manual yang salah bisa bikin:

history tidak bisa dibaca lagi 😭🔥

---

🟠 HIGH RISK AREA

⚠️ "main.py"

Area Tanggung Jawab

- startup lifecycle
- middleware
- router registration
- observability
- request lifecycle

Risiko

Salah modifikasi bisa menyebabkan:

- server gagal start
- tracing rusak
- middleware behavior aneh
- request lifecycle bocor 😭🔥

---

⚠️ "api/routes.py"

Area Tanggung Jawab

- endpoint contract
- request schema
- response schema
- compatibility alias

Risiko

Perubahan kecil bisa mematahkan:

- client existing
- automation
- backward compatibility
- integration workflow 😭🔥

---

⚠️ "services/ai/router.py"

⚠️ "services/ai/registry.py"

Area Tanggung Jawab

- provider routing
- fallback orchestration
- provider registry

Risiko

Kalau salah konfigurasi:

seluruh panggilan AI bisa gagal bersamaan 😭🔥

---

📌 PANDUAN MODIFIKASI

✅ Sebelum Mengubah File Sensitif

Pastikan memahami:

- impact ke client
- impact ke workflow
- impact ke observability
- impact ke compatibility

---

✅ Jika Error Contract Berubah

WAJIB update:

- "README.md"
- "DOCS/HISTORY/"

Karena:

public contract bukan area coba-coba 😭🔥

---

✅ Jika Storage Disentuh

Lakukan validasi:

- read
- write
- corruption check
- history recovery

---

❌ Jangan Refactor Besar Hanya Karena:

“kelihatan lebih rapi”

Karena:

rapi belum tentu stabil 😭🔥