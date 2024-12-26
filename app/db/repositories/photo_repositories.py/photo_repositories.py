from typing import Optional, List, Union

from db.models.abstract.abstract_photo import EntityType
from db.models.photo_models.photo_model import Photo
from db.schemas.photo_schemas.photo_shema import PhotoUpdateSchema


class PhotoRepository:
    """
    Репозиторий для работы с фотографиями
    """
    
    @staticmethod
    async def create(data: PhotoUpdateSchema) -> Photo:
        """
        Создание новой фотографии
        """
        return await Photo.create(**data.dict())

    @staticmethod
    async def get_by_id(photo_id: int) -> Optional[Photo]:
        """
        Получение фотографии по ID
        """
        return await Photo.get_or_none(id=photo_id)

    @staticmethod
    async def update(photo_id: int, data: PhotoUpdateSchema) -> Optional[Photo]:
        """
        Обновление фотографии
        """
        # Исключаем None значения из обновления
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        
        if update_data:
            await Photo.filter(id=photo_id).update(**update_data)
        return await PhotoRepository.get_by_id(photo_id)

    @staticmethod
    async def delete(photo_id: int) -> bool:
        """
        Удаление фотографии
        """
        deleted_count = await Photo.filter(id=photo_id).delete()
        return deleted_count > 0

    @staticmethod
    async def get_entity_photos(
        entity_type: EntityType,
        entity_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
        only_main: bool = False
    ) -> List[Photo]:
        """
        Получение фотографий для конкретной сущности
        """
        return await Photo.get_entity_photos(
            entity_type=entity_type,
            entity_id=entity_id,
            limit=limit,
            offset=offset,
            only_main=only_main
        )

    @staticmethod
    async def get_main_photo(
        entity_type: EntityType,
        entity_id: int
    ) -> Optional[Photo]:
        """
        Получение главной фотографии сущности
        """
        return await Photo.get_main_photo(entity_type, entity_id)

    @staticmethod
    async def set_main_photo(
        entity_type: EntityType,
        entity_id: int,
        photo_id: int
    ) -> bool:
        """
        Установка главной фотографии для сущности
        """
        # Сначала сбрасываем главную фотографию у всех фото данной сущности
        if entity_type in [EntityType.MASTER_AVATAR, EntityType.MASTER_WORK, EntityType.MASTER_POST]:
            await Photo.filter(entity_type=entity_type, master_id=entity_id).update(is_main=False)
        elif entity_type in [EntityType.SALON_INTERIOR, EntityType.SALON_POST, EntityType.SALON_LOGO]:
            await Photo.filter(entity_type=entity_type, salon_id=entity_id).update(is_main=False)
        elif entity_type == EntityType.SERVICE_PHOTO:
            await Photo.filter(entity_type=entity_type, service_id=entity_id).update(is_main=False)
        
        # Устанавливаем новую главную фотографию
        updated_count = await Photo.filter(id=photo_id).update(is_main=True)
        return updated_count > 0

    @staticmethod
    async def update_sort_order(photo_ids: List[int], start_order: int = 0) -> bool:
        """
        Обновление порядка сортировки фотографий
        """
        try:
            await Photo.update_sort_order(photo_ids, start_order)
            return True
        except Exception:
            return False

    @staticmethod
    async def count_entity_photos(
        entity_type: EntityType,
        entity_id: int
    ) -> int:
        """
        Подсчет количества фотографий для сущности
        """
        query = Photo.filter(entity_type=entity_type)
        
        if entity_type in [EntityType.MASTER_AVATAR, EntityType.MASTER_WORK, EntityType.MASTER_POST]:
            query = query.filter(master_id=entity_id)
        elif entity_type in [EntityType.SALON_INTERIOR, EntityType.SALON_POST, EntityType.SALON_LOGO]:
            query = query.filter(salon_id=entity_id)
        elif entity_type == EntityType.SERVICE_PHOTO:
            query = query.filter(service_id=entity_id)
            
        return await query.count()