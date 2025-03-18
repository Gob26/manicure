from typing import Optional
from fastapi import HTTPException, status
from db.models import StandardService
from db.repositories.services_repositories.service_standart_repositories import ServiceStandartRepository
from db.schemas.service_schemas.service_standart_schemas import StandardServiceUpdate
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class StandardServiceService:
    @staticmethod
    async def create_standart_service(
            **service_data
    ) -> StandardService | None:

        try:
            category = await ServiceStandartRepository.get_category_by_id(service_data.get("category_id"))
            if not category:
                logger.warning(f"StandardServiceService.create_standart_service: Category with ID {service_data.get("category_id")} not found.")
                raise HTTPException(status_code=404, detail=f"Категория с ID {service_data.get("category_id")} не найдена")

            if not service_data.get("slug"):
                service_data["slug"] = await generate_unique_slug(StandardService, service_data.get("name"))

            service = await ServiceStandartRepository.create_service_standart(
                **service_data
            )
            logger.info(f"StandardServiceService.create_standart_service: Standard service created successfully: {service}")
            return service

        except Exception as e:
            logger.error(f"StandardServiceService.create_standart_service: Error creating standard service: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при создании сервиса.")

    @staticmethod
    async def update_standart_service(
            service_id: int,
            schema: StandardServiceUpdate
    ) -> StandardService:

        logger.debug(f"StandardServiceService.update_standart_service:  Получена схема: {schema}") # <----  Отладочный лог для схемы

        if not schema.slug: # <---- Используем schema.slug
            schema.slug = await generate_unique_slug(StandardService, schema.name) # <---- Используем schema.name


        try:
            update_service = await ServiceStandartRepository.update_service(service_id, schema=schema) # <---- Передаем schema
            logger.info(f"StandardServiceService.update_standart_service: Standard service ID {service_id} updated successfully.")
            return update_service

        except TypeError as e:
            logger.error(f"StandardServiceService.update_standart_service: TypeError updating standard service ID {service_id}: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при обновлении стандартной услуги."
            )
        except Exception as e:
            logger.error(f"StandardServiceService.update_standart_service: System error updating standard service ID {service_id}: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Системная ошибка при обновлении стандартной услуги."
            )
        
    @staticmethod
    async def get_standard_service_by_id(service_id: int):
        try:
            return await ServiceStandartRepository.get_service_by_id(service_id)
        except Exception as e:
            logger.error(f"StandardServiceService.get_standard_service_by_id: Error getting standard service by ID {service_id}: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получении стандартной услуги."
            )

    @staticmethod
    async def delete_service(service_id: int):
        try:
            return await ServiceStandartRepository.delete(service_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении стандартной услуги с ID {service_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при удалении стандартной услуги."
            )