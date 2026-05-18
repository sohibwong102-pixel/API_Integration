import logging
from services.ai.registry import get_provider
from services.ai.models import AIResponse
from core import settings

logger = logging.getLogger(__name__)

class AIRouter:
    """
    Router yang bertanggung jawab atas penentuan rute provider dan penanganan failover (fallback).
    """
    def __init__(self):
        # Menggunakan shared settings object dari core config
        self.primary_name = settings.PRIMARY_PROVIDER
        self.fallback_name = settings.FALLBACK_PROVIDER
        self.enable_fallback = settings.ENABLE_FALLBACK

    def route_request(self, prompt: str) -> AIResponse:
        """
        Mengarahkan request prompt ke provider yang sesuai berdasarkan konfigurasi dan menangani failover.
        """
        # 1. Percobaan Pertama: Kirim ke Primary Provider
        try:
            logger.info(f"Routing request ke Primary Provider: {self.primary_name}")
            provider = get_provider(self.primary_name)
            response_text = provider.generate(prompt)
            return AIResponse(text=response_text, provider=self.primary_name)
            
        except Exception as primary_err:
            logger.error(f"Gagal memproses dengan Primary Provider '{self.primary_name}': {primary_err}")
            
            # 2. Rencana Cadangan: Failover ke Fallback Provider jika diaktifkan
            if self.enable_fallback and self.primary_name != self.fallback_name:
                try:
                    logger.warning(f"Mengaktifkan auto-failover ke Fallback Provider: {self.fallback_name}")
                    fallback_provider = get_provider(self.fallback_name)
                    response_text = fallback_provider.generate(prompt)
                    return AIResponse(text=response_text, provider=self.fallback_name)
                    
                except Exception as fallback_err:
                    logger.error(f"Failover gagal menggunakan Fallback Provider '{self.fallback_name}': {fallback_err}")
                    raise RuntimeError(
                        f"Semua provider gagal. Primary ({self.primary_name}) error: {primary_err}. "
                        f"Fallback ({self.fallback_name}) error: {fallback_err}"
                    )
            else:
                # Jika fallback dinonaktifkan atau primary sama dengan fallback
                raise RuntimeError(
                    f"Gagal memproses dengan Primary Provider '{self.primary_name}' dan fallback dinonaktifkan/tidak tersedia. "
                    f"Error: {primary_err}"
                )
