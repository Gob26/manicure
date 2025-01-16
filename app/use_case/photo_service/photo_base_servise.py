from typing import Union, List, Type, Any
from fastapi import HTTPException, UploadFile
from io import BytesIO
from PIL import Image as PILImage

from config.components.logging_config import logger
from db.repositories.photo_repositories.photo_standard_service_repository import PhotoRepository
from use_case.utils.image import ImageOptimizer

class PhotoHandler:
    @staticmethod
    async def add_photos_to_service(
        images: Union[UploadFile, List[UploadFile]],  # Одно изображение или список
        model: Type[Any],  # Модель для записи
        slug: str,
        city: str = "default_city",
        role: str = "service",
        image_type: str = "default"
    ) -> Union[Any, List[Any]]:
        try:
            if not isinstance(images, list):  # Если это одно изображение
                images = [images]

            photo_ids = []  # Список для хранения ID созданных записей

            for image in images:
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
                    city=city,
                    role=role,
                    slug=slug,
                    image_type=image_type
                )

                # Получаем URL для фото
                default_photo_url = saved_paths.get("pc")
                if not default_photo_url:
                    raise ValueError(f"Не удалось сохранить изображение: {image.filename}")

                # Создаем запись в БД
                photo = await PhotoRepository.create_photo(
                    model=model,
                    file_name=image.filename,
                    file_path=default_photo_url,
                    mime_type=image.content_type,
                    size=len(image_bytes),
                    width=width,
                    height=height,
                )

                photo_ids.append(photo.id)

            # Если передано одно изображение, возвращаем ID как одно значение
            return photo_ids[0] if len(photo_ids) == 1 else photo_ids

        except Exception as e:
            logger.error(f"Error while adding photos to service: {str(e)}")
            raise HTTPException(status_code=500, detail="Error while adding photos")
