from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.job.resume_salon import Resume


ResumeSchema = pydantic_model_creator(Resume)