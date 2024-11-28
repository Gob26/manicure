from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.user.user import User    

UserSchema = pydantic_model_creator(User)
