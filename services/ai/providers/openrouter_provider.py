import os
import requests
from services.ai.base import BaseProvider

class OpenRouterProvider(BaseProvider):
    """
    Implementasi cloud AI Provider menggunakan REST API OpenRouter.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct:free")
        
    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("Kunci API 'OPENROUTER_API_KEY' belum diatur!")
            
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Gagal menghubungi OpenRouter API: {e}")
