import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
from config.components.logging_config import logger
from config.envs.development import Settings
import re
from typing import Optional
from config.components.logging_config import logger


settings = Settings()


def is_valid_email(email: str) -> bool:
    """Проверка валидности email адреса."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


async def send_confirmation_email(
        user_email: str,
        confirmation_token: str,
        base_url: Optional[str] = None
) -> None:
    """
    Отправка email для подтверждения.

    Args:
        user_email: Email адрес получателя
        confirmation_token: Токен для подтверждения
        base_url: Базовый URL для ссылки подтверждения

    Raises:
        HTTPException: При ошибке отправки или невалидных данных
        ValueError: При невалидном email или токене
    """
    if not is_valid_email(user_email):
        raise ValueError("Невалидный email адрес")

    if not confirmation_token or len(confirmation_token) < 32:
        raise ValueError("Невалидный токен подтверждения")

    sender_email = settings.SENDER_EMAIL
    password = settings.SENDER_PASSWORD
    base_url = base_url or settings.BASE_URL

    subject = "Подтверждение email"
    confirmation_url = f"{base_url}/api/v1/auth/confirm-email?token={confirmation_token}"
    body = f"Перейдите по следующей ссылке для подтверждения вашего email: \n{confirmation_url}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Логируем значения sender_email и password перед server.login
        logger.debug(f"Отправка email: Используется sender_email: '{sender_email}'")
        logger.debug(f"Отправка email: Используется password: '{password}' (обратите внимание, пароль может быть замаскирован в логах)")


        # В реальном приложении здесь стоит использовать асинхронный SMTP клиент
        with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server: # <---  Изменено на smtp.mail.ru
            server.login(sender_email, password)
            server.sendmail(sender_email, user_email, message.as_string())
        logger.info(f"Email подтверждения успешно отправлен на {user_email}")
    except Exception as e:
        logger.error(f"Ошибка при отправке email: {e}")
        raise HTTPException(status_code=500, detail="Не удалось отправить email")