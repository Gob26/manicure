from tortoise import fields

from db.models.abstract.abstract_service import AbstractService
from db.models.services_models.service_standart_model import StandardService

# Модель категории услуг
class Category(AbstractService):
    services = fields.ReverseRelation["StandardService"]

    class Meta:
        table = "categories"
        ordering = ["name"]
