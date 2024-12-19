import os

from io import BytesIO
from PIL import Image

from config.constants import MEDIA_DIR
from config.components.logging_config import logger

class ImageOptimizer:

    @staticmethod
    def _open_image(image_file):
        """
        Открывает изображение из файла или объекта FileStorage.
        """
        try:
            if hasattr(image_file, 'read'):
                image = Image.open(image_file)
                # Проверяем, есть ли атрибут filename, если нет - выводим путь или имя по-другому
                file_info = getattr(image_file, 'filename', 'неизвестный файл')
                logger.info(f"Открыт файл из объекта FileStorage: {file_info}")
            else:
                image = Image.open(image_file)
                logger.info(f"Открыт файл по пути: {image_file}")
            return image
        except Exception as e:
            logger.error(f"Ошибка при открытии изображения: {e}")
            return None  # Возвращаем None, если произошла ошибка


    @staticmethod
    def _create_save_path(city, role, slug, image_type):
        """
        Создает путь для сохранения изображения на основе города, роли, slug и типа изображения.
        """
        save_path = MEDIA_DIR.joinpath(city, role, slug, image_type)
        os.makedirs(save_path, exist_ok=True)
        logger.info(f"Папка создана или существует: {save_path}")
        return save_path

    @staticmethod
    def _resize_image(image, max_dimension):
        """
        Изменяет размер изображения, чтобы его самая большая сторона не превышала max_dimension.
        """
        width, height = image.size
        if width > max_dimension or height > max_dimension:
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"Размер изменен: {new_width}x{new_height}")
        return image

    @staticmethod
    def _convert_to_rgb(image):
        """
        Преобразует изображение в RGB, если оно в формате RGBA или LA.
        """
        if image.mode in ('RGBA', 'LA'):
            logger.info(f"Изображение имеет режим {image.mode}. Преобразование в RGB.")
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
            logger.info("Преобразование в RGB успешно завершено.")
        return image

    @staticmethod
    def _optimize_image(image, quality_start, max_size_kb):
        """
        Оптимизирует изображение, сжимая его до требуемого размера и качества.
        """
        buffer = BytesIO()
        quality = quality_start
        while quality > 5:
            buffer.seek(0)
            buffer.truncate()
            image.save(buffer, format='WebP', quality=quality, optimize=True)
            if buffer.tell() <= max_size_kb * 1024:
                break
            quality -= 5
            logger.warning(f"Размер превышает лимит, уменьшаем качество: {quality}")
        buffer.seek(0)
        return buffer

    @staticmethod
    def _save_image(image, file_path):
        """
        Сохраняет изображение в файл.
        """
        try:
            image.save(file_path, format='WebP', quality=95, optimize=True)
            logger.info(f"Изображение сохранено: {file_path}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении изображения: {e}")
            raise

    @staticmethod
    def optimize_and_save(image_file, city, role, slug, image_type, max_sizes, quality_start=95):
        """
        Обрабатывает изображение: изменяет размер, оптимизирует и сохраняет его в несколько размеров.
        """
        logger.info("Начало обработки изображения")

        original_filename = os.path.splitext(os.path.basename(image_file))[0]

        # Открываем изображение
        image = ImageOptimizer._open_image(image_file)

        # Преобразуем в RGB, если необходимо
        image = ImageOptimizer._convert_to_rgb(image)

        saved_paths = {}

        for size_name, max_dimension in max_sizes.items():
            logger.info(f"Начало обработки размера: {size_name} (максимальная сторона: {max_dimension}px)")

            try:
                # Изменяем размер изображения
                resized_image = ImageOptimizer._resize_image(image, max_dimension)

                # Создаем путь для сохранения
                save_path = ImageOptimizer._create_save_path(city, role, slug, image_type)

                # Сохраняем изображение
                new_filename = f"{original_filename}_{size_name}.webp"
                file_path = save_path.joinpath(new_filename)

                # Оптимизация и сохранение изображения
                buffer = ImageOptimizer._optimize_image(resized_image, quality_start, max_dimension)
                ImageOptimizer._save_image(resized_image, file_path)

                saved_paths[size_name] = str(file_path)

            except Exception as e:
                logger.error(f"Ошибка при обработке размера {size_name}: {e}")
                raise

        logger.info("Обработка изображения завершена успешно.")
        return saved_paths

"""РЕКОМЕНДАЦИИ
Кэширование: Если изображения часто запрашиваются, можно добавить кэширование или использование CDN (Content Delivery Network) для уменьшения нагрузки на сервер.
Валидация изображений: Было бы полезно добавить валидацию для изображений, например, проверку на формат и размер файла до начала оптимизации, чтобы исключить невалидные файлы на ранней стадии.
Ошибки при создании путей: Возможно, стоит добавить обработку ошибок при создании путей (например, если возникает проблема с доступом к директории или с правами на запись).
Асинхронность: Если процесс загрузки изображений занимает много времени, можно рассмотреть асинхронную обработку, чтобы не блокировать основной поток приложения.
"""