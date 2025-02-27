from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from config.components.logging_config import logger
from .base import ApplicationException
from ..errors.error_codes import get_error_details


async def application_exception_handler(request: Request, exc: ApplicationException):
    """Обработчик для всех кастомных исключений приложения"""
    error_details = get_error_details(exc.error_code)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": error_details["code"],
                "message": exc.message,
                "details": getattr(exc, "errors", None)
            }
        }
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    """Обработчик для ошибок валидации Pydantic"""
    errors = {}
    for error in exc.errors():
        location = ".".join(str(loc) for loc in error["loc"])
        errors[location] = error["msg"]

    error_details = get_error_details("VALIDATION_ERROR")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": error_details["code"],
                "message": "Ошибка валидации данных",
                "details": errors
            }
        }
    )


async def internal_server_error_handler(request: Request, exc: Exception):
    """Обработчик для всех непредвиденных исключений"""
    error_details = get_error_details("UNKNOWN_ERROR")

    logger.exception(f"Непредвиденная ошибка: {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": error_details["code"],
                "message": "Произошла внутренняя ошибка сервера"
            }
        }
    )