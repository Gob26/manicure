from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.user.user import User  # Импортируй свою модель User

# Создаем Pydantic-схему на основе модели User
UserLoginSchema = pydantic_model_creator(
    User,
    include=("username", "password"),  # Указываем поля, которые хотим использовать
    name="UserLoginSchema"  # Задаем имя для Pydantic-схемы
)
