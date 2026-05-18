import os
import requests
from services.ai.base import BaseProvider

class OllamaProvider(BaseProvider):
    """
    Implementasi local AI Provider menggunakan Ollama (misal model Qwen 2.5).
    """
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
        
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
