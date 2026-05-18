from typing import Any, Optional

class AIResponse:
    """
    Model representasi data respon terpadu (normalized response).
    Semua response dari berbagai provider harus dikonversi ke format ini sebelum dikembalikan.
    """
    def __init__(self, text: str, provider: str, raw_response: Optional[Any] = None):
        self.text = text.strip()
        self.provider = provider
        self.raw_response = raw_response

    def __str__(self) -> str:
        return self.text
