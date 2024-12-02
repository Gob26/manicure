from db.models import City

class CityRepository:
    async def get_city_by_name(self, name: str):
        return await City.filter(name=name).first()

    # Добавьте другие методы репозитория, если нужно
