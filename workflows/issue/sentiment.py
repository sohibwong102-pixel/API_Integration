import re

from prompts import load_prompt_template, format_prompt
from services import get_ai_service


class IssueSentimentWorkflow:
    """Workflow untuk klasifikasi sentimen issue reporter."""

    # Urutan sentimen eksplisit agar fallback normalization deterministic.
    ORDERED_SENTIMENT = ("frustrated", "concerned", "neutral", "positive")

    @classmethod
    def execute(cls, text: str, request_id: str) -> str:
        template = load_prompt_template("issue/sentiment.txt")
        prompt = format_prompt(template, text=text)

        ai_service = get_ai_service()
        raw_output = ai_service.generate_summary(prompt)
        return cls._normalize_sentiment(raw_output)

    @classmethod
    def _normalize_sentiment(cls, value: str) -> str:
        first_line = (value or "").strip().splitlines()[0].lower() if (value or "").strip() else ""
        first_chunk = re.split(r"[,;]", first_line)[0].strip()
        token = re.sub(r"[^a-z]", "", first_chunk)

        if token in cls.ORDERED_SENTIMENT:
            return token

        for sentiment in cls.ORDERED_SENTIMENT:
            if cls._contains_whole_token(first_line, sentiment):
                return sentiment

        return "neutral"

    @staticmethod
    def _contains_whole_token(text: str, token: str) -> bool:
        # Boundary-aware matching untuk mencegah accidental partial match.
        return re.search(rf"(?<![a-z0-9_]){re.escape(token)}(?![a-z0-9_])", text) is not None
