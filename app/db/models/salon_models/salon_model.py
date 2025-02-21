from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel


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
    title = fields.CharField(max_length=255, null=False) 
    slug = fields.CharField(max_length=255, unique=True, null=True)
    description = fields.TextField(null=True)  
    text = fields.TextField(null=True) 

    # Контактная информация
    address = fields.CharField(max_length=255)  # Адрес
    phone = fields.CharField(max_length=20, null=False, help_text="Телефон мастера")  # Телефон
    telegram = fields.CharField(max_length=255, null=True, help_text="Ссылка на Telegram")  # Telegram
    whatsapp = fields.CharField(max_length=255, null=True, help_text="Ссылка на WhatsApp")  # WhatsApp
    website = fields.CharField(max_length=255, null=True, help_text="Веб-сайт мастера")  # Веб-сайт
    vk = fields.CharField(max_length=255, null=True, help_text="Ссылка на VK")  # ВКонтакте
    instagram = fields.CharField(max_length=255, null=True, help_text="Ссылка на Instagram")  # Instagram    
    # Связь с аватаркой
    avatar = fields.ForeignKeyField(
        'server.AvatarPhotoSalon',
        related_name='salon',
        on_delete=fields.SET_NULL,
        null=True,
        help_text="Аватар салона"
    )

    
    # Связанные сущности
    services = fields.ReverseRelation["CustomService"]  # Связь с услугами
    relations = fields.ReverseRelation["SalonMasterRelation"]  # Связь с мастерами через SalonMasterRelation
    vacancies = fields.ReverseRelation["Vacancy"]  # Связь с вакансиями
    invitations = fields.ReverseRelation["SalonMasterInvitation"]  # Связь с приглашениями мастеров

    class Meta:
        table = "salon"