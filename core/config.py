import os
from pathlib import Path
from typing import Optional

# Menetapkan basis direktori proyek secara absolut
BASE_DIR = Path(__file__).resolve().parent.parent

# Centralized provider whitelist (reusable di seluruh app)
SUPPORTED_PROVIDERS = {
    "mock",
    "local_ollama",
    "openai",
    "google_gemini",
    "openrouter",
}

def load_dotenv(dotenv_path: str = str(BASE_DIR / ".env")):
    """
    Membaca berkas .env secara manual tanpa dependensi pihak ketiga.
    Memasukkan nilai variabel lingkungan ke os.environ jika belum ada.
    """
    if os.path.exists(dotenv_path):
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    # Menghilangkan tanda kutip jika ada
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    if key not in os.environ:
                        os.environ[key] = val

class Settings:
    """
    Representasi typed configuration untuk mengelola semua variabel lingkungan sistem secara runtime.
    """
    def __init__(self):
        # 1. Pemuatan dinamis file .env saat instansiasi objek (runtime)
        load_dotenv()

        # 🖥️ 2. KONFIGURASI SERVER UTAMA (Instance Variables)
        self.APP_ENV: str = os.getenv("APP_ENV", "development")
        self.APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
        self.APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

        # 🤖 3. KONFIGURASI PENYEDIA AI (AI ROUTER CONFIG)
        self.PRIMARY_PROVIDER: str = os.getenv("PRIMARY_PROVIDER") or os.getenv("AI_PROVIDER") or "mock"
        self.FALLBACK_PROVIDER: str = os.getenv("FALLBACK_PROVIDER", "mock")
        self.ENABLE_FALLBACK: bool = os.getenv("ENABLE_FALLBACK", "true").lower() in ("true", "1", "yes", "on")

        # 🛡️ VALIDASI STRICT PENYEDIA AI (Fail Fast saat Instansiasi)
        # Menolak langsung jika ada typo pada primary atau fallback provider di konfigurasi
        if self.PRIMARY_PROVIDER not in SUPPORTED_PROVIDERS:
            available = ", ".join(sorted(SUPPORTED_PROVIDERS))
            raise ValueError(
                f"GAGAL STARTUP: PRIMARY_PROVIDER '{self.PRIMARY_PROVIDER}' tidak valid/didukung!\n"
                f"Pilihan yang tersedia: [{available}]"
            )

        if self.ENABLE_FALLBACK and self.FALLBACK_PROVIDER not in SUPPORTED_PROVIDERS:
            available = ", ".join(sorted(SUPPORTED_PROVIDERS))
            raise ValueError(
                f"GAGAL STARTUP: FALLBACK_PROVIDER '{self.FALLBACK_PROVIDER}' tidak valid/didukung!\n"
                f"Pilihan yang tersedia: [{available}]"
            )

        # A. Konfigurasi AI Lokal (Ollama)
        self.OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        self.OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")

        # B. Konfigurasi Cloud AI (Google Gemini)
        self.GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

        # C. Konfigurasi Cloud AI (OpenAI)
        self.OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # D. Konfigurasi Agregator AI (OpenRouter)
        self.OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct:free")

        # 💾 5. KONFIGURASI PENYIMPANAN DATA
        self.DB_STORAGE_PATH: str = os.getenv("DB_STORAGE_PATH", "storage/history.json")

    def validate(self):
        """
        Validasi startup kritis. Mencegah server menyala jika penyedia AI aktif
        kehilangan kredensial wajib (fail fast).
        """
        # Kumpulkan penyedia yang aktif
        active_providers = [self.PRIMARY_PROVIDER]
        if self.ENABLE_FALLBACK:
            active_providers.append(self.FALLBACK_PROVIDER)

        # Hanya validasi jika provider yang aktif membutuhkan API Key
        for provider in active_providers:
            if provider == "google_gemini" and not self.GEMINI_API_KEY:
                raise ValueError(
                    "GAGAL STARTUP: 'GEMINI_API_KEY' wajib diatur di file .env jika menggunakan google_gemini!"
                )
            elif provider == "openai" and not self.OPENAI_API_KEY:
                raise ValueError(
                    "GAGAL STARTUP: 'OPENAI_API_KEY' wajib diatur di file .env jika menggunakan openai!"
                )
            elif provider == "openrouter" and not self.OPENROUTER_API_KEY:
                raise ValueError(
                    "GAGAL STARTUP: 'OPENROUTER_API_KEY' wajib diatur di file .env jika menggunakan openrouter!"
                )

# Inisialisasi global settings singleton secara runtime
settings = Settings()
