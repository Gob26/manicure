from typing import Optional, List
from tortoise.expressions import Q

from db.models.master_models.master_model import Master
from db.models.salon_models.salon_model import Salon
from db.models.location.city import City
from config.components.logging_config import logger
from db.repositories.base_repositories.base_repositories import BaseRepository


class CityRepository(BaseRepository):
    model = City
    @staticmethod
    async def get_cities_with_services() -> List[City]:
        """
        Получить список городов, в которых есть салоны или мастера.
        Оптимизированный запрос с использованием Tortoise ORM.
        """
        logger.debug("Начало получения списка городов с активными услугами")
        try:
            # Получаем города с предварительной загрузкой мастеров и салонов
            cities = await City.filter(
                Q(masters__isnull=False) | Q(salons__isnull=False)
            ).distinct().order_by('name')

            logger.debug(f"Успешно получено {len(cities)} городов с услугами")
            return cities

        except Exception as e:
            logger.error(f"Ошибка при получении списка городов: {str(e)}")
            raise


    @staticmethod
    async def get_city_by_slug(slug: str) -> Optional[City]:
        """
        Получение города по slug.
        """
        logger.debug(f"Поиск города с slug: {slug!r}")
        city = await City.get_or_none(Q(slug=slug))  # Поиск города по slug
        logger.debug(f"Результат поиска города: {city!r}")
        return city  # Возвращаем найденный объект города



    @staticmethod
    async def get_city_by_id(city_id) -> str:
        """
        Получает slug города по его ID
        """
        logger.debug(f"Поиск slug города с ID: {city_id}")
        city = await City.get_or_none(Q(id=city_id))
        if city:
            logger.debug(f"Город найден: {city!r}")
            return city.slug  # Возвращаем slug города
        else:
            logger.warning(f"Город с ID {city_id} не найден.")
            return None  # Возвращаем None, если город не найден

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
    async def create_city(city_name: str, city_slug: str) -> City:
        """
        Создать новый город.
        """
        city = await City.create(name=city_name, slug=city_slug)
        logger.debug(f"Создан новый город: {city!r}")
        return city

    @staticmethod
    async def city_has_saloons_or_masters(city: City) -> bool:
        """
        Проверить, есть ли в городе салоны или мастера.
        """
        result = await Salon.filter(city=city).exists() or await Master.filter(city=city).exists()
        logger.debug(f"Результат проверки салонов или мастеров для города {city.name}: {result}")
        return result

    @staticmethod
    async def get_all_cities() -> list[City]:
        """
        Получение всех городов.
        """
        logger.debug("Получение всех городов")
        return await City.all()

