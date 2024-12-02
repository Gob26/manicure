import pytest
from app.use_case.user.user_login import login
from db.repositories.user_repositories.user_login import get_user_by_username, verify_password
from db.models.user.user import User
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_successful_login(mock_get_user_by_username, mock_verify_password, mock_logger):
    mock_get_user_by_username.return_value = User(username="gob26", password="hashed_password")
    mock_verify_password.return_value = True

    user = await login("gob26", "03071986")

    # Проверяем, что логирование произошло
    mock_logger.assert_any_call("Попытка логина для пользователя gob26")
    mock_logger.assert_any_call("Пользователь gob26 найден, проверка пароля.")
    mock_logger.assert_any_call("Пользователь gob26 успешно авторизован")
