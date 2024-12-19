from tortoise import fields

from db.models.abstract.abstract_photo import AbstractPhoto

# Модель фотографий услуг
class ServicePhoto(AbstractPhoto):
    service = fields.ForeignKeyField(
        "server.CustomService",
        related_name="photos",
        on_delete=fields.CASCADE,
        help_text="Привязка фотографии к услуге"
    )

    class Meta:
        table = "service_photos"
