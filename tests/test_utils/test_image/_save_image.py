import pytest
from unittest.mock import patch
from PIL import Image
from your_module import ImageOptimizer  # замените на фактический импорт

@patch('PIL.Image.Image.save')
def test_save_image(mock_save):
    image = Image.new('RGB', (100, 100), color='blue')
    file_path = 'test_image.webp'
    
    ImageOptimizer._save_image(image, file_path)
    
    mock_save.assert_called_once_with(file_path, format='WebP', quality=95, optimize=True)
