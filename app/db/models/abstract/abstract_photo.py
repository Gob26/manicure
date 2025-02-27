from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel
from typing import Optional


class AbstractPhoto(AbstractModel):
    """
    Абстрактная модель для фотографий
    Поддерживает разные версии одного изображения (pc, phone, tablet)
    """
    file_name = fields.CharField(max_length=255, null=True, default="default_name.jpg")  # Имя файла по умолчанию
    file_path = fields.CharField(max_length=1000)
    mime_type = fields.CharField(max_length=100, null=True)
    size = fields.IntField()
    width = fields.IntField(null=True)
    height = fields.IntField(null=True)
    is_main = fields.BooleanField(default=False)
    sort_order = fields.IntField(default=0)
    version = fields.CharField(max_length=50, default="pc")  # Добавляем поле для версии изображения

    class Meta:
        abstract = True