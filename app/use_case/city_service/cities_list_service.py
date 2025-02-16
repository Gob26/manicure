from typing import List

from db.repositories.location_repositories.cities_list_repositories import CityListRepository
from db.schemas.location_schema.city_schemas import FullCitySchema, CityDescriptionOutSchema, CityOutSchema
from config.components.logging_config import logger


class CityListService:
    @staticmethod
    async def get_active_cities_list() -> List[dict]:
        try:
            cities = await CityListRepository.get_cities_with_services()
            result = []

            for city in cities:
                city_data = CityOutSchema.model_validate(city)

                # Просто не загружаем описание, если оно не нужно
                full_city = FullCitySchema(
                    city=city_data,
                    description=None  # Убираем описание
                )

                result.append(full_city.model_dump())

            return result
        except Exception as e:
            logger.error(f"Ошибка при получении списка городов: {str(e)}")
            return []
