from tortoise import fields
from pydantic import EmailStr
from enum import Enum

from db.models.abstract.abstract_model import AbstractModel

# Перечисление ролей
class UserRole(str, Enum):
    client = "client"
    master = "master"
    salon = "salon"

# Модель пользователя
class User(AbstractModel):
    username: str = fields.CharField(max_length=255, unique=True)
    email: EmailStr = fields.CharField(max_length=255, unique=True)
    password: str = fields.CharField(max_length=255)
    # Заменяем city_name на связь с моделью City
    city = fields.ForeignKeyField('server.City', related_name='users')
    role = fields.CharEnumField(UserRole, default=UserRole.client)

    class Meta:
        table = "users"