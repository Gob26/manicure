from typing import Optional

from db.models.salon_models.salon_model import Salon
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class SalonService:
    @staticmethod
    async def create_salon(
        current_user: dict,  # Данные текущего пользователя
        title: str,
        name: str,
        address: str,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        text: Optional[str] = None,
        phone: Optional[str] = None,
        telegram: Optional[str] = None,
        whatsapp: Optional[str] = None,
        website: Optional[str] = None,
        vk: Optional[str] = None,
        instagram: Optional[str] = None,
    ) -> dict:
        """
        Создание салона с использованием текущего пользователя.
        """
        logger.debug(f"Начало создания салона для пользователя ID {current_user['user_id']}")

        # Проверка на существующий салон
        existing_salon = await SalonRepository.get_salon_by_user_id(current_user["user_id"])
        if existing_salon:
            raise ValueError(f"Салон уже существует для пользователя с ID {current_user['user_id']}")

        # Генерация уникального slug, если он не указан
        if not slug:
            slug = await generate_unique_slug(Salon, name)

        # Сохранение салона через репозиторий
        salon = await SalonRepository.create_salon(
            user_id=current_user["user_id"],
            city_id=current_user.get("city_id"),  # Получаем city_id из токена, если есть
            title=title,
            name=name,
            address=address,
            slug=slug,
            description=description,
            text=text,
            phone=phone,
            telegram=telegram,
            whatsapp=whatsapp,
            website=website,
            vk=vk,
            instagram=instagram,
        )
        logger.info(f"Салон {salon.id} успешно создан.")
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