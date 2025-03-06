from typing import Union, List, Type, Any
from fastapi import HTTPException, UploadFile
from io import BytesIO
from PIL import Image as PILImage
import uuid

from config.components.logging_config import logger
from db.repositories.photo_repositories.photo_repository import PhotoRepository
from use_case.utils.image import ImageOptimizer
from use_case.utils.unique_name import generate_unique_filename


class PhotoHandler:
    @staticmethod
    async def add_photos_to_entity(
            images: Union[UploadFile, List[UploadFile]],  # Одно изображение или список
            model: Type[Any],  # Модель для записи фото (например, AvatarPhotoSalon, ServicePhoto и т.д.)
            entity_id: int = None,  # ID связанной сущности (salon_id, master_id, service_id и т.д.)
            entity_field_name: str = None,  # Имя поля для entity_id в модели (например, "salon_id", "master_id", "service_id")
            role: str = "entity", # Роль сущности для формирования пути сохранения (например, "salons", "masters", "services")
            image_type: str = "avatar", # Тип изображения для формирования пути сохранения (например, "avatar", "portfolio", "gallery")
            is_main: bool = False,  # Является ли главным изображением
            sort_order: int = 0,  # Порядок сортировки
            city: str = "default_city", # Город для определения директории сохранения
    ) -> List[int]:
        """
        Универсальный метод для добавления фотографий к различным сущностям.

        Args:
            images: Одно или список изображений UploadFile.
            model: Модель SQLAlchemy для сохранения фото (например, AvatarPhotoSalon, ServicePhoto).
            entity_id: ID сущности, к которой привязываются фото (например, salon_id, master_id, service_id).
            entity_field_name: Имя поля внешнего ключа в модели photo, связывающего с сущностью (например, 'salon_id').
            role: Роль сущности для формирования пути сохранения (например, 'salons', 'masters', 'services').
            image_type: Тип изображения для формирования пути сохранения (например, 'avatar', 'portfolio', 'gallery').
            is_main: Является ли изображение главным.
            sort_order: Порядок сортировки изображений.
            city: Город для определения директории сохранения.

        Returns:
            List[int]: Список ID созданных записей фотографий.

        Raises:
            HTTPException: В случае ошибок валидации или сохранения.
        """
        try:
            if not isinstance(images, list):  # Если это одно изображение
                images = [images]

            photo_ids = []  # Список для хранения ID созданных записей

            for image in images:
                if not image.content_type.startswith("image"):
                    raise HTTPException(status_code=400, detail="Загруженный файл не является изображением")

                # Прочитаем изображение
                image_bytes = await image.read()
                image_stream = BytesIO(image_bytes)

                # Получим размеры изображения
                with PILImage.open(image_stream) as pil_image:
                    width, height = pil_image.size

                # Сбрасываем поток, чтобы можно было повторно его использовать
                image_stream.seek(0)

                # Асинхронно генерируем уникальное имя файла
                new_filename = await generate_unique_filename(image.filename)

                # Определяем slug для сохранения
                entity_slug = f"{role}_{entity_id}" if entity_id else str(uuid.uuid4())

                # Асинхронно обрабатываем изображение (оптимизируем и сохраняем)
                saved_paths = await ImageOptimizer.optimize_and_save_async(
                    image_stream,
                    city=city,
                    role=role,
                    slug=entity_slug,
                    image_type=image_type,
                    new_filename=new_filename
                )

                image_stream.close()

                # Создаем запись в БД
                params = {
                    "file_name": new_filename,
                    "file_path": saved_paths.get("original", ""),
                    "mime_type": image.content_type,
                    "size": len(image_bytes),
                    "width": width,
                    "height": height,
                    "is_main": is_main,
                    "sort_order": sort_order,
                    "small": saved_paths.get("small", None),
                    "medium": saved_paths.get("medium", None),
                    "large": saved_paths.get("large", None)
                }

                # Добавляем ID сущности, если он предоставлен и имя поля указано
                if entity_field_name and entity_id:
                    params[entity_field_name] = entity_id

                photo = await PhotoRepository.create_photo(model=model, **params)

                logger.info(f"Создана запись фото для {model.__name__}: "
                            f"file_name={new_filename}, entity_id={entity_id}, "
                            f"small={saved_paths.get('small')}, medium={saved_paths.get('medium')}, "
                            f"large={saved_paths.get('large')}")

                photo_ids.append(photo.id)

            return photo_ids

        except Exception as e:
            logger.error(f"Ошибка при добавлении фото: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Ошибка при добавлении фото: {str(e)}")

    # Вспомогательные методы для удобства использования
    @staticmethod
    async def add_photos_to_salon(
            images: Union[UploadFile, List[UploadFile]],
            salon_id: int,
            model: Type[Any],
            is_main: bool = False,
            sort_order: int = 0,
            city: str = "default_city"
    ) -> List[int]:
        return await PhotoHandler.add_photos_to_entity(
            images=images,
            model=model,
            entity_id=salon_id,
            entity_field_name="salon_id", # Указываем имя поля salon_id
            role="salons",
            image_type="avatar",
            is_main=is_main,
            sort_order=sort_order,
            city=city
        )

    @staticmethod
    async def add_photos_to_master(
            images: Union[UploadFile, List[UploadFile]],
            master_id: int,
            model: Type[Any],
            is_main: bool = False,
            sort_order: int = 0,
            city: str = "default_city"
    ) -> List[int]:
        return await PhotoHandler.add_photos_to_entity(
            images=images,
            model=model,
            entity_id=master_id,
            entity_field_name="master_id", # Указываем имя поля master_id
            role="masters",
            image_type="avatar",
            is_main=is_main,
            sort_order=sort_order,
            city=city
        )

    @staticmethod
    async def add_photos_to_service(
            images: Union[UploadFile, List[UploadFile]],
            service_id: int,
            model: Type[Any],
            is_main: bool = False,
            sort_order: int = 0,
            city: str = "default_city"
    ) -> List[int]:
        """
        Вспомогательный метод для добавления фото к услугам.
        """
        return await PhotoHandler.add_photos_to_entity(
            images=images,
            model=model,
            entity_id=service_id,
            entity_field_name="service_id", # Указываем имя поля service_id
            role="services", # Роль для услуг
            image_type="portfolio", # Тип изображения для услуг (например, портфолио)
            is_main=is_main,
            sort_order=sort_order,
            city=city
        )