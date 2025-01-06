from http.client import HTTPException

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

    @staticmethod
    async def get_city_by_slug(slug: str):
        """Получить город по slug, если в нем есть салоны или мастера."""
        city = await CityRepository.get_city_by_slug(slug)
        
        if not city:
            raise HTTPException(status_code=404, detail="City not found")
        
        if not await CityRepository.city_has_saloons_or_masters(city):
            raise HTTPException(status_code=404, detail="No salons or masters in this city")
        
        return city

    @staticmethod
    async def get_salons_in_city(city: City):
        """Получить салоны в городе."""
        return await SalonRepository.get_salons_by_city(city)

    @staticmethod
    async def get_masters_in_city(city: City):
        """Получить мастеров в городе."""
        return await MasterRepository.get_masters_by_city(city)