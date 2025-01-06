from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel

class City(AbstractModel):
    name = fields.CharField(max_length=100, unique=True, index=True)
    district = fields.CharField(max_length=50)
    subject = fields.CharField(max_length=100)
    population = fields.IntField(index=True)
    latitude = fields.FloatField(index=True)
    longitude = fields.FloatField(index=True)
    slug = fields.CharField(max_length=255, unique=True, index=True)

    # Отношение к описанию города
    description = fields.ReverseRelation["CityDescription"]

    def __str__(self):
        return self.name

    class Meta:
        table = "cities"  
        indexes = [
            ("population",),
            ("latitude", "longitude"), # Индекс на координатах,
        ]

class CityDescription(AbstractModel):
    city = fields.OneToOneField("server.City", related_name="description", on_delete=fields.CASCADE)
    title = fields.CharField(max_length=255, null=True)  # Заголовок
    description = fields.TextField(null=True)  # Описание
    text = fields.TextField(null=True)  # Дополнительный текст

    class Meta:
        table = "city_descriptions"

"""КЛАСТИРЕЗАЦИЯ ПО НАСЕЛЕНИЮ будет полезна в дальнейшем"""