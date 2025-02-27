from core.exceptions.base import ApplicationException


class RepositoryException(ApplicationException):
    """Базовое исключение для всех ошибок репозитория"""
    def __init__(self, message: str, error_code: str = "REPOSITORY_ERROR", status_code: int = 500):
        super().__init__(message=message, error_code=error_code, status_code=status_code)

class DatabaseConnectionException(RepositoryException):
    """Исключение при проблемах с подключением к БД"""
    def __init__(self, message: str = "Ошибка подключения к базе данных", error_code: str = "DB_CONNECTION_ERROR"):
        super().__init__(message=message, error_code=error_code)

class EntityNotFoundException(RepositoryException):
    """Исключение при отсутствии сущности в БД"""
    def __init__(self, entity_name: str, identifier: str, error_code: str = "ENTITY_NOT_FOUND"):
        message = f"{entity_name} с идентификатором {identifier} не найден"
        super().__init__(message=message, error_code=error_code, status_code=404)