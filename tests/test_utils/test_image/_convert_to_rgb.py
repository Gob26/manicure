import pytest
from PIL import Image
from app.use_case.utils.image import ImageOptimizer

def test_convert_to_rgb():
    # Создаем изображение в формате RGBA
    image = Image.new('RGBA', (100, 100), color='blue')
    
    rgb_image = ImageOptimizer._convert_to_rgb(image)
    
    assert rgb_image.mode == 'RGB'  # Проверяем, что изображение преобразовано в RGB
