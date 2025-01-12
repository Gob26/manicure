from typing import Optional

from tortoise.exceptions import DoesNotExist

from db.models.services_models.category_model import Category
from db.repositories.services_repositories.category_service_repositories import ServiceCategoryRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


class CategoryService:
    @staticmethod
    async def create_category(category_data: dict) -> Category:
        """
        Создание новой категории.
        """
        slug = category_data.get("slug") or await generate_unique_slug(Category, category_data["name"])
        category = await ServiceCategoryRepository.create_category(
            name=category_data["name"],
            slug=slug,
            description=category_data.get("description"),
            title=category_data.get("title"),
            content=category_data.get("content"),
        )
        # Явно извлекаем связанные услуги, если они есть
        services = await category.services.all()  # Получаем все связанные услуги

        return category, services
    
    @staticmethod
    async def get_all_categories() -> list[Category]:
        """
        Получение всех категорий через репозиторий.
        """
        categories = await ServiceCategoryRepository.get_all_categories()
        return await Category.all().prefetch_related('services')

    @staticmethod
    async def get_category_by_id(category_id: int) -> Optional[Category]:
        try:
            category = await ServiceCategoryRepository.get_category_id(category_id=category_id)
            return category
        except DoesNotExist:
            return None
        
    @staticmethod
    async def update_category(category_id: int, category_data: dict) -> Optional[Category]:
        """
        Обновление категории.
        """
        try:
            category = await ServiceCategoryRepository.get_category_id(category_id=category_id)
            if category:
                updated_category = await ServiceCategoryRepository.update_category(
                    category_id=category_id,
                    category_data=category_data
                )
                return updated_category
            else:
                return None
        except DoesNotExist:
            return None    

    @staticmethod
    async def delete_category(category_id: int) -> bool:
        """
        Удаление категории.
        """
        try:
            category = await ServiceCategoryRepository.get_category_id(category_id=category_id)
            if category:
                await ServiceCategoryRepository.delete_category(category_id=category_id)
                return True
            else:
                return False
        except DoesNotExist:
            return False