from typing import Type, TypeVar, Generic, Optional, List
from db.repositories.base_repositories.base_repositories import BaseRepository
from tortoise.models import Model

T = TypeVar("T", bound=Model)


class BaseService(Generic[T]):
    repository: Type[BaseRepository[T]]

    @classmethod
    async def get_or_none(cls, **filters) -> Optional[T]:
        return await cls.repository.get_or_none(**filters)

    @classmethod
    async def create(cls, **data) -> T:
        return await cls.repository.create(**data)

    @classmethod
    async def update(cls, instance: T, **data) -> T:
        return await cls.repository.update(instance, **data)

    @classmethod
    async def delete(cls, instance: T) -> None:
        await cls.repository.delete(instance)

    @classmethod
    async def list(cls, **filters) -> List[T]:
        return await cls.repository.list(**filters)
