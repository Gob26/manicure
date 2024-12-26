from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel

# Абстрактная модель услуг
class AbstractService(AbstractModel):
    name = fields.CharField(max_length=255, null=False, help_text="Название услуги.")  # Название услуги
    title = fields.CharField(max_length=255, null=True, help_text="Тайтл для SEO.")  # Тайтл для SEO
    description = fields.TextField(null=True, help_text="Описание для поисковиков.")  # SEO описание
    content = fields.TextField(null=True, help_text="Текстовое содержание, добавляемое администратором.") 
    slug = fields.CharField(max_length=255, null=True, help_text="Уникальный идентификатор для SEO-оптимизации")


    class Meta:
        abstract = True

