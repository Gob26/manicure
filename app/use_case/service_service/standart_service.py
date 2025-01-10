from typing import Optional
from typing import Any
from fastapi import HTTPException, status

from db.models.services_models.service_standart_model import StandardService
from db.repositories.services_repositories.service_standart_repositories import ServiceStandartRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class StandardServiceService:
    @staticmethod
    async def create_standart_service(
        current_user: dict,
        category_id: int,
        name: str,
        title: str,
        description: str,
        content: str,
        slug: str,
        
        
        


