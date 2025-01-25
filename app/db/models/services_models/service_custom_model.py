#service_custom_model.py
from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel
from db.models.abstract.abstract_service import AbstractService

class CustomService(AbstractModel):
    """
    Модель пользовательской услуги (для мастеров и салонов)
    """
    # Связи с владельцем (только одна из них должна быть заполнена)
    master = fields.ForeignKeyField(
        'server.Master',
        related_name='services',
        null=True,
        on_delete=fields.CASCADE,
        help_text="Мастер, предоставляющий услугу"
    )
    salon = fields.ForeignKeyField(
        'server.Salon',
        related_name='services',
        null=True,
        on_delete=fields.CASCADE,
        help_text="Салон, предоставляющий услугу"
    )

    # Связь с базовой услугой
    standard_service = fields.ForeignKeyField(
        'server.StandardService',
        related_name='custom_services',
        on_delete=fields.CASCADE,
        help_text="Базовый шаблон услуги"
    )

    # Основная информация
    base_price = fields.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Базовая стоимость услуги"
    )
    duration_minutes = fields.IntField(
        help_text="Длительность услуги в минутах"
    )
    is_active = fields.BooleanField(
        default=True,
        help_text="Активна ли услуга"
    )

    # Дополнительная информация
    description = fields.TextField(
        null=True,
        help_text="Дополнительное описание услуги"
    )

    custom_service_photos: fields.ReverseRelation['CustomServicePhoto']

    class Meta:
        table = "custom_services"
        unique_together = [
            ["master", "standard_service"],
            ["salon", "standard_service"]
        ]


class CustomServiceAttribute(AbstractModel):
    """
    Выбранные атрибуты услуги с ценами
    """
    custom_service = fields.ForeignKeyField(
        'server.CustomService',
        related_name='attributes',
        on_delete=fields.CASCADE,
        help_text="Пользовательская услуга"
    )
    attribute_value = fields.ForeignKeyField(
        'server.ServiceAttributeValue',
        related_name='custom_attributes',
        on_delete=fields.CASCADE,
        help_text="Значение атрибута"
    )
    additional_price = fields.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Дополнительная стоимость за атрибут"
    )
    is_active = fields.BooleanField(
        default=True,
        help_text="Активен ли атрибут"
    )

    class Meta:
        table = "custom_service_attributes"
        unique_together = ("custom_service", "attribute_value")