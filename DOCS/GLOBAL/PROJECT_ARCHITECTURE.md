# PROJECT_ARCHITECTURE.md

> blueprint otak backend orchestration 😎🔥
>
> dokumen ini menjelaskan struktur tingkat tinggi dan pola arsitektur yang digunakan dalam project **CIVILIZATION GROUP PROJECT**.

---

# 🧠 Core Identity

Project ini adalah:

- backend FastAPI
- workflow-first orchestration system
- provider-agnostic AI backend
- interface-independent service layer

Arsitektur utamanya mengikuti prinsip:

```txt
Workflow Conductor Architecture
```

Artinya:

- API menerima dan memvalidasi request
- workflow menjadi pusat orchestration
- prompt dipisahkan dari kode
- provider AI dimodularisasi
- storage dipisahkan dari workflow dan transport

Karena kalau semua layer dicampur:

```txt
future self mulai mempertanyakan keputusan hidup 😭🔥
```

---

# ⚙️ Tech Stack

- **Language**: Python 3.10+
- **Framework**: `FastAPI`
- **Validation**: `Pydantic`
- **Server**: `Uvicorn`
- **Storage**: `storage/history.json`

## 🤖 AI Providers

- Mock
- Ollama
- Google Gemini
- OpenAI
- OpenRouter

---

# 🗺️ Struktur Folder & Tanggung Jawab

| Folder | Tanggung Jawab |
| :--- | :--- |
| `api/` | HTTP transport layer, routing, dan validasi request/response. |
| `core/` | Konfigurasi runtime dan centralized error handling. |
| `workflows/` | Workflow conductor untuk sequence bisnis per use case issue. |
| `prompts/` | Template prompt mentah dan helper formatting prompt. |
| `services/` | Integrasi provider AI dan facade akses AI. |
| `storage/` | Persistensi riwayat proses ke file JSON lokal. |
| `DOCS/` | Memory system biar orchestration tidak berubah jadi archaeological site 😭🔥 |

---

# 🔄 Alur Kerja Utama

1. Client mengirim request HTTP ke endpoint API.
2. `api/routes.py` memvalidasi payload menggunakan Pydantic.
3. Router mendelegasikan eksekusi ke workflow yang sesuai.
4. Workflow memuat template prompt dari `prompts/`.
5. Workflow memanggil service AI melalui facade yang provider-agnostic.
6. Workflow menormalkan hasil lalu menyimpan history ke `storage/local_storage.py` jika relevan.
7. Router mengembalikan response JSON yang stabil ke client.

Flow sederhananya:

```txt
client
→ api
→ workflow
→ AI facade
→ provider
→ normalize
→ response
```

---

# 📌 Prinsip Engineering Penting

## 1. No Business Logic in API

`api/` hanya bertugas sebagai HTTP adapter.

Karena kalau business logic bocor ke API layer:

```txt
transport mulai jadi monster segala fungsi 😭🔥
```

---

## 2. Workflow as Conductor

Sequence bisnis berada di `workflows/`.

Workflow adalah:

- conductor
- orchestration brain
- lifecycle manager

bukan sekadar helper random.

---

## 3. Provider-Agnostic Services

Logic integrasi AI tidak boleh hard-coupled ke satu vendor.

Tujuannya:

- provider bisa diganti
- fallback lebih aman
- migration lebih waras
- experimentation lebih fleksibel

---

## 4. Prompt Separation

Instruksi AI disimpan di `prompts/`, bukan giant inline string.

Karena giant prompt inline biasanya berakhir menjadi:

```txt
ancient forbidden paragraph 😭🔥
```

---

## 5. Stable Error Contract

Error response mengikuti kontrak enum stabil di `core/error_handlers.py`.

Tujuannya:

- client tidak rusak tiap refactor
- debugging lebih predictable
- observability lebih konsisten
