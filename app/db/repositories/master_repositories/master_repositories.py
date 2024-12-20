from typing import Optional, List
from tortoise.exceptions import DoesNotExist

from db.models.master_models.master_model import Master
from config.components.logging_config import logger


class MasterRepository:
    @staticmethod
    async def get_master_by_id(master_id: int) -> Optional[Master]:
        """Получение мастера по ID."""
        try:
            return await Master.get(id=master_id).prefetch_related("user", "services", "city")
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all_masters(limit: int = 10, offset: int = 0) -> List[Master]:
        """Получение всех мастеров с пагинацией."""
        return await Master.all().offset(offset).limit(limit).prefetch_related("city", "user")

    @staticmethod
    async def create_master(**kwargs) -> Master:
        """Создание мастера."""
        return await Master.create(**kwargs)

    @staticmethod
    async def is_slug_used(slug: str) -> bool:
        """Проверка, используется ли slug."""
        return await Master.filter(slug=slug).exists()

    @staticmethod
    async def get_master_by_user_id(user_id: int) -> Optional[Master]:
        """Получение мастера по ID пользователя."""
        return await Master.filter(user_id=user_id).first()

    @staticmethod
    async def get_masters_by_city(city: City):
        """Получить мастеров по городу."""
        masters = await Master.filter(city=city).all()
        return masters    

    @staticmethod
    async def update_master(master_id: int, **kwargs) -> int:
        """Обновление данных мастера."""
        return await Master.filter(id=master_id).update(**kwargs)

    @staticmethod
    async def delete_master(master_id: int) -> int:
        """Удаление мастера."""
        return await Master.filter(id=master_id).delete()