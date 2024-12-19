import pytest
from unittest.mock import MagicMock, patch
from io import BytesIO
from PIL import Image
import os

from app.config.constants import MEDIA_DIR
from app.use_case.utils.image import optimize_image_multisize

# Импортируем функцию для тестирования

# Создадим фикстуру для временных файлов
@pytest.fixture
def mock_image():
    # Создадим изображение для теста
    img = Image.new('RGB', (500, 500), color=(73, 109, 137))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# Вместо 'app.use_case.utils.image.Image.open', указываем правильный путь
@patch('app.use_case.utils.image.Image.open')
@patch('app.use_case.utils.image.create_save_path')
@patch('app.use_case.utils.image.save_image')
@patch('app.use_case.utils.image.optimize_image')
@patch('app.use_case.utils.image.resize_image')
@patch('app.use_case.utils.image.convert_to_rgb')
def test_optimize_image_multisize(mock_convert_to_rgb, mock_resize_image, mock_optimize_image, mock_save_image, mock_create_save_path, mock_image):
    # Создаем изображение для теста
    img = Image.new('RGB', (500, 500), color=(73, 109, 137))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    mock_image.return_value = img  # Замокать Image.open, чтобы возвращался этот объект

    # Мокаем нужные функции
    mock_convert_to_rgb.return_value = img  # Возвращаем mock_image как результат
    mock_resize_image.return_value = img
    mock_optimize_image.return_value = BytesIO()  # Имитация оптимизированного изображения
    mock_create_save_path.return_value = MEDIA_DIR  # Возвращаем базовый путь

    # Определим параметры
    max_sizes = {'small': 100, 'medium': 200, 'large': 400}
    city = 'Moscow'
    role = 'salon'
    slug = 'unique_slug'
    image_type = 'portfolio'

    # Запустим основную функцию
    result = optimize_image_multisize(mock_image, city, role, slug, image_type, max_sizes)

    # Проверим, что функции были вызваны
    mock_convert_to_rgb.assert_called_once_with(img)  # Проверка, что convert_to_rgb вызван с изображением
    mock_resize_image.assert_any_call(img, 100)  # Для small
    mock_resize_image.assert_any_call(img, 200)  # Для medium
    mock_resize_image.assert_any_call(img, 400)  # Для large
    mock_create_save_path.assert_called_with(MEDIA_DIR, city, role, slug, image_type)
    mock_save_image.assert_called()  # Проверка вызова save_image для каждого размера

    # Проверим, что результат функции содержит пути
    assert 'small' in result
    assert 'medium' in result
    assert 'large' in result

    # Проверим, что все сохраненные пути корректны
    for size_name, path in result.items():
        assert path.startswith(str(MEDIA_DIR))  # Проверяем, что путь начинается с MEDIA_DIR
