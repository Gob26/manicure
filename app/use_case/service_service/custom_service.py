from typing import Any, List, Optional, Dict
from fastapi import HTTPException, UploadFile, status

from app.db.repositories.master_repositories.master_repositories import MasterRepository
from app.db.repositories.salon_repositories.salon_repositories import SalonRepository

from db.models import CustomService
from db.repositories.services_repositories.service_standart_repositories import ServiceStandartRepository
from db.repositories.services_repositories.service_custom_repositories import ServiceCustomRepository
from db.models.photo_models.photo_standart_service_model import CustomServicePhoto
from use_case.photo_service.photo_base_servise import PhotoHandler
from config.components.logging_config import logger
from use_case.utils.permissions import UserAccessService


class CustomServiceService():
    @staticmethod
    async def create_custom_service(
        current_user: dict,
        standard_service_id: int,
        base_price: float,
        duration_minutes: int,
        description: Optional[str],
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

        # Получаем master_id или salon_id
        master_or_salon_id = await UserAccessService.get_master_or_salon_id(
            user_role=user_role,
            user_id=user_id,
            master_repository=MasterRepository,
            salon_repository=SalonRepository
        )

        logger.info(f"Получен ID: {master_or_salon_id} для роли: {user_role}")

        logger.info(f"Создание пользовательской услуги с ID стандартной услуги {standard_service_id}")
        custom_service = await ServiceCustomRepository.create_custom_service(
            standard_service_id=standard_service_id,
            base_price=base_price,
            duration_minutes=duration_minutes,
            master_id=master_or_salon_id if user_role == 'master' else (master_id if master_id else None),
            salon_id=master_or_salon_id if user_role == 'salon' else (salon_id if salon_id else None),
            description=description,
            is_active=True,
        )

        return custom_service


    @staticmethod
    async def update_custom_service(
            current_user: dict,
            custom_service_id: int,
            updated_service_data: Dict[str, Any],
    ) -> CustomService:

        try:
            # Загружаем услугу с полной информацией
            custom_service = await ServiceCustomRepository.get_custom_service_by_id(id=custom_service_id)

            if not custom_service:
                raise HTTPException(status_code=404, detail=f"Услуга не найдена " )

            # Проверка прав
            user_id = current_user.get("user_id")
            user_role = current_user.get("role")

            # Проверяем права на обновление услуги
            await UserAccessService.check_admin_or_owner_permission(
                user_role=user_role,
                user_id=user_id,
                custom_service=custom_service,
                master_repository=MasterRepository,
                salon_repository=SalonRepository
            )

            # Обновление данных услуги
            custom_service = await ServiceCustomRepository.update_service(custom_service_id, updated_service_data)


            await custom_service.fetch_related("standard_service", "master", "salon", "attributes", "custom_service_photos")
            return custom_service

        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logger.error(f"Ошибка при обновлении услуги {custom_service_id}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при обновлении услуги")
        


    @staticmethod
    async def delete_custom_service(
        custom_service_id: int,
        current_user: dict,
    ):
        """
        Удаляет услугу после проверки прав.

        :param custom_service_id: ID услуги, которую нужно удалить.
        :param current_user: Данные текущего пользователя.
        :param custom_service_repository: Репозиторий для работы с услугами.
        :param master_repository: Репозиторий для работы с мастерами.
        :param salon_repository: Репозиторий для работы с салонами.
        :raises HTTPException: Если пользователь не имеет прав или услуга не найдена.
        """
        user_id = current_user.get("user_id")
        user_role = current_user.get("role")

        # Получение услуги из базы данных
        custom_service = await ServiceCustomRepository.get_custom_service_by_id(custom_service_id)
        if not custom_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Услуга с ID {custom_service_id} не найдена"
            )

        # Проверка прав на удаление услуги
        await UserAccessService.check_admin_or_owner_permission(
            user_role=user_role,
            user_id=user_id,
            custom_service=custom_service,
            master_repository=MasterRepository,
            salon_repository=SalonRepository
        )

        # Удаление услуги
        try:
            await ServiceCustomRepository.delete_custom_service_by_id(custom_service_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при удалении услуги: {str(e)}"
            )

        return {"detail": f"Услуга с ID {custom_service_id} успешно удалена"}

            