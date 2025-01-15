import asyncio
import os
from io import BytesIO
from pathlib import Path
from PIL import Image
from config.constants import MEDIA_DIR
from config.components.logging_config import logger


class ImageOptimizer:
    MAX_SIZES = {"pc": 1920, "phone": 1080, "tablet": 1280}

    @staticmethod
    async def optimize_and_save_async(image_file, city, role, slug, image_type, quality=85):
        logger.info("Начало асинхронной обработки изображения")

        try:
            # Открытие изображения
            if isinstance(image_file, BytesIO):
                image = Image.open(image_file)
            else:
                raise ValueError("Поддерживаются только объекты BytesIO")

            image = ImageOptimizer._convert_to_rgb(image)
            saved_paths = {}

            for size_name, max_dim in ImageOptimizer.MAX_SIZES.items():
                resized_image = ImageOptimizer._resize_image(image, max_dim)

                save_path = ImageOptimizer._create_save_path(city, role, slug, image_type)
                file_name = f"{slug}_{size_name}.webp"
                file_path = os.path.join(save_path, file_name)

                await ImageOptimizer._save_image_async(resized_image, file_path, quality)
                saved_paths[size_name] = file_path

            return saved_paths

        except Exception as e:
            logger.error(f"Ошибка оптимизации изображения: {e}")
            raise

    @staticmethod
    def _resize_image(image, max_dim):
        width, height = image.size
        if max(width, height) > max_dim:
            scale = max_dim / max(width, height)
            new_size = (int(width * scale), int(height * scale))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
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
        except Exception as e:
            logger.error(f"Ошибка при сохранении изображения {path}: {e}")
            raise