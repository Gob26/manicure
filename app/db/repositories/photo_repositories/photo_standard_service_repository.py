from typing import Any, Optional, List
from db.models.photo_models.photo_standart_service_model import StandardServicePhoto
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger


class StandardServicePhotoRepository(BaseRepository):
    model = StandardServicePhoto

    @classmethod
    async def create_photo(cls, **kwargs: Any) -> StandardServicePhoto:
        """
        Создает запись фотографии с использованием базового метода.
        """
        photo = await cls.create(**kwargs)
        logger.info(f"Фотография создана с данными: {kwargs}")
        return photo

    @classmethod
    async def get_photo_by_id(cls, photo_id: int) -> Optional[StandardServicePhoto]:
        """
        Получает фотографию по её ID.
        """
        photo = await cls.get(id=photo_id)
        if photo:
            logger.info(f"Фотография найдена с ID: {photo_id}")
        else:
            logger.warning(f"Фотография с ID {photo_id} не найдена")
        return photo

    @classmethod
    async def delete_photo(cls, photo_id: int) -> bool:
        """
        Удаляет фотографию по её ID.
        """
        photo = await cls.get(id=photo_id)
        if not photo:
            logger.warning(f"Фотография с ID {photo_id} не найдена")
            return False
        await cls.delete(photo)
        logger.info(f"Фотография с ID {photo_id} удалена")
        return True
