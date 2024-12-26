# Модель услуг мастера
from dataclasses import fields
from db.models.abstract.abstract_service import AbstractService


class MasterService(AbstractService):
    """
    Услуги, которые оказывает мастер, основанные на стандартных услугах.
    """
    master_id = fields.IntField(help_text="ID мастера, оказывающего услугу.")  # ID мастера
    standard_service = fields.ForeignKeyField(
        'server.StandardService',
        related_name='master_services',
        on_delete=fields.CASCADE,
        help_text="Стандартная услуга, на которой основана услуга мастера."
    )
    price = fields.DecimalField(max_digits=10, decimal_places=2, help_text="Стоимость услуги мастера.")  # Цена
    duration = fields.IntField(help_text="Длительность услуги в минутах.")  # Длительность
    description = fields.TextField(null=True, help_text="Индивидуальное описание услуги мастера.")  # Описание мастера
    is_active = fields.BooleanField(default=True, help_text="Активна ли услуга")
    
    class Meta:
        table = "master_services"
        unique_together = ("master_id", "standard_service")  # Мастер не может дублировать услуги
