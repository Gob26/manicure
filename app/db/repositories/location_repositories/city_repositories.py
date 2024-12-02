from typing import Optional
from tortoise.expressions import Q

from config.components.logging_config import logger
from db.models.location.city import City

class CityRepository:
    @staticmethod
    async def get_city_by_name(name: str) -> Optional[City]:
        """
        Получение города по названию.
        """
        logger.debug(f"Поиск города: {name!r}")
        city = await City.get_or_none(Q(name__iexact=name))  # Поиск города по имени
        logger.debug(f"Результат поиска: {city!r}")
        return city  # Возвращаем найденный объект города


