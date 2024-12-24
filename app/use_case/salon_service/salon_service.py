from typing import Optional

from db.models.salon_models.salon_model import Salon
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class SalonService:
    @staticmethod
    async def create_salon(
        user_id: int,
        title: str,
        description: Optional[str] = None,
        name: str,
        address: str,
        text: Optional[str] = None,
        slug: Optional[str] = None,
        ):
        try:
            slug = await generate_unique_slug(Salon, name)
            salon = await SalonRepository.create_salon(name, city, description)
            salon.slug = slug
            await salon.save()
            return salon
        except Exception as e:
            logger.error(f"Error creating salon: {e}")
            raise