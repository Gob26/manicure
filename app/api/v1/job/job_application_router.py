from fastapi import APIRouter, Depends, HTTPException, status
from app.use_case.job_service.job_application_service import JobApplicationService
from db.schemas.job_schemas.job_application_schemas import JobApplicationCreateSchema, JobApplicationResponseSchema
from app.use_case.utils.jwt_handler import get_current_user
from use_case.utils.permissions import UserAccessService
from config.components.logging_config import logger


job_application_router = APIRouter()

@job_application_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=JobApplicationResponseSchema,
    summary="Создание заявки мастером",
    description="Мастер выбирает вакансию и отправляет заявку, указывая сообщение (например, мотивационное письмо).",
)
async def create_job_application_master(
        data: JobApplicationCreateSchema,
        current_user: dict = Depends(get_current_user),
):
    
    try:
        UserAccessService.check_user_permission(current_user, ["master"], ["admin"])

        result = await JobApplicationService.create_job_application(
            data=data,
            current_user=current_user
        )
        return result
    except HTTPException as http_ex:
        # Пробрасываем HTTP исключения дальше
        raise http_ex
    except Exception as e:
        logger.error(f"Ошибка при создании вакансии: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании вакансии: {str(e)}"
        )