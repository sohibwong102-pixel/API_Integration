import os
import logging
from services.ai.registry import get_provider
from services.ai.models import AIResponse

logger = logging.getLogger(__name__)

class AIRouter:
    """
    Router yang bertanggung jawab atas penentuan rute provider dan penanganan failover (fallback).
    """
    def __init__(self):
        # Membaca primary provider dari env: prioritas ke PRIMARY_PROVIDER, lalu AI_PROVIDER, default mock
        self.primary_name = os.getenv("PRIMARY_PROVIDER") or os.getenv("AI_PROVIDER") or "mock"
        
        # Membaca fallback provider dari env
        self.fallback_name = os.getenv("FALLBACK_PROVIDER") or "mock"
        
        # Membaca flag penentu apakah fallback diaktifkan
        enable_fallback_str = os.getenv("ENABLE_FALLBACK", "true").lower()
        self.enable_fallback = enable_fallback_str in ("true", "1", "yes", "on")

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
