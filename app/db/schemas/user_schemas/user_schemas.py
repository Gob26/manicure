from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    client = "client"
    master = "master"
    salon = "salon"

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    city_id: int  # ID города вместо имени
    role: UserRole

    class Config:
        from_attributes = True  # Позволяет Pydantic конвертировать данные из моделей Tortoise
