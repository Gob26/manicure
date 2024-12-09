from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.location.city import City


# Создаем Pydantic-схему на основе модели City
CityCreateSchema = pydantic_model_creator(
    City,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужно создавать
    name="CityCreateSchema"  # Задаем имя для Pydantic-схемы
)
