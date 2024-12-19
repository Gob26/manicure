from tortoise import fields

from db.models.abstract.abstract_model import AbstractModel
from db.models.services_models.service_standart_model import StandardService

# Модель категории услуг
class Category(AbstractModel):
    name = fields.CharField(max_length=255, unique=True, help_text="Название категории.")
    slug = fields.CharField(max_length=255, unique=True, help_text="Слаг для SEO.")
    description = fields.TextField(null=True, help_text="Описание категории.")
    services = fields.ReverseRelation["StandardService"]

    class Meta:
        table = "categories"
        ordering = ["name"]
