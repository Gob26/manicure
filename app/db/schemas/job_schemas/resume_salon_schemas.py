from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.job.resume_salon import Resume


# Создаем Pydantic-схему на основе модели Resume
ResumeCreateSchema = pydantic_model_creator(
    Resume,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужно создавать
    name="ResumeCreateSchema"  # Задаем имя для Pydantic-схемы
)
