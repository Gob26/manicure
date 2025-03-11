# Коды ошибок для всего приложения
ERROR_CODES = {
    # Общие ошибки (1000-1999)
    "UNKNOWN_ERROR": {"code": "1000", "message": "Неизвестная ошибка"},
    "VALIDATION_ERROR": {"code": "1001", "message": "Ошибка валидации данных"},
    "AUTHENTICATION_ERROR": {"code": "1002", "message": "Ошибка аутентификации"},

    # Ошибки репозитория (2000-2999)
    "REPOSITORY_ERROR": {"code": "2000", "message": "Ошибка доступа к данным"},
    "DB_CONNECTION_ERROR": {"code": "2001", "message": "Ошибка подключения к базе данных"},
    "ENTITY_NOT_FOUND": {"code": "2002", "message": "Сущность не найдена"},

    # Ошибки сервисного слоя (3000-3999)
    "SERVICE_ERROR": {"code": "3000", "message": "Ошибка бизнес-логики"},
    "BUSINESS_RULE_VIOLATION": {"code": "3001", "message": "Нарушение бизнес-правила"},
    "RESOURCE_NOT_FOUND": {"code": "3002", "message": "Ресурс не найден"},

    # Ошибки API слоя (4000-4999)
    "BAD_REQUEST": {"code": "4000", "message": "Некорректный запрос"},
    "UNAUTHORIZED": {"code": "4001", "message": "Необходима авторизация"},
    "FORBIDDEN": {"code": "4002", "message": "Доступ запрещен"},
    "NOT_FOUND": {"code": "4003", "message": "Ресурс не найден"},

    # Ошибки, специфичные для конкретных модулей (5000+)
    # Модуль салонов (5000-5099)
    "SALON_NOT_FOUND": {"code": "5000", "message": "Салон не найден"},
    "SALON_INACTIVE": {"code": "5001", "message": "Салон не активен"},
}


def get_error_details(error_code: str):
    """Получить детали ошибки по коду"""
    return ERROR_CODES.get(error_code, ERROR_CODES["UNKNOWN_ERROR"])