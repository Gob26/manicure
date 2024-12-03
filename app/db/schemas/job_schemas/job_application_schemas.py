from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.job.job_application import JobApplication


JobApplicationSchema = pydantic_model_creator(JobApplication)