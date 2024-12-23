from pydantic import BaseModel, Field

# Схема для входа пользователя
class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=255, title="Имя пользователя", example="john_doe")
    password: str = Field(..., min_length=8, title="Пароль", example="securepassword123")

    class Config:
        orm_mode = True  # Поддержка объектов Tortoise ORM
