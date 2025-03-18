import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from pydantic import ValidationError

from api import cities_list_router  # Проверь, что импорт верный
from config.components.logging_config import logger
from core.redis import get_redis_client
from db.schemas.location_schema.city_schemas import CityOutAllSchema, FullCitySchema


# Создаем тестовое приложение и подключаем маршруты
@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(cities_list_router, prefix="/api/v1/cities_list")
    return app


@pytest.mark.asyncio
async def test_get_all_cities(test_app):
    # Тестируем отображение всех городов
    async with AsyncClient(
            transport=ASGITransport(app=test_app),
            base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/cities_list/all")
        assert response.status_code == 200

        cities_data = response.json()
        assert isinstance(cities_data, list)  # Проверяем, что вернулся список

        # Проверяем, что все объекты в списке соответствуют схеме CityOutAllSchema
        for city in cities_data:
            try:
                # Пытаемся преобразовать данные в схему
                CityOutAllSchema(**city)
            except ValidationError as e:
                # Логируем ошибку, если валидация не прошла
                logger.error(f"Ошибка валидации данных города: {city}, ошибка: {e}")
                assert False, f"Ошибка валидации данных города: {e}"

        logger.info(f"Статус: {response.status_code},")  # Логируем данные для проверки


@pytest.mark.asyncio
async def test_active_cities(test_app):
# Тестируем отображение активных городов
    async with AsyncClient(
            transport=ASGITransport(app=test_app),
            base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/cities_list/")
        assert response.status_code == 200

        cities_active_data = response.json()
        assert isinstance(cities_active_data,list)

        for city in cities_active_data:
            try:
                # Преобразовые данные в схему
                FullCitySchema(**city)
            except ValidationError as e:
                logger.error(f"Ошибка валидации данных города: {city}, ошибка: {e}")
                assert False, f"Ошибка валидации данных города: {e}"

        logger.info(f"Статус: {response.status_code}, Response: {cities_active_data}")  # Логируем данные для проверки
