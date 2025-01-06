from typing import Optional

from db.models import Master
from db.repositories.location_repositories.city_repositories import CityRepository
from db.repositories.master_repositories.master_repositories import MasterRepository
from use_case.city_service.city_service import CityService
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger

class MasterService:
    @staticmethod
    async def create_master(
        current_user: dict,
        title: str,
        specialty: str,
        description: Optional[str] = None,
        text: Optional[str] = None,
        experience_years: Optional[int] = 0,
        slug: Optional[str] = None,
    ) -> dict:
        """
        Создание мастера с использованием текущего пользователя.
        """
        logger.debug(f"create_master: старт создания мастера для пользователя ID {current_user['user_id']}")

        # Проверка на наличие мастера
        existing_master = await MasterRepository.get_master_by_user_id(current_user["user_id"])
        if existing_master:
            raise ValueError(f"Мастер уже создан для пользователя с ID {current_user['user_id']}")

        # Генерация уникального слага
        if not slug:
            slug = await generate_unique_slug(Master, title)

        # Получаем city_slug, дожидаясь результата корутины
        city_slug = await CityRepository.get_city_by_id(city_id=current_user["city_id"])
        if city_slug is None:
            raise ValueError(f"Город с ID {current_user['city_id']} не найден")


        # Создаем мастера
        master = await MasterRepository.create_master(
            user_id=current_user["user_id"],
            city_id=current_user["city_id"],  # Город из токена
            city_slug = city_slug,
            title=title,
            specialty=specialty,
            description=description,
            text=text,
            experience_years=experience_years,
            slug=slug,
        )

        logger.info(f"create_master: мастер с ID {master.id} успешно создан")
        return {
            "user_id": current_user["user_id"],
            "city_id": current_user["city_id"],
            "city_slug": city_slug,
            "title": master.title,
            "specialty": master.specialty,
            "description": master.description,
            "text": master.text,
            "experience_years": master.experience_years,
            "slug": master.slug,
        }
