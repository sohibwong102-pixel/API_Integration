import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("app.errors")

def register_error_handlers(app: FastAPI):
    """
    Mendaftarkan centralized exception handlers untuk menangkap error HTTP,
    validasi input, value error, dan error internal lainnya di satu pintu terpadu.
    """
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Memetakan status code ke kode error publik yang sesuai
        status_code = exc.status_code
        if status_code == status.HTTP_400_BAD_REQUEST:
            code = "BAD_REQUEST"
        elif status_code == status.HTTP_401_UNAUTHORIZED:
            code = "UNAUTHORIZED"
        elif status_code == status.HTTP_403_FORBIDDEN:
            code = "FORBIDDEN"
        elif status_code == status.HTTP_404_NOT_FOUND:
            code = "NOT_FOUND"
        elif status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            code = "VALIDATION_ERROR"
        else:
            code = "INTERNAL_SERVER_ERROR"

        logger.error(f"HTTP Exception [{status_code}]: {exc.detail}")
        
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "error": {
                    "code": code,
                    "message": exc.detail
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
        # ValueError dipetakan langsung sebagai BAD_REQUEST (400)
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
        # Logging internal lengkap beserta traceback
        logger.exception("Unexpected system error occurred:")

        # Mengembalikan error generik tanpa membocorkan detail internal traceback ke client
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected server error occurred."
                }
            }
        )
