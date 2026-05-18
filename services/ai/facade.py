from services.ai.base import BaseAIService
from services.ai.router import AIRouter

class AIFacade(BaseAIService):
    """
    Facade sebagai entri point tunggal yang menyembunyikan kompleksitas multi-provider bagi workflow.
    Menjamin workflow hanya memanggil satu metode terpadu.
    """
    def __init__(self):
        self.router = AIRouter()

    def generate_summary(self, prompt: str) -> str:
        """
        Memenuhi kontrak generate_summary untuk workflow dengan mendelegasikan ke router.
        """
        response = self.router.route_request(prompt)
        # Mengembalikan string teks yang ternormalisasi
        return response.text
