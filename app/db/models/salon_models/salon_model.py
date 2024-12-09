from tortoise import fields

from db.models.abstract.abstract_model import AbstractModel

# Модель мастера
class Salon(AbstractModel):
    user = fields.OneToOneField("server.User", related_name='master', on_delete=fields.CASCADE)
    title = fields.CharField(max_length=255, null=False)  # Заголовок, пока может быть null
    description = fields.TextField(null=True)  # Описание, пока может быть null
    name = fields.CharField(max_length=255)
    address = fields.CharField(max_length=255)
    text = fields.TextField(null=True)  # Текст, пока может быть null
    slug = fields.CharField(max_length=255, unique=False, null=False)

    class Meta:
        table = "salon"
