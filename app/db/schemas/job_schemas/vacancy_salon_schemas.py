from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.job.vacancy_salon import Vacancy


# Создаем Pydantic-схему на основе модели Vacancy
VacancyCreateSchema = pydantic_model_creator(
    Vacancy,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужно создавать
    name="VacancyCreateSchema"  # Задаем имя для Pydantic-схемы
)