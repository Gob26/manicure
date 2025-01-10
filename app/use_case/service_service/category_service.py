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
        slug = category_data.get("slug") or generate_unique_slug(Category, category_data["name"])
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

