from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.job.job_application import JobApplication


JobApplicationCreateSchema = pydantic_model_creator(
    JobApplication,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужно создавать
    name="JobApplicationCreateSchema"  # Задаем имя для Pydantic-схемы
)