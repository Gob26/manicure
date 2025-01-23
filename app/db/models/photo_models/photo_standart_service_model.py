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
    custom_service: fields.ForeignKeyNullableRelation[CustomService] = fields.ForeignKeyField(
        'server.CustomService',
        related_name='custom_service_photos',    # Изменено related_name для удобства
        on_delete=fields.CASCADE,
        null=True
    )

    class Meta:
        table = "custom_service_photo"