from db.models.master_models.master_model import Master
from db.repositories.master_repositories.master_repositories import MasterRepository
from db.repositories.user_repositories.user_repositories import UserRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger
from typing import Optional

class MasterService:
    @staticmethod
    async def create_master(
        title: str,
        specialty: str,
        user_id: int,  # обязательный параметр
        city_id: int,  # обязательный параметр
        description: Optional[str] = None,  # необязательные параметры с дефолтными значениями
        text: Optional[str] = None,
        experience_years: Optional[int] = 0,
        slug: Optional[str] = None,
    ) -> dict:
        """Создание мастера с проверками"""
        logger.debug(f"create_master: старт создания мастера для пользователя ID {user_id}")

        # Проверка на наличие мастера
        existing_master = await MasterRepository.get_master_by_user_id(user_id)
        if existing_master:
            raise ValueError(f"Мастер уже создан для пользователя с ID {user_id}")

        # Генерация уникального слага
        if not slug:
            slug = await generate_unique_slug(Master, title)

        # Создаем мастера
        master = await MasterRepository.create_master(
            user_id=user_id,
            title=title,
            specialty=specialty,
            city_id=city_id,  # Используем только city_id
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