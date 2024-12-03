from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.job.vacancy_salon import Vacancy


VacancySchema = pydantic_model_creator(Vacancy)