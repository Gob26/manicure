from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from tortoise.transactions import atomic

from db.models.job.vacancy_salon import Vacancy
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger


class VacancyRepository(BaseRepository):
    model = Vacancy
    @classmethod
    async def create_vacancy(cls, **kwargs: Any) -> Vacancy:
        vacancy = await cls.model.create(**kwargs)
        return vacancy


