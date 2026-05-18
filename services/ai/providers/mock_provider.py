import re
from services.ai.base import BaseProvider

class MockProvider(BaseProvider):
    """
    Mock AI Provider untuk simulasi respons LLM saat masa development secara gratis & offline.
    """
    def generate(self, prompt: str) -> str:
        # Ekstraksi keluhan asli dari prompt menggunakan regex
        match = re.search(r"Issue Text:\s*(.*?)\n\nSummary:", prompt, re.DOTALL | re.IGNORECASE)
        
        if match:
            issue_text = match.group(1).strip().lower()
        else:
            issue_text = prompt.lower()
            
        # Keyword-matching logic untuk simulasi kecerdasan buatan
        if "auth" in issue_text or "middleware" in issue_text:
            return "Deployment issue related to auth middleware conflict."
            
        elif "db" in issue_text or "database" in issue_text or "koneksi" in issue_text:
            return "Database connection timeout preventing successful service startup."
            
        elif "gagal" in issue_text or "failed" in issue_text or "deploy" in issue_text:
            return "CI/CD deployment pipeline failure due to build environment setup."
            
        elif "api" in issue_text or "route" in issue_text or "endpoint" in issue_text:
            return "API gateway routing mismatch resulting in HTTP 404 errors."
            
        else:
            return f"Operational interruption detected in system workflow: '{issue_text[:30]}...'."
