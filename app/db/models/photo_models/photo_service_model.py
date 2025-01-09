#photo_service_model.py
from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel

class ServicePhoto(AbstractModel):
    """
    Фотографии услуг
    """
    custom_service = fields.ForeignKeyField(
        'server.CustomService',
        related_name='photos',
        on_delete=fields.CASCADE,
        help_text="Услуга, к которой относится фото"
    )
    photo = fields.ForeignKeyField(
        'server.Photo',
        related_name='service_photos',
        on_delete=fields.CASCADE,
        help_text="Фотография услуги"
    )
    is_main = fields.BooleanField(
        default=False,
        help_text="Является ли фото главным"
    )
    order = fields.IntField(
        default=0,
        help_text="Порядок отображения фото"
    )

    class Meta:
        table = "service_photos"
        ordering = ["order"]