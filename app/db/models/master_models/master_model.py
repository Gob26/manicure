from tortoise import fields, models

from db.models.abstract.abstract_model import AbstractModel
from db.models.job.job_application import JobApplication
from db.models.salon_models.salon_master_relation import SalonMasterRelation
from db.models.job.resume_salon import Resume


# Модель мастера
class Master(AbstractModel):
    user = fields.OneToOneField('server.User', related_name='master', on_delete=fields.CASCADE)
    title = fields.CharField(max_length=255, null=False)  # Заголовок, пока может быть null
    description = fields.TextField(null=True)  # Описание, пока может быть null
    text = fields.TextField(null=True)  # Текст, пока может быть null
    experience_years = fields.IntField()
    specialty = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255, unique=False, null=False)


    # Связь с резюме
    resumes = fields.ReverseRelation["Resume"]

    # Связь с заявками
    applications = fields.ReverseRelation["JobApplication"]

    # Связь с салонами через отношение
    relations = fields.ReverseRelation["SalonMasterRelation"]
   
    class Meta:
        table = "master"