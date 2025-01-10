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
        title: str,
        description: str,
        price: int,
        duration: int,
        text: str,
        slug: str = None,
    ) -> StandardService:
        if not current_user["is_admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет прав на создание стандартного сервиса",
            )

        if not slug:
            slug = generate_unique_slug(title)

        service_data = {
            "title": title,
            "description": description,
            "price": price,
            "duration": duration,
            "text": text,
            "slug": slug,
        }

        service = await ServiceStandartRepository.create(**service_data)
        logger.info(f"create_standart_service: стандартный сервис с ID {service.id} успешно создан")
        return service


