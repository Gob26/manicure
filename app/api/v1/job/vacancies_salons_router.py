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

@vacancy_router.delete(
    "/{vacancy_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление вакансии",
    description="Удаляем вакансию салона",
)
async def delete_vacancy(
        vacancy_id: int,
        current_user: dict = Depends(get_current_user),
):
    UserAccessService.check_user_permission(current_user, ["salon", "admin"])
    logger.info(f"Запрос на удаление вакансии {vacancy_id}. Пользователь: {current_user}")

    try:
        success = await VacancyService.delete_vacancy_salon(
            vacancy_id=vacancy_id,
            current_user=current_user
        )
        if not success:
            logger.warning(f"Вакансия {vacancy_id} не найдена")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relation not found"
            )
        logger.info(f"Вакансия {vacancy_id} успешно удалена")
        return {"message": "Вакансия была удалена"}
    except HTTPException as e:
        logger.warning(f"Ошибка доступа при удалении Вакансии {vacancy_id}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Системная ошибка при удалении Вакансии {vacancy_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Системная ошибка при удалении Вакансии"
        )

