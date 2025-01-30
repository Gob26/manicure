from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from tortoise.transactions import atomic

from db.models.salon_models.salon_master_relation import SalonMasterRelation
from db.repositories.base_repositories.base_repositories import BaseRepository
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
    
    
    #получаем id салона и id мастера
    @classmethod
    async def get_id_master_salon(cls, relation_id: int) -> Optional[Dict[str, Any]]:
        relation = await cls.model.get_or_none(id=relation_id)
        if not relation:
            return None
        return {
            "salon_id": relation.salon_id,
            "master_id": relation.master_id
        }
    
    #получаем связь по id
    @classmethod
    async def get_relation_by_id(cls, relation_id: int) -> Optional[SalonMasterRelation]:
        return await cls.get_or_none(id=relation_id)
    
    @classmethod
    async def update_relation(cls, relation_id: int, **update_data):
        relation = await cls.get_or_none(relation_id)
        if not relation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Связь не найдена"
            )

        # Применяем изменения только к переданным полям
        for key, value in update_data.items():
            setattr(relation, key, value)

        await relation.save()
        return relation

    
    #удаляем связь мастера и салона
    @classmethod
    async def delete_relation(cls, id: int):
        await cls.delete(id=id)
