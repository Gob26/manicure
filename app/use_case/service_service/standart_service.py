from typing import Optional, Dict
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from db.models import StandardService, StandardServicePhoto, Category
from db.repositories.services_repositories.category_service_repositories import ServiceCategoryRepository
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
            default_photo_id: Optional[int] = None,
    ) -> StandardService:
        try:
            # Проверяем существование категории
            category = await StandardServiceService.get_category_by_id(category_id)
            if not category:
                raise HTTPException(
                    status_code=404,
                    detail=f"Category with ID {category_id} not found"
                )
            if not slug:
                slug = await generate_unique_slug(StandardService, name)

            create_data = {
                "name": name,
                "title": title,
                "content": content,
                "slug": slug,
                "category_id": category_id,
            }

            if default_photo_id:
                create_data["default_photo_id"] = default_photo_id

            # Создание услуги
            service = await ServiceStandartRepository.create_service_standart(**create_data)

            # Загружаем связанные данные
            await service.fetch_related('category', 'default_photo') # Ленивая загрузка

            return service

        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Ошибка при создании стандартного сервиса: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при создании сервиса.")

    @staticmethod
    async def link_photo_to_service(service_id: int, photo_id: int) -> None:
        """
        Привязывает фото к услуге, обновляя default_photo_id.
        """
        try:
            service = await StandardService.get_or_none(id=service_id)
            if not service:
                raise HTTPException(
                    status_code=404,
                    detail=f"Сервис с ID {service_id} не найден."
                )

            photo = await StandardServicePhoto.get_or_none(id=photo_id)
            if not photo:
                raise HTTPException(
                    status_code=404,
                    detail=f"Фото с ID {photo_id} не найдено."
                )

            service.default_photo_id = photo.id
            await service.save()

            logger.info(f"Фото с ID: {photo_id} успешно привязано к сервису ID: {service_id}")
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Ошибка при привязке фото к сервису: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при привязке фото к сервису.")

    @staticmethod
    async def get_category_by_id(category_id: int) -> Optional[Category]:
        """
        Возвращает категорию по её ID или None, если не найдена.
        """
        try:
            category = await ServiceCategoryRepository.get_category_id(category_id=category_id)
            return category
        except DoesNotExist:
            return None
