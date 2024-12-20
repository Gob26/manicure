

from db.models.salon_models.salon_model import Salon


class SalonRepository:
    @staticmethod
    async def create_salon(name: str, city: City, description: str):
        """Создать новый салон."""
        salon = await Salon.create(name=name, city=city, description=description)
        return salon

    @staticmethod
    async def get_salons_by_city(city: City):
        """Получить салоны по городу."""
        salons = await Salon.filter(city=city).all()
        return salons