from typing import Any, List, Optional, Dict
from fastapi import HTTPException, UploadFile
from tortoise.exceptions import DoesNotExist
from app.db.repositories.photo_repositories.photo_standard_service_repository import PhotoRepository
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
from use_case.photo_service.photo_custom_service import PhotoCustomRepository
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

        standard_service = await ServiceStandartRepository.get_service_by_id(service_id=standard_service_id)
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

    @staticmethod
    async def update_custom_service(
            current_user: dict,
            custom_service_id: int,
            updated_service_data: Dict[str, Any],
            images: Optional[List[UploadFile]],
    ) -> CustomService:
        try:
            # Загружаем услугу с полной информацией
            custom_service = await ServiceCustomRepository.get_custom_service_by_id(id=custom_service_id)
            await custom_service.fetch_related("master", "salon")

            if not custom_service:
                raise HTTPException(status_code=404, detail="Услуга не найдена")

            # Проверка прав
            user_id = current_user.get("user_id")
            user_role = current_user.get("role")

            # Проверка прав для администратора или владельца услуги
            if user_role != "admin":
                if custom_service.master and custom_service.master.user_id != user_id:
                    if custom_service.salon and custom_service.salon.user_id != user_id:
                        raise HTTPException(status_code=403, detail="Нет прав для обновления этой услуги")

            # Обновление данных услуги
            custom_service = await ServiceCustomRepository.update_service(custom_service_id, updated_service_data)

            # Работа с фотографиями (без изменений)
            if images:
                await PhotoCustomRepository.delete_by_custom_service_id(custom_service_id)

                try:
                    photo_ids = await PhotoHandler.add_photos_to_service(
                        images,
                        CustomServicePhoto,
                        str(custom_service_id),
                        str(current_user.get("city_id")),
                        current_user.get("role"),
                        "IMAGE_TYPE",
                    )
                    for photo_id in photo_ids:
                        await ServiceCustomRepository.add_photos_to_custom_service(
                            custom_service_id=custom_service.id,
                            photo_id=photo_id
                        )
                except Exception as photo_error:
                    logger.error(f"Ошибка при загрузке фото: {photo_error}", exc_info=True)
                    raise HTTPException(status_code=500, detail="Ошибка при загрузке фото")

            await custom_service.fetch_related("standard_service", "master", "salon", "attributes", "photos")
            return custom_service

        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logger.error(f"Ошибка при обновлении услуги {custom_service_id}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при обновлении услуги")