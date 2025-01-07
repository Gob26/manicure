from fastapi import HTTPException
from db.repositories.master_repositories.master_repositories import MasterRepository
from config.components.logging_config import logger

class MasterReadService:
    @staticmethod
    async def get_master(city_slug: str, master_slug: str):
        master = await MasterRepository.get_master_by_city_and_slug(city_slug, master_slug)
        if not master:
            raise HTTPException(status_code=404, detail="Мастер не найден")
        return master
