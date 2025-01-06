from pydantic import BaseModel, EmailStr, Field
from enum import Enum


# Перечисление ролей
class UserRole(str, Enum):
    client = "client"
    master = "master"
    salon = "salon"
    amin = "admin"

# Схема для отображения пользователя
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    city_id: int = Field(..., title="ID города", example=1)
    role: UserRole = Field(..., title="Роль пользователя", example=UserRole.client.value)

    class Config:
        from_attributes = True  # Поддержка объектов Tortoise ORM

# Схема для создания нового пользователя
class UserCreateSchema(BaseModel):
    username: str = Field(..., max_length=255, title="Имя пользователя", example="john_doe")
    email: EmailStr = Field(..., title="Электронная почта", example="john@example.com")
    password: str = Field(..., min_length=8, title="Пароль", example="securepassword123")
    city_id: int = Field(..., title="ID города", example=1)
    role: UserRole = Field(default=UserRole.client, title="Роль пользователя", example=UserRole.client.value)
