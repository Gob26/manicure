from typing import TypeVar, Type, Optional, List, Dict, Any
from tortoise import Model
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction
from config.components.logging_config import logger

ModelType = TypeVar("ModelType", bound=Model)

class BasePhotoRepository:
    model: Type[ModelType] = None

    @classmethod
    async def get_by_id(cls, id: int) -> Optional[ModelType]:
        """Получение объекта фотографии по ID"""
        try:
            return await cls.model.get(id=id)
        except DoesNotExist:
            logger.info(f"{cls.model.__name__} с ID {id} не найден.")
            return None

    @classmethod
    async def get_all(cls, limit: int = 10, offset: int = 0, **filters: Any) -> List[ModelType]:
        """Получение всех фотографий с пагинацией и фильтрацией"""
        query = cls.model.filter(**filters)
        return await query.offset(offset).limit(limit)

    @classmethod
    async def create(cls, **kwargs: Any) -> ModelType:
        """Создание новой фотографии"""
        instance = await cls.model.create(**kwargs)
        logger.info(f"{cls.model.__name__} создан с данными: {kwargs}")
        return instance

    @classmethod
    async def update(cls, id: int, **kwargs: Any) -> Optional[ModelType]:
        """Обновление данных фотографии"""
        async with in_transaction() as conn:
            updated = await cls.model.filter(id=id).using_db(conn).update(**kwargs)
            if not updated:
                logger.warning(f"Не удалось обновить {cls.model.__name__} с ID {id}")
                return None
            logger.info(f"{cls.model.__name__} с ID {id} обновлен с данными: {kwargs}")
            return await cls.get_by_id(id)

    @classmethod
    async def delete(cls, id: int) -> int:
        """Удаление фотографии по ID"""
        deleted_count = await cls.model.filter(id=id).delete()
        logger.info(f"Удалено {cls.model.__name__} с ID {id}: {deleted_count}")
        return deleted_count

    @classmethod
    async def set_main_photo(cls, id: int, entity_id: int, entity_field: str = "entity_id") -> bool:
        """Установка фотографии как основной для указанной сущности"""
        async with in_transaction() as conn:
            # Снимаем признак основной с других фотографий
            await cls.model.filter(**{entity_field: entity_id}).using_db(conn).update(is_main=False)
            # Устанавливаем текущей фотографии признак основной
            updated = await cls.model.filter(id=id).using_db(conn).update(is_main=True)
            if updated:
                logger.info(f"{cls.model.__name__} с ID {id} установлена как основная.")
                return True
            logger.warning(f"Не удалось установить {cls.model.__name__} с ID {id} как основную.")
            return False

    @classmethod
    async def bulk_create(cls, data_list: List[Dict[str, Any]], batch_size: int = 100) -> List[ModelType]:
        """Массовое создание фотографий"""
        async with in_transaction() as conn:
            instances = await cls.model.bulk_create(
                [cls.model(**data) for data in data_list],
                batch_size=batch_size
            )
            logger.info(f"Создано {len(instances)} объектов {cls.model.__name__}")
            return instances

    @classmethod
    async def reorder_photos(cls, entity_id: int, new_order: List[int], entity_field: str = "entity_id") -> bool:
        """Переназначение порядка фотографий для указанной сущности"""
        async with in_transaction() as conn:
            for sort_order, photo_id in enumerate(new_order):
                await cls.model.filter(id=photo_id, **{entity_field: entity_id}).using_db(conn).update(sort_order=sort_order)
            logger.info(f"Переназначен порядок для {cls.model.__name__} сущности с ID {entity_id}.")
            return True
