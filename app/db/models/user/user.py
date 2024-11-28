from tortoise import fields
from enum import Enum

from db.models.abstract.abstract_model import AbstractModel

class UserRole(str, Enum):
    client = "client"
    master = "master"
    salon = "salon"

class User(AbstractModel):
    username = fields.CharField(max_length=100, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=128)
    city = fields.ForeignKeyField("server.City", null=True, on_delete=fields.SET_NULL)  # Установка SET_NULL через константу
    role = fields.CharEnumField(UserRole, default=UserRole.client)  # Используем CharEnumField
   
    class Meta:
        table = "users"  # Явное указание имени таблицы
