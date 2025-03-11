from typing import Optional, List, Union, Any
from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist
from db.models.services_models.category_model import Category
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger


class ServiceCategoryRepository(BaseRepository):
    model = Category

    @classmethod
    async def create_category(cls, **kwargs: Any) -> Category:
        logger.info(f"Начало создания категории с параметрами: {kwargs}")
        try:
            category = await cls.create(**kwargs)
            logger.info(f"Категория успешно создана: ID={category.id}")
            return category
        except Exception as e:
            logger.error(f"Ошибка при создании категории: {e}")
            raise

    @classmethod
    async def get_all_categories(cls) -> List[Category]:
        """
        Получение всех категорий из базы данных.
        """
        return await cls.get_all()

    @classmethod
    async def get_category_id(cls, category_id: int) -> Optional[Category]:
        """
        Получение категории по ее ID.
        """
        try:
            # Сначала получаем корутину и ждем её выполнения
            category = await cls.get_by_id(id=category_id)
            # Затем делаем prefetch_related
            await category.fetch_related('services')
            return category
        except DoesNotExist:
            logger.error(f"Категория с ID {category_id} не найдена")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {category_id} не найдена"
            )
        except Exception as e:
            logger.error(f"Ошибка при получении категории по ID {category_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )

    @classmethod
    async def update_category(cls, category_id: int, category_data: dict) -> Optional[Category]:
        """
        Обновление категории по ее ID.
        """
        try:
            category = await cls.get_by_id(id=category_id)
            if category:
                updated_category = await cls.update(id=category_id, **category_data)
                return updated_category
            else:
                return None
            # raise HTTPException(status_code=404, detail="Категория не найдена")
        except DoesNotExist:
            logger.error(f"Категория с ID {category_id} не найдена")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {category_id} не найдена"
            )
        
    @classmethod
    async def delete_category(cls, category_id: int) -> None:
        """
        Удаление категории по ее ID.
        """
        # Пытаемся найти категорию
        category = await cls.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {category_id} не найдена"
            )

        # Удаляем категорию
        deleted_count = await cls.delete(category_id)
        if deleted_count == 0:
            logger.error(f"Не удалось удалить категорию с ID {category_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка удаления категории с ID {category_id}"
            )

        logger.info(f"Категория с ID {category_id} успешно удалена")
