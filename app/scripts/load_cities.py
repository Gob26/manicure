import sys
import json
from pathlib import Path
from config.components.logging_config import logger
from slugify import slugify
from tortoise import Tortoise, run_async
from db.models.location.city import City
from pydantic_settings import BaseSettings, SettingsConfigDict
from tortoise.exceptions import IntegrityError, ConfigurationError
from tortoise.models import Model

# Добавление пути к корню проекта
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow'
    )

    postgres_connection_string: str = "postgresql://postgres:postgres@localhost:5433/manicure_db"
    jwt_secret_key: str = "dev_secret_key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    env: str = "development"


async def generate_unique_slug(model: Model, name: str, slug_field: str = "slug") -> str:
    """
    Генерирует уникальный slug для указанной модели.
    """
    base_slug = slugify(name)
    slug = base_slug

    try:
        if await model.filter(**{slug_field: slug}).exists():
            logger.debug(f"Слаг {slug} для города {name} уже существует, пропускаем.")
            return slug
    except Exception as e:
        logger.error(f"Ошибка при проверке существования слага: {str(e)}")
        raise

    return slug


async def init_tortoise(db_config: DatabaseConfig):
    """
    Инициализация Tortoise ORM с обработкой ошибок.
    """
    logger.debug(f"Инициализация Tortoise с connection_string: {db_config.postgres_connection_string}")

    tortoise_config = {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'database': db_config.postgres_connection_string.split('/')[-1],
                    'host': db_config.postgres_connection_string.split('@')[1].split(':')[0],
                    'password': db_config.postgres_connection_string.split(':')[2].split('@')[0],
                    'port': int(db_config.postgres_connection_string.split(':')[-1].split('/')[0]),
                    'user': db_config.postgres_connection_string.split('://')[1].split(':')[0],
                }
            }
        },
        'apps': {
            'server': {
                'models': ['db.models.location.city'],
                'default_connection': 'default',
            }
        },
        'use_tz': False,
        'timezone': 'UTC'
    }

    logger.debug("Закрытие существующих соединений...")
    try:
        await Tortoise.close_connections()
    except Exception as e:
        logger.warning(f"Ошибка при закрытии существующих соединений: {str(e)}")

    logger.debug("Инициализация новых соединений...")
    try:
        await Tortoise.init(config=tortoise_config)
        logger.info("Tortoise инициализирован успешно")

        logger.debug("Генерация схем...")
        await Tortoise.generate_schemas()
        logger.info("Схемы созданы успешно")
    except Exception as e:
        logger.error(f"Ошибка при инициализации Tortoise: {str(e)}")
        raise


async def load_cities():
    """
    Загрузка городов из файла JSON в базу данных.
    """
    try:
        logger.debug("Создание конфигурации базы данных...")
        db_config = DatabaseConfig()
        logger.info("Конфигурация успешно загружена")

        logger.debug("Инициализация базы данных...")
        await init_tortoise(db_config)

        json_path = project_root / "app" / "static" / "data" / "cities.json"
        logger.debug(f"Чтение JSON из: {json_path}")

        if not json_path.exists():
            raise FileNotFoundError(f"Файл {json_path} не найден")

        with open(json_path, "r", encoding="utf-8") as f:
            cities_data = json.load(f)

        logger.info(f"Найдено {len(cities_data)} городов в JSON")

        for idx, city in enumerate(cities_data, 1):
            try:
                coords = city["coords"]
                logger.debug(f"Обработка города {idx}/{len(cities_data)}: {city['name']}")

                slug = await generate_unique_slug(City, city["name"])

                existing_city, created = await City.get_or_create(
                    name=city["name"],
                    district=city["district"],
                    subject=city["subject"],
                    defaults={
                        "population": city["population"],
                        "latitude": float(coords["lat"]),
                        "longitude": float(coords["lon"]),
                        "slug": slug
                    }
                )

                if created:
                    logger.info(f"Город {city['name']} добавлен в базу данных (слаг: {slug})")
                else:
                    logger.debug(f"Город {city['name']} уже существует, пропущен")

            except IntegrityError as e:
                logger.error(f"Ошибка целостности данных при добавлении города {city['name']}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Непредвиденная ошибка при обработке города {city['name']}: {str(e)}")
                continue

        logger.info("Загрузка городов успешно завершена!")

    except Exception as e:
        logger.error(f"Критическая ошибка при выполнении скрипта: {str(e)}")
        raise
    finally:
        try:
            await Tortoise.close_connections()
            logger.info("Соединения с базой данных закрыты")
        except Exception as e:
            logger.error(f"Ошибка при закрытии соединений с базой данных: {str(e)}")


if __name__ == "__main__":
    try:
        run_async(load_cities())
    except Exception as e:
        logger.critical(f"Программа завершилась с ошибкой: {str(e)}")
        sys.exit(1)