from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from tortoise.expressions import Q
from tortoise.transactions import atomic
from tortoise.functions import Count

from db.models.salon_models.salon_master_relation import SalonMasterRelation
from db.repositories.base_repositories.base_repositories import BaseRepository
from db.schemas.salon_schemas.salon_master_relation_schemas import SalonMasterRelationResponse, SalonMasterRelationCreate
from config.components.logging_config import logger


class SalonMasterRelationRepository(BaseRepository):
    model = SalonMasterRelation

    @classmethod
    @atomic()
    async def create_relation(cls, salon_id: int, master_id: int) -> SalonMasterRelation:
        # Проверяем существование связи
        existing_relation = await cls.model.filter(salon_id=salon_id, master_id=master_id).first()
        if existing_relation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Связь между этим салоном и мастером уже существует"
            )
        # Создаем новую связь
        relation = await cls.model.create(salon_id=salon_id, master_id=master_id, status="pending")
        logger.info(f"Связь создана: Salon {salon_id} -> Master {master_id}")
        return relation