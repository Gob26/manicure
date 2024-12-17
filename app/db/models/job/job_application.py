from tortoise import fields
from enum import Enum

from db.models.abstract.abstract_model import AbstractModel


class JobStatusEnum(Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

# Модель заявки
class JobApplication(AbstractModel):
    vacancy = fields.ForeignKeyField('server.Vacancy', related_name='applications', on_delete=fields.CASCADE)
    master = fields.ForeignKeyField('server.Master', related_name='applications', on_delete=fields.CASCADE)
    status = fields.CharEnumField(enum_type=JobStatusEnum, default=JobStatusEnum.pending)
    message = fields.TextField(null=True, help_text="Сообщение от мастера при отклике.")

    class Meta:
        table = "job_applications"