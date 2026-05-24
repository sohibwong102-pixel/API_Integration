import re

from prompts import load_prompt_template, format_prompt
from services import get_ai_service


class IssueCategorizeWorkflow:
    """Workflow untuk klasifikasi kategori issue dengan output token deterministik."""

    # Urutan kategori dibuat eksplisit agar fallback scan deterministic antar runtime/process.
    ORDERED_CATEGORIES = (
        "authentication",
        "authorization",
        "security",
        "database",
        "deployment",
        "infrastructure",
        "network",
        "performance",
        "ui",
        "api",
        "other",
    )
    # Priority keyword map untuk fallback deterministic + overlap-safe matching.
    CATEGORY_KEYWORDS = (
        ("authentication", ("authentication", "auth", "login", "signin", "credential", "token")),
        ("authorization", ("authorization", "forbidden", "permission", "access_denied", "rbac")),
        ("security", ("security", "vulnerability", "xss", "csrf", "breach", "exploit")),
        ("database", ("database", "db", "sql", "postgres", "mysql", "query")),
        ("deployment", ("deployment", "deploy", "release", "rollback", "pipeline", "cicd")),
        ("infrastructure", ("infrastructure", "server", "kubernetes", "cluster", "node", "container")),
        ("network", ("network", "dns", "latency", "timeout", "connection", "gateway")),
        ("performance", ("performance", "slow", "throughput", "cpu", "memory", "latency")),
        ("ui", ("ui", "frontend", "button", "layout", "render", "screen")),
        ("api", ("api", "endpoint", "route", "rest", "graphql", "http")),
    )

    @classmethod
    def execute(cls, text: str, request_id: str) -> str:
        template = load_prompt_template("issue/categorize.txt")
        prompt = format_prompt(template, text=text)

        ai_service = get_ai_service()
        raw_output = ai_service.generate_summary(prompt)
        return cls._normalize_category(raw_output)

    @classmethod
    def _normalize_category(cls, value: str) -> str:
        first_line = (value or "").strip().splitlines()[0].lower() if (value or "").strip() else ""
        first_chunk = re.split(r"[,;]", first_line)[0].strip()
        token = re.sub(r"[^a-z_]", "", first_chunk)

        if token in cls.ORDERED_CATEGORIES:
            return token

        for category, keywords in cls.CATEGORY_KEYWORDS:
            if any(cls._contains_whole_token(first_line, keyword) for keyword in keywords):
                return category

        return "other"

    @staticmethod
    def _contains_whole_token(text: str, token: str) -> bool:
        # Boundary-aware matching untuk menghindari partial collision antar keyword.
        return re.search(rf"(?<![a-z0-9_]){re.escape(token)}(?![a-z0-9_])", text) is not None
