from typing import Optional, Any, List
from fastapi import HTTPException, status

from db.schemas.salon_schemas.salon_master_relation_schemas import SalonMasterRelationCreate, SalonMasterRelationResponse
from db.repositories.salon_repositories.salon_master_relation_repositoies import SalonMasterRelationRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class SalonMasterRelationService:
    @staticmethod
    async def create_relation_salon_master(data: SalonMasterRelationCreate) -> SalonMasterRelationResponse:
        try:
            logger.info(f"Создание связи мастера и салона с данными: {data}")
            # Создаем связь через репозиторий
            relation = await SalonMasterRelationRepository.create_relation(
                salon_id=data.salon_id, 
                master_id=data.master_id
            )
            # Возвращаем объект через распаковку __dict__
            return SalonMasterRelationResponse(**relation.__dict__)
        except Exception as e:
            logger.error(f"Ошибка при создании связи: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось создать связь между мастером и салоном"
            )

