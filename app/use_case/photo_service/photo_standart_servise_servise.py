

from typing import Optional
from fastapi import HTTPException, UploadFile, File
from io import BytesIO
from PIL import Image as PILImage
from db.models import StandardServicePhoto
from config.components.logging_config import logger
from db.repositories.photo_repositories.photo_standard_service_repository import StandardServicePhotoRepository
from use_case.utils.image import ImageOptimizer

class PhotoStandardServiceService:
    @staticmethod
    async def add_photo_to_service(image
    ) -> StandardServicePhoto:
        try:
            # Прочитаем изображение
            image_bytes = await image.read()
            image_stream = BytesIO(image_bytes)

            # Получим размеры изображения
            with PILImage.open(image_stream) as pil_image:
                width, height = pil_image.size

            # Сбрасываем поток, чтобы можно было повторно его использовать
            image_stream.seek(0)

            # Асинхронно обрабатываем изображение (оптимизируем и сохраняем)
            saved_paths = await ImageOptimizer.optimize_and_save_async(
                image_stream,
                city="default_city",  # Используйте текущий город, если он есть в контексте
                role="service",
                slug="example_slug",  # Используйте динамичный slug из данных
                image_type="default"
            )

            # Получаем URL для фото
            default_photo_url = saved_paths.get("pc")
            if not default_photo_url:
                raise ValueError("Не удалось сохранить изображение")

            # Создаем запись в БД
            photo = await StandardServicePhotoRepository.create_photo(
                file_name=image.filename,
                file_path=default_photo_url,
                mime_type=image.content_type,
                size=len(image_bytes),
                width=width,
                height=height,
            )

            return photo.id #id фото из базы данных

        except Exception as e:
            logger.error(f"Error while adding photo to service : {str(e)}")
            raise HTTPException(status_code=500, detail="Error while adding photo")
