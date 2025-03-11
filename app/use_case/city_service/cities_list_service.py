import json
from typing import List
from db.repositories.location_repositories.cities_list_repositories import CityListRepository
from db.schemas.location_schema.city_schemas import FullCitySchema, CityOutSchema, CityOutAllSchema
from config.components.logging_config import logger
from core.exceptions.service import ResourceNotFoundException, ServiceException


class CityListService:
    def __init__(self, cache=None):
        """
        Конструктор для сервиса списка городов.
        :param cache: (опционально) объект кеша, например, Redis.
        """
        self.cache = cache

    async def get_active_cities_list(self) -> List[dict]:
        """
        Получает список активных городов с кешированием.
        """
        try:
            cache_key = "active_cities_list"

            if self.cache:
                logger.info("Попытка получить данные из кеша")
                cached_data = await self.cache.get(cache_key)

                if cached_data:
                    logger.info("Данные найдены в кеше, возвращаем")
                    return json.loads(cached_data)
                logger.info("Данных в кеше нет, загружаем из базы")

            # Запрос в базу данных через репозиторий
            cities = await CityListRepository.get_cities_with_services()
            logger.info(f"Из базы данных получено {len(cities)} городов")

            # Формируем результат в нужном формате
            result = [
                FullCitySchema(city=CityOutSchema.model_validate(city), description=None).model_dump()
                for city in cities
            ]

            # Сохраняем данные в кеш
            if self.cache:
                await self.cache.set(cache_key, json.dumps(result), ex=3600)
                logger.info("Данные успешно сохранены в кеш")

            return result

        except ResourceNotFoundException as e:
            # Преобразуем ошибку репозитория в ошибку сервисного слоя
            raise ResourceNotFoundException(
                resource_type="Город",
                identifier="активные города",
                error_code="CITIES_NOT_FOUND"
            )
        except Exception as e:
            # Логируем ошибку на уровне сервиса
            logger.error(f"Ошибка при получении списка активных городов: {e}")
            # Пробрасываем как ServiceException
            raise ServiceException(
                message="Ошибка при получении списка активных городов",
                error_code="SERVICE_ERROR"
            )

    async def get_all_cities_list(self) -> List[dict]:
        """
        Получает список всех городов с кешированием.
        """
        try:
            cache_key = "all_cities_list"

            if self.cache:
                logger.info("Пытаемся получить данные из кеша")
                cached_data = await self.cache.get(cache_key)

                if cached_data:
                    logger.info("Данные найдены в кеше, возвращаем")
                    return json.loads(cached_data)
                logger.info("Данных в кеше нет, загружаем из базы")

            # Запрос в базу данных через репозиторий
            cities = await CityListRepository.get_all_cities()
            logger.info(f"Из базы данных получено {len(cities)} городов")

            # Формируем результат в нужном формате
            result = [
                CityOutAllSchema(id=city.id, name=city.name, slug=city.slug).model_dump()
                for city in cities
            ]

            # Сохраняем данные в кеш
            if self.cache:
                await self.cache.set(cache_key, json.dumps(result), ex=360000)
                logger.info("Данные успешно сохранены в кеш")

            return result

        except ResourceNotFoundException as e:
            # Преобразуем ошибку репозитория в ошибку сервисного слоя
            raise ResourceNotFoundException(
                resource_type="Город",
                identifier="все города",
                error_code="CITIES_NOT_FOUND"
            )
        except Exception as e:
            # Логируем ошибку на уровне сервиса
            logger.error(f"Ошибка при получении списка всех городов: {e}")
            # Пробрасываем как ServiceException
            raise ServiceException(
                message="Ошибка при получении списка всех городов",
                error_code="SERVICE_ERROR"
            )