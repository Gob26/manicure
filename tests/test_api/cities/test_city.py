import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from api import city_router  # Проверьте правильность импорта

# Создаем тестовое приложение и подключаем маршруты
@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(city_router, prefix="/api/v1/cities")
    return app

@pytest.mark.asyncio
async def test_get_city_by_slug_success(test_app):
    """
    Тест для проверки успешного получения города по slug.
    """
    city_slug = "omsk"

    # Выполняем запрос через AsyncClient
    async with AsyncClient(
            transport=ASGITransport(app=test_app),
            base_url="http://test"
    ) as ac:
        response = await ac.get(f"/api/v1/cities/{city_slug}")

    # Проверяем, что статус ответа 200 OK
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Проверяем, что в ответе есть нужное поле slug
    city_data = response.json()
    assert "slug" in city_data.get("city", {}), "Response does not contain the expected 'slug' field"
    assert city_data["city"]["slug"] == city_slug, f"Expected slug '{city_slug}', but got '{city_data['city']['slug']}'"

@pytest.mark.asyncio
async def test_get_city_by_slug_not_found(test_app):
    """
    Тест для проверки случая, когда город не найден.
    """
    city_slug = "nonexistent-city"

    async with AsyncClient(
            transport=ASGITransport(app=test_app),
            base_url="http://test"
    ) as ac:
        response = await ac.get(f"/api/v1/cities/{city_slug}")

    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
