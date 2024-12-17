from enum import Enum
from tortoise import fields

from db.models.abstract.abstract_model import AbstractModel
from db.models.job.job_application import JobApplication

class VacancyStatusEnum(Enum):
    open = "open"
    closed = "closed"

class Vacancy(AbstractModel):
    title = fields.CharField(max_length=255, null=False)
    position = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=True)
    salon = fields.ForeignKeyField('server.Salon', related_name='vacancies', on_delete=fields.CASCADE)
    status = fields.CharEnumField(VacancyStatusEnum, default=VacancyStatusEnum.open)

    # Связь с заявками
    applications = fields.ReverseRelation["JobApplication"]

    class Meta:
        table = "vacancies"
