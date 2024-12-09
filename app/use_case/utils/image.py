import os
from io import BytesIO
from PIL import Image
from config.components.logging_config import logger
from pathlib import Path


def create_save_path(base_path, city, role, image_type):
    """
    Создает путь для сохранения изображения на основе города, роли и типа изображения.

    Args:
        base_path: Базовый путь для сохранения
        city: Город, к которому относится изображение
        role: Роль (например, 'master', 'salon')
        image_type: Тип изображения ('portfolio', 'general')

    Returns:
        Path: Путь к папке, где будут сохранены изображения
    """
    save_path = base_path.joinpath(city, role, image_type)
    os.makedirs(save_path, exist_ok=True)
    logger.info(f"Папка создана или существует: {save_path}")
    return save_path


def resize_image(image, max_dimension):
    """
    Изменяет размер изображения, чтобы его самая большая сторона не превышала max_dimension.

    Args:
        image: Изображение, которое нужно изменить
        max_dimension: Максимальный размер стороны

    Returns:
        Image: Измененное изображение
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


def convert_to_rgb(image):
    """
    Преобразует изображение в RGB, если оно в формате RGBA или LA.

    Args:
        image: Исходное изображение

    Returns:
        Image: Преобразованное изображение
    """
    if image.mode in ('RGBA', 'LA'):
        logger.info(f"Изображение имеет режим {image.mode}. Преобразование в RGB.")
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        image = background
        logger.info("Преобразование в RGB успешно завершено.")
    return image


def optimize_image(image, quality_start, max_size_kb):
    """
    Оптимизирует изображение, сжимая его до требуемого размера и качества.

    Args:
        image: Изображение, которое нужно оптимизировать
        quality_start: Начальное качество для сжатия
        max_size_kb: Максимальный размер файла в килобайтах

    Returns:
        BytesIO: Оптимизированное изображение
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


def save_image(image, file_path):
    """
    Сохраняет изображение в файл.

    Args:
        image: Изображение, которое нужно сохранить
        file_path: Путь, куда нужно сохранить изображение
    """
    try:
        image.save(file_path, format='WebP', quality=95, optimize=True)
        logger.info(f"Изображение сохранено: {file_path}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении изображения: {e}")
        raise


def optimize_image_multisize(image_file, city, role, image_type, max_sizes, quality_start=95):
    """
    Основная функция для обработки изображения: оптимизирует и сохраняет его в несколько размеров.

    Args:
        image_file: Путь к файлу или объект FileStorage
        city: Город, к которому относится изображение
        role: Роль (например, 'master', 'salon')
        image_type: Тип изображения ('portfolio', 'general')
        max_sizes: Словарь с максимальными размерами для разных типов изображений
        quality_start: Начальное значение качества для WebP

    Returns:
        dict: Словарь с путями к сохраненным файлам для каждого размера
    """
    logger.info("Начало обработки изображения")
    
    try:
        # Открываем изображение
        if hasattr(image_file, 'read'):
            image = Image.open(image_file)
            original_filename = os.path.splitext(image_file.filename)[0]
            logger.info(f"Открыт файл из объекта FileStorage: {image_file.filename}")
        else:
            image = Image.open(image_file)
            original_filename = os.path.splitext(os.path.basename(image_file))[0]
            logger.info(f"Открыт файл по пути: {image_file}")
    except Exception as e:
        logger.error(f"Ошибка при открытии изображения: {e}")
        raise

    # Преобразуем в RGB если нужно
    image = convert_to_rgb(image)

    # Результаты для каждого размера
    saved_paths = {}

    for size_name, max_dimension in max_sizes.items():
        logger.info(f"Начало обработки размера: {size_name} (максимальная сторона: {max_dimension}px)")
        try:
            # Изменяем размер изображения
            resized_image = resize_image(image, max_dimension)

            # Создаем путь для сохранения
            save_path = create_save_path(MEDIA_DIR, city, role, image_type)

            # Сохраняем изображение
            new_filename = f"{original_filename}_{size_name}.webp"
            file_path = save_path.joinpath(new_filename)

            # Оптимизация и сохранение изображения
            buffer = optimize_image(resized_image, quality_start, max_dimension)
            save_image(resized_image, file_path)

            saved_paths[size_name] = str(file_path)
        except Exception as e:
            logger.error(f"Ошибка при обработке размера {size_name}: {e}")
            raise

    logger.info("Обработка изображения завершена успешно.")
    return saved_paths
