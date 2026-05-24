import re

from prompts import load_prompt_template, format_prompt
from services import get_ai_service


class IssueSeverityWorkflow:
    """Workflow untuk klasifikasi tingkat keparahan issue."""

    # Urutan severity eksplisit (priority highest -> lowest) agar fallback konsisten.
    ORDERED_SEVERITY = ("critical", "high", "medium", "low")

    @classmethod
    def execute(cls, text: str, request_id: str) -> str:
        template = load_prompt_template("issue/severity.txt")
        prompt = format_prompt(template, text=text)

        ai_service = get_ai_service()
        raw_output = ai_service.generate_summary(prompt)
        return cls._normalize_severity(raw_output)

    @classmethod
    def _normalize_severity(cls, value: str) -> str:
        first_line = (value or "").strip().splitlines()[0].lower() if (value or "").strip() else ""
        first_chunk = re.split(r"[,;]", first_line)[0].strip()
        token = re.sub(r"[^a-z]", "", first_chunk)

        if token in cls.ORDERED_SEVERITY:
            return token

        for level in cls.ORDERED_SEVERITY:
            if cls._contains_whole_token(first_line, level):
                return level

        return "medium"

    @staticmethod
    def _contains_whole_token(text: str, token: str) -> bool:
        # Boundary-aware scan mencegah partial overlap saat fallback matching.
        return re.search(rf"(?<![a-z0-9_]){re.escape(token)}(?![a-z0-9_])", text) is not None
