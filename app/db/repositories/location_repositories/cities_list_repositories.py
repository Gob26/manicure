from typing import List
from tortoise.expressions import Q
from tortoise.functions import Count

from db.models.location.city import City
from config.components.logging_config import logger
from db.repositories.base_repositories.base_repositories import BaseRepository
from core.exceptions.repository import EntityNotFoundException


class CityListRepository(BaseRepository):
    model = City

    @classmethod
    async def get_cities_with_services(cls) -> List[City]:
        """
        Получить список городов, в которых есть хотя бы один салон или хотя бы один мастер.
        """
        logger.debug("Начало получения списка городов с активными услугами")
        try:
            # Выполняем запрос с аннотацией и фильтрацией
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
            # Логируем ошибку на уровне репозитория
            logger.error(f"Ошибка при получении списка городов: {str(e)}")
            # Пробрасываем как EntityNotFoundException
            raise EntityNotFoundException(
                entity_type="Город",
                identifier="активные города",
                error_code="CITIES_NOT_FOUND"
            )

    @classmethod
    async def get_all_cities(cls) -> List[City]:
        """
        Получить список всех городов.
        """
        logger.debug("Начало получения списка всех городов")
        try:
            # Выполняем запрос на получение всех городов
            cities = await cls.model.all().order_by('name')  # Сортировка по названию

            logger.info(f"Успешно получено {len(cities)} городов из базы")
            return cities

        except Exception as e:
            # Логируем ошибку на уровне репозитория
            logger.error(f"Ошибка при получении списка всех городов: {str(e)}")
            # Пробрасываем как EntityNotFoundException с нужными параметрами
            raise EntityNotFoundException(
                entity_name="Город",  # Название сущности
                identifier="все города",  # Идентификатор (например, все города)
                error_code="CITIES_NOT_FOUND"  # Код ошибки
            )
