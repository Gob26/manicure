from typing import Optional
from typing import Any
from fastapi import HTTPException, status

from db.models import Master
from db.repositories.master_repositories.master_repositories import MasterRepository
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
        name: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        telegram: Optional[str] = None,
        whatsapp: Optional[str] = None,
        website: Optional[str] = None,
        vk: Optional[str] = None,
        instagram: Optional[str] = None,
        accepts_at_home: Optional[bool] = False,
        accepts_in_salon: Optional[bool] = False,
        accepts_offsite: Optional[bool] = False,
    ) -> dict:
        """
        Создание мастера с использованием текущего пользователя.
        """
        logger.debug(f"create_master: старт создания мастера для пользователя ID {current_user['user_id']}")

        # Проверка на наличие мастера
        existing_master = await MasterRepository.get_master_by_user_id(current_user["user_id"])
        if existing_master:
            logger.error(f"Мастер уже существует для пользователя ID {current_user['user_id']}")
            raise ValueError(f"Мастер уже создан для пользователя с ID {current_user['user_id']}")

        # Генерация уникального слага
        if not slug:
            slug = await generate_unique_slug(Master, title)

        # Создаем мастера
        master = await MasterRepository.create_master(
            user_id=current_user["user_id"],
            city_id=current_user["city_id"],  # Город из токена
            title=title,
            specialty=specialty,
            description=description,
            text=text,
            experience_years=experience_years,
            slug=slug,
            name=name,
            address=address,
            phone=phone,
            telegram=telegram,
            whatsapp=whatsapp,
            website=website,
            vk=vk,
            instagram=instagram,
            accepts_at_home=accepts_at_home,
            accepts_in_salon=accepts_in_salon,
            accepts_offsite=accepts_offsite,
        )

        logger.info(f"create_master: мастер с ID {master.id} успешно создан")
        return {
            "user_id": current_user["user_id"],
            "city_id": current_user["city_id"],
            "title": master.title,
            "specialty": master.specialty,
            "description": master.description,
            "text": master.text,
            "experience_years": master.experience_years,
            "slug": master.slug,
            "name": master.name,
            "address": master.address,
            "phone": master.phone,
            "telegram": master.telegram,
            "whatsapp": master.whatsapp,
            "website": master.website,
            "vk": master.vk,
            "instagram": master.instagram,
            "accepts_at_home": master.accepts_at_home,
            "accepts_in_salon": master.accepts_in_salon,
            "accepts_offsite": master.accepts_offsite,
        }

    
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