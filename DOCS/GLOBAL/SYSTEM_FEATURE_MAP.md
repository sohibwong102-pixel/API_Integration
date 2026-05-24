# 🗂️ SYSTEM_FEATURE_MAP.md

> Peta fitur, arsitektur aktif, alur orchestration, dan mapping implementation terbaru.
>
> Dokumen ini menjadi source of truth untuk:
>
> - feature mapping
> - endpoint ecosystem
> - workflow architecture
> - provider orchestration
> - request lifecycle
> - governance consistency

---

# 🧠 SYSTEM PHILOSOPHY

Project ini menggunakan:

```txt
Workflow Conductor Architecture
```

Artinya:

- API layer hanya transport layer
- workflow menjadi pusat orchestration
- AI provider bersifat modular
- prompt dipisahkan dari implementation
- request lifecycle dibuat centralized
- provider dapat diganti tanpa mengubah workflow

Tujuan utama:

- scalability
- maintainability
- deterministic flow
- AI-agent friendly ecosystem
- predictable public contract

---

# 🌐 ACTIVE API ECOSYSTEM

## Primary Endpoints

| Endpoint | Method | Capability | Workflow |
|---|---|---|---|
| `/api/issue/summary` | `POST` | Issue summarization | `workflows/issue/summary.py` |
| `/api/issue/categorize` | `POST` | Issue categorization | `workflows/issue/categorize.py` |
| `/api/issue/severity` | `POST` | Severity classification | `workflows/issue/severity.py` |
| `/api/issue/tags` | `POST` | Tag extraction | `workflows/issue/tags.py` |
| `/api/issue/sentiment` | `POST` | Sentiment analysis | `workflows/issue/sentiment.py` |

---

## Legacy Compatibility Endpoint

| Endpoint | Status | Purpose |
|---|---|---|
| `/api/issue-summary` | Compatibility Layer | mempertahankan backward compatibility client lama |

Legacy endpoint tetap aktif agar:

- client lama tidak rusak
- migration lebih aman
- public contract tetap stabil

Response compatibility:

```json
{
  "summary": "...",
  "request_id": "..."
}
```

---

# 🏗️ FEATURE TO CODE MAPPING

## API Layer

| File | Responsibility |
|---|---|
| `api/routes.py` | endpoint registration, request validation, response contract |
| `main.py` | FastAPI bootstrap, request lifecycle ownership, middleware |

Rules:

```txt
API layer tidak boleh memegang business logic.
```

Workflow tetap menjadi orchestration source utama.

---

# 🧠 WORKFLOW ECOSYSTEM

## Workflow Folder

```txt
workflows/issue/
```

## Active Workflows

| Workflow | Responsibility |
|---|---|
| `summary.py` | issue summarization |
| `categorize.py` | issue categorization |
| `severity.py` | severity classification |
| `tags.py` | tag extraction |
| `sentiment.py` | sentiment analysis |

Workflow behavior:

- orchestration-only
- deterministic
- reusable
- provider-agnostic
- contract-driven

General flow:

```txt
load prompt
→ call AI facade
→ normalize output
→ optional persistence
→ return response
```

---

# 📝 PROMPT SYSTEM

## Prompt Folder

```txt
prompts/issue/
```

## Active Prompt Files

| Prompt File | Purpose |
|---|---|
| `summary.txt` | summarization instruction |
| `categorize.txt` | categorization instruction |
| `severity.txt` | severity instruction |
| `tags.txt` | tag extraction instruction |
| `sentiment.txt` | sentiment analysis instruction |

Prompt doctrine:

- concise
- deterministic
- single responsibility
- no markdown output
- no JSON output

Tujuan:

- isolated prompt tuning
- safer iteration
- reusable orchestration
- easier maintenance

---

# 🤖 AI PROVIDER ARCHITECTURE

## Supported Providers

- OpenAI
- Gemini
- Ollama
- OpenRouter
- Mock

## Architecture Mapping

```txt
Facade
→ Router
→ Registry
→ Provider Adapter
```

## Main Provider Files

| File | Responsibility |
|---|---|
| `services/ai/facade.py` | unified AI access layer |
| `services/ai/router.py` | provider routing logic |
| `services/ai/registry.py` | provider registration mapping |
| `services/ai/models.py` | model configuration |
| `services/ai/base.py` | provider contract/interface |

## Provider Adapters

```txt
services/ai/providers/
```

Contains:

- openai provider
- gemini provider
- ollama provider
- openrouter provider
- mock provider

---

# 🔍 REQUEST LIFECYCLE

Request lifecycle ownership berada di:

```txt
main.py
```

Flow:

```txt
client request
→ request_id injected/restored
→ request.state populated
→ propagated across layers
→ exposed via X-Request-ID header
→ structured access logging
```

Structured logging fields:

- request_id
- method
- path
- status_code
- duration_ms

Tujuan:

- observability
- tracing
- debugging consistency
- request tracking

---

# 💾 STORAGE LAYER

## Storage Files

| File | Purpose |
|---|---|
| `storage/local_storage.py` | local persistence helper |
| `storage/history.json` | request history storage |

Saat ini storage masih menggunakan local JSON persistence.

Cocok untuk:

- local development
- experimentation
- workflow prototyping

Belum direkomendasikan untuk:

- massive concurrency
- production-scale persistence

---

# ⚠️ CURRENT LIMITATIONS

| Limitation | Impact | Recommendation |
|---|---|---|
| JSON persistence | scaling limitation | migrate ke PostgreSQL/MongoDB |
| local file storage | concurrency risk | gunakan transactional database |
| no distributed queue | heavy workflow bottleneck | tambah worker queue system |
| no cache layer | repeated AI computation | integrate Redis caching |

---

# 📚 DOCS GOVERNANCE

## Documentation Rules

Semua docs harus:

- beginner friendly
- sinkron dengan implementation aktif
- sinkron dengan README
- sinkron dengan SYSTEM_FEATURE_MAP
- menjelaskan WHY dan FLOW
- tidak membuat asumsi behavior

---

# 📌 REQUIREMENT AUTHORITY DOCTRINE

```txt
Implementation mengikuti explicit operator intent.
```

Jika requirement:

- ambigu
- tidak lengkap
- tidak menjelaskan expected behavior

maka:

```txt
multiple implementation interpretation dapat terjadi.
```

Reviewer dan updater docs:

- tidak boleh mengarang intended behavior
- tidak boleh membuat asumsi pribadi
- harus mengikuti explicit operator direction

---

# 🚀 FUTURE SCALING DIRECTION

Recommended evolution:

```mermaid
graph LR
    Step1[Input Validation & Fallback] --> Step2[Database Migration]
    Step2 --> Step3[Queue & Worker System]
    Step3 --> Step4[Redis Cache & Rate Limiter]
```

Potential future improvements:

- PostgreSQL persistence
- Redis caching
- async worker queue
- provider auto-fallback
- distributed orchestration
- request analytics
- workflow observability

---

# 😎 FINAL NOTE

```txt
SYSTEM_FEATURE_MAP.md
bukan sekadar daftar endpoint.

Tapi:
- anti-documentation drift layer
- architecture synchronization layer
- onboarding memory system
- AI ecosystem context source
```
