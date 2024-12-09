#слой для работы с мастерами
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.master_models.master_model import Master


# Создаем Pydantic-схему для создания мастера
MasterCreateSchema = pydantic_model_creator(
    Master,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужно передавать при создании
    name="MasterCreateSchema"  # Задаем имя для схемы
)

# Создаем Pydantic-схему для обновления мастера
MasterUpdateSchema = pydantic_model_creator(
    Master,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужно обновлять
    name="MasterUpdateSchema"  # Задаем имя для схемы
)

# Создаем Pydantic-схему для получения списка мастеров
MasterListSchema = pydantic_model_creator(Master, exclude=("password",), name="MasterListSchema")       

# Создаем Pydantic-схему для получения мастера по ID
MasterGetSchema = pydantic_model_creator(Master, exclude=("password",), name="MasterGetSchema")

# Удаление мастера  
MasterDeleteSchema = pydantic_model_creator(Master, name="MasterDeleteSchema")  
