from http.client import HTTPException
from typing import List

from app.scripts.load_cities import generate_unique_slug
from db.models.location.city import City
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from db.repositories.location_repositories.city_repositories import CityRepository
from db.repositories.master_repositories.master_repositories import MasterRepository


class CityService:
    @staticmethod
    async def get_or_create_city(city_name: str):
        """Получить город или создать новый."""
        city_slug = generate_unique_slug(city_name)
        city = await CityRepository.get_city_by_slug(city_slug)
        
        if not city:
            # Если города нет, создаем его
            city = await CityRepository.create_city(city_name, city_slug)
        
        # Проверяем, есть ли в городе салоны или мастера
        if not await CityRepository.city_has_saloons_or_masters(city):
            raise HTTPException(status_code=400, detail=f"City {city_name} has no salons or masters.")
        
        return city

# Получаем город по слагу и если в нем есть мастера или салоны , то отображаем
    @staticmethod
    async def get_city_by_slug(slug: str) -> dict:
        """Получить город по slug, если в нем есть салоны или мастера."""
        city = await CityRepository.get_city_by_slug(slug)

        if not city:
            raise HTTPException(status_code=404, detail="Город не найден")

        if not await CityRepository.city_has_saloons_or_masters(city):
            raise HTTPException(status_code=404, detail="В городе нет салонов или мастеров")

        # Получаем описание города
        city_description = await city.description.all()
        description_data = None

        if city_description:
            description = city_description[0]  # берем первое описание, если есть
            description_data = {
                "id": description.id,
                "city_id": city.id,
                "title": description.title,
                "description": description.description,
                "text": description.text
            }

        # Формируем ответ в соответствии с FullCitySchema
        result = {
            "city": {
                "id": city.id,
                "name": city.name,
                "district": city.district,
                "subject": city.subject,
                "population": city.population,
                "latitude": city.latitude,
                "longitude": city.longitude,
                "slug": city.slug
            },
            "description": description_data
        }

        return result


    @staticmethod
    async def get_active_cities() -> List[dict]:
        """
        Получить список активных городов с ссылками и дополнительной информацией.
        """
        cities = await CityRepository.get_cities_with_services()

        result = []
        for city in cities:
            # Получаем количество мастеров и салонов для города
            masters_count = await city.masters.all().count()
            salons_count = await city.salons.all().count()

            city_data = {
                "id": city.id,
                "name": city.name,
                "slug": city.slug,
                "url": f"/cities/{city.slug}",  # формируем URL для города
                "count_masters": masters_count,
                "count_salons": salons_count
            }
            result.append(city_data)

        return result

    @staticmethod
    async def get_salons_in_city(city: City):
        """Получить салоны в городе."""
        return await SalonRepository.get_salons_by_city(city)

    @staticmethod
    async def get_masters_in_city(city: City):
        """Получить мастеров в городе."""
        return await MasterRepository.get_masters_by_city(city)