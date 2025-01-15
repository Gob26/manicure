from enum import Enum
from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel
from typing import Optional


class AbstractPhoto(AbstractModel):
    """
    Абстрактная модель для фотографий
    """
    file_name = fields.CharField(max_length=255)
    file_path = fields.CharField(max_length=1000)
    mime_type = fields.CharField(max_length=100)
    size = fields.IntField()
    width = fields.IntField(null=True)
    height = fields.IntField(null=True)
    is_main = fields.BooleanField(default=False)
    sort_order = fields.IntField(default=0)

    class Meta:
        abstract = True
