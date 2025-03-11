# tests/test_mail.py
import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from use_case.utils.email_services.send_jwt_email import send_confirmation_email


@pytest.mark.asyncio
async def test_send_confirmation_email_success():
    with patch('smtplib.SMTP_SSL') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        await send_confirmation_email(
            "profservis26@yandex.ru",
            "1234567890abcdef1234567890abcdef"
        )

        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()


@pytest.mark.asyncio
async def test_send_confirmation_email_invalid_email():
    with pytest.raises(ValueError, match="Невалидный email адрес"):
        await send_confirmation_email(
            "invalid-email",
            "1234567890abcdef1234567890abcdef"
        )


@pytest.mark.asyncio
async def test_send_confirmation_email_invalid_token():
    with pytest.raises(ValueError, match="Невалидный токен подтверждения"):
        await send_confirmation_email(
            "test@example.com",
            "short-token"
        )


@pytest.mark.asyncio
async def test_send_confirmation_email_smtp_error():
    with patch('smtplib.SMTP_SSL') as mock_smtp:
        mock_server = MagicMock()
        mock_server.sendmail.side_effect = Exception("SMTP Error")
        mock_smtp.return_value.__enter__.return_value = mock_server

        with pytest.raises(HTTPException) as exc_info:
            await send_confirmation_email(
                "test@example.com",
                "1234567890abcdef1234567890abcdef"
            )

        assert exc_info.value.status_code == 500
        assert "Не удалось отправить email" in str(exc_info.value.detail)