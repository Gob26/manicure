from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.master_models.master_model import Master


# Создаем Pydantic-схему для создания мастера
MasterCreateSchema = pydantic_model_creator(
    Master,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужно передавать при создании
    name="MasterCreateSchema"  # Задаем имя для схемы
)

# Схема для обновления мастера
MasterUpdateSchema = pydantic_model_creator(
    Master,
    exclude=("created_at", "updated_at", "id"),  # Исключаем поля, которые не обновляются напрямую
    name="MasterUpdateSchema",
    optional=("title", "description", "text", "experience_years", "specialty", "city", "slug", "user"),  # Делаем все поля необязательными
)
