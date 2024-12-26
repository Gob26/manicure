from tortoise import fields
from db.models.abstract.abstract_service import AbstractService

# Модель стандартных услуг
class StandardService(AbstractService):
    """
    Модель для стандартных услуг
    """
 # Контент услуги
    category = fields.ForeignKeyField(
        'server.Category',
        related_name='services',
        null=True,
        on_delete=fields.SET_NULL,
        help_text="Категория услуги."
    )
    default_photo = fields.ForeignKeyField(
        'server.Photo',
        related_name='default_services',
        null=True,
        on_delete=fields.SET_NULL,
        help_text="Стандартное фото для услуги."
    )

    class Meta:
        table = "standard_services"
        ordering = ["name"]  # Упорядочивание услуг по имени
