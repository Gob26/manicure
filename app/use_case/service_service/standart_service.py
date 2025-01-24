from typing import Optional, List
from fastapi import HTTPException
from db.models import StandardService
from db.repositories.services_repositories.service_standart_repositories import ServiceStandartRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger

class StandardServiceService:
    @staticmethod
    async def create_standart_service(
            name: str,
            title: str,
            content: str,
            slug: str,
            category_id: int,
            default_photo_id: Optional[List[int]] = None
    ) -> StandardService:
        try:
            category = await ServiceStandartRepository.get_category_by_id(category_id)
            if not category:
                raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")

            if not slug:
                slug = await generate_unique_slug(StandardService, name)

            create_data = {
                "name": name,
                "title": title,
                "content": content,
                "slug": slug,
                "category_id": category_id,
            }

            service = await ServiceStandartRepository.create_service_standart(**create_data)

            if default_photo_id:
                for photo_id in default_photo_id:
                    await ServiceStandartRepository.link_photo_to_service(service.id, photo_id)

            await service.fetch_related('category', 'default_photo')  # Eager loading after creation

            return service

        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Ошибка при создании стандартного сервиса: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при создании сервиса.")