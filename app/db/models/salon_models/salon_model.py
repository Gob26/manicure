from tortoise import fields

from app.db.models.services_model.service_custom_model import CustomService
from db.models.abstract.abstract_model import AbstractModel
from db.models.job.vacancy_salon import Vacancy
from db.models.salon_models.salon_master_relation import SalonMasterRelation
from db.models.salon_models.salon_master_invitation import SalonMasterInvitation

# Модель мастера
class Salon(AbstractModel):
    user = fields.OneToOneField("server.User", related_name='salon', on_delete=fields.CASCADE)
    title = fields.CharField(max_length=255, null=False)  # Заголовок, пока может быть null
    description = fields.TextField(null=True)  # Описание, пока может быть null
    name = fields.CharField(max_length=255)
    address = fields.CharField(max_length=255)
    text = fields.TextField(null=True)  # Текст, пока может быть null
    slug = fields.CharField(max_length=255, unique=False, null=False)

    # Связь услугами
    services = fields.ReverseRelation["CustomService"]  

    # Связь с мастерами через `SalonMasterRelation`
    relations = fields.ReverseRelation["SalonMasterRelation"]

    # Связь с вакансиями
    vacancies = fields.ReverseRelation["Vacancy"]

    # Связь с приглашениями мастеров
    invitations = fields.ReverseRelation["SalonMasterInvitation"]

    class Meta:
        table = "salon"
