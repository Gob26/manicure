from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.salon_models.salon_model import Salon


# Создаем Pydantic-схему для создания салона
SalonCreateSchema = pydantic_model_creator(
    Salon,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужны при создании
    name="SalonCreateSchema"  # Имя схемы
)