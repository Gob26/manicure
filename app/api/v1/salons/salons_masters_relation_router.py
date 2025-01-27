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
    UserAccessService.check_user_permission(current_user, ["salon", "admin"])

    logger.info(f"Текущий пользователь: {current_user}")
    try:
        return await SalonMasterRelationService.create_relation_salon_master(**data.dict())
    except Exception as e:
        logger.error(f"Системная ошибка при создании связи мастера и салона: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при создании связи мастера и салона")


