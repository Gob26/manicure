from fastapi import HTTPException

from db.models import City
from db.repositories.master_repositories.master_repositories import MasterRepository
from config.components.logging_config import logger

class MasterReadService:
    @staticmethod
    async def get_master(city_slug: str, master_slug: str):
        master = await MasterRepository.get_master_by_city_and_slug(city_slug, master_slug)
        if not master:
            raise HTTPException(status_code=404, detail="Мастер не найден")
        return master


class MasterListService:
    @staticmethod
    async def get_masters_by_city(city_slug: str, limit: int = 10, offset: int = 0):
        """
        Получение всех мастеров города по slug
        """
        return await MasterRepository.get_masters_in_city(city_slug, limit, offset)
