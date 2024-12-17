from tortoise import fields
from enum import Enum
from db.models.abstract.abstract_model import AbstractModel

# Перечисление для статуса
class StatusEnum(str, Enum):
    active = "active"
    pending = "pending"
    inactive = "inactive"

# Перечисление для роли
class RoleEnum(str, Enum):
    employee = "employee"
    freelancer = "freelancer"

# Модель связи мастера и салонов
class SalonMasterRelation(AbstractModel):
    salon = fields.ForeignKeyField("server.Salon", on_delete=fields.CASCADE)
    master = fields.ForeignKeyField("server.Master", on_delete=fields.CASCADE)
    
    # Использование перечислений для статусов и ролей
    status = fields.CharEnumField(enum_type=StatusEnum, default=StatusEnum.pending)
    role = fields.CharEnumField(enum_type=RoleEnum, default=RoleEnum.employee)
    
    start_date = fields.DateField(null=True, help_text="Дата начала работы.")
    end_date = fields.DateField(null=True, help_text="Дата завершения работы.")
    notes = fields.TextField(null=True, help_text="Дополнительная информация.")

    class Meta:
        unique_together = ("salon", "master")  # Запретить дублирование связей
