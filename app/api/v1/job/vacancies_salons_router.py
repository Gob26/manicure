from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from app.use_case.salon_service.salon_master_relation_service import SalonMasterRelationService
from app.use_case.utils.jwt_handler import get_current_user
from db.schemas.job_schemas.vacancy_salon_schemas import VacancyCreateSchema, VacancyResponseSchema
from use_case.job_service.vacancy_salon_service import VacancyService
from use_case.utils.permissions import UserAccessService
from config.components.logging_config import logger


vacancy_router = APIRouter()

@vacancy_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=VacancyResponseSchema,
    summary="Создание вакансии",
    description="Создает вакансии для салона.",
)
async def create_vacancy(
        data: VacancyCreateSchema,
        current_user: dict = Depends(get_current_user),
):
    try:
        # Проверка прав доступа
        UserAccessService.check_user_permission(current_user, ["admin", "salon"])

        # Создание вакансии
        result = await VacancyService.create_vacancy_salon(
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