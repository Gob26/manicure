from typing import List
from fastapi import APIRouter, HTTPException, status
from use_case.salon_service.salon_read_service import SalonListService
from db.schemas.salon_schemas.salon_schemas import SalonListSchema
from config.components.logging_config import logger

salon_list_router = APIRouter()


@salon_list_router.get(
    "/{city_slug}/salon",
    response_model=List[SalonListSchema],
    summary="Получение салонов города",
    description="Получить салоны определенного города по слагу"
)
async def get_salon_by_city_slug(city_slug: str):
    """
    Получение списка мастеров для города по slug
    """
