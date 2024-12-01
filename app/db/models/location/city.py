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

    class Meta:
        table = "cities"
