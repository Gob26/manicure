import pytest
from PIL import Image
from your_module import ImageOptimizer  # замените на фактический импорт

def test_resize_image():
    # Создаем тестовое изображение 400x500
    image = Image.new('RGB', (400, 500))
    max_dimension = 300

    resized_image = ImageOptimizer._resize_image(image, max_dimension)
    resized_width, resized_height = resized_image.size

    assert resized_width <= max_dimension  # Ширина не должна превышать max_dimension
    assert resized_height <= max_dimension  # Высота не должна превышать max_dimension
