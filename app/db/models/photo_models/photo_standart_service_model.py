from db.models import CustomService
from db.models.abstract.abstract_photo import AbstractPhoto
from tortoise import fields


class StandardServicePhoto(AbstractPhoto):
    """
    Фотографии стандартных услуг
    """
    class Meta:
        table = "standard_service_photo"

class CustomServicePhoto(AbstractPhoto):
    """
    Фотографии для пользовательских услуг
    """
    custom_service = fields.ForeignKeyField(
        'server.CustomService',  # Связь с кастомной услугой
        related_name='custom_service_photos',    # Обратная связь, чтобы получить все фотографии для услуги
        on_delete=fields.CASCADE,  # Удаление фотографий при удалении услуги
        null=True  # Фотографии теперь могут быть необязательными
    )

    class Meta:
        table = "custom_service_photo"