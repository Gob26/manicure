from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.location.city import City


CitySchema = pydantic_model_creator(City)
