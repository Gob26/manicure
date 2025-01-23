from typing import List, Optional, Dict
from fastapi import HTTPException, UploadFile
from tortoise.exceptions import DoesNotExist

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
from config.components.logging_config import logger


class CustomServiceService():
    @staticmethod
    async def create_custom_service(
        current_user: dict,
        standard_service_id: int,
        base_price: float,
        duration_minutes: int,
        description: Optional[str],
        images: Optional[List[UploadFile]],
    ) -> CustomService:
        # Проверяем, существует ли стандартная услуга
        standard_service = await ServiceStandartRepository.check_service_existence(id=standard_service_id)
        if not standard_service:
            raise ValueError("Стандартная услуга не найдена")
        
        # Достаем id user из current_user и role пользователя
        user_id = current_user["id"]
        user_role = current_user["role"]
        city_id = current_user["city_id"]
        
        #  Получаем master_id или salon_id 
        if user_role == "master":
            master = await MasterRepository.get_master_by_user_id(user_id=user_id)
            if master:
                master_id = master.id
            else:
                raise HTTPException(status_code=404, detail="Мастер не найден")
        if user_role == "salon":
            salon = await SalonRepository.get_salon_by_user_id(user_id=user_id)
            if salon:
                salon_id = salon.id
            else:
                raise HTTPException(status_code=404, detail="Салон не найден")
        else:
            raise HTTPException(status_code=403, detail="Роль пользователя не разрешена")

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
            # Загрузка фото
            photo_ids = await PhotoHandler.add_photos_to_service(
                images=images,  # Поддержка одного изображения
                model=CustomServicePhoto,
                slug=str(standard_service_id),
                city=str(city_id),
                role=user_role,
                image_type="IMAGE_TYPE"
            )

             # Связываем фото с услугой
            for photo_id in photo_ids:
                await ServiceCustomRepository.add_photos_to_custom_service(
                    custom_service_id=custom_service.id,
                    photo_id=photo_id
                )

        return custom_service
