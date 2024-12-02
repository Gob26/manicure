import pytest
from unittest import mock
from unittest.mock import AsyncMock
from tortoise import Tortoise
from fastapi import HTTPException
from db.models.user.user import User
from app.use_case.user.user_login import login

# Инициализация базы данных для тестов
@pytest.fixture(scope="module", autouse=True)
async def setup_tortoise():
    await Tortoise.init(
        db_url="sqlite://:memory:",  # Используем SQLite в памяти для тестирования
        modules={"models": ["db.models.user.user"]}  # Укажите путь к вашим моделям
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

# Мокирование User.get
@pytest.fixture
def mock_get_user_by_username():
    with mock.patch("db.models.user.user.User.get", new_callable=AsyncMock) as mock_get:
        yield mock_get

# Мокирование проверки пароля
@pytest.fixture
def mock_verify_password():
    with mock.patch("app.use_case.user.user_login.verify_password", return_value=True) as mock_verify:
        yield mock_verify

# Мокирование логирования
@pytest.fixture
def mock_logger():
    with mock.patch("app.use_case.user.user_login.logger.info") as mock_log:
        yield mock_log

@pytest.mark.asyncio
async def test_successful_login(mock_get_user_by_username, mock_verify_password, mock_logger):
    # Настроим мок для возврата объекта User
    mock_get_user_by_username.return_value = User(username="gob26", password="hashed_password")
    mock_verify_password.return_value = True

    # Вызов функции логина
    user = await login("gob26", "03071986")

    # Проверка логирования
    mock_logger.assert_any_call("Попытка логина для пользователя gob26")
    mock_logger.assert_any_call("Пользователь gob26 найден, проверка пароля.")
    mock_logger.assert_any_call("Пользователь gob26 успешно авторизован")

    # Проверка успешного логина
    assert user.username == "gob26"
