from abc import ABC, abstractmethod

class BaseAIService(ABC):
    """
    Base contract untuk layanan AI utama yang dipanggil oleh workflow.
    """
    @abstractmethod
    def generate_summary(self, prompt: str) -> str:
        """
        Menghasilkan teks ringkasan keluhan sistem.
        """
        pass

class BaseProvider(ABC):
    """
    Interface/kontrak bagi adapter penyedia AI (Provider).
    Setiap provider baru wajib mengimplementasikan interface ini.
    """
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Mengirim prompt ke model provider dan mengembalikan respon teks murni.
        """
        pass
