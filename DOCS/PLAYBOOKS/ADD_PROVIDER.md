````md id="playbook1"
# 🛠️ ADD_PROVIDER PLAYBOOK 😎🔥

> cara nambah provider baru tanpa menghancurkan orchestration ecosystem 😭🔥

---

# 🧠 Tujuan

Playbook ini dibuat supaya:

- provider baru bisa ditambah dengan konsisten
- routing tetap waras
- abstraction tidak bocor
- future self tidak depresi 😭

---

# 📂 Lokasi Provider

Semua provider disimpan di:

```txt
services/ai/providers/
```

Contoh:

```txt
providers/
├── openai_provider.py
├── gemini_provider.py
└── openrouter_provider.py
```

---

# 🔥 RULE BESAR

Provider:

```txt
TIDAK BOLEH 😭🔥
```

- pegang workflow logic
- pegang HTTP route
- pegang storage
- pegang orchestration besar

Provider hanya bertugas:

```txt
request masuk 😎
→ kirim ke model 😎
→ return response 😎
```

---

# 🏗️ STEP 1 — Buat File Provider

Contoh:

```txt
services/ai/providers/deepseek_provider.py
```

---

# 🧩 STEP 2 — Inherit Base Provider

Gunakan contract dari:

```python
from services.ai.base import BaseAIProvider
```

Contoh:

```python
class DeepseekProvider(BaseAIProvider):
    ...
```

Tujuan:

- semua provider punya interface sama
- router tidak chaos 😭🔥

---

# ⚙️ STEP 3 — Implement Method Wajib

Minimal implement:

```python
generate()
```

Contoh:

```python
async def generate(self, prompt: str) -> str:
    ...
```

---

# 🧠 STEP 4 — Tambahkan Config

Tambahkan:

- API key
- endpoint
- timeout
- model default

Di:

```txt
core/config.py
```

Dan `.env`

Contoh:

```env
DEEPSEEK_API_KEY=
DEEPSEEK_BASE_URL=
```

---

# 🔄 STEP 5 — Register Provider

Tambahkan ke:

```txt
services/ai/registry.py
```

Contoh:

```python
PROVIDER_REGISTRY = {
    "deepseek": DeepseekProvider,
}
```

Kalau lupa register:

```txt
provider jadi hantu 😭🔥
```

---

# 🚦 STEP 6 — Tambahkan Routing

Edit:

```txt
services/ai/router.py
```

Contoh:

- fallback priority
- provider selection
- retry strategy

---

# 🧪 STEP 7 — Testing

Minimal test:

- provider bisa connect
- response masuk
- timeout handling
- invalid key behavior
- fallback jalan

Checklist:

```txt
[ ] response normal
[ ] auth aman
[ ] timeout aman
[ ] retry aman
[ ] fallback aman
```

---

# ⚠️ COMMON MISTAKES

## ❌ Logic bocor ke provider

Salah:

```python
if user_is_premium:
```

Provider tidak boleh tau business logic 😭🔥

---

## ❌ Hardcode config

Salah:

```python
api_key = "sk-goblin"
```

Gunakan:

- env
- centralized config

---

## ❌ Provider beda format sendiri

Semua provider:

```txt
harus civilized 😎🔥
```

Karena router bergantung pada consistency.

---

# 😭 EMERGENCY CHECKLIST

Kalau provider tidak jalan:

```txt
[ ] sudah register?
[ ] env sudah kebaca?
[ ] endpoint benar?
[ ] async benar?
[ ] return format sesuai?
[ ] router sudah update?
```

---

# 🧠 FINAL DOCTRINE

```txt
provider interchangeable 😎🔥

kalau ganti provider bikin system hancur:
berarti abstraction gagal 😭🔥
```
````
