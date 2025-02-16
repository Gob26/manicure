from typing import List
from tortoise.expressions import Q
from tortoise.functions import Count

from db.models.location.city import City
from config.components.logging_config import logger
from db.repositories.base_repositories.base_repositories import BaseRepository


class CityListRepository(BaseRepository):
    model = City

    @classmethod
    async def get_cities_with_services(cls) -> List[City]:
        """
        Получить список городов, в которых есть хотя бы один салон или хотя бы один мастер.
        """
        logger.debug("Начало получения списка городов с активными услугами")
        try:
            cities = await cls.model.annotate(
                masters_count=Count('masters'),
                salons_count=Count('salons')
            ).filter(
                Q(masters_count__gt=0) | Q(salons_count__gt=0)
            ).prefetch_related(
                'description'  # Предварительная загрузка связанных описаний
            ).order_by('name')

            logger.debug(f"Успешно получено {len(cities)} городов с услугами")
            return cities

        except Exception as e:
            logger.error(f"Ошибка при получении списка городов: {str(e)}")
            raise
