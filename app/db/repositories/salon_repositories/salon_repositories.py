from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist
from tortoise.expressions import Q
from tortoise.transactions import atomic
from tortoise.functions import Count

from core.exceptions.repository import EntityNotFoundException
from db.models import City
from db.models.salon_models.salon_model import Salon
from db.repositories.base_repositories.base_repositories import BaseRepository
from db.schemas.salon_schemas.salon_schemas import SalonUpdateSchema
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
    async def get_salon_by_user_id(cls, user_id: int) -> Optional[Salon]:
        """Получение салона по ID пользователя!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
        return await cls.get_or_none(user_id=user_id)

    @classmethod
    async def update_salon(cls, salon_id: int, schema: SalonUpdateSchema) -> Optional[Salon]:
        """Обновление информации о салоне"""
        update_data = {
            k: v for k, v in schema.dict(exclude_unset=True).items()
            if v is not None
        }
        await cls.update(salon_id, **update_data)  # Выполняем обновление в БД
        updated_salon = await cls.get_by_id(salon_id)  # Получаем обновленный салон из БД
        return updated_salon  # Возвращаем обновленный салон

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
    async def get_salon_in_city(cls, city_slug: str, limit: int = 10, offset: int = 0) -> List[Salon]:
        """
        Получение салонов для конкретного города.
        """
        try:
            # Получаем город по slug
            city = await City.get(slug=city_slug)

        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Город не найден.")

        # Получаем салоны в этом городе
        salons = await Salon.filter(city=city).offset(offset).limit(limit).all()

        if not salons:
            raise HTTPException(status_code=404, detail="Салоны не найдены в данном городе.")

        return salons

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

    @staticmethod
    async def _get_salon_by_slug_with_avatar(slug: str):
        """
        Асинхронно получает объект салона по его slug с предзагрузкой связанных данных аватара.

        Эта функция использует метод prefetch_related для предзагрузки связанных данных аватара,
        что позволяет уменьшить количество запросов к базе данных и улучшить производительность.

        Args:
            slug (str): Уникальный идентификатор салона в формате slug.

        Returns:
            Salon: Объект салона с предзагруженными данными аватара.

        Raises:
            EntityNotFoundException: Если салон с указанным slug не найден.
            Exception: Если произошла любая другая ошибка во время выполнения запроса.

        Example:
            salon = await Salon.get_salon_by_slug_with_avatar('example-slug')
            print(salon.name, salon.images)
        """
        try:
            # Используем prefetch_related для предзагрузки связанных данных аватара
            salon = await Salon.filter(slug=slug).prefetch_related('images').first()
            if not salon:
                raise EntityNotFoundException(f"Салон с slug={slug} не найден")
            return salon
        except DoesNotExist:
            raise EntityNotFoundException(f"Салон с slug={slug} не найден")
        except Exception as e:
            # Логирование и пробрасывание исключения
            raise e
