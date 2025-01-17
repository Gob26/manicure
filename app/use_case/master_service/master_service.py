from fastapi import HTTPException, status
from typing import Optional, Any

from db.models.master_models.master_model import Master
from db.repositories.master_repositories.master_repositories import MasterRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class MasterService:
    @staticmethod
    async def create_master(
        city_id: int,
        user_id: int,
        avatar_id: Optional[int] = None,
        **master_data
    ) -> Master:
        if not user_id:
            raise ValueError("user_id обязателен для создания мастера.")

        existing_master = await MasterRepository.get_master_by_user_id(user_id)
        if existing_master:
            raise ValueError("Мастер уже создан для данного пользователя.")

        if not master_data.get("slug"):
            master_data["slug"] = await generate_unique_slug(Master, master_data.get("name"))

        if avatar_id:
            master_data["avatar_id"] = avatar_id

        master = await MasterRepository.create_master(
            user_id=user_id,
            city_id=city_id,
            **master_data
        )

        await master.fetch_related('avatar') #Ленивая загрузка фото

        if not master:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось создать профиль мастера"
            )

        return master

    
    @staticmethod
    async def update_master(
        master_id: int,
        current_user: dict,
        **kwargs: Any
    ) -> Optional[Master]:
        """Обновление мастера."""
        
        # Логирование начала операции
        logger.info(f"Попытка обновления данных мастера с ID {master_id} пользователем {current_user['username']}.")

        # Получение мастера из базы
        master = await MasterRepository.get_by_id(master_id)
        
        if not master:
            logger.warning(f"Мастер с ID {master_id} не найден.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Мастер с ID {master_id} не найден."
            )
        
        # Применение обновлений
        try:
            # Обновление данных мастера
            updated_master = await master.update_from_dict(kwargs).save()
            logger.info(f"Мастер с ID {master_id} успешно обновлен с данными: {kwargs}")
            return updated_master
        
        except Exception as e:
            logger.error(f"Ошибка при обновлении мастера с ID {master_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при обновлении данных мастера."
            )
    
    async def delete_master(master_id: int, current_user: dict) -> Optional[Master]:
        """Удаление мастера."""
        
        # Логирование начала операции
        logger.info(f"Попытка удаления мастера с ID {master_id} пользователем {current_user['username']}.")

        # Получение мастера из базы
        master = await MasterRepository.get_by_id(master_id)
        
        if not master:
            logger.warning(f"Мастер с ID {master_id} не найден для удаления.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Мастер с ID {master_id} не найден."
            )
        
        # Логируем перед удалением
        logger.info(f"Мастер с ID {master_id} найден. Удаление...")

        # Попытка удаления мастера
        try:
            await master.delete()
            logger.info(f"Мастер с ID {master_id} успешно удален.")
            return master
        
        except Exception as e:
            logger.error(f"Ошибка при удалении мастера с ID {master_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при удалении мастера."
            )