from typing import Optional, List, Union, Any
from db.models.services_models.service_custom_model import CustomService
from db.models.master_models.master_model import Master
from db.models.location.city import City
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger


class MasterRepository(BaseRepository):
    model = Master

    @classmethod
    async def create_master(cls, **kwargs: Any) -> Master:
        """Создание мастера с использованием базового метода."""
        master = await cls.create(**kwargs)
        logger.info(f"Мастер создан с данными: {kwargs}")
        return master

    @classmethod
    async def get_master_by_id(cls, master_id: int) -> Optional[Master]:
        """Получение мастера по ID в одной таблице."""
        return await cls.get_by_id(master_id)

    @classmethod
    async def get_master_by_id_all(cls, master_id: int) -> Optional[Master]:
        """Получение мастера по ID загружая связанные объекты."""
        return await cls.get_by_id_with_related(
            master_id,
            "user", "services", "city", "applications", "relations"
        )

#    @classmethod
 #   async def get_all_masters(cls, limit: int = 10, offset: int = 0) -> List[Master]:
  #      """Получение всех мастеров с пагинацией."""
   #     return await cls.get_all(
    #        limit=limit,
     #       offset=offset,
      #      "city", "user", "relations", "services"
       # )

    @classmethod
    async def is_slug_used(cls, slug: str) -> bool:
        """Проверка, используется ли slug."""
        return await cls.exists(slug=slug)

    @classmethod
    async def get_master_by_user_id(cls, user_id: int) -> Optional[Master]:
        """Получение мастера по ID пользователя."""
        return await cls.get_or_none(user_id=user_id)

    @classmethod
    async def get_masters_by_city(cls, city: City, limit: int = 10, offset: int = 0) -> List[Master]:
        """Получить мастеров по городу."""
        return await cls.filter(
            limit=limit,
            offset=offset,
            city=city
        )

    @classmethod
    async def get_masters_with_specialty(cls, specialty: str, limit: int = 10, offset: int = 0) -> List[Master]:
        """Получение мастеров по специализации."""
        return await cls.filter(
            limit=limit,
            offset=offset,
            specialty__icontains=specialty
        )

    @classmethod
    async def add_service_to_master(cls, master_id: int, service_id: int) -> bool:
        """Добавление услуги мастеру."""
        try:
            master = await cls.get_by_id(master_id)
            service = await CustomService.get(id=service_id)
            if master and service:
                await master.services.add(service)
                logger.info(f"Услуга {service_id} добавлена мастеру {master_id}.")
                return True
            return False
        except Exception as e:
            logger.error(f"Ошибка при добавлении услуги {service_id} мастеру {master_id}: {e}")
            return False

    @classmethod
    async def get_master_applications(cls, master_id: int) -> List:
        """Получение всех заявок мастера."""
        master = await cls.get_by_id_with_related(master_id, "applications")
        return await master.applications.all() if master else []

    @classmethod
    async def get_related_salon_masters(cls, master_id: int) -> List:
        """Получение связей мастера с салонами."""
        master = await cls.get_by_id_with_related(master_id, "relations")
        return await master.relations.all() if master else []

    @classmethod
    async def bulk_create_masters(cls, masters_data: List[dict]) -> List[Master]:
        """Массовое создание мастеров."""
        return await cls.bulk_create(masters_data)