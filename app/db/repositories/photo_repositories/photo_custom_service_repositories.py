from typing import Any, Optional, List, Type, TypeVar
from tortoise import models
from db.models.photo_models.photo_standart_service_model import StandardServicePhoto
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger


T = TypeVar("T", bound=models.Model)

class PhotoRepository(BaseRepository):