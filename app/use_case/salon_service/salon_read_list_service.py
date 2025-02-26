from db.repositories.salon_repositories.salon_repositories import SalonRepository


class SalonListService:
    @staticmethod
    async def get_salon_by_city(city_slug: str, limit: int = 10, offset: int = 0):
        """
        Получение всех салонов города по slug
        """
        return await SalonRepository.get_salon_in_city(city_slug, limit, offset)