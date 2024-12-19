import pytest
from io import BytesIO
from PIL import Image
from your_module import ImageOptimizer  # замените на фактический импорт

def test_optimize_image():
    # Создаем тестовое изображение
    image = Image.new('RGB', (100, 100), color='blue')
    buffer = ImageOptimizer._optimize_image(image, quality_start=95, max_size_kb=50)
    
    assert isinstance(buffer, BytesIO)  # Проверяем, что возвращается объект BytesIO
    assert buffer.tell() <= 50 * 1024  # Проверяем, что размер меньше максимума
