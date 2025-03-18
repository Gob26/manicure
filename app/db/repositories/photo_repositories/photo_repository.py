from typing import Type, Any, Dict, Union
from tortoise.models import Model
from config.components.logging_config import logger


class PhotoRepository:
    @staticmethod
    async def create_photo(model: Type[Model], **kwargs) -> Model:
        """
        Создает запись фотографии в базе данных.

        Args:
            model: Класс модели (AvatarPhotoSalon, AvatarPhotoMaster и т.д.)
            **kwargs: Параметры для создания модели

        Returns:
            Созданный объект модели
        """
        try:
            photo = await model.create(**kwargs)
            logger.info(f"Создана запись фото: {model.__name__}, id={photo.id}")
            return photo
        except Exception as e:
            logger.error(f"Ошибка при создании фото {model.__name__}: {str(e)}")
            raise

    @staticmethod
    async def get_photo_by_id(model: Type[Model], photo_id: int) -> Union[Model, None]:
        """
        Получает фотографию по ID.

        Args:
            model: Класс модели
            photo_id: ID фотографии

        Returns:
            Объект модели или None, если не найден
        """
        return await model.filter(id=photo_id).first()

    @staticmethod
    async def _get_entity_photos(model: Type[Model], entity_field: str, entity_id: int) -> list:
        """
        Асинхронно получает все фотографии, связанные с определенной сущностью.

        Эта функция выполняет фильтрацию по заданному полю и идентификатору сущности,
        а затем возвращает отсортированный список фотографий.

        Args:
            model (Type[Model]): Класс модели, представляющий фотографии.
            entity_field (str): Имя поля модели, по которому будет выполняться фильтрация.
                                Например, 'salon_id' для фильтрации по идентификатору салона.
            entity_id (int): Идентификатор сущности, фотографии которой необходимо получить.

        Returns:
            list: Список объектов фотографий, отсортированных по полю 'sort_order'.

        Example:
            photos = await _get_entity_photos(PhotoModel, 'salon_id', 123)
            for photo in photos:
                print(photo.url)
        """
        filter_params = {entity_field: entity_id}
        return await model.filter(**filter_params).order_by("sort_order")

    @staticmethod
    async def update_photo(model: Type[Model], photo_id: int, **kwargs) -> Union[Model, None]:
        """
        Обновляет запись фотографии.

        Args:
            model: Класс модели
            photo_id: ID фотографии
            **kwargs: Параметры для обновления

        Returns:
            Обновленный объект модели или None, если не найден
        """
        photo = await PhotoRepository.get_photo_by_id(model, photo_id)
        if photo:
            for key, value in kwargs.items():
                setattr(photo, key, value)
            await photo.save()
            return photo
        return None

    @staticmethod
    async def delete_photo(model: Type[Model], photo_id: int) -> bool:
        """
        Удаляет запись фотографии.

        Args:
            model: Класс модели
            photo_id: ID фотографии

        Returns:
            True при успешном удалении, False если запись не найдена
        """
        deleted_count = await model.filter(id=photo_id).delete()
        return deleted_count > 0

    @staticmethod
    async def set_main_photo(model: Type[Model], entity_field: str, entity_id: int, photo_id: int) -> bool:
        """
        Устанавливает фото в качестве основного, сбрасывая флаг у остальных.

        Args:
            model: Класс модели
            entity_field: Имя поля для фильтрации (например, 'salon_id')
            entity_id: ID сущности
            photo_id: ID фотографии, которая должна стать основной

        Returns:
            True при успешном обновлении, False при ошибке
        """
        try:
            filter_params = {entity_field: entity_id}
            # Сбрасываем флаг у всех фотографий сущности
            await model.filter(**filter_params).update(is_main=False)
            # Устанавливаем флаг у выбранной фотографии
            await model.filter(id=photo_id).update(is_main=True)
            return True
        except Exception as e:
            logger.error(f"Ошибка при установке основного фото: {str(e)}")
            return False

    @staticmethod
    async def get_photo(model: Type[Model], **filters) -> Union[Model, None]:
        """
        Получает фотографию по заданным параметрам.

        Args:
            model: Класс модели (например, AvatarPhotoMaster, AvatarPhotoSalon)
            **filters: Произвольные фильтры (например, master_id=123, is_main=True)

        Returns:
            Объект фото или None, если фото не найдено.
        """
        return await model.filter(**filters).first()


    @staticmethod
    async def get_photo_count(model: Type[Model], id: int) -> int:
        """
        Получает количество фотографий для заданной модели и идентификатора.

        Функция возвращает количество фотографий, связанных с указанной сущностью
        в базе данных на основе предоставленной модели и ID.

        Args:
            model (Type[Model]): Модель Tortoise ORM, представляющая таблицу фотографий.
            id (int): Идентификатор сущности, для которой нужно получить количество фотографий.

        Returns:
            int: Количество фотографий для заданной сущности.

        Пример использования:
            photo_count = await PhotoService.get_photo_count(CustomServicePhoto, custom_service_id)
        """
        return await model.filter(custom_service_id=id).count()