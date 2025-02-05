from typing import Optional, Any, List
from fastapi import HTTPException, status

from db.repositories.job_repositories.salon_master_invitation_repositories import InvitationRepository
from db.schemas.job_schemas.salon_master_invitation_schemas import SalonMasterInvitationCreateSchema, SalonMasterInvitationResponseSchema

from use_case.utils.permissions import UserAccessService
from config.components.logging_config import logger

class InvitationService:
    @staticmethod
    async def create_invitation(
        data: SalonMasterInvitationCreateSchema,
    ) -> SalonMasterInvitationResponseSchema:
        try:
            invitation = await InvitationRepository.create_invitation(**data)
            return SalonMasterInvitationResponseSchema(**invitation.__dict__)
        except Exception as e:
            logger.error(f"Ошибка при отправке приглашения: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при отправке приглашения")
            
