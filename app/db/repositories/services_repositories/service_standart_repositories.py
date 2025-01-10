from typing import Optional, List, Union, Any
from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist
from db.models.services_models.service_standart_model import StandardService
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger


class ServiceStandartRepository(BaseRepository):
    model = StandardService
