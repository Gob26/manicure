from tortoise import fields
from db.models.services_models.service_custom_model import CustomService
from db.models.abstract.abstract_model import AbstractModel
from db.models.job.vacancy_salon import Vacancy
from db.models.salon_models.salon_master_relation import SalonMasterRelation
from db.models.salon_models.salon_master_invitation import SalonMasterInvitation

class Salon(AbstractModel):
    # Связь с городом
    city = fields.ForeignKeyField(
        "server.City",
        related_name="salons",
        on_delete=fields.SET_NULL,
        null=True,
        help_text="Город, в котором находится салон",
    )
    # Связь с пользователем
    user = fields.OneToOneField('server.User', related_name='salon', on_delete=fields.CASCADE)
    
    # Основная информация
    name = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255, null=False)  # Заголовок
    slug = fields.CharField(max_length=255, unique=False, null=False)
    
    # Информация о местоположении
    address = fields.CharField(max_length=255)  # Адрес
    
    # Поля с контентом
    description = fields.TextField(null=True)  # Описание
    text = fields.TextField(null=True)  # Текст
    
    # Связанные сущности
    services = fields.ReverseRelation["CustomService"]  # Связь с услугами
    relations = fields.ReverseRelation["SalonMasterRelation"]  # Связь с мастерами через SalonMasterRelation
    vacancies = fields.ReverseRelation["Vacancy"]  # Связь с вакансиями
    invitations = fields.ReverseRelation["SalonMasterInvitation"]  # Связь с приглашениями мастеров

    class Meta:
        table = "salon"