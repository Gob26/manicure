from slugify import slugify
from tortoise.models import Model


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

    # Проверяем, существует ли уже такой slug
    while await model.filter(**{slug_field: slug}).exists():
        # Если существует, добавляем цифру к slug
        slug = f"{base_slug}-{count}"
        count += 1

    return slug
