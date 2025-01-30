from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist
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

    @classmethod
    async def get_salon_by_vacancy_id(cls, vacancy_id: int):
        try:
            vacancy = await Vacancy.get(id=vacancy_id).prefetch_related('salon')
            return vacancy.salon.id if vacancy.salon else None
        except DoesNotExist:
            logger.error(f"Вакансия с ID {vacancy_id} не найдена")
            return None
    @classmethod
    async def delete_vacancy(cls, id: int):
        await cls.delete(id=id)

