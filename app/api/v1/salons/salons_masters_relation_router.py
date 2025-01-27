from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from typing import Optional, List
from app.use_case.salon_service.salon_master_relation_service import SalonMasterRelationService
from app.use_case.utils.jwt_handler import get_current_user
from db.models.salon_models.salon_master_relation import SalonMasterRelation
from db.schemas.salon_schemas.salon_master_relation_schemas import SalonMasterRelationCreate, SalonMasterRelationResponse
from use_case.utils.permissions import UserAccessService
from config.components.logging_config import logger


salon_master_relation_router = APIRouter()

@salon_master_relation_router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=SalonMasterRelationResponse,
    summary="Создание связи мастера и салона",
    description="Создает связь мастера и салона.",
    tags=["SalonMasterRelation"],
)
async def create_salon_master_relation(
    data: SalonMasterRelationCreate,
    current_user: dict = Depends(get_current_user),
):
    UserAccessService.check_user_permission(current_user, ["salon", "admin", "master"])

    logger.info(f"Текущий пользователь: {current_user}")
    try:
        return await SalonMasterRelationService.create_relation_salon_master(
            data=data,
            current_user=current_user
        )
    except Exception as e:
        logger.error(f"Системная ошибка при создании связи мастера и салона: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при создании связи мастера и салона")


@salon_master_relation_router.delete(
    "/{relation_id}",
    status_code=status.HTTP_200_OK,
    summary="Удаление связи мастера и салона",
    description="Удаляет существующую связь между мастером и салоном.",
    tags=["SalonMasterRelation"],
)
async def delete_salon_master_relation(
    relation_id: int,
    current_user: dict = Depends(get_current_user),
):
    UserAccessService.check_user_permission(current_user, ["salon", "admin", "master"])
    logger.info(f"Запрос на удаление связи {relation_id}. Пользователь: {current_user}")

    try:
        success = await SalonMasterRelationService.delete_relation_salon_master(
            relation_id=relation_id,
            current_user=current_user
        )
        if not success:
            logger.warning(f"Связь {relation_id} не найдена")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relation not found"
            )
        logger.info(f"Связь {relation_id} успешно удалена")
        return {"message": "Relation deleted successfully"}
    except HTTPException as e:
        logger.warning(f"Ошибка доступа при удалении связи {relation_id}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Системная ошибка при удалении связи {relation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Системная ошибка при удалении связи"
        )