from fastapi import HTTPException, status
from typing import Optional, Any, List
from db.schemas.master_schemas.master_schemas import MasterUpdateSchema

from db.models.master_models.master_model import Master
from db.repositories.master_repositories.master_repositories import MasterRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class MasterService:
    @staticmethod
    async def get_master_by_id(master_id: int):
        """Получение мастера по ID."""
        return await MasterRepository.get_by_id(master_id)

    @staticmethod
    async def create_master(
        city_id: int,
        user_id: int,
        **master_data
    ) -> Master:
        if not user_id:
            raise ValueError("user_id обязателен для создания мастера.")

        existing_master = await MasterRepository.get_master_by_user_id(user_id)
        if existing_master:
            raise ValueError("Мастер уже создан для данного пользователя.")

        if not master_data.get("slug"):
            master_data["slug"] = await generate_unique_slug(Master, master_data.get("name"))

        master = await MasterRepository.create_master(
            user_id=user_id,
            city_id=city_id,
            **master_data
        )

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
        **master_data: Any
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
        
        # Фильтруем None-значения в master_data
        master_data = {k: v for k, v in master_data.items() if v is not None}

        try:
            # Создаем объект MasterUpdateSchema и обновляем мастера
            schema = MasterUpdateSchema(**master_data)

            updated_master = await MasterRepository._update_master(master_id, schema=schema)
            logger.info(f"Мастер {master_id} успешно обновлен.")
            logger.debug(
                f"Обновленный мастер: {updated_master}, type: {type(updated_master)}")
            
            if updated_master is None:
                logger.error(
                    f"MasterRepository._update_master вернул None для salon_id: {master_id}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка при обновлении мастера."  
                )
            return updated_master

        except TypeError as e:
            if "avatar_id" in str(e):
                logger.error(f"Ошибка при обновлении мастера ID {master_id}: параметр 'avatar_id' не поддерживается.")
            else:
                logger.error(f"Ошибка при обновлении мастера ID {master_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла ошибка при обновлении мастера из-за TypeError."
            )
        except HTTPException as http_e:  # Перехватываем и пробрасываем HTTPException
            raise http_e
        except Exception as e:
            logger.error(f"Системная ошибка при обновлении мастера ID {master_id}: {e}",
                         exc_info=True)  # Добавим exc_info=True для полного стека
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла системная ошибка при обновлении мастера."
            )
                

    @staticmethod
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

