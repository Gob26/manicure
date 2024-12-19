from tortoise import fields

from db.models.abstract.abstract_service import AbstractService
from db.models.photo_models.service_photo_model import ServicePhoto

# Модель индивидуальных услуг
class CustomService(AbstractService):
    user = fields.ForeignKeyField(
        "server.User",
        related_name="custom_services",
        on_delete=fields.CASCADE,
        help_text="Пользователь, добавивший услугу (мастер или салон)"
    )
    photo = fields.ReverseRelation["ServicePhoto"]
    is_active = fields.BooleanField(default=True, help_text="Активна ли услуга?")  # Новое поле

    standard_service = fields.ForeignKeyField(
        "server.StandardService",
        related_name="custom_services",
        null=True,
        on_delete=fields.SET_NULL,
        help_text="Связь с базовой услугой, если используется стандартная"
    )

    class Meta:
        table = "custom_services"
