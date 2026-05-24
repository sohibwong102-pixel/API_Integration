from prompts import load_prompt_template, format_prompt
from services import get_ai_service
from storage import LocalStorage


class IssueSummaryWorkflow:
    """Workflow ringkas untuk menghasilkan summary issue dan menyimpan history."""

    @classmethod
    def execute(cls, text: str, request_id: str) -> str:
        template = load_prompt_template("issue/summary.txt")
        prompt = format_prompt(template, text=text)

        ai_service = get_ai_service()
        raw_output = ai_service.generate_summary(prompt)
        summary = cls._normalize_summary(raw_output)

        LocalStorage.save_record(original_text=text, summary=summary, request_id=request_id)
        return summary

    @staticmethod
    def _normalize_summary(value: str) -> str:
        # Menjaga output tetap satu string ringkas dan aman untuk response contract.
        cleaned = " ".join((value or "").strip().split())
        return cleaned if cleaned else "not enough information"
