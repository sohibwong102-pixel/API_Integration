# 🗺️ PANDUAN PERUTEAN PENYEDIA AI (AI PROVIDER ROUTING GUIDE)
> **Pedoman Arsitektur, Integrasi, & Strategi Auto-Failover AI untuk Pemula**
> 
> Dokumen ini dirancang khusus untuk membantu pemula memahami bagaimana cara menghubungkan, mengarahkan (*routing*), dan mengelola berbagai jenis penyedia kecerdasan buatan—mulai dari LLM lokal yang berjalan di komputer Anda, hingga layanan cloud skala besar global—secara fleksibel tanpa merusak struktur kode program utama.

---

## 🧭 1. Apa itu AI Provider Routing?

Dalam pembuatan aplikasi berbasis AI, Anda seringkali dihadapkan pada pilihan: *"Di mana saya harus menjalankan model AI?"*

**AI Routing** adalah seni merancang kode program sedemikian rupa sehingga aplikasi Anda dapat **berpindah penyedia AI secara instan** hanya dengan mengubah satu baris konfigurasi, tanpa perlu membongkar atau menulis ulang seluruh logika bisnis sistem Anda.

---

## 🏛️ 2. Tiga Pilar Penyedia AI (The 3 Pillars of AI Providers)

Untuk memilih penyedia yang tepat, mari pelajari karakteristik masing-masing jenis penyedia AI berikut:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TIGA PILAR PROVIDER AI                          │
├────────────────────────────────────────────────────────────────────────┤
│  1. LOCAL AI (Lokal)       2. CLOUD AI (Awan)     3. THIRD-PARTY (Pihak 3)│
│  - Berjalan di PC sendiri   - API Raksasa Teknologi- Agregator Model   │
│  - Gratis & Offline         - Berbayar, Super Cepat- 1 API Key, Ratusan│
│  - Contoh: Ollama Qwen      - Contoh: Google Gemini - Contoh: OpenRouter│
└────────────────────────────────────────────────────────────────────────┘
```

### 💻 1. Local AI (Kecerdasan Lokal)
Model AI diunduh dan dieksekusi langsung menggunakan perangkat keras (CPU/GPU/RAM) di komputer server Anda sendiri.
* **Cara Kerja**: Menggunakan alat seperti **Ollama** untuk menjalankan model open-source seperti *Qwen2.5*, *Llama3*, atau *Mistral*.
* **Kelebihan**:
  - **100% Gratis**: Tidak ada biaya per token.
  - **Privasi Tinggi**: Data sensitif tidak pernah meninggalkan komputer server Anda.
  - **Bisa Offline**: Sangat andal meskipun koneksi internet terputus.
* **Kekurangan**:
  - Sangat memakan performa komputer (bisa membuat komputer lokal melambat saat memproses).
  - Kecepatan respon bergantung penuh pada kekuatan kartu grafis (GPU) Anda.

### ☁️ 2. Cloud AI (Kecerdasan Awan)
Layanan AI komersial berlisensi yang dihosting oleh raksasa teknologi dunia di pusat data raksasa mereka.
* **Cara Kerja**: Aplikasi mengirimkan request HTTP aman ke endpoint API penyedia dengan menyertakan *API Key* otentikasi. Contoh: **Google Gemini API**, **OpenAI API**, atau **Anthropic Claude**.
* **Kelebihan**:
  - **Sangat Cepat**: Proses generasi teks selesai dalam hitungan milidetik karena dijalankan di superkomputer.
  - **Model Tercanggih**: Memiliki basis pengetahuan dan kecerdasan pemecahan masalah tingkat tertinggi.
  - **Tidak Membebani Server Lokal**: Server Anda tetap dingin dan ringan.
* **Kekurangan**:
  - **Berbayar**: Dikenakan tarif berdasarkan jumlah token/kata yang diproses.
  - **Ketergantungan Internet**: Jika koneksi internet mati, aplikasi Anda tidak dapat berfungsi.

### 🔌 3. Third-Party API (Agregator Pihak Ketiga)
Layanan perantara yang menjembatani server Anda dengan ratusan model AI open-source yang dihosting di cloud.
* **Cara Kerja**: Cukup mendaftar di satu platform, Anda mendapatkan satu *API Key* yang bisa digunakan untuk memanggil ratusan model AI berbeda secara bergantian. Contoh: **OpenRouter**, **Together AI**, atau **Groq**.
* **Kelebihan**:
  - Sangat fleksibel (bisa berganti dari Llama ke Mistral atau Qwen dalam satu detik).
  - Tarif seringkali jauh lebih murah karena persaingan harga komputasi cloud.
* **Kekurangan**:
  - Memiliki ketergantungan pada stabilitas pihak ketiga (*middleman stability*).

---

## 📐 3. Desain Arsitektur Longgar (Loose Coupling) di Proyek Ini

Mengapa kode program di proyek ini sangat mudah dipasangkan penyedia AI baru? Jawabannya adalah karena kita menerapkan prinsip **Loose Coupling** menggunakan **Factory Pattern** dan **Interface Abstraction**:

```mermaid
graph TD
    Workflow[workflows/issue/summary.py] -->|1. Panggil get_ai_service| Factory[get_ai_service Factory]
    Factory -->|2. Kembalikan Instans Aktif| BaseAIService[Interface BaseAIService]
    BaseAIService <|-- QwenLocal[QwenALocalServices - Local AI]
    BaseAIService <|-- GeminiCloud[GeminiCloudServices - Cloud AI]
    BaseAIService <|-- OpenRouterThirdParty[OpenRouterServices - Third-Party]
    BaseAIService <|-- MockService[MockAIService - Mock Dev]
```

* **`BaseAIService`**: Adalah kontrak/antarmuka hukum. Ia menegaskan bahwa *"siapapun penyedia AI-nya, dia WAJIB memiliki fungsi bernama `generate_summary(prompt: str)` yang mengembalikan nilai berupa teks string"*.
* **Workflow Conductor** (`workflows/issue/summary.py`): Tidak peduli dan tidak ingin tahu apakah AI yang digunakan adalah Ollama lokal atau Gemini Cloud. Dia hanya memanggil fungsi `ai_service.generate_summary(prompt)` dan menerima hasilnya.

---

## 🛠️ 4. Panduan Integrasi Kode (Step-by-Step Integration Guide)

Berikut adalah cetak biru (*blueprint*) konsep integrasi untuk masing-masing penyedia AI di layer `services/ai/` dan gateway `services/ai_service.py`:

### 💻 Opsi A: Integrasi Local AI (Ollama)
Ini adalah implementasi aktif saat ini, memanfaatkan endpoint lokal Ollama yang berjalan secara gratis di komputer Anda:

```python
import requests

class QwenALocalServices(BaseAIService):
    """Integrasi dengan LLM Qwen Lokal menggunakan server Ollama."""
    
    def generate_summary(self, prompt: str) -> str:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False
        }
        try:
            # Mengirim permintaan ke Ollama lokal dengan batas waktu 30 detik
            response = requests.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            raise RuntimeError(f"Gagal menghubungi Ollama Lokal: {e}")
```

---

### ☁️ Opsi B: Integrasi Cloud AI (Google Gemini API)
Untuk bermigrasi ke cloud super cepat milik Google, ikuti langkah berikut:

#### 1. Instalasi SDK Resmi Google Generative AI
```bash
pip install google-generativeai
```

#### 2. Tulis Kode Kelas Integrasi di `services/ai_service.py`
```python
import google.generativeai as genai
import os

class GeminiCloudServices(BaseAIService):
    """Integrasi dengan Google Gemini Cloud API tingkat produksi."""
    
    def __init__(self):
        # Mengambil API Key dari env variabel untuk keamanan
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Kunci API 'GEMINI_API_KEY' belum diatur di lingkungan system!")
        genai.configure(api_key=api_key)
        # Menggunakan model Gemini 1.5 Flash untuk rangkuman super cepat
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def generate_summary(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Gagal memproses dokumen di Gemini Cloud: {e}")
```

---

### 🔌 Opsi C: Integrasi Third-Party API (OpenRouter)
OpenRouter menggunakan format payload yang identik dengan OpenAI, mempermudah peralihan ke berbagai model open-source dunia:

```python
import requests
import os

class OpenRouterServices(BaseAIService):
    """Integrasi dengan ratusan model open-source di OpenRouter Cloud."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("Kunci API 'OPENROUTER_API_KEY' belum diatur!")
            
    def generate_summary(self, prompt: str) -> str:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/llama-3-8b-instruct:free", # Menggunakan model Llama 3 gratis/berbayar
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=25.0)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise RuntimeError(f"Gagal menghubungi OpenRouter: {e}")
```

---

## 🛡️ 5. Strategi Auto-Failover & Circuit Breaker (Ketahanan Mandiri)

Sebuah API kelas produksi tidak boleh mati hanya karena satu penyedia AI sedang bermasalah. Kita dapat merancang fungsi **`get_ai_service()`** agar memiliki sistem **Auto-Failover** cerdas:

> [!TIP]
> **Konsep Failover untuk Pemula**:  
> *"Gunakan model Lokal Ollama terlebih dahulu untuk menghemat biaya (Prioritas 1). Jika Ollama lokal mati atau memakan waktu terlalu lama (timeout), otomatis alihkan panggilan secara diam-diam ke Google Gemini API di cloud (Prioritas 2) agar pengguna tidak mendapati aplikasi Anda error!"*

Berikut adalah arsitektur logika failover yang diimplementasikan pada fungsi pabrik `get_ai_service()`:

```python
# Blueprint Logika Auto-Failover di services/ai_service.py

def get_ai_service() -> BaseAIService:
    """
    Pabrik pembuatan instansi AI Service cerdas dengan failover otomatis.
    Mencoba menghubungi Ollama Lokal terlebih dahulu, jika gagal otomatis 
    menggunakan Google Gemini Cloud API.
    """
    # 1. Inisialisasi penyedia utama (Ollama Lokal)
    local_service = QwenALocalServices()
    
    try:
        # Lakukan pengecekan kesehatan ringan (ping) ke server Ollama lokal
        # (Misal: mengirim request kosong berdurasi timeout 2 detik)
        response = requests.get("http://localhost:11434/", timeout=2.0)
        if response.status_code == 200:
            print("🟢 Ollama Lokal Sehat. Menggunakan Qwen Lokal.")
            return local_service
    except Exception:
        # Jika server Ollama mati/tidak merespon dalam 2 detik
        print("⚠️ Ollama Lokal tidak merespon. Mengaktifkan Failover ke Gemini Cloud...")
        
    # 2. Aktifkan Rencana Cadangan (Gemini Cloud API)
    try:
        return GeminiCloudServices()
    except Exception as e:
        # Jika cadangan cloud juga gagal (tidak ada internet atau API Key salah)
        print(f"🔴 Failover Cloud gagal: {e}. Mengaktifkan Mock Service sebagai pertolongan terakhir.")
        return MockAIService()
```

Dengan desain ketahanan mandiri di atas, API Platform Anda dijamin **99.9% selalu aktif dan andal**, memberikan pengalaman integrasi terbaik bagi mitra bisnis Anda!
