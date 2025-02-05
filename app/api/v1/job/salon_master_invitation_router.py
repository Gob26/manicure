from fastapi import APIRouter, Depends, HTTPException, status

from app.use_case.job_service.salon_master_invitation_service import InvitationService
from db.schemas.job_schemas.salon_master_invitation_schemas import SalonMasterInvitationCreateSchema, SalonMasterInvitationResponseSchema
from app.use_case.utils.jwt_handler import get_current_user
from use_case.utils.permissions import UserAccessService
from config.components.logging_config import logger

invitation_router = APIRouter()

@invitation_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SalonMasterInvitationResponseSchema,
    summary="Отправка приглашения мастеру",
    description="Салон отправляет приглашение мастеру, возможно, с привязкой к вакансии.",
    tags=["Приглашения"],
)
async def create_invitation(
        data: SalonMasterInvitationCreateSchema,
        current_user: dict = Depends(get_current_user),
):
    # Проверяем, что роль пользователя — салон или админ
    UserAccessService.check_user_permission(current_user, ["salon", "admin"])
    try:
        return await InvitationService.create_invitation(data)
    except Exception as e:
        logger.error(f"Ошибка при отправке приглашения: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при отправке приглашения")
