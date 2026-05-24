from typing import List, Optional

from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field, field_validator

from storage import LocalStorage
from workflows import (
    IssueSummaryWorkflow,
    IssueCategorizeWorkflow,
    IssueSeverityWorkflow,
    IssueTagsWorkflow,
    IssueSentimentWorkflow,
)

router = APIRouter()


class IssueRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Issue text from client.",
        examples=["backend deploy failed after middleware update"],
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Text input cannot be empty.")
        return cleaned


class SummaryResponse(BaseModel):
    summary: str


class LegacySummaryResponse(BaseModel):
    summary: str
    request_id: str


class CategoryResponse(BaseModel):
    category: str


class SeverityResponse(BaseModel):
    severity: str


class TagsResponse(BaseModel):
    tags: List[str]


class SentimentResponse(BaseModel):
    sentiment: str


class HistoryRecordResponse(BaseModel):
    id: int = Field(..., description="Auto-increment local record id")
    request_id: Optional[str] = Field(None, description="Unique request id")
    timestamp: str = Field(..., description="Record creation time in ISO format")
    original_text: str = Field(..., description="Original issue text")
    summary: str = Field(..., description="Stored issue summary")


def _resolve_request_id(request: Request) -> str:
    request_id = getattr(request.state, "request_id", None)
    if not request_id:
        # Safety guard untuk memastikan lifecycle tidak pernah kosong.
        raise RuntimeError("Request context missing request_id")
    return request_id


def _execute_issue_summary(text: str, request_id: str) -> tuple[str, str]:
    summary = IssueSummaryWorkflow.execute(text, request_id=request_id)
    return summary, request_id


@router.post(
    "/issue-summary",
    response_model=LegacySummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Legacy alias - summarize issue",
)
def summarize_issue_legacy(payload: IssueRequest, request: Request):
    # Compatibility adapter: menjaga contract lama agar client existing tidak break.
    request_id = _resolve_request_id(request)
    summary, request_id = _execute_issue_summary(payload.text, request_id=request_id)
    return LegacySummaryResponse(summary=summary, request_id=request_id)


@router.post(
    "/issue/summary",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Summarize issue",
)
def summarize_issue(payload: IssueRequest, request: Request):
    request_id = _resolve_request_id(request)
    summary, _request_id = _execute_issue_summary(payload.text, request_id=request_id)
    return SummaryResponse(summary=summary)


@router.post(
    "/issue/categorize",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Categorize issue",
)
def categorize_issue(payload: IssueRequest, request: Request):
    request_id = _resolve_request_id(request)
    category = IssueCategorizeWorkflow.execute(payload.text, request_id=request_id)
    return CategoryResponse(category=category)


@router.post(
    "/issue/severity",
    response_model=SeverityResponse,
    status_code=status.HTTP_200_OK,
    summary="Classify issue severity",
)
def severity_issue(payload: IssueRequest, request: Request):
    request_id = _resolve_request_id(request)
    severity = IssueSeverityWorkflow.execute(payload.text, request_id=request_id)
    return SeverityResponse(severity=severity)


@router.post(
    "/issue/tags",
    response_model=TagsResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract issue tags",
)
def tags_issue(payload: IssueRequest, request: Request):
    request_id = _resolve_request_id(request)
    tags = IssueTagsWorkflow.execute(payload.text, request_id=request_id)
    return TagsResponse(tags=tags)


@router.post(
    "/issue/sentiment",
    response_model=SentimentResponse,
    status_code=status.HTTP_200_OK,
    summary="Classify issue sentiment",
)
def sentiment_issue(payload: IssueRequest, request: Request):
    request_id = _resolve_request_id(request)
    sentiment = IssueSentimentWorkflow.execute(payload.text, request_id=request_id)
    return SentimentResponse(sentiment=sentiment)


@router.get(
    "/history",
    response_model=List[HistoryRecordResponse],
    status_code=status.HTTP_200_OK,
    summary="Get issue summary history",
)
def get_issue_history():
    return LocalStorage.get_all_records()
