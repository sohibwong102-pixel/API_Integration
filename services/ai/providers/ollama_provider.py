import requests
from services.ai.base import BaseProvider
from core import settings

class OllamaProvider(BaseProvider):
    """
    Implementasi local AI Provider menggunakan Ollama (misal model Qwen 2.5).
    """
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        
    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        try:
            response = requests.post(
                url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            return result["response"].strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Gagal menghubungi local Ollama API: {e}")
