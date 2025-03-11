from core.exceptions.base import ApplicationException


class BadRequestException(ApplicationException):
    """400 Bad Request"""
    def __init__(self, message: str, error_code: str = "BAD_REQUEST"):
        super().__init__(message=message, error_code=error_code, status_code=400)

class UnauthorizedException(ApplicationException):
    """401 Unauthorized"""
    def __init__(self, message: str = "Необходима авторизация", error_code: str = "UNAUTHORIZED"):
        super().__init__(message=message, error_code=error_code, status_code=401)

class ForbiddenException(ApplicationException):
    """403 Forbidden"""
    def __init__(self, message: str = "Доступ запрещен", error_code: str = "FORBIDDEN"):
        super().__init__(message=message, error_code=error_code, status_code=403)

class NotFoundException(ApplicationException):
    """404 Not Found"""
    def __init__(self, message: str = "Ресурс не найден", error_code: str = "NOT_FOUND"):
        super().__init__(message=message, error_code=error_code, status_code=404)