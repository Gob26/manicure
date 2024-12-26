from tortoise import fields

from db.models.abstract.abstract_model import AbstractModel

# Модель связи услуги с мастером или салоном
class ServiceRelation(AbstractModel):
    user = fields.ForeignKeyField(
        'server.User',
        related_name='service_relations',
        on_delete=fields.CASCADE,
        help_text="Пользователь, предлагающий услугу (мастер или салон)."
    )
    service = fields.ForeignKeyField(
        'server.StandardService',
        related_name='service_relations',
        null=True,
        help_text="Стандартная услуга."
    )
    custom_service = fields.ForeignKeyField(
        'server.CustomService',
        related_name='relations',
        null=True,
        help_text="Индивидуальная услуга, если есть."
    )
    price = fields.DecimalField(max_digits=10, decimal_places=2, help_text="Цена услуги.")
    duration = fields.IntField(help_text="Длительность услуги в минутах.")
    description = fields.TextField(null=True, help_text="Описание услуги.")
    is_active = fields.BooleanField(default=True, help_text="Активна ли услуга?")  # Новое поле

    class Meta:
        table = "service_relations"

