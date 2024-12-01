from tortoise import fields
from pydantic import EmailStr, BaseModel, validator, Field

from enum import Enum
from db.models.abstract.abstract_model import AbstractModel


class UserRole(str, Enum):
    client = "client"
    master = "master"
    salon = "salon"

class User(AbstractModel):
    username: str = fields.CharField(max_length=255, unique=True)
    email: EmailStr = fields.CharField(max_length=255, unique=True)
    password: str = fields.CharField(max_length=255)
    city_name: str = fields.CharField(max_length=255)
    role = fields.CharEnumField(UserRole, default=UserRole.client) 

    class Meta:
        table = "users"  # Явное указание имени таблицы
