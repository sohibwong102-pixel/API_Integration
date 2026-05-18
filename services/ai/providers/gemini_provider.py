import requests
from services.ai.base import BaseProvider
from core import settings

class GeminiProvider(BaseProvider):
    """
    Implementasi cloud AI Provider menggunakan Google Gemini REST API resmi.
    """
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL
        
    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("Kunci API 'GEMINI_API_KEY' belum diatur!")
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            result = response.json()
            # Ekstraksi response text dari skema Google Gemini API
            return result["candidates"][0]["content"]["parts"][0]["text"].strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Gagal menghubungi Google Gemini API: {e}")
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Format respon Google Gemini API tidak sesuai: {e}")
