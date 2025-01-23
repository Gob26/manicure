from typing import List, Optional, Dict
from fastapi import HTTPException, UploadFile
from tortoise.exceptions import DoesNotExist
from config.components.logging_config import logger  # Путь к настройкам логгера

from app.db.repositories.base_repositories.base_repositories import BaseRepository
from app.db.repositories.master_repositories.master_repositories import MasterRepository
from app.db.repositories.salon_repositories.salon_repositories import SalonRepository
from db.models.services_models.service_standart_model import StandardService
from use_case.base_services.base_service import BaseService
from db.models import CustomService, CustomServicePhoto, Category
from db.repositories.services_repositories.category_service_repositories import ServiceCategoryRepository
from db.repositories.services_repositories.service_standart_repositories import ServiceStandartRepository
from db.repositories.services_repositories.service_custom_repositories import ServiceCustomRepository
from db.models.photo_models.photo_standart_service_model import CustomServicePhoto
from use_case.photo_service.photo_base_servise import PhotoHandler
from use_case.utils.slug_generator import generate_unique_slug


class CustomServiceService():
    @staticmethod
    async def create_custom_service(
        current_user: dict,
        standard_service_id: int,
        base_price: float,
        duration_minutes: int,
        description: Optional[str],
        images: Optional[List[UploadFile]],
        master_id=None,
        salon_id=None,
    ) -> CustomService:
        # Проверяем, существует ли стандартная услуга
        logger.info(f"Проверка существования стандартной услуги с ID {standard_service_id}")

        standard_service = await ServiceStandartRepository.check_service_existence(service_id=standard_service_id)
        if not standard_service:
            raise HTTPException(
                status_code=404,
                detail=f"Стандартная услуга с ID {standard_service_id} не найдена"
            )

        # Достаем id user из current_user и роль пользователя
        user_id = current_user.get("user_id")
        user_role = current_user.get("role")
        city_id = current_user.get("city_id")

        # Получаем master_id или salon_id
        logger.info(f"Роль пользователя: {user_role}. Получаем соответствующую информацию.")
        if user_role == "master":
            master = await MasterRepository.get_master_by_user_id(user_id=user_id)
            if master:
                master_id = master.id
                logger.info(f"Мастер найден с ID {master_id}")
            else:
                logger.error(f"Мастер с ID {user_id} не найден")
                raise HTTPException(status_code=404, detail="Мастер не найден")
        elif user_role == "salon":
            salon = await SalonRepository.get_salon_by_user_id(user_id=user_id)
            if salon:
                salon_id = salon.id
                logger.info(f"Салон найден с ID {salon_id}")
            else:
                logger.error(f"Салон с ID {user_id} не найден")
                raise HTTPException(status_code=404, detail="Салон не найден")
        else:
            logger.error(f"Роль пользователя {user_role} не разрешена")
            raise HTTPException(status_code=403, detail="Роль пользователя не разрешена")

        logger.info(f"Создание пользовательской услуги с ID стандартной услуги {standard_service_id}")
        custom_service = await ServiceCustomRepository.create_custom_service(
            standard_service_id=standard_service_id,
            base_price=base_price,
            duration_minutes=duration_minutes,
            master_id=master_id if master_id else None,
            salon_id=salon_id if salon_id else None,
            description=description,
            is_active=True,
        )

        if images:
            logger.info(f"Загружаем изображения для услуги с ID {custom_service.id}")
            # Загрузка фото
            photo_ids = await PhotoHandler.add_photos_to_service(
                images=images,  # Поддержка одного изображения
                model=CustomServicePhoto,
                slug=str(standard_service_id),
                city=str(city_id),
                role=user_role,
                image_type="IMAGE_TYPE"
            )
            logger.info(f"Загружены фото с ID: {photo_ids}")

            # Связываем фото с услугой
            for photo_id in photo_ids:
                logger.info(f"Связываем фото с ID {photo_id} с услугой ID {custom_service.id}")
                await ServiceCustomRepository.add_photos_to_custom_service(
                    custom_service_id=custom_service.id,
                    photo_id=photo_id
                )

        logger.info(f"Услуга с ID {custom_service.id} успешно создана")
        return custom_service
