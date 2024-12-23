from typing import Optional, List, Union
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction

from db.models.services_models.service_custom_model import CustomService
from db.models.master_models.master_model import Master
from db.models.location.city import City
from config.components.logging_config import logger


class MasterRepository:
    @staticmethod
    async def get_master_by_id(master_id: int) -> Optional[Master]:
        """Получение мастера по ID."""
        try:
            return await Master.get(id=master_id).prefetch_related("user", "services", "city", "applications", "relations")
        except DoesNotExist:
            logger.info(f"Мастер с ID {master_id} не найден.")
            return None

    @staticmethod
    async def get_all_masters(limit: int = 10, offset: int = 0) -> List[Master]:
        """Получение всех мастеров с пагинацией."""
        return await Master.all().offset(offset).limit(limit).prefetch_related("city", "user", "relations", "services")

    @staticmethod
    async def create_master(**kwargs) -> Master:
        """Создание мастера."""
        master = await Master.create(**kwargs)
        logger.info(f"Мастер создан с данными: {kwargs}")
        return master

    @staticmethod
    async def is_slug_used(slug: str) -> bool:
        """Проверка, используется ли slug."""
        slug_exists = await Master.filter(slug=slug).exists()
        logger.debug(f"Slug '{slug}' используется: {slug_exists}")
        return slug_exists

    @staticmethod
    async def get_master_by_user_id(user_id: int) -> Optional[Master]:
        """Получение мастера по ID пользователя."""
        return await Master.filter(user_id=user_id).first()

    @staticmethod
    async def get_masters_by_city(city: City, limit: int = 10, offset: int = 0) -> List[Master]:
        """Получить мастеров по городу."""
        return await Master.filter(city=city).offset(offset).limit(limit).prefetch_related("services", "user")

    @staticmethod
    async def update_master(master_id: int, **kwargs) -> Union[Master, None]:
        """Обновление данных мастера."""
        async with in_transaction() as conn:
            updated = await Master.filter(id=master_id).using_db(conn).update(**kwargs)
            if updated:
                logger.info(f"Мастер с ID {master_id} обновлен с данными: {kwargs}")
                return await Master.get(id=master_id)
            else:
                logger.warning(f"Не удалось обновить мастера с ID {master_id}.")
                return None

    @staticmethod
    async def delete_master(master_id: int) -> int:
        """Удаление мастера."""
        deleted_count = await Master.filter(id=master_id).delete()
        logger.info(f"Удалено мастеров с ID {master_id}: {deleted_count}")
        return deleted_count

    @staticmethod
    async def get_masters_with_specialty(specialty: str, limit: int = 10, offset: int = 0) -> List[Master]:
        """Получение мастеров по специализации."""
        return await Master.filter(specialty__icontains=specialty).offset(offset).limit(limit)

    @staticmethod
    async def add_service_to_master(master_id: int, service_id: int) -> bool:
        """Добавление услуги мастеру."""
        try:
            master = await Master.get(id=master_id)
            service = await CustomService.get(id=service_id)
            await master.services.add(service)
            logger.info(f"Услуга {service_id} добавлена мастеру {master_id}.")
            return True
        except DoesNotExist:
            logger.error(f"Мастер {master_id} или услуга {service_id} не найдены.")
            return False

    @staticmethod
    async def get_master_applications(master_id: int) -> List:
        """Получение всех заявок мастера."""
        try:
            master = await Master.get(id=master_id).prefetch_related("applications")
            return await master.applications.all()
        except DoesNotExist:
            logger.warning(f"Мастер с ID {master_id} не найден.")
            return []

    @staticmethod
    async def get_related_salon_masters(master_id: int) -> List:
        """Получение связей мастера с салонами."""
        try:
            master = await Master.get(id=master_id).prefetch_related("relations")
            return await master.relations.all()
        except DoesNotExist:
            logger.warning(f"Мастер с ID {master_id} не найден.")
            return []

    @staticmethod
    async def bulk_create_masters(masters_data: List[dict]) -> List[Master]:
        """Массовое создание мастеров."""
        async with in_transaction() as conn:
            masters = await Master.bulk_create([Master(**data) for data in masters_data], batch_size=100)
            logger.info(f"Создано {len(masters)} мастеров.")
            return masters
