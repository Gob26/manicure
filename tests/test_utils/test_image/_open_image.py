import pytest
from unittest.mock import patch
from PIL import Image
from io import BytesIO
from app.use_case.utils.image import ImageOptimizer  # замените на фактический импорт

# Тест для метода _open_image
@patch('PIL.Image.open')
def test_open_image(mock_open):
    # Создадим мок изображения
    mock_image = Image.new('RGB', (100, 100), color='blue')
    mock_open.return_value = mock_image

    image_file = BytesIO(b"fake image data")
    image = ImageOptimizer._open_image(image_file)
    
    assert isinstance(image, Image.Image)  # Проверяем, что возвращается объект Image
    mock_open.assert_called_once()  # Проверяем, что Image.open был вызван
