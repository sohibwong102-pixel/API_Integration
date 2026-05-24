# PROJECT_ARCHITECTURE.md

Dokumen ini menjelaskan struktur tingkat tinggi dan pola arsitektur yang digunakan dalam project **CIVILIZATION GROUP PROJECT**.

## Core Identity

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

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: `FastAPI`
- **Validation**: `Pydantic`
- **Server**: `Uvicorn`
- **Storage**: `storage/history.json`
- **AI Providers**:
  - Mock
  - Ollama
  - Google Gemini
  - OpenAI
  - OpenRouter

## Struktur Folder & Tanggung Jawab

| Folder | Tanggung Jawab |
| :--- | :--- |
| `api/` | HTTP transport layer, routing, dan validasi request/response. |
| `core/` | Konfigurasi runtime dan centralized error handling. |
| `workflows/` | Workflow conductor untuk sequence bisnis per use case issue. |
| `prompts/` | Template prompt mentah dan helper formatting prompt. |
| `services/` | Integrasi provider AI dan facade akses AI. |
| `storage/` | Persistensi riwayat proses ke file JSON lokal. |
| `DOCS/` | Dokumentasi arsitektur, aturan kerja, riwayat perubahan, dan evidence. |

## Alur Kerja Utama

1. Client mengirim request HTTP ke endpoint API.
2. `api/routes.py` memvalidasi payload menggunakan Pydantic.
3. Router mendelegasikan eksekusi ke workflow yang sesuai.
4. Workflow memuat template prompt dari `prompts/`.
5. Workflow memanggil service AI melalui facade yang provider-agnostic.
6. Workflow menormalkan hasil lalu menyimpan history ke `storage/local_storage.py` jika relevan.
7. Router mengembalikan response JSON yang stabil ke client.

## Prinsip Engineering Penting

1. **No Business Logic in API**: `api/` hanya bertugas sebagai HTTP adapter.
2. **Workflow as Conductor**: sequence bisnis berada di `workflows/`.
3. **Provider-Agnostic Services**: logic integrasi AI tidak boleh hard-coupled ke satu vendor.
4. **Prompt Separation**: instruksi AI disimpan di `prompts/`, bukan inline giant string di workflow.
5. **Stable Error Contract**: error response mengikuti kontrak enum stabil di `core/error_handlers.py`.
