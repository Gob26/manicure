from tortoise import fields

import typing
if typing.TYPE_CHECKING:
    from db.models import AvatarPhotoMaster
from db.models.abstract.abstract_model import AbstractModel

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
    images: fields.ReverseRelation["AvatarPhotoMaster"]
    
    # Основная информация
    title = fields.CharField(max_length=255, null=False)  # Заголовок
    description = fields.TextField(null=True)  # Краткое описание
    text = fields.TextField(null=True)  # Подробное описание
    experience_years = fields.IntField()  # Стаж в годах
    specialty = fields.CharField(max_length=255, null=False)  # Специализация
    slug = fields.CharField(max_length=255, unique=True, null=False)  # Ссылка
    
    # Контактная информация
    name = fields.CharField(max_length=257, null=False, help_text="Имя мастера")  # Имя мастера
    address = fields.CharField(max_length=255, null=False, help_text="Адрес мастера")  # Адрес
    phone = fields.CharField(max_length=20, null=False, help_text="Телефон мастера")  # Телефон
    telegram = fields.CharField(max_length=255, null=True, help_text="Ссылка на Telegram")  # Telegram
    whatsapp = fields.CharField(max_length=255, null=True, help_text="Ссылка на WhatsApp")  # WhatsApp
    website = fields.CharField(max_length=255, null=True, help_text="Веб-сайт мастера")  # Веб-сайт
    vk = fields.CharField(max_length=255, null=True, help_text="Ссылка на VK")  # ВКонтакте
    instagram = fields.CharField(max_length=255, null=True, help_text="Ссылка на Instagram")  # Instagram
    
    # Место приема
    accepts_at_home = fields.BooleanField(default=False, help_text="Прием у себя")  # У себя
    accepts_in_salon = fields.BooleanField(default=False, help_text="Прием в салоне")  # В салоне
    accepts_offsite = fields.BooleanField(default=False, help_text="Выезд к клиенту")  # Выезд
    
    # Связи
    services = fields.ReverseRelation["CustomService"]  # Услуги мастера
    resumes = fields.ReverseRelation["Resume"]  # Резюме мастера
    applications = fields.ReverseRelation["JobApplication"]  # Заявки мастера

    class Meta:
        table = "master"
