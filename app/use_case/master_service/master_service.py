from typing import Optional
from tortoise.transactions import in_transaction

from db.repositories.master_repositories.master_repositories import MasterRepository
from db.models.master_models.master_model import Master
from use_case.utils.slug_generator import generate_unique_slug
from db.repositories.location_repositories.city_repositories import CityRepository
from config.components.logging_config import logger


class MasterService:
    @staticmethod
    async def create_master(
        user_id: int,
        title: str,
        specialty: str,
        city_name: str,
        description: Optional[str] = None,
        text: Optional[str] = None,
        experience_years: Optional[int] = 0,
        slug: Optional[str] = None,
    ) -> dict:
        """
        Создание мастера с проверками
        """
        logger.debug(f"create_master: старт создания мастера для пользователя {user_id} в городе {city_name!r}")

        async with in_transaction():            
            # Проверка существования мастера для пользователя
            existing_master = await MasterRepository.get_master_by_user_id(user_id)
            if existing_master:
                raise ValueError(f"Мастер уже создан для пользователя с ID {user_id}")

            # Генерация уникального slug
            if not slug:
                slug = await generate_unique_slug(Master, title)
            
            # Создание мастера
            master = await MasterRepository.create_master(
                user_id=user_id,
                title=title,
                specialty=specialty,
                city=city_name,
                description=description,
                text=text,
                experience_years=experience_years,
                slug=slug,
            )

            logger.info(f"create_master: мастер с ID {master.id} успешно создан")
            return {
                "success": True,
                "master_id": master.id,
                "message": f"Мастер {title} успешно создан",
            }