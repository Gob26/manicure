import sys
import json
from pathlib import Path
from config.components.logging_config import logger
from slugify import slugify
from tortoise import Tortoise, run_async
from db.models.location.city import City
from config.components.db import DatabaseConfig
from tortoise.exceptions import IntegrityError
from tortoise.models import Model

# Добавление пути к корню проекта
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))


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

    # Проверяем, существует ли уже такой слаг
    if await model.filter(**{slug_field: slug}).exists():
        # Если слаг существует, возвращаем его без изменений
        logger.debug(f"Слаг {slug} для города {name} уже существует, пропускаем.")
        return slug

    # Если слаг не существует, возвращаем его как уникальный
    return slug


async def load_cities():
    """
    Загрузка городов из файла JSON в базу данных с проверкой на дублирование и генерацией уникальных slugs.
    """
    db_config = DatabaseConfig()

    logger.debug(f"Корень проекта: {project_root}")
    logger.debug(
        f"Строка подключения: {db_config.postgres_connection_string.replace('postgres://', 'postgres://***:***@')}")

    # Обновленная конфигурация Tortoise
    config = {
        'connections': {
            'default': db_config.postgres_connection_string
        },
        'apps': {
            'models': {
                'models': ['db.models.location.city'],  # Убран префикс 'app.'
                'default_connection': 'default',
            }
        },
        'use_tz': False,
        'timezone': 'UTC'
    }

    logger.debug(f"Конфигурация Tortoise: {config}")

    # Закрываем предыдущие соединения, если они есть
    try:
        await Tortoise.close_connections()
    except Exception:
        pass

    # Инициализация подключения к базе данных
    await Tortoise.init(config=config)

    logger.debug("Генерация схем...")
    await Tortoise.generate_schemas()

    # Чтение данных из JSON
    json_path = project_root / "app" / "static" / "data" / "cities.json"
    logger.debug(f"Чтение JSON из: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        cities_data = json.load(f)

    logger.debug(f"Найдено {len(cities_data)} городов в JSON")

    try:
        # Добавление городов в базу данных с проверкой на дубли
        for idx, city in enumerate(cities_data):
            coords = city["coords"]
            logger.debug(f"Проверка города {idx + 1}/{len(cities_data)}: {city['name']}")

            try:
                # Генерация уникального слага для города
                slug = await generate_unique_slug(City, city["name"])

                # Используем get_or_create для предотвращения дублирования
                existing_city, created = await City.get_or_create(
                    name=city["name"],
                    district=city["district"],
                    subject=city["subject"],
                    defaults={
                        "population": city["population"],
                        "latitude": float(coords["lat"]),
                        "longitude": float(coords["lon"]),
                        "slug": slug  # Добавляем слаг
                    }
                )

                if created:
                    logger.debug(f"Город {city['name']} был добавлен в базу данных с слагом {slug}.")
                else:
                    logger.debug(f"Город {city['name']} уже существует, пропущен.")

            except IntegrityError as exc:
                # Ловим ошибку уникальности и логируем ее
                logger.error(f"Ошибка при добавлении города {city['name']}: {str(exc)}")
                continue  # Продолжаем с другими городами

        print("Города успешно загружены!")
    except Exception as e:
        logger.error(f"Ошибка при создании городов: {str(e)}")
        raise
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(load_cities())
