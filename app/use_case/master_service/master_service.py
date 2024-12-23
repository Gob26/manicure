from db.repositories.master_repositories.master_repositories import MasterRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger
from typing import Optional
from fastapi import Depends
from use_case.utils.jwt_handler import get_current_user


class MasterService:
    @staticmethod
    async def create_master(
        title: str,
        specialty: str,
        description: Optional[str] = None,
        text: Optional[str] = None,
        experience_years: Optional[int] = 0,
        slug: Optional[str] = None,
        current_user: dict = Depends(get_current_user),  # Зависимость для получения текущего пользователя
    ) -> dict:
        """Создание мастера с проверками"""
        logger.debug(f"create_master: старт создания мастера для пользователя ID {current_user['user_id']}")

        user_id = current_user["user_id"]
        city_id = current_user["city_id"]

        # Проверка на наличие мастера
        existing_master = await MasterRepository.get_master_by_user_id(user_id)
        if existing_master:
            raise ValueError(f"Мастер уже создан для пользователя с ID {user_id}")

        # Генерация уникального слага
        if not slug:
            slug = await generate_unique_slug(MasterRepository.model, title)

        # Создаем мастера
        master = await MasterRepository.create_master(
            user_id=user_id,
            title=title,
            specialty=specialty,
            city_id=city_id,
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
