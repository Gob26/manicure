from typing import Optional, List, Union, Any
from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist
from db.models.services_models.category_model import Category
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger


class ServiceCategoryRepository(BaseRepository):
    model = Category

    @classmethod
    async def create_category(cls, **kwargs: Any) -> Category:
        logger.info(f"Мастер создан с данными: {kwargs}")
        return await cls.create(**kwargs)
