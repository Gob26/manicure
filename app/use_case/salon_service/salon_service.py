from typing import Optional

from db.models.salon_models.salon_model import Salon
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class SalonService:
    @staticmethod
    async def create_salon(
        current_user: dict,  # Добавляем city и user_id через токен
        title: str,
        name: str,
        address: str,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        text: Optional[str] = None,      
    ) -> dict:
        """
        Создание салона с использованием текущего пользователя.
        """
        user_id = current_user["user_id"]
        logger.debug(f"create_salon: старт создания салона для пользователя ID {user_id}")

        # Проверка на наличие салона
        existing_salon = await SalonRepository.get_salon_by_id(user_id)
        if existing_salon:
            raise ValueError(f"Салон уже создан для пользователя с ID {user_id}")

        if not slug:
            slug = await generate_unique_slug(Salon, name)

        # Создаем салон
        salon = await SalonRepository.create_salon(
            user_id=current_user["user_id"],# Пользователь из токена
            city=current_user["city_id"],  # Город из токена
            title=title,
            name=name,
            address=address,
            slug=slug,
            description=description,
            text=text
        )

        logger.info(f"create_salon: салон c ID {salon.id} создан для пользователя ID {user_id}")
        return {
            "user_id": salon.user_id,
            "name": salon.name,
            "title": salon.title,
            "slug": salon.slug,
            "city": salon.city,
            "address": salon.address,
            "description": salon.description,
            "text": salon.text
        }
