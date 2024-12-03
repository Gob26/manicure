from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.master_models.master_model import Master


MasterSchema = pydantic_model_creator(Master)