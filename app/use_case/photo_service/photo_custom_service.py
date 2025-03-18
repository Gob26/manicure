from typing import Dict, List
from fastapi import HTTPException, UploadFile
from app.db.repositories.master_repositories.master_repositories import MasterRepository
from app.db.repositories.salon_repositories.salon_repositories import SalonRepository
from app.db.repositories.services_repositories.service_custom_repositories import ServiceCustomRepository
from app.use_case.photo_service.photo_base_servise import PhotoHandler
from app.use_case.utils.permissions import UserAccessService
from db.models.photo_models.photo_standart_service_model import CustomServicePhoto
from config.components.logging_config import logger


class CustomServicePhotoService:

    MAX_PHOTOS_PER_SERVICE = 30

    @staticmethod
    async def upload_photo_for_custom_service(
        custom_service_id: int, 
        images: List[UploadFile],
        current_user: Dict[str, str]
    ) -> List[int]:
        """
        Загружает фотографии для услуги, проверяя права пользователя.

        Args:
            custom_service_id (int): ID услуги, к которой привязываются фото.
            images (List[UploadFile]): Список загружаемых файлов изображений.
            current_user (dict): Информация о текущем пользователе (`user_id`, `role`, `city_id`).

        Returns:
            List[int]: Список ID загруженных изображений.

        Raises:
            HTTPException: 404 - Услуга не найдена.
            HTTPException: 403 - Недостаточно прав.
            HTTPException: 500 - Ошибка при загрузке фото.
        """
        try:
            # Загружаем услугу
            custom_service = await ServiceCustomRepository.get_custom_service_by_id(custom_service_id)
            if not custom_service:
                raise HTTPException(status_code=404, detail="Услуга не найдена")

            # Проверяем права пользователя
            user_id = current_user.get("user_id")
            user_role = current_user.get("role")
            city_id = current_user.get("city_id")

            await UserAccessService.check_admin_or_owner_permission(
                user_role=user_role,
                user_id=user_id,
                custom_service=custom_service,
                master_repository=MasterRepository,
                salon_repository=SalonRepository
            )
            # Проверяем количество фотографий для услуги
            existing_photos_count = await PhotoHandler.get_photo_count(model=CustomServicePhoto, id=custom_service_id)

            if len(images) + existing_photos_count > CustomServicePhotoService.MAX_PHOTOS_PER_SERVICE:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Превышено максимальное количество фотографий для услуги. "
                        f"Максимум: {CustomServicePhotoService.MAX_PHOTOS_PER_SERVICE} фотографий. "
                        f"Текущее количество загруженных фотографий: {existing_photos_count}."
                    )
                )

            try:
                # Загрузка фотографий
                photo_ids = await PhotoHandler.add_photos_to_custom_service(
                    images=images,
                    service_id=custom_service_id,
                    model=CustomServicePhoto,
                    city=str(city_id)
                )

                last_uploaded_photo_id = photo_ids[-1]

                await PhotoHandler.update_photo_is_main(CustomServicePhoto,entity_field="custom_service_id",entity_id=custom_service_id,photo_id=last_uploaded_photo_id, )

                logger.info(f"Загружены фото для услуги {custom_service_id}: {photo_ids}")
                return photo_ids

            except Exception as e:
                logger.error(f"Ошибка при загрузке фото для услуги {custom_service_id}: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Ошибка при загрузке фото: {str(e)}")

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Ошибка в upload_photo_for_custom_service: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Ошибка при загрузке фото: {str(e)}")


    @staticmethod
    async def delete_photo_for_custom_service(
            photo_id: int,
            current_user: Dict[str, str],
    ) -> None:
        """
        Удаляет фото, привязанное к услуге, с проверкой прав пользователя.

        Args:
            photo_id (int): Уникальный идентификатор фотографии.
            current_user (dict): Информация о текущем пользователе (ключи `user_id`, `role`).

        Raises:
            HTTPException: 404 - Фото не найдено.
            HTTPException: 404 - Услуга не найдена.
            HTTPException: 403 - Недостаточно прав на удаление фото.
            HTTPException: 500 - Ошибка при удалении фото.
        """
        try:
            # Получаем фотографию из базы
            photo = await PhotoHandler.get_photo_by_id(model=CustomServicePhoto, id=photo_id)
            if not photo:
                raise HTTPException(status_code=404, detail="Фотография не найдена")

            # Получаем услугу, к которой относится фото
            custom_service = await ServiceCustomRepository.get_custom_service_by_id(id=photo.custom_service_id)
            if not custom_service:
                raise HTTPException(status_code=404, detail="Услуга не найдена")

            # Проверяем права пользователя
            user_id = current_user.get("user_id")
            user_role = current_user.get("role")

            await UserAccessService.check_admin_or_owner_permission(
                user_role=user_role,
                user_id=user_id,
                custom_service=custom_service,
                master_repository=MasterRepository,
                salon_repository=SalonRepository
            )

            # Удаляем фото
            await PhotoHandler.delete_photo(photo_id=photo_id, model=CustomServicePhoto)
            logger.info(f"Фото (ID: {photo_id}) успешно удалено.")

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Ошибка при удалении фото (ID: {photo_id}): {str(e)}")
            raise HTTPException(status_code=500, detail=f"Ошибка при удалении фото: {str(e)}")