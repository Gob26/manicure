from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.salon_models.salon_master_relation import SalonMasterRelation


# Создаем Pydantic-схему для связи между мастером и салоном
SalonMasterRelationCreateSchema = pydantic_model_creator(
    SalonMasterRelation,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужны при создании
    name="SalonMasterRelationCreateSchema"  # Имя схемы
)