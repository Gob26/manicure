from typing import Dict, Any, Optional
from core.exceptions.base import ApplicationException


class ValidationException(ApplicationException):
    """Ошибка валидации данных"""
    def __init__(
        self,
        message: str = "Ошибка валидации данных",
        error_code: str = "VALIDATION_ERROR",
        errors: Optional[Dict[str, Any]] = None
    ):
        self.errors = errors or {}
        super().__init__(message=message, error_code=error_code, status_code=422)