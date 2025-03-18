import pytest
from fastapi import FastAPI, status, HTTPException, UploadFile, File, Form, Depends
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from typing import Optional
from pydantic import ValidationError
from pydantic.networks import HttpUrl

from api import salon_router
from db.models import AvatarPhotoSalon
from db.schemas.salon_schemas.salon_schemas import SalonCreateSchema, SalonCreateInputSchema, SalonUpdateSchema

from use_case.utils.jwt_handler import get_current_user  # Import the original dependency


# Подготовка тестового приложения FastAPI
app = FastAPI()
app.include_router(salon_router)


def mock_get_current_user_dependency():
    """Mock dependency to bypass authentication for tests."""
    return {"user_id": 1, "city_id": 1, "permissions": ["salon"], "role": "salon"} #  Добавлен ключ "role": "salon"

app.dependency_overrides[get_current_user] = mock_get_current_user_dependency


client = TestClient(app)


# --- Тесты для POST / (create_salon_route) ---

def test_create_salon_success():
    """Тест успешного создания салона"""
    mock_salon_data = SalonCreateSchema(
        id=1,
        user_id=1,
        city_id=1,
        name='Тестовый салон',
        title='Тестовый тайтл',
        slug='test-salon',
        address='Тестовый адрес',
        phone='+79991234567',
        description='Описание тестового салона',
        avatar_id=1,
    )

    def mock_create_salon(**kwargs):
        """Mock для create_salon."""
        return {"id": 1, "user_id": 1, "city_id": 1, "name": 'Тестовый салон', 'title': 'Тестовый тайтл',
                'slug': 'test-salon', 'address': 'Тестовый адрес', 'phone': '+79991234567',
                'description': 'Описание тестового салона', 'avatar_id': 1}
        return mock_salon_data

    async def mock_add_photos_to_salon(**kwargs):
        return [1]

    with patch("use_case.salon_service.salon_service.SalonService.create_salon", new_callable=AsyncMock, side_effect=mock_create_salon) as mock_create, \
         patch("use_case.photo_service.photo_base_servise.PhotoHandler.add_photos_to_salon", new_callable=AsyncMock, side_effect=mock_add_photos_to_salon) as mock_add_photo, \
         patch("use_case.utils.permissions.check_user_permission") as mock_check_permission:

        response = client.post(
            "/",
            files={"image": ("test_image.png", b"file content", "image/png")},
            data={
                "name": "Тестовый салон",
                "title": "Тестовый тайтл",
                "address": "Тестовый адрес",
                "phone": "+79991234567",
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['name'] == 'Тестовый салон'
        mock_create.assert_called_once()
        mock_add_photo.assert_called_once()
        mock_check_permission.assert_called_once()


def test_create_salon_validation_error():
    """Тест ошибки валидации при создании салона"""
    with patch("use_case.utils.permissions.check_user_permission"):
        response = client.post(
            "/",
            files={"image": ("test_image.png", b"file content", "image/png")},
            data={
                "name": "", # Empty name - validation error
                "title": "Тестовый тайтл",
                "address": "Тестовый адрес",
                "phone": "+79991234567",
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "value_error" in response.json()['detail']


def test_create_salon_permission_denied():
    """Тест отказа в доступе при создании салона"""
    with patch("use_case.utils.permissions.check_user_permission") as mock_check_permission:
        response = client.post(
            "/",
            files={"image": ("test_image.png", b"file content", "image/png")},
            data={
                "name": "Тестовый салон",
                "title": "Тестовый тайтл",
                "address": "Тестовый адрес",
                "phone": "+79991234567",
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        mock_check_permission.assert_called_once()


def test_create_salon_service_error():
    """Тест ошибки сервисного слоя при создании салона"""
    async def mock_create_salon(**kwargs):
        raise Exception("Service error")

    with patch("use_case.salon_service.salon_service.SalonService.create_salon", new_callable=AsyncMock, side_effect=mock_create_salon) as mock_create, \
         patch("use_case.utils.permissions.check_user_permission"):

        response = client.post(
            "/",
            files={"image": ("test_image.png", b"file content", "image/png")},
            data={
                "name": "Тестовый салон",
                "title": "Тестовый тайтл",
                "address": "Тестовый адрес",
                "phone": "+79991234567",
            }
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_create.assert_called_once()


# --- Тесты для PUT /{salon_id} (update_salon_route) ---

def test_update_salon_success():
    """Тест успешного обновления салона"""
    mock_salon_data = SalonUpdateSchema(
        name='Обновленный салон',
        title='Обновленный тайтл',
        slug='updated-salon',
        address='Обновленный адрес',
        phone='+79997654321',
        description='Обновленное описание',
    )
    async def mock_get_salon_by_id(salon_id: int):
        return SalonCreateSchema(id=salon_id, user_id=1, city_id=1, name='Старый салон', title='Старый тайтл', slug='old-salon', address='Старый адрес', phone='+79991234567', description='Старое описание', avatar_id=1)

    async def mock_update_salon(**kwargs):
        return SalonCreateSchema(id=1, user_id=1, city_id=1, name='Обновленный салон', title='Обновленный тайтл', slug='updated-salon', address='Обновленный адрес', phone='+79997654321', description='Обновленное описание', avatar_id=2)

    async def mock_add_photos_to_salon(**kwargs):
        return [2]
    async def mock_get_photo_by_id(**kwargs):
        return AvatarPhotoSalon(id=1, salon_id=1, photo_url="old_url")
    async def mock_delete_photo(**kwargs):
        return None


    with patch("use_case.salon_service.salon_service.SalonService.get_salon_by_id", new_callable=AsyncMock, side_effect=mock_get_salon_by_id) as mock_get_salon, \
         patch("use_case.salon_service.salon_service.SalonService.update_salon", new_callable=AsyncMock, side_effect=mock_update_salon) as mock_update, \
         patch("use_case.photo_service.photo_base_servise.PhotoHandler.add_photos_to_salon", new_callable=AsyncMock, side_effect=mock_add_photos_to_salon) as mock_add_photo, \
         patch("use_case.photo_service.photo_base_servise.PhotoHandler.get_photo_by_id", new_callable=AsyncMock, side_effect=mock_get_photo_by_id) as mock_get_photo, \
         patch("use_case.photo_service.photo_base_servise.PhotoHandler.delete_photo", new_callable=AsyncMock, side_effect=mock_delete_photo) as mock_delete_photo, \
         patch("use_case.utils.permissions.check_user_permission") as mock_check_permission:

        response = client.put(
            "/1",
            files={"image": ("updated_image.png", b"updated file content", "image/png")},
            data={
                "name": "Обновленный салон",
                "title": "Обновленный тайтл",
                "address": "Обновленный адрес",
                "phone": "+79997654321",
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['name'] == 'Обновленный салон'
        mock_get_salon.assert_called_once_with(1)
        mock_update.assert_called_once()
        mock_add_photo.assert_called_once()
        mock_get_photo.assert_called_once()
        mock_delete_photo.assert_called_once()
        mock_check_permission.assert_called_once()


def test_update_salon_not_found():
    """Тест не найден салон при обновлении"""
    async def mock_get_salon_by_id(salon_id: int):
        return None

    with patch("use_case.salon_service.salon_service.SalonService.get_salon_by_id", new_callable=AsyncMock, side_effect=mock_get_salon_by_id) as mock_get_salon, \
         patch("use_case.utils.permissions.check_user_permission"):

        response = client.put(
            "/999", # Non-existent salon_id
            files={"image": ("updated_image.png", b"updated file content", "image/png")},
            data={
                "name": "Обновленный салон",
                "title": "Обновленный тайтл",
                "address": "Обновленный адрес",
                "phone": "+79997654321",
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        mock_get_salon.assert_called_once_with(999)


def test_update_salon_permission_denied():
    """Тест отказа в доступе при обновлении салона"""
    async def mock_get_salon_by_id(salon_id: int):
        return SalonCreateSchema(id=salon_id, user_id=2, city_id=1, name='Чужой салон', title='Чужой тайтл', slug='other-salon', address='Чужой адрес', phone='+79991112233', description='Чужое описание', avatar_id=1) # Different user_id

    with patch("use_case.salon_service.salon_service.SalonService.get_salon_by_id", new_callable=AsyncMock, side_effect=mock_get_salon_by_id) as mock_get_salon, \
         patch("use_case.utils.permissions.check_user_permission"):

        response = client.put(
            "/1",
            files={"image": ("updated_image.png", b"updated file content", "image/png")},
            data={
                "name": "Обновленный салон",
                "title": "Обновленный тайтл",
                "address": "Обновленный адрес",
                "phone": "+79997654321",
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        mock_get_salon.assert_called_once_with(1)


def test_update_salon_validation_error():
    """Тест ошибки валидации при обновлении салона"""
    async def mock_get_salon_by_id(salon_id: int):
        return SalonCreateSchema(id=salon_id, user_id=1, city_id=1, name='Старый салон', title='Старый тайтл', slug='old-salon', address='Старый адрес', phone='+79991234567', description='Старое описание', avatar_id=1)

    with patch("use_case.salon_service.salon_service.SalonService.get_salon_by_id", new_callable=AsyncMock, side_effect=mock_get_salon_by_id) as mock_get_salon, \
         patch("use_case.utils.permissions.check_user_permission"):

        response = client.put(
            "/1",
            files={"image": ("updated_image.png", b"updated file content", "image/png")},
            data={
                "name": "", # Empty name - validation error
                "title": "Обновленный тайтл",
                "address": "Обновленный адрес",
                "phone": "+79997654321",
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "value_error" in response.json()['detail']
        mock_get_salon.assert_called_once_with(1)


def test_update_salon_service_error():
    """Тест ошибки сервисного слоя при обновлении салона"""
    async def mock_get_salon_by_id(salon_id: int):
        return SalonCreateSchema(id=salon_id, user_id=1, city_id=1, name='Старый салон', title='Старый тайтл', slug='old-salon', address='Старый адрес', phone='+79991234567', description='Старое описание', avatar_id=1)
    async def mock_update_salon(**kwargs):
        raise Exception("Service error")

    with patch("use_case.salon_service.salon_service.SalonService.get_salon_by_id", new_callable=AsyncMock, side_effect=mock_get_salon_by_id) as mock_get_salon, \
         patch("use_case.salon_service.salon_service.SalonService.update_salon", new_callable=AsyncMock, side_effect=mock_update_salon) as mock_update, \
         patch("use_case.utils.permissions.check_user_permission"):

        response = client.put(
            "/1",
            files={"image": ("updated_image.png", b"updated file content", "image/png")},
            data={
                "name": "Обновленный салон",
                "title": "Обновленный тайтл",
                "address": "Обновленный адрес",
                "phone": "+79997654321",
            }
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_get_salon.assert_called_once_with(1)
        mock_update.assert_called_once()


# --- Тесты для DELETE /{salon_id} (delete_salon_route) ---

def test_delete_salon_success():
    """Тест успешного удаления салона"""
    async def mock_get_salon_by_id(salon_id: int):
        return SalonCreateSchema(id=salon_id, user_id=1, city_id=1, name='Тестовый салон', title='Тестовый тайтл', slug='test-salon', address='Тестовый адрес', phone='+79991234567', description='Описание тестового салона', avatar_id=1)
    async def mock_delete_salon(**kwargs):
        return None

    with patch("use_case.salon_service.salon_service.SalonService.get_salon_by_id", new_callable=AsyncMock, side_effect=mock_get_salon_by_id) as mock_get_salon, \
         patch("use_case.salon_service.salon_service.SalonService.delete_salon", new_callable=AsyncMock, side_effect=mock_delete_salon) as mock_delete, \
         patch("use_case.utils.permissions.check_user_permission") as mock_check_permission:

        response = client.delete("/1")
        assert response.status_code == status.HTTP_200_OK
        mock_get_salon.assert_called_once_with(1)
        mock_delete.assert_called_once()
        mock_check_permission.assert_called_once()


def test_delete_salon_not_found():
    """Тест не найден салон при удалении"""
    async def mock_get_salon_by_id(salon_id: int):
        return None

    with patch("use_case.salon_service.salon_service.SalonService.get_salon_by_id", new_callable=AsyncMock, side_effect=mock_get_salon_by_id) as mock_get_salon, \
         patch("use_case.utils.permissions.check_user_permission"):

        response = client.delete("/999") # Non-existent salon_id
        assert response.status_code == status.HTTP_404_NOT_FOUND
        mock_get_salon.assert_called_once_with(999)


def test_delete_salon_permission_denied():
    """Тест отказа в доступе при удалении салона"""
    async def mock_get_salon_by_id(salon_id: int):
        return SalonCreateSchema(id=salon_id, user_id=2, city_id=1, name='Чужой салон', title='Чужой тайтл', slug='other-salon', address='Чужой адрес', phone='+79991112233', description='Чужое описание', avatar_id=1) # Different user_id

    with patch("use_case.salon_service.salon_service.SalonService.get_salon_by_id", new_callable=AsyncMock, side_effect=mock_get_salon_by_id) as mock_get_salon, \
         patch("use_case.utils.permissions.check_user_permission"):

        response = client.delete("/1")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        mock_get_salon.assert_called_once_with(1)


def test_delete_salon_service_error():
    """Тест ошибки сервисного слоя при удалении салона"""
    async def mock_get_salon_by_id(salon_id: int):
        return SalonCreateSchema(id=salon_id, user_id=1, city_id=1, name='Тестовый салон', title='Тестовый тайтл', slug='test-salon', address='Тестовый адрес', phone='+79991234567', description='Описание тестового салона', avatar_id=1)
    async def mock_delete_salon(**kwargs):
        raise Exception("Service error")

    with patch("use_case.salon_service.salon_service.SalonService.get_salon_by_id", new_callable=AsyncMock, side_effect=mock_get_salon_by_id) as mock_get_salon, \
         patch("use_case.salon_service.salon_service.SalonService.delete_salon", new_callable=AsyncMock, side_effect=mock_delete_salon) as mock_delete, \
         patch("use_case.utils.permissions.check_user_permission"):

        response = client.delete("/1")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_get_salon.assert_called_once_with(1)
        mock_delete.assert_called_once()