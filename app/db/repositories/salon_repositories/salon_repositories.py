from typing import Optional, List, Dict, Any
from tortoise.expressions import Q
from tortoise.transactions import atomic
from tortoise.functions import Count

from db.models.salon_models.salon_model import Salon
from db.repositories.base_repositories.base_repositories import BaseRepository
from db.schemas.salon_schemas.salon_schemas import SalonCreateSchema, SalonUpdateSchema
from config.components.logging_config import logger


class SalonRepository(BaseRepository):
    model = Salon

    @classmethod
    async def create_salon(cls, **kwargs: Any) -> Salon:
        """Создание нового салона!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
        salon = await cls.create(**kwargs)
        logger.info(f"Салон создан с данными: {kwargs}")

        return salon

    @classmethod
    async def update_salon(cls, salon_id: int, schema: SalonUpdateSchema) -> Optional[Salon]:
        """Обновление информации о салоне"""
        update_data = {
            k: v for k, v in schema.dict(exclude_unset=True).items()
            if v is not None
        }
        return await cls.update(salon_id, **update_data)

    @classmethod
    async def delete_salon(cls, salon_id: int) -> bool:
        """Удаление салона"""
        return await cls.delete(salon_id)

    @classmethod
    async def get_salon_by_id(cls, salon_id: int) -> Optional[Salon]:
        """Получение салона по ID"""
        return await cls.get_by_id(salon_id)

    @classmethod
    async def get_salon_by_slug(cls, slug: str) -> Optional[Salon]:
        """Получение салона по slug"""
        return await cls.get_or_none(slug=slug)

    @classmethod
    async def get_salons_by_city(cls, city: str) -> List[Salon]:
        """Получение списка салонов по городу"""
        return await cls.filter(city=city)

    @classmethod
    async def search_salons(cls, query: str) -> List[Salon]:
        """Поиск салонов по названию, описанию или адресу"""
        return await cls.model.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query)
        )

    @classmethod
    async def get_salon_with_relations(cls, salon_id: int) -> Optional[Dict[str, Any]]:
        """Получение полной информации о салоне со всеми связанными данными"""
        salon = await cls.model.get_or_none(id=salon_id).prefetch_related(
            'services',
            'relations',
            'vacancies',
            'invitations'
        )
        
        if not salon:
            return None

        return {
            'salon': salon,
            'services': await salon.services.all(),
            'relations': await salon.relations.all(),
            'vacancies': await salon.vacancies.all(),
            'invitations': await salon.invitations.all()
        }

    @classmethod
    async def get_salons_by_user_id(cls, user_id: int) -> List[Salon]:
        """Получение всех салонов пользователя"""
        return await cls.filter(user_id=user_id)

    @classmethod
    @atomic()
    async def transfer_salon_ownership(cls, salon_id: int, new_user_id: int) -> Optional[Salon]:
        """Передача прав владения салоном другому пользователю"""
        salon = await cls.get_by_id(salon_id)
        if not salon:
            return None

        salon.user_id = new_user_id
        await salon.save()
        return salon

    @classmethod
    async def get_salons_with_filters(
        cls,
        city: Optional[str] = None,
        has_services: Optional[bool] = None,
        has_vacancies: Optional[bool] = None
    ) -> List[Salon]:
        """Получение салонов с применением фильтров"""
        query = cls.model.all()
        
        if city:
            query = query.filter(city=city)
        
        if has_services is not None:
            query = query.filter(services__isnull=not has_services)
            
        if has_vacancies is not None:
            query = query.filter(vacancies__isnull=not has_vacancies)
        
        return await query.distinct()

    @classmethod
    async def update_salon_status(cls, salon_id: int, is_active: bool) -> Optional[Salon]:
        """Обновление статуса активности салона"""
        return await cls.update(salon_id, is_active=is_active)

    @classmethod
    async def get_popular_cities(cls) -> List[Dict[str, Any]]:
        """Получение списка городов с количеством салонов"""
        return await cls.model.all().group_by('city').values('city').annotate(
            salon_count=Count('id')
        ).order_by('-salon_count')