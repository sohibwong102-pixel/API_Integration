# =====================================================================
# SYSTEM COMPONENT: AI SERVICE LAYER (LAPISAN LAYANAN AI)
# =====================================================================
# Deskripsi:
# Berkas ini mengelola integrasi dengan Large Language Model (LLM).
# Sesuai aturan "AI SERVICE RULE", layer ini didesain menggunakan Contract/Interface.
#
# Mengapa harus pakai Contract/Interface? (Konsep bagi Pemula):
# Jika kita langsung memanggil OpenAI atau Gemini di dalam file Workflow kita, maka 
# kode kita menjadi kaku (tightly coupled). Jika esok hari kita ingin ganti dari 
# OpenAI ke Gemini, kita terpaksa membongkar banyak file.
#
# Dengan membuat "BaseAIService" (Kontrak/Interface) dan menggunakan "Factory Pattern":
# 1. Workflow hanya tahu memanggil method `.generate_summary(prompt)`.
# 2. Kita bisa menukar provider AI di bawah dengan sangat mudah (cukup ganti di fungsi factory).
# 3. Workflow TIDAK akan menyadari pergantian tersebut karena semua provider mematuhi kontrak yang sama!
# =====================================================================

from abc import ABC, abstractmethod
import re
import requests

class BaseAIService(ABC):
    """
    Abstract Base Class (Interface) untuk AI Service.
    
    Penjelasan Pemula:
    Kelas ini bertindak sebagai "Kontrak Resmi". Kelas ini tidak memiliki logika 
    program asli, melainkan hanya menyatakan: "Siapapun kelas yang ingin menjadi 
    layanan AI di proyek ini, WAJIB memiliki fungsi `generate_summary`."
    """
    
    @abstractmethod
    def generate_summary(self, prompt: str) -> str:
        """
        Menerima teks prompt yang sudah terformat dan mengembalikan rangkuman dari AI.
        
        Args:
            prompt (str): Prompt lengkap siap kirim ke model LLM.
            
        Returns:
            str: Hasil respons rangkuman berupa string.
        """
        pass


# =====================================================================
# 🧠 1. IMPLEMENTASI MOCK AI SERVICE (PILIHAN DEFAULT UNTUK DEVELOPMENT)
# =====================================================================
class MockAIService(BaseAIService):
    """
    Mock AI Service yang mensimulasikan respons LLM secara dinamis.
    
    Penjelasan Pemula:
    Untuk menghemat kuota API / token berbayar saat masa pengembangan (development),
    kita menggunakan "Mocking" (tiruan). Kelas ini membaca input prompt secara pintar
    menggunakan pencarian kata kunci (keyword-matching) dan merespons seolah-olah 
    dia adalah AI sungguhan.
    """
    
    def generate_summary(self, prompt: str) -> str:
        # ─── LANGKAH 1: Ekstraksi Teks Isu Asli ───
        # Prompt yang diterima memiliki template khusus. Kita menggunakan Regex (Regular Expression)
        # untuk mengambil teks keluhan asli yang disisipkan di antara "Issue Text:" dan "Summary:".
        match = re.search(r"Issue Text:\s*(.*?)\n\nSummary:", prompt, re.DOTALL | re.IGNORECASE)
        
        issue_text = ""
        if match:
            # Jika teks keluhan berhasil ditemukan di dalam prompt
            issue_text = match.group(1).strip().lower()
        else:
            # Jika format template tidak sesuai, kita pakai seluruh prompt sebagai fallback
            issue_text = prompt.lower()
            
        # ─── LANGKAH 2: Simulasi Kepintaran AI (Keyword Matching) ───
        # Kami memeriksa kata kunci tertentu di dalam teks keluhan, 
        # lalu mengembalikan jawaban rangkuman bahasa Inggris yang relevan.
        if "auth" in issue_text or "middleware" in issue_text:
            return "Deployment issue related to auth middleware conflict."
            
        elif "db" in issue_text or "database" in issue_text or "koneksi" in issue_text:
            return "Database connection timeout preventing successful service startup."
            
        elif "gagal" in issue_text or "failed" in issue_text or "deploy" in issue_text:
            return "CI/CD deployment pipeline failure due to build environment setup."
            
        elif "api" in issue_text or "route" in issue_text or "endpoint" in issue_text:
            return "API gateway routing mismatch resulting in HTTP 404 errors."
            
        else:
            # Jika tidak ada kata kunci yang cocok, berikan rangkuman dinamis sederhana
            return f"Operational interruption detected in system workflow: '{issue_text[:30]}...'."


# =====================================================================
# 🔮 2. CONTOH IMPLEMENTASI GEMINI AI SERVICE (UNTUK REFERENSI MASA DEPAN)
# =====================================================================
# Penjelasan Pemula:
# Jika nanti Anda sudah siap menghubungkan sistem ke Google Gemini asli:
# 1. Install package resmi: `pip install google-generativeai`
# 2. Hapus tanda kutip multi-baris di bawah ini untuk mengaktifkan kelasnya.
# 3. Ubah return di `get_ai_service()` menjadi: `return GeminiAIService(api_key="API_KEY_ANDA")`
"""
import google.generativeai as genai

class GeminiAIService(BaseAIService):
    def __init__(self, api_key: str):
        # Konfigurasi kunci API Google Gemini
        genai.configure(api_key=api_key)
        # Menggunakan model Gemini 1.5 Flash yang sangat cepat dan murah
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def generate_summary(self, prompt: str) -> str:
        # Memanggil API Google Gemini secara langsung lewat internet
        response = self.model.generate_content(prompt)
        return response.text.strip()
"""


# =====================================================================
# 🔮 3. CONTOH IMPLEMENTASI OPENAI SERVICE (UNTUK REFERENSI MASA DEPAN)
# =====================================================================
# Penjelasan Pemula:
# Jika Anda lebih memilih menggunakan OpenAI ChatGPT (GPT-4o mini):
# 1. Install package resmi: `pip install openai`
# 2. Hapus tanda kutip multi-baris di bawah ini untuk mengaktifkan kelasnya.
# 3. Ubah return di `get_ai_service()` menjadi: `return OpenAIService(api_key="API_KEY_ANDA")`
"""
from openai import OpenAI

class OpenAIService(BaseAIService):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        
    def generate_summary(self, prompt: str) -> str:
        # Memanggil API Chat Completion OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3 # Suhu rendah (0.3) agar hasil respons konsisten dan tidak terlalu kreatif
        )
        return response.choices[0].message.content.strip()
"""
class QwenALocalServices(BaseAIService):
    """
    Implementasi local AI Service menggunakan model Qwen 2.5 melalui Ollama.
    """
    
    def generate_summary(self, prompt: str) -> str:
        model_ai = "qwen2.5:1.5b"
        url = "http://localhost:11434/api/generate"
        
        try:
            # Mengirimkan post request ke local Ollama API
            response = requests.post(
                url,
                json={
                    "model": model_ai,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30.0 # Tambahkan timeout agar server tidak hang selamanya jika Ollama macet
            )
            response.raise_for_status() # Lemparkan error jika status HTTP bukan 2xx
            result = response.json()
            return result["response"].strip()
            
        except requests.exceptions.RequestException as e:
            # Jika Ollama mati atau bermasalah, catat log kesalahan
            print(f"Error: Gagal menghubungi local Ollama API: {e}")
            # Lemparkan exception bisnis yang deskriptif agar ditangkap oleh API Router
            raise RuntimeError(f"Gagal menghubungi server kecerdasan buatan (Ollama): {e}")


# =====================================================================
# 🏭 SERVICE FACTORY (POLA PABRIK PENYEDIA SERVICE AGNOSTIK)
# =====================================================================
def get_ai_service() -> BaseAIService:
    """
    Fungsi Pabrik (Factory) untuk mengambil instansi AI Service yang aktif.
    
    Penjelasan Pemula:
    Di sinilah sihir loose coupling terjadi! Lapisan Workflow tidak pernah melakukan
    instansiasi `MockAIService()` secara manual. Workflow hanya memanggil `get_ai_service()`.
    
    Jika Anda ingin mengganti backend kecerdasan buatan dari MOCK ke GEMINI atau OPENAI,
    Anda CUKUP mengganti kode di dalam fungsi ini saja! Bagian workflow dan routing
    sama sekali tidak perlu diubah satu huruf pun.
    
    Returns:
        BaseAIService: Objek service AI aktif yang mematuhi kontrak BaseAIService.
    """
    # Saat ini secara default kita mengembalikan MockAIService agar bisa langsung
    # dijalankan secara offline dan gratis.
    return QwenALocalServices()

