from fastapi import APIRouter, HTTPException, status
from use_case.master_service.master_read_service import MasterReadService
from db.schemas.master_schemas.master_schemas import MasterCreateSchema
from config.components.logging_config import logger


master_read_router = APIRouter()


# Получение мастера по slug
@master_read_router.get(
    "/{city_slug}/masters/{master_slug}",
    response_model=MasterCreateSchema,
    summary="Получение мастера по slug города и slug мастера"
)
async def get_master_by_city_and_slug_route(city_slug: str, master_slug: str):
    """
    Получение мастера по slug города и slug мастера.
    """
    return await MasterReadService.get_master(city_slug, master_slug)

