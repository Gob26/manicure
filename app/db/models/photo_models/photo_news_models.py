from tortoise import fields

from db.models.abstract.abstract_photo import AbstractPhoto


class NewsPhoto(AbstractPhoto):
    """  
    Модель фотографий новостей с описанием  
    """
    description = fields.TextField(null=True)