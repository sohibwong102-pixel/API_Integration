from typing import Dict, Type
from services.ai.base import BaseProvider
from services.ai.providers import (
    MockProvider,
    OllamaProvider,
    OpenAIProvider,
    GeminiProvider,
    OpenRouterProvider
)

# Registry mapping pencocokan nama provider di config/env dengan class implementasinya
PROVIDER_REGISTRY: Dict[str, Type[BaseProvider]] = {
    "mock": MockProvider,
    "local_ollama": OllamaProvider,
    "openai": OpenAIProvider,
    "google_gemini": GeminiProvider,
    "openrouter": OpenRouterProvider,
}

def get_provider(name: str) -> BaseProvider:
    """
    Mengambil dan menginstansiasi adapter provider berdasarkan nama.
    
    Args:
        name (str): Nama provider (misal: 'local_ollama', 'mock', etc.)
        
    Returns:
        BaseProvider: Instansi adapter yang mewarisi BaseProvider.
    """
    provider_class = PROVIDER_REGISTRY.get(name)
    if not provider_class:
        available = ", ".join(PROVIDER_REGISTRY.keys())
        raise ValueError(f"Provider '{name}' tidak dikenal. Pilihan yang tersedia: {available}")
    return provider_class()
