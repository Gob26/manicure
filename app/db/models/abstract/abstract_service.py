from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel

# Абстрактная модель услуг
class AbstractService(AbstractModel):
    name = fields.CharField(max_length=255, help_text="Название услуги")
    slug = fields.CharField(max_length=255, null=True, help_text="Уникальный идентификатор для SEO-оптимизации")
    description = fields.TextField(null=True, help_text="Описание услуги")
    duration = fields.IntField(null=True, help_text="Длительность услуги в минутах")
    price = fields.DecimalField(max_digits=10, decimal_places=2, null=True, help_text="Цена услуги")
    is_active = fields.BooleanField(default=True, help_text="Активна ли услуга")

    class Meta:
        abstract = True

