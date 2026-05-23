import logging
from typing import Any, Dict
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("app.errors")

"""
Centralized HTTP exception handlers.

Notes:
- `ValueError` handler below is intentionally mapped to `400 BAD_REQUEST` and
    is only intended for simple application-level validation/errors (lightweight
    business validation). This prevents noisy traceback leakage and keeps
    handler semantics predictable for clients.
- Future recommendation: replace generic `ValueError` usage across the app
    with a custom application exception (e.g. `AppError` or `BusinessValidationError`)
    so that error handling is explicit and cannot be accidentally misused.
"""

def _build_error_context(request: Request) -> Dict[str, Any]:
    # Structured context untuk observability 5xx agar root cause lebih mudah ditelusuri.
    return {
        "method": request.method,
        "path": request.url.path,
        "query": str(request.query_params),
        "client_host": request.client.host if request.client else None,
        "request_id": request.headers.get("x-request-id"),
    }

def register_error_handlers(app: FastAPI):
    """
    Mendaftarkan centralized exception handlers untuk menangkap error HTTP,
    validasi input, value error, dan error internal lainnya di satu pintu terpadu.
    """
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Memetakan status code ke kode error publik yang sesuai
        # Penambahan mapping explicit untuk membuat semantics error lebih akurat
        status_code = exc.status_code
        if status_code == status.HTTP_400_BAD_REQUEST:
            code = "BAD_REQUEST"
        elif status_code == status.HTTP_401_UNAUTHORIZED:
            code = "UNAUTHORIZED"
        elif status_code == status.HTTP_403_FORBIDDEN:
            code = "FORBIDDEN"
        elif status_code == status.HTTP_404_NOT_FOUND:
            code = "NOT_FOUND"
        elif status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            # 405 -> METHOD_NOT_ALLOWED (baru)
            code = "METHOD_NOT_ALLOWED"
        elif status_code == status.HTTP_408_REQUEST_TIMEOUT:
            # 408 -> REQUEST_TIMEOUT (baru)
            code = "REQUEST_TIMEOUT"
        elif status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            code = "VALIDATION_ERROR"
        elif status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            # 429 -> RATE_LIMITED (baru)
            code = "RATE_LIMITED"
        elif status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
            # 503 -> SERVICE_UNAVAILABLE (baru)
            code = "SERVICE_UNAVAILABLE"
        else:
            # Static fallback enum strategy (contract-stable):
            # - unknown 5xx -> INTERNAL_SERVER_ERROR
            # - unknown 4xx -> CLIENT_ERROR
            # - selain itu -> INTERNAL_SERVER_ERROR
            # Catatan:
            # Tidak menggunakan dynamic code `HTTP_<status_code>` agar consumer
            # tidak bergantung pada enum yang berubah-ubah.
            if 500 <= status_code < 600:
                code = "INTERNAL_SERVER_ERROR"
            elif 400 <= status_code < 500:
                code = "CLIENT_ERROR"
            else:
                code = "INTERNAL_SERVER_ERROR"

        # Untuk 5xx, detail exception asli tetap dicatat di internal log (tidak dikirim ke client).
        if status_code >= 500:
            logger.error(
                "http_exception_5xx",
                extra={
                    "event": "http_exception_5xx",
                    "status_code": status_code,
                    "exception_type": type(exc).__name__,
                    "exception_detail": repr(exc.detail),
                    "context": _build_error_context(request),
                },
            )
        else:
            logger.error(f"HTTP Exception [{status_code}]: {exc.detail}")

        # Sanitize message for 5xx to avoid leaking internal details to clients
        message = exc.detail if status_code < 500 else "Internal server error"

        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "error": {
                    "code": code,
                    "message": message
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Ekstraksi pesan error validasi agar readable oleh client
        errors = exc.errors()
        if errors:
            first_err = errors[0]
            loc = " -> ".join(str(l) for l in first_err.get("loc", []))
            msg = first_err.get("msg", "Validation error")
            message = f"Invalid request payload. Field [{loc}]: {msg}"
        else:
            message = "Invalid request payload."

        logger.error(f"Validation Error: {exc.errors()}")

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": message
                }
            }
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle `ValueError` thrown by business logic.

        Intention: map simple application validation errors to 400 so clients
        receive a clear `BAD_REQUEST` semantic. Avoid using this as a catch-all
        for unexpected failures — prefer raising a custom exception type for
        explicit application errors.
        """

        # ValueError dipetakan langsung sebagai BAD_REQUEST (400)
        # NOTE: This handler is for simple app-level validation only.
        # For more complex error semantics replace ValueError with a custom exception.
        logger.error(f"Business Validation/ValueError: {exc}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": {
                    "code": "BAD_REQUEST",
                    "message": str(exc)
                }
            }
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(request: Request, exc: Exception):
        # 5xx tak terduga: simpan traceback + context terstruktur untuk root cause analysis.
        logger.exception(
            "unexpected_exception_5xx",
            extra={
                "event": "unexpected_exception_5xx",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "context": _build_error_context(request),
            },
        )

        # Mengembalikan error generik tanpa membocorkan detail internal traceback ke client
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Internal server error"
                }
            }
        )
