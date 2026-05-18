# =====================================================================
# SYSTEM COMPONENT: AI SERVICE LAYER (LAPISAN LAYANAN AI - COMPATIBILITY INTERFACE)
# =====================================================================
# Deskripsi:
# Berkas ini bertindak sebagai gerbang kompatibilitas (backward compatibility) 
# bagi layer workflow/API lama agar tetap bisa menggunakan get_ai_service()
# tanpa mengetahui bahwa di bawahnya arsitektur sudah bermigrasi ke modular AI Router.
# =====================================================================

from services.ai.base import BaseAIService
from services.ai.facade import AIFacade

# Ekspos BaseAIService agar class eksternal/workflow tetap bisa melakukan type hinting
__all__ = ["BaseAIService", "get_ai_service"]

def get_ai_service() -> BaseAIService:
    """
    Fungsi Pabrik (Factory) lama yang kini mengembalikan instansi AIFacade terpadu.
    Menerapkan prinsip Loose Coupling secara penuh.
    
    Returns:
        BaseAIService: Objek AIFacade yang mematuhi kontrak BaseAIService.
    """
    return AIFacade()
