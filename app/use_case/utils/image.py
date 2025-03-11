import asyncio
import os
from io import BytesIO
from PIL import Image
from config.constants import MEDIA_DIR
from config.components.logging_config import logger


class ImageOptimizer:
    # Определение размеров для разных версий изображений
    SIZE_CONFIGS = {
        "small": 320,    # Маленькая версия (320px)
        "medium": 768,   # Средняя версия (768px)
        "large": 1200,   # Большая версия (1200px)
        "original": 1920 # Оригинальная версия (1920px максимум)
    }

    @staticmethod
    async def optimize_and_save_async(image_file, city, role, slug, image_type, new_filename: str, quality=85):
        logger.info("Начало асинхронной обработки изображения")

        try:
            # Открытие изображения
            if isinstance(image_file, BytesIO):
                image = Image.open(image_file)
            else:
                raise ValueError("Поддерживаются только объекты BytesIO")

            image = ImageOptimizer._convert_to_rgb(image)
            saved_paths = {}

            # Создаем базовый путь для сохранения
            save_path = ImageOptimizer._create_save_path(city, role, slug, image_type)

            # Обрабатываем каждый размер изображения
            for size_name, max_dim in ImageOptimizer.SIZE_CONFIGS.items():
                resized_image = ImageOptimizer._resize_image(image, max_dim)

                file_name = f"{size_name}_{new_filename}.webp"
                file_path = os.path.join(save_path, file_name)

                relative_path = await ImageOptimizer._save_image_async(resized_image, file_path,
                                                                       quality)  # Получаем относительный путь!
                saved_paths[size_name] = relative_path  # Сохраняем относительный путь в saved_paths!

            return saved_paths

        except Exception as e:
            logger.error(f"Ошибка оптимизации изображения: {e}")
            raise

        except Exception as e:
            logger.error(f"Ошибка оптимизации изображения: {e}")
            raise

    @staticmethod
    def _resize_image(image, max_dim):
        width, height = image.size
        if max(width, height) > max_dim:
            scale = max_dim / max(width, height)
            new_size = (int(width * scale), int(height * scale))
            image = image.resize(new_size, Image.LANCZOS)
        return image

    @staticmethod
    def _convert_to_rgb(image):
        if image.mode in ("RGBA", "LA"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            return background
        return image

    @staticmethod
    def _create_save_path(city, role, slug, image_type):
        save_path = os.path.join(MEDIA_DIR, city, role, slug, image_type)
        os.makedirs(save_path, exist_ok=True)
        return save_path

    @staticmethod
    async def _save_image_async(image, path, quality):
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: image.save(path, format="WEBP", quality=quality))

            relative_path = os.path.relpath(path, MEDIA_DIR)
            return relative_path
        except Exception as e:
            logger.error(f"Ошибка при сохранении изображения {path}: {e}")
            raise

    @staticmethod
    async def delete_file(relative_path):
        try:
            file_path = os.path.join(MEDIA_DIR, relative_path)
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Удален файл: {file_path}")
            else:
                logger.warning(f"Файл не найден: {file_path}")
        except Exception as e:
            logger.error(f"Ошибка при удалении файла {file_path}: {e}")
            raise