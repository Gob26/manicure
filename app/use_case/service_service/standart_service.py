from typing import List, Optional, Dict
from tortoise.exceptions import DoesNotExist

from db.models import StandardService
from db.repositories.services_repositories.service_standart_repositories import ServiceStandartRepository
from config.components.logging_config import logger
from use_case.utils.slug_generator import generate_unique_slug


class StandardServiceService:
    @staticmethod
    async def create_standart_service(
            current_user: dict,
            **service_data: dict
    ) -> StandardService:
        """
        Создает новый стандартный сервис.
        """
        # Создаем копию данных, чтобы не модифицировать оригинальные
        create_data = service_data.copy()

        # Если slug не предоставлен, генерируем его
        if not create_data.get("slug"):
            create_data["slug"] = await generate_unique_slug(StandardService, create_data["name"])

        # Добавляем created_by
        create_data["created_by"] = current_user["user_id"]

        try:
            service = await ServiceStandartRepository.create_service_standart(**create_data)
            logger.info(f"Создан новый стандартный сервис: {service.name}")
            return service
        except Exception as e:
            logger.error(f"Ошибка при создании стандартного сервиса в репозитории: {e}")
            raise

    @staticmethod
    async def get_standart_service(service_id: int, current_user: dict) -> StandardService:
        """
        Получает стандартный сервис по ID.
        """
        try:
            service = await StandardService.get(id=service_id).prefetch_related(
                'category',
                'default_photo'
            )
            return service
        except DoesNotExist:
            raise ValueError(f"Сервис с ID {service_id} не найден")

    @staticmethod
    async def list_standart_services(
            current_user: dict,
            skip: int = 0,
            limit: int = 100
    ) -> List[StandardService]:
        """
        Получает список всех стандартных сервисов с пагинацией.
        """
        services = await StandardService.all().offset(skip).limit(limit).prefetch_related(
            'category',
            'default_photo'
        )
        return services

    @staticmethod
    async def update_standart_service(
            service_id: int,
            current_user: dict,
            **update_data
    ) -> StandardService:
        """
        Обновляет существующий стандартный сервис.
        """
        try:
            service = await StandardService.get(id=service_id)

            # Проверяем уникальность slug если он обновляется
            if 'slug' in update_data and update_data['slug'] != service.slug:
                exists = await StandardService.filter(slug=update_data['slug']).exists()
                if exists:
                    raise ValueError(f"Сервис со slug '{update_data['slug']}' уже существует")

            # Добавляем информацию об обновившем пользователе
            update_data['updated_by'] = current_user["user_id"]

            # Обновляем поля
            await service.update_from_dict(update_data).save()

            # Перезагружаем данные с связанными объектами
            await service.refresh_from_db()
            await service.fetch_related('category', 'default_photo')

            logger.info(f"Обновлен стандартный сервис: {service.name}")
            return service

        except DoesNotExist:
            raise ValueError(f"Сервис с ID {service_id} не найден")

    @staticmethod
    async def delete_standart_service(service_id: int, current_user: dict) -> None:
        """
        Удаляет стандартный сервис.
        """
        try:
            service = await StandardService.get(id=service_id)
            await service.delete()
            logger.info(f"Удален стандартный сервис с ID: {service_id}")
        except DoesNotExist:
            raise ValueError(f"Сервис с ID {service_id} не найден")

    @staticmethod
    async def check_service_exists(service_id: int) -> bool:
        """
        Проверяет существование сервиса по ID.
        """
        return await StandardService.filter(id=service_id).exists()