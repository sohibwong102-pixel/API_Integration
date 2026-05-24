# SAFE_TO_EDIT.md

> panduan area yang relatif aman disentuh 😎🔥
>
> dokumen ini membantu developer memahami area mana yang aman dimodifikasi dan area mana yang bisa bikin civilization goyang 😭🔥

---

# 🟢 Low Risk

## `prompts/issue/*.txt`

Aman untuk tuning instruksi AI selama kontrak output tetap dijaga.

Karena:

```txt
prompt experimentation memang habitat goblin 😎🔥
```

---

## `DOCS/HISTORY/`

Aman untuk menambah catatan perubahan setelah implementasi selesai.

History penting supaya:

- perubahan tidak hilang
- refactor tidak jadi misteri
- future self tidak tersesat 😭🔥

---

## `DOCS/TEST_EVIDENCE/`

Aman untuk menambah evidence validasi.

Karena:

```txt
"trust me bro"
bukan testing strategy 😭🔥
```

---

# 🟡 Medium Risk

## `workflows/issue/*.py`

Aman diubah jika tetap menjaga kontrak input/output tiap workflow.

Workflow adalah conductor utama.

Kalau flow berubah tanpa kontrol:

```txt
orchestration mulai chaos diam diam 😭🔥
```

---

## `services/ai/providers/*.py`

Aman untuk perbaikan provider spesifik.

TAPI:

interface provider harus tetap konsisten.

Karena kalau tidak:

- router bisa rusak
- fallback bisa gagal
- provider abstraction runtuh 😭🔥

---

## `core/config.py`

Aman untuk menambah config baru.

Tapi hati-hati kalau:

- rename env existing
- ubah default penting
- ubah loading lifecycle

karena efeknya bisa nyebar ke seluruh system.

---

# 🔴 High Risk

## `api/routes.py`

Memegang public contract.

Perubahan kecil bisa berdampak langsung ke:

- client
- automation
- workflow integration
- backward compatibility

---

## `main.py`

Menyangkut:

- startup lifecycle
- middleware
- router registration
- observability
- request lifecycle

Salah modifikasi bisa bikin:

```txt
server hidup
TAPI behavior diam diam rusak 😭🔥
```

---

## `core/error_handlers.py`

Mengatur seluruh bentuk response error publik.

Kalau error contract berubah sembarangan:

- client parsing gagal
- automation bisa pecah
- observability jadi tidak stabil

---

## `storage/local_storage.py`

Menyangkut integritas data riwayat.

Kesalahan kecil bisa menyebabkan:

- history korup
- write gagal
- debugging kehilangan jejak 😭🔥

---

# 📌 Panduan Aman

1. Mulai dari perubahan paling kecil yang menyelesaikan masalah.
2. Jika menyentuh layer `api/`, cek dampaknya ke workflow dan documentation contract.
3. Jika menyentuh storage atau error handler, lakukan validasi lebih ketat.
4. Hindari mengubah banyak layer sekaligus tanpa alasan yang jelas.

---

# 😎 Final Reminder

```txt
semakin dekat ke core lifecycle,
semakin besar kemungkinan chaos tersembunyi 😭🔥
```
