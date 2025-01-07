import pytest
import httpx
from fastapi import status

# ... (импортируйте ваше приложение FastAPI)

@pytest.mark.asyncio
async def test_create_master_route(test_client: httpx.AsyncClient, create_test_user, create_test_city):
    """Тест создания мастера."""

    user_data = await create_test_user(role="master")  # Создаем тестового пользователя с ролью мастера
    city_data = await create_test_city()
    city_slug = city_data.slug

    token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    master_data = {
        "title": "Test Master",
        "specialty": "Test Specialty",
        "description": "Test Description",
        "text": "Test Text",
        "experience_years": 5,
    }

    url = f"/cities/{city_slug}/masters"
    response = await test_client.post(url, json=master_data, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert "slug" in response_data
    assert response_data["title"] == master_data["title"]
    # ... другие проверки полей ...
    #проверка что в базе есть запись
    # master_in_db = await Master.get(slug = response_data["slug"])
    # assert master_in_db is not None

@pytest.fixture
async def create_test_user(db):
    async def _create_test_user(role: str):
        from use_case.utils.jwt_handler import create_access_token
        from db.models import User
        import uuid
        user = await User.create(
            id = uuid.uuid4(),
            email = f"{uuid.uuid4()}@mail.ru",
            hashed_password = "test",
            is_active = True,
            is_verified = True,
            role = role,
            city_id = 1901
        )
        access_token = create_access_token(data={"user_id": str(user.id), "role": user.role, "city_id": user.city_id})
        return {"access_token": access_token, "user_id": str(user.id)}
    return _create_test_user


@pytest.fixture
async def create_test_city(db):
    async def _create_test_city():
        from db.models import City
        import uuid
        city = await City.create(
            id = uuid.uuid4(),
            name = f"{uuid.uuid4()}",
            slug = f"{uuid.uuid4()}"
        )
        return city
    return _create_test_city