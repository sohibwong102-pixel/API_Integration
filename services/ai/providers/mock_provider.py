import os
from services.ai.base import BaseProvider

class MockProvider(BaseProvider):
    """
    Mock AI Provider untuk kebutuhan testing/development offline yang deterministik.

    Catatan arsitektur:
    - Provider ini sengaja TIDAK melakukan parsing struktur prompt internal.
    - Tujuannya mencegah drift saat template prompt berevolusi.
    """
    DEFAULT_FIXTURE_SUMMARY = (
        "Mock summary for testing: operational issue detected and requires backend investigation."
    )

    def generate(self, prompt: str) -> str:
        # Opsi override fixture via env untuk skenario test tertentu tanpa ubah kode.
        fixture = os.getenv("MOCK_SUMMARY_FIXTURE", self.DEFAULT_FIXTURE_SUMMARY).strip()

        # Fallback aman jika env diisi kosong/whitespace.
        if not fixture:
            return self.DEFAULT_FIXTURE_SUMMARY

        # Mengembalikan satu string summary deterministik (provider-agnostic terhadap format prompt).
        return fixture
