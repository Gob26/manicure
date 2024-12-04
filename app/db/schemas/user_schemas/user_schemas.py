from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.user.user import User
# Создаем Pydantic-схему для User
UserSchema = pydantic_model_creator(User, name="User", exclude=("id",))  # Исключаем id
