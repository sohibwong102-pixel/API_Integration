import requests
from services.ai.base import BaseProvider
from core import settings

class OpenAIProvider(BaseProvider):
    """
    Implementasi cloud AI Provider menggunakan REST API OpenAI resmi.
    """
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        
    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("Kunci API 'OPENAI_API_KEY' belum diatur!")
            
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Gagal menghubungi OpenAI API: {e}")
