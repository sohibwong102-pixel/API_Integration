import re
from typing import List

from prompts import load_prompt_template, format_prompt
from services import get_ai_service


class IssueTagsWorkflow:
    """Workflow untuk menghasilkan daftar tag issue secara deterministik."""

    @classmethod
    def execute(cls, text: str, request_id: str) -> List[str]:
        template = load_prompt_template("issue/tags.txt")
        prompt = format_prompt(template, text=text)

        ai_service = get_ai_service()
        raw_output = ai_service.generate_summary(prompt)
        return cls._normalize_tags(raw_output)

    @staticmethod
    def _normalize_tags(value: str) -> List[str]:
        source = (value or "").strip().lower()
        if not source:
            return ["general"]

        parts = re.split(r"[,;\n]", source)
        tags: List[str] = []

        for part in parts:
            cleaned = part.strip().replace(" ", "_")
            cleaned = re.sub(r"[^a-z0-9_-]", "", cleaned)
            if not cleaned:
                continue
            if cleaned not in tags:
                tags.append(cleaned)
            if len(tags) >= 5:
                break

        return tags if tags else ["general"]
