from pathlib import Path  # Модуль для работы с путями и файлами

# Определение корневой директории проекта
ROOT_DIR = Path(__file__).parents[2]

# Определение пути к директории с приложением
APP_DIR = ROOT_DIR.joinpath('app')

# Определение пути к .env файлу
ENV_FILE_PATH = ROOT_DIR.joinpath('.env')

MEDIA_DIR = ROOT_DIR.joinpath('media')
MEDIA_URL = "/media/"

# Важно: Убираем импорт RedisConfig и создание redis_config отсюда