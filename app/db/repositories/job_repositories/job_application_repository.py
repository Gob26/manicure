from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from tortoise.transactions import atomic

from db.models.job.job_application import JobApplication
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger


class JobApplicationRepository(BaseRepository):
    model = JobApplication

    @classmethod
    async def create_job_application(cls, **kwargs: Any) -> JobApplication:
        return await cls.create(**kwargs)