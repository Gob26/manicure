from tortoise import fields
from db.models.services_models.service_custom_model import CustomService
from db.models.abstract.abstract_model import AbstractModel
from db.models.job.job_application import JobApplication
from db.models.salon_models.salon_master_relation import SalonMasterRelation
from db.models.job.resume_salon import Resume
from db.models.photo_models.photo_model import Photo

# Модель мастера
class Master(AbstractModel):
    # Связь с городом
    city = fields.ForeignKeyField(
        "server.City",
        related_name="masters",
        on_delete=fields.SET_NULL,
        null=True,
        help_text="Город, в котором находится мастер",
    )
    
    # Связь с пользователем
    user = fields.OneToOneField('server.User', related_name='master', on_delete=fields.CASCADE)
    
    # Связь с аватаркой
    avatar = fields.ForeignKeyField(
        'server.Photo',
        related_name='master_avatar',
        on_delete=fields.SET_NULL,
        null=True,
        help_text="Аватар мастера"
    )
    
    title = fields.CharField(max_length=255, null=False)  # Заголовок, пока может быть null
    description = fields.TextField(null=True)  # Описание, пока может быть null
    text = fields.TextField(null=True)  # Текст, пока может быть null
    experience_years = fields.IntField()
    specialty = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255, unique=False, null=False)
    
    # Связь с услугами
    services = fields.ReverseRelation["CustomService"]
    # Связь с резюме
    resumes = fields.ReverseRelation["Resume"]
    # Связь с заявками
    applications = fields.ReverseRelation["JobApplication"]
    # Связь с салонами через отношение
    relations = fields.ReverseRelation["SalonMasterRelation"]

    class Meta:
        table = "master"
