# app/db/models/location/city.py
from tortoise import fields, models

class City(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    district = fields.CharField(max_length=50)
    subject = fields.CharField(max_length=100)
    population = fields.IntField()
    latitude = fields.FloatField()
    longitude = fields.FloatField()
