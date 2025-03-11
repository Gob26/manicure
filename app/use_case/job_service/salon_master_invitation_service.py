from typing import Optional, Any, List
from fastapi import HTTPException, status

from db.repositories.job_repositories.salon_master_invitation_repositories import InvitationRepository
from db.repositories.master_repositories.master_repositories import MasterRepository
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from db.schemas.job_schemas.salon_master_invitation_schemas import SalonMasterInvitationCreateSchema, SalonMasterInvitationResponseSchema

from use_case.utils.permissions import UserAccessService
from config.components.logging_config import logger

class InvitationService:
    @staticmethod
    async def create_invitation(
        data: SalonMasterInvitationCreateSchema,
        current_user: dict
    ) -> SalonMasterInvitationResponseSchema:
        try:
            user_id = current_user.get("user_id")
            user_role = current_user.get("role")

            # Получаем salon_id (если пользователь - салон или админ)
            salon_id = await UserAccessService.get_master_or_salon_id(
                user_role=user_role,
                user_id=user_id,
                master_repository=MasterRepository,
                salon_repository=SalonRepository
            )

            # Преобразуем данные в словарь и добавляем salon_id
            data_dict = data.dict()
            data_dict["salon_id"] = salon_id

            # Создаем приглашение, передавая словарь через оператор распаковки
            invitation = await InvitationRepository.create_invitation(**data_dict)

            return SalonMasterInvitationResponseSchema(**invitation.__dict__)
        except Exception as e:
            logger.error(f"Ошибка при отправке приглашения: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при отправке приглашения")

            
