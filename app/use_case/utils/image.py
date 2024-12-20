import os
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
                file_info = getattr(image_file, 'filename', 'неизвестный файл')
                logger.info(f"Открыт файл из объекта FileStorage: {file_info}")
            else:
                image = Image.open(image_file)
                logger.info(f"Открыт файл по пути: {image_file}")
            return image
        except Exception as e:
            logger.error(f"Ошибка при открытии изображения: {e}")
            return None

    @staticmethod
    def _create_save_path(city, role, slug, image_type):
        """
        Создает путь для сохранения изображения.
        """
        save_path = MEDIA_DIR.joinpath(city, role, slug, image_type)
        os.makedirs(save_path, exist_ok=True)
        logger.info(f"Папка создана или существует: {save_path}")
        return save_path

    @staticmethod
    def _resize_image(image, max_dimension):
        """
        Изменяет размер изображения.
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
        Преобразует изображение в RGB.
        """
        if image.mode in ('RGBA', 'LA'):
            logger.info(f"Изображение имеет режим {image.mode}. Преобразование в RGB.")
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        return image

    @staticmethod
    def _save_image(image, file_path, quality):
        """
        Сохраняет изображение в файл.
        """
        try:
            image.save(file_path, format='WebP', quality=quality, optimize=True)
            logger.info(f"Изображение сохранено: {file_path}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении изображения: {e}")
            raise

    @staticmethod
    def optimize_and_save(image_file, city, role, slug, image_type, max_sizes, quality_start=95):
        """
        Обрабатывает изображение: изменяет размер, оптимизирует и сохраняет его.
        """
        logger.info("Начало обработки изображения")

        original_filename = os.path.splitext(os.path.basename(image_file))[0]
        image = ImageOptimizer._open_image(image_file)
        image = ImageOptimizer._convert_to_rgb(image)
        saved_paths = {}

        for size_name, max_dimension in max_sizes.items():
            logger.info(f"Начало обработки размера: {size_name} (максимальная сторона: {max_dimension}px)")

            try:
                # Изменяем размер изображения
                resized_image = ImageOptimizer._resize_image(image, max_dimension)

                # Создаем путь для сохранения
                save_path = ImageOptimizer._create_save_path(city, role, slug, image_type)
                new_filename = f"{original_filename}_{size_name}.webp"
                file_path = save_path.joinpath(new_filename)

                # Сохраняем изображение (один вызов save)
                ImageOptimizer._save_image(resized_image, file_path, quality=quality_start)
                saved_paths[size_name] = str(file_path)

            except Exception as e:
                logger.error(f"Ошибка при обработке размера {size_name}: {e}")
                raise

        logger.info("Обработка изображения завершена успешно.")
        return saved_paths
