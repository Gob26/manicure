import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app  # точка входа FastAPI
from app.core.exceptions import UserAlreadyExistsError, InvalidCityError
from app.use_case.user.user_register import register_user


# Фикстура для клиента
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# Успешная регистрация пользователя
@pytest.mark.asyncio
async def test_register_success(client, mocker):
    mock_user = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "city_name": "Москва",
        "role": "client"
    }

    mocker.patch("app.use_case.user.user_register.register_user", return_value=mock_user)

    response = await client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "city_name": "Москва",
        "role": "client"
    })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "testuser"


# Ошибка: пользователь уже существует
@pytest.mark.asyncio
async def test_register_user_already_exists(client, mocker):
    mocker.patch("app.use_case.user.user_register.register_user", side_effect=UserAlreadyExistsError)

    response = await client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "city_name": "Москва",
        "role": "client"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Пользователь с таким email уже существует"


# Ошибка: город не найден
@pytest.mark.asyncio
async def test_register_invalid_city(client, mocker):
    mocker.patch("app.use_case.user.user_register.register_user", side_effect=InvalidCityError)

    response = await client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "city_name": "НеизвестныйГород",
        "role": "client"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Указанный город не найден"


# Ошибка целостности данных (например, дублирующий email)
@pytest.mark.asyncio
async def test_register_integrity_error(client, mocker):
    from tortoise.exceptions import IntegrityError
    mocker.patch("app.use_case.user.user_register.register_user", side_effect=IntegrityError)

    response = await client.post("/register", json={
        "username": "testuser",
        "email": "duplicate@example.com",
        "password": "password123",
        "city_name": "Москва",
        "role": "client"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Ошибка в данных пользователя"


# Непредвиденная ошибка сервера
@pytest.mark.asyncio
async def test_register_unexpected_error(client, mocker):
    mocker.patch("app.use_case.user.user_register.register_user", side_effect=Exception("Some internal error"))

    response = await client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "city_name": "Москва",
        "role": "client"
    })

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == "Ошибка при регистрации пользователя"
