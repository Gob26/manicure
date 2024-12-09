from tortoise import fields, models

from db.models.abstract.abstract_model import AbstractModel

# Модель мастера
class Master(AbstractModel):
    user = fields.OneToOneField('server.User', related_name='salon', on_delete=fields.CASCADE)
    title = fields.CharField(max_length=255, null=False)  # Заголовок, пока может быть null
    description = fields.TextField(null=True)  # Описание, пока может быть null
    text = fields.TextField(null=True)  # Текст, пока может быть null
    experience_years = fields.IntField()
    specialty = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255, unique=False, null=False)

    class Meta:
        table = "master"