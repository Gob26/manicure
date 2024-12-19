from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.photo_models.service_photo_model import ServicePhoto

# Создаем Pydantic-схему для фотографий услуг
ServicePhotoCreateSchema = pydantic_model_creator(
    ServicePhoto,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужно передавать при создании
    name="ServicePhotoCreateSchema"  # Задаем имя для схемы
)
