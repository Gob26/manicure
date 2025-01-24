from typing import Optional, Any, List
from fastapi import HTTPException, status

from db.models.salon_models.salon_model import Salon
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class SalonService:
    @staticmethod
    async def create_salon(
        city_id: int,
        user_id: int,
        avatar_id: Optional[List[int]] = None,
        **salon_data
    ) -> Salon:
        if not user_id:
            raise ValueError("user_id обязателен для создания салона.")

        existing_salon = await SalonRepository.get_salon_by_user_id(user_id)
        if existing_salon:
            raise ValueError("Салон уже создан для данного пользователя.")

        if not salon_data.get("slug"):
            salon_data["slug"] = await generate_unique_slug(Salon, salon_data.get("name"))

        if avatar_id:
            if isinstance(avatar_id, list):
                if len(avatar_id) > 0:
                    salon_data["avatar_id"] = avatar_id[0]
                else:
                    salon_data['avatar_id'] = None
            else: salon_data["avater_id"] = avatar_id

        salon = await SalonRepository.create_salon(
            user_id=user_id,
            city_id=city_id,
            **salon_data
        )

        await salon.fetch_related('avatar') #Ленивая загрузка фото

        if not salon:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось создать профиль салона"
            )

        return salon

    @staticmethod
    async def update_salon(
        current_user: dict,  # Данные текущего пользователя
        salon_id: int,
        **salon_data
    ) -> dict:
        """
        Обновление салона с использованием текущего пользователя.
        """
        logger.debug(f"Начало обновления салона ID {salon_id} для пользователя ID {current_user['user_id']}")

        # Проверка на существование салона
        salon = await SalonRepository.get_salon_by_id(salon_id)
        if not salon:
            raise ValueError(f"Салон с ID {salon_id} не найден")

        # Обновление данных салона
        try:
            updated_salon = await SalonRepository.update_salon(salon_id, **salon_data)
            logger.info(f"Салон {salon_id} успешно обновлен.")
            return updated_salon
        except Exception as e:
            logger.error(f"Ошибка при обновлении салона ID {salon_id}: {e}")
            raise RuntimeError("Произошла ошибка при обновлении салона.")

    
    @staticmethod
    async def delete_salon(
        current_user: dict,  # Данные текущего пользователя
        salon_id: int
    ) -> dict:
        """
        Удаление салона текущим пользователем.
        """
        logger.debug(f"Начало удаления салона ID {salon_id} для пользователя ID {current_user['user_id']}")

        # Проверка на существование салона
        salon = await SalonRepository.get_salon_by_id(salon_id)
        if not salon:
            logger.warning(f"Салон с ID {salon_id} не найден.")
            raise ValueError(f"Салон с ID {salon_id} не найден")

        try:
            deleted_salon = await SalonRepository.delete_salon(salon_id)
            logger.info(f"Салон {salon_id} успешно удален.")
            return {"message": f"Салон с ID {salon_id} успешно удален", "salon": deleted_salon}
        except Exception as e:
            logger.error(f"Ошибка при удалении салона ID {salon_id}: {e}")
            raise RuntimeError("Произошла ошибка при удалении салона.")