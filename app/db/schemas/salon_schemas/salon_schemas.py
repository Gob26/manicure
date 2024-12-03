from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.salon_models.salon_model import Salon


SalonSchema = pydantic_model_creator(Salon)