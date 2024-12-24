from typing import TypeVar, Type, Optional, List, Any, Dict, Union
from tortoise import Model
from tortoise.expressions import Q
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic, in_transaction
from config.components.logging_config import logger


ModelType = TypeVar("ModelType", bound=Model)

class BaseRepository:
    model: Type[ModelType] = None

    @classmethod
    async def get_by_id(cls, id: int) -> Optional[ModelType]:
        """Получение объекта по ID"""
        try:
            return await cls.model.get(id=id)
        except DoesNotExist:
            logger.info(f"{cls.model.__name__} с ID {id} не найден.")
            return None

    @classmethod
    async def get_by_id_with_related(cls, id: int, *related_fields) -> Optional[ModelType]:
        """Получение объекта по ID со связанными полями"""
        try:
            return await cls.model.get(id=id).prefetch_related(*related_fields)
        except DoesNotExist:
            logger.info(f"{cls.model.__name__} с ID {id} не найден.")
            return None

    @classmethod
    async def get_all(cls, limit: int = 10, offset: int = 0, *related_fields) -> List[ModelType]:
        """Получение всех объектов с пагинацией и связанными полями"""
        query = cls.model.all()
        if related_fields:
            query = query.prefetch_related(*related_fields)
        return await query.offset(offset).limit(limit)

    @classmethod
    async def create(cls, **kwargs: Any) -> ModelType:
        """Создание нового объекта"""
        instance = await cls.model.create(**kwargs)
        logger.info(f"{cls.model.__name__} создан с данными: {kwargs}")
        return instance

    @classmethod
    async def update(cls, id: int, **kwargs: Any) -> Optional[ModelType]:
        """Обновление объекта"""
        async with in_transaction() as conn:
            updated = await cls.model.filter(id=id).using_db(conn).update(**kwargs)
            if not updated:
                logger.warning(f"Не удалось обновить {cls.model.__name__} с ID {id}")
                return None
            logger.info(f"{cls.model.__name__} с ID {id} обновлен с данными: {kwargs}")
            return await cls.get_by_id(id)

    @classmethod
    async def delete(cls, id: int) -> int:
        """Удаление объекта"""
        deleted_count = await cls.model.filter(id=id).delete()
        logger.info(f"Удалено {cls.model.__name__} с ID {id}: {deleted_count}")
        return deleted_count

    @classmethod
    async def filter(cls, limit: int = 10, offset: int = 0, **kwargs: Any) -> List[ModelType]:
        """Фильтрация объектов по указанным параметрам с пагинацией"""
        return await cls.model.filter(**kwargs).offset(offset).limit(limit)

    @classmethod
    async def exists(cls, **kwargs: Any) -> bool:
        """Проверка существования объекта с указанными параметрами"""
        exists = await cls.model.filter(**kwargs).exists()
        logger.debug(f"{cls.model.__name__} с параметрами {kwargs} существует: {exists}")
        return exists

    @classmethod
    async def count(cls, **kwargs: Any) -> int:
        """Подсчет количества объектов с указанными параметрами"""
        return await cls.model.filter(**kwargs).count()

    @classmethod
    async def get_or_create(cls, **kwargs: Any) -> tuple[ModelType, bool]:
        """Получение объекта или его создание, если он не существует"""
        return await cls.model.get_or_create(**kwargs)

    @classmethod
    async def bulk_create(cls, data_list: List[Dict[str, Any]], batch_size: int = 100) -> List[ModelType]:
        """Массовое создание объектов"""
        async with in_transaction() as conn:
            instances = await cls.model.bulk_create(
                [cls.model(**data) for data in data_list],
                batch_size=batch_size
            )
            logger.info(f"Создано {len(instances)} объектов {cls.model.__name__}")
            return instances

    @classmethod
    async def get_or_none(cls, **kwargs: Any) -> Optional[ModelType]:
        """Получение объекта или None, если он не существует"""
        try:
            return await cls.model.get(**kwargs)
        except DoesNotExist:
            return None