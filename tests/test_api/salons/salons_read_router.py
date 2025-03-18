import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch

from api import salon_detail_by_slug_router
from core.exceptions.http import NotFoundException, BadRequestException
from core.exceptions.service import ResourceNotFoundException, BusinessRuleException
from db.schemas.salon_schemas.salon_schemas import SalonDetailsSchema


# Создаем тестовое приложение FastAPI
app = FastAPI()
app.include_router(salon_detail_by_slug_router)

client = TestClient(app)


def test_get_salon_by_slug_success():
    """Тест успешного получения салона по slug"""
    test_salon_data = {
        'id': 1,
        'user_id': 1,
        'name': 'Тестовый салон',
        'title': 'Тестовый тайтл',
        'slug': 'test-salon',
        'address': 'Тестовый адрес',
        'phone': '+79991234567',
        'telegram': None,
        'whatsapp': None,
        'website': None,
        'vk': None,
        'instagram': None,
        'avatar_urls': None,
        'description': 'Описание тестового салона',
        'text': None
    }
    with patch("use_case.salon_service.salon_read_service.SalonReadService.get_salon_by_slug", return_value=test_salon_data) as mock_service:
        response = client.get("/test-salon")
        assert response.status_code == 200
        assert response.json() == test_salon_data
        mock_service.assert_called_once_with("test-salon")


def test_get_salon_by_slug_unexpected_exception():
    """Тест обработки непредвиденной ошибки"""
    with patch("use_case.salon_service.salon_read_service.SalonReadService.get_salon_by_slug", side_effect=Exception("Непредвиденная ошибка")) as mock_service:
        response = client.get("/test-any-salon")
        assert response.status_code == 500
        assert response.json() == {"detail": "Системная ошибка при получении информации о салоне"}
        mock_service.assert_called_once_with("test-any-salon")