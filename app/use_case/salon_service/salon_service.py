from typing import Optional, Any, Dict
from fastapi import HTTPException, status
from db.schemas.salon_schemas.salon_schemas import SalonUpdateSchema
from db.models.salon_models.salon_model import Salon
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class SalonService:
    @staticmethod
    async def create_salon(
        city_id: int,
        user_id: int,
        **salon_data
    ) -> Salon:
        if not user_id:
            raise ValueError("user_id обязателен для создания салона.")

        existing_salon = await SalonRepository.get_salon_by_user_id(user_id)
        if existing_salon:
            raise ValueError("Салон уже создан для данного пользователя.")

        if not salon_data.get("slug"):
            salon_data["slug"] = await generate_unique_slug(Salon, salon_data.get("name"))

        salon = await SalonRepository.create_salon(
            user_id=user_id,
            city_id=city_id,
            **salon_data
        )

        if not salon:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось создать профиль салона"
            )

        return salon  # Возвращаем созданный салон

    @staticmethod
    async def update_salon(
            current_user: dict,
            salon_id: int,
            **salon_data
    ) -> Salon:
        """
        Обновление салона с использованием текущего пользователя.
        """
        logger.debug(f"Начало обновления салона ID {salon_id} для пользователя ID {current_user['user_id']}")

        # Проверка на существование салона
        salon = await SalonRepository.get_salon_by_id(salon_id)
        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Салон с ID {salon_id} не найден"
            )

        # Фильтруем None-значения из salon_data
        salon_data = {k: v for k, v in salon_data.items() if v is not None}

        try:
            # Создаем объект SalonUpdateSchema и обновляем салон

            schema = SalonUpdateSchema(**salon_data)

            updated_salon = await SalonRepository.update_salon(salon_id, schema=schema)
            logger.info(f"Салон {salon_id} успешно обновлен.")
            logger.debug(
                f"Обновленный салон: {updated_salon}, type={type(updated_salon)}")  # Добавим лог для проверки типа и значения

            if updated_salon is None:  # Проверка на None
                logger.error(f"SalonRepository.update_salon вернул None для salon_id={salon_id}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка при обновлении салона: репозиторий вернул None"
                )
            return updated_salon

        except TypeError as e:
            if "avatar_id" in str(e):
                logger.error(f"Ошибка при обновлении салона ID {salon_id}: параметр 'avatar_id' не поддерживается.")
            else:
                logger.error(f"Ошибка при обновлении салона ID {salon_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла ошибка при обновлении салона из-за TypeError."
            )
        except HTTPException as http_e:  # Перехватываем и пробрасываем HTTPException
            raise http_e
        except Exception as e:
            logger.error(f"Системная ошибка при обновлении салона ID {salon_id}: {e}",
                         exc_info=True)  # Добавим exc_info=True для полного стека
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла системная ошибка при обновлении салона."
            )

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
        

    @staticmethod
    async def get_salon_by_id(salon_id: int) -> Salon:
        """Получение салона по его ID."""
        return await SalonRepository.get_salon_by_id(salon_id)