from tortoise import fields

from db.models.abstract.abstract_service import AbstractService

# Модель стандартных услуг
class StandardService(AbstractService):
    category = fields.ForeignKeyField(
        'server.Category',
        related_name='services',
        null=True,
        on_delete=fields.SET_NULL,
        help_text="Категория услуги."
    )

    class Meta:
        table = "standard_services"
        ordering = ["name"]  # Упорядочивание услуг по имени
