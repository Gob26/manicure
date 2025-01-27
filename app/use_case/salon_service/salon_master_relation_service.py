from typing import Optional, Any, List
from fastapi import HTTPException, status

from db.repositories.master_repositories.master_repositories import MasterRepository
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from db.schemas.salon_schemas.salon_master_relation_schemas import SalonMasterRelationCreate, SalonMasterRelationResponse
from db.repositories.salon_repositories.salon_master_relation_repositoies import SalonMasterRelationRepository
from use_case.utils.permissions import UserAccessService
from config.components.logging_config import logger


class SalonMasterRelationService:
    @staticmethod
    async def create_relation_salon_master(
            data: SalonMasterRelationCreate,
            current_user: dict,
    ) -> SalonMasterRelationResponse:
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

        # Преобразуем data в словарь и добавляем salon_id
        data_dict = data.dict()
        data_dict["salon_id"] = master_or_salon_id

        try:
            logger.info(f"Создание связи мастера и салона с данными: {data_dict}")
            # Создаем связь через репозиторий
            relation = await SalonMasterRelationRepository.create_relation(
                salon_id=data_dict["salon_id"],
                master_id=data_dict["master_id"]
            )
            # Возвращаем объект через распаковку __dict__
            return SalonMasterRelationResponse(**relation.__dict__)
        except Exception as e:
            logger.error(f"Ошибка при создании связи: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось создать связь между мастером и салоном"
            )

    @staticmethod
    async def delete_custom_service(
            relation_id: int,
            current_user: dict,
):


