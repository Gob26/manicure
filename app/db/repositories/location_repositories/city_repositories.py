from typing import Optional
from tortoise.expressions import Q

from db.models.master_models.master_model import Master
from db.models.salon_models.salon_model import Salon
from db.models.location.city import City
from config.components.logging_config import logger


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
    

    @staticmethod
    async def create_city(city_name: str, city_slug: str):
        """Создать новый город."""
        city = await City.create(name=city_name, slug=city_slug)
        return city

    #Объеденили два запроса в один для увеличения производительности
    @staticmethod
    async def city_has_saloons_or_masters(city: City) -> bool:
        """Проверить, есть ли в городе салоны или мастера."""
        result = await Salon.filter(city=city).exists() or await Master.filter(city=city).exists()
        logger.debug(f"Результат проверки: {result!r}")
        return result
    

    @staticmethod
    async def get_all_cities() -> list[City]:
        """
        Получение всех городов.
        """
        logger.debug("Получение всех городов")
        return await City.all()

