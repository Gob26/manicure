from core.exceptions.base import ApplicationException


class ServiceException(ApplicationException):
    """Базовое исключение для всех ошибок сервисного слоя"""
    def __init__(self, message: str, error_code: str = "SERVICE_ERROR", status_code: int = 500):
        super().__init__(message=message, error_code=error_code, status_code=status_code)

class BusinessRuleException(ServiceException):
    """Исключение при нарушении бизнес-правил"""
    def __init__(self, message: str, error_code: str = "BUSINESS_RULE_VIOLATION"):
        super().__init__(message=message, error_code=error_code, status_code=400)

class ResourceNotFoundException(ServiceException):
    """Исключение при отсутствии бизнес-ресурса"""
    def __init__(self, resource_type: str, identifier: str, error_code: str = "RESOURCE_NOT_FOUND"):
        message = f"{resource_type} с идентификатором {identifier} не найден"
        super().__init__(message=message, error_code=error_code, status_code=404)