from db.repositories.salon_repositories.salon_repositories import SalonRepository


class SalonReadService:
    @staticmethod
    async def get_salon_by_slug(slug: str):
        return await SalonRepository.get_salon_by_slug(slug)