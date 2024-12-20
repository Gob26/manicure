from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel

class City(AbstractModel):
    name = fields.CharField(max_length=100, unique=True)
    district = fields.CharField(max_length=50)
    subject = fields.CharField(max_length=100)
    population = fields.IntField()
    latitude = fields.FloatField()  # Географические координаты города
    longitude = fields.FloatField()
    slug = fields.CharField(max_length=255, unique=True, null=True)

    class Meta:
        table = "cities"

class CityDescription(AbstractModel):
    city = fields.OneToOneField("server.City", related_name="description", on_delete=fields.CASCADE)
    title = fields.CharField(max_length=255, null=True)  # Заголовок
    description = fields.TextField(null=True)  # Описание
    text = fields.TextField(null=True)  # Дополнительный текст

    class Meta:
        table = "city_descriptions"