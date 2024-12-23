from slugify import slugify
from tortoise.models import Model

from config.components.logging_config import logger


async def generate_unique_slug(model: Model, name: str, slug_field: str = "slug") -> str:
    """
    Генерирует уникальный slug для указанной модели, добавляя цифры, если слаг уже существует.
    
    :param model: Модель Tortoise ORM, в которой проверяется уникальность slug.
    :param name: Название для генерации slug.
    :param slug_field: Поле, по которому проверяется уникальность slug (по умолчанию 'slug').
    :return: Уникальный slug.
    """
    base_slug = slugify(name)
    slug = base_slug
    count = 1
    
    while await model.filter(**{slug_field: slug}).exists():
        logger.debug(f"Slug '{slug}' already exists. Trying '{base_slug}-{count}'")
        slug = f"{base_slug}-{count}"
        count += 1

    logger.debug(f"Generated unique slug: '{slug}'")
    return slug
