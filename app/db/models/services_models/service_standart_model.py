from tortoise import fields
from db.models.abstract.abstract_service import AbstractService

# Модель стандартных услуг
class StandardService(AbstractService):
    category = fields.CharField(max_length=255, null=True, help_text="Категория услуги (например, Маникюр, Педикюр)")
    
    class Meta:
        table = "standard_services"
        ordering = ["name"]  # Упорядочивание услуг по имени
