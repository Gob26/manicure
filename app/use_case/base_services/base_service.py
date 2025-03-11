from typing import Type, Optional, List
from db.repositories.base_repositories.base_repositories import BaseRepository

class BaseService:
    repository: Type[BaseRepository]

    @classmethod
    async def get_or_none(cls, **filters) -> Optional[BaseRepository]:
        """Получение объекта или None, если он не существует"""
        return await cls.repository.get_or_none(**filters)

    @classmethod
    async def create(cls, **data) -> BaseRepository:
        """Создание нового объекта"""
        return await cls.repository.create(**data)

    @classmethod
    async def update(cls, instance: BaseRepository, **data) -> BaseRepository:
        """Обновление объекта"""
        return await cls.repository.update(instance, **data)

    @classmethod
    async def delete(cls, instance: BaseRepository) -> None:
        """Удаление объекта"""
        await cls.repository.delete(instance)

    @classmethod
    async def list(cls, **filters) -> List[BaseRepository]:
        """Получение списка объектов с фильтрацией"""
        return await cls.repository.list(**filters)
