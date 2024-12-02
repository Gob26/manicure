from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel

class City(AbstractModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    district = fields.CharField(max_length=50)
    subject = fields.CharField(max_length=100)
    population = fields.IntField()
    latitude = fields.FloatField()  # Если будет использоваться геокодирование, подумайте о пределах значений.
    longitude = fields.FloatField()
    title = fields.CharField(max_length=255, null=True)  # Заголовок, пока может быть null
    description = fields.TextField(null=True)  # Описание, пока может быть null
    text = fields.TextField(null=True)  # Текст, пока может быть null

    class Meta:
        table = "cities"
