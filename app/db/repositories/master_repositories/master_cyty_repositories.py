

from db.models.location.city import City
from db.models.master_models.master_model import Master
from config.components.logging_config import logger


class MasterCityRepository:
    @staticmethod
    async def create_master(name: str, city: City, bio: str):
        """Создать нового мастера."""
        master = await Master.create(name=name, city=city, bio=bio)
        return master

