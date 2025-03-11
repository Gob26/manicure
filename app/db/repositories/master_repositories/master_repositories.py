from typing import Optional, List, Union, Any

from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from app.core.exceptions.repository import EntityNotFoundException
from app.db.schemas.master_schemas.master_schemas import MasterUpdateSchema
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
    async def get_master_by_slug(cls, slug: str) -> Optional[Master]:
        """Получение мастера по слагу."""
        return await cls.get_or_none(slug=slug)

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
    @classmethod
    async def get_master_by_city_and_slug(cls, city_slug: str, master_slug: str) -> Optional[Master]:
        """
        Получение мастера по slug города и slug мастера без загрузки связанных объектов.
        """
        query = cls.model.filter(city__slug=city_slug, slug=master_slug)
        return await query.first()

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
    async def get_masters_by_city(cls, city: str) -> List[Master]:
        """Получение списка мастеров по городу"""
        return await cls.filter(city=city)

    @classmethod
    async def get_masters_in_city(cls, city_slug: str, limit: int = 10, offset: int = 0) -> List[Master]:
        """
        Получение мастеров для конкретного города.
        """
        try:
            # Один запрос для получения города и всех мастеров в нем
            city = await City.get(slug=city_slug)  # Получаем город по slug

            # Получаем мастеров, связанных с этим городом
            masters = await Master.filter(
                city=city
            ).offset(offset).limit(limit).prefetch_related('city')  # Загружаем город для каждого мастера

            return masters
        except City.DoesNotExist:
            raise HTTPException(status_code=404, detail="Город не найден.")


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
    
    @classmethod
    async def _update_master(cls, master_id: int, schema: MasterUpdateSchema) -> Optional[Master]:
        """
        Асинхронно обновляет данные мастера в базе данных.

        Эта функция принимает идентификатор мастера и схему обновления,
        затем обновляет соответствующие поля в базе данных. После обновления
        функция возвращает обновленный объект мастера.

        Args:
            master_id (int): Идентификатор мастера, данные которого необходимо обновить.
            schema (MasterUpdateSchema): Схема обновления, содержащая новые данные для мастера.

        Returns:
            Optional[Master]: Обновленный объект мастера, если обновление прошло успешно.
                              Возвращает None, если мастер с указанным ID не найден.

        Example:
            updated_master = await Master._update_master(123, MasterUpdateSchema(name='New Name'))
            if updated_master:
                print(f"Master updated: {updated_master.name}")
            else:
                print("Master not found")
        """
        update_data = {
            k: v for k, v in schema.dict(exclude_unset=True).items()
            if v is not None
        }
        logger.debug(f"Данные для обновления мастера {master_id}: {update_data}")
        await cls.update(master_id, **update_data)  # Выполняем обновление в БД
        updated_master = await cls.get_by_id(master_id)  # Получаем обновленный мастер из БД
        return updated_master

    @classmethod
    async def _get_master_by_city_and_slug_with_avatar(cls, city: str, slug: str) -> Optional[Master]:
        """
        Асинхронно получает мастера по городу и slug с предзагрузкой аватара.

        Эта функция выполняет фильтрацию по заданному городу и slug,
        а затем возвращает мастера с предзагруженными данными аватара.

        Args:
            city (str): Slug города, в котором находится мастер.
            slug (str): Уникальный идентификатор мастера в формате slug.

        Returns:
            Optional[Master]: Объект мастера с предзагруженными данными аватара, если найден.
                            Возвращает None, если мастер с указанными параметрами не найден.

        Raises:
            EntityNotFoundException: Если мастер с указанными параметрами не найден.
            Exception: Если произошла любая другая ошибка во время выполнения запроса.

        Example:
            try:
                master = await Master._get_master_by_city_and_slug_with_avatar('moscow', 'example-slug')
                if master:
                    print(f"Master found: {master.name}")
            except EntityNotFoundException as e:
                print(e)
        """
        try:
            master = await Master.filter(city__slug=city, slug=slug).prefetch_related('images').first()
            if not master:
                raise EntityNotFoundException("Мастер", identifier=slug)
            return master
        except DoesNotExist:
            raise EntityNotFoundException("Мастер", identifier=slug)
        except Exception as e:
            # Логирование и прописываем исключения
            raise e


    @classmethod
    async def delete_master(cls, master_id: int) -> Optional[Master]:
        """Удаление мастера."""
        master = await cls.get_by_id(master_id)
        if master:
            await master.delete()
            logger.info(f"Мастер с ID {master_id} удален.")
            return master
        return None