from unittest.mock import patch
from pathlib import Path
from app.use_case.utils.image import ImageOptimizer
from app.config.constants import MEDIA_DIR


@patch('os.makedirs')
def test_create_save_path(mock_makedirs):
    city = 'Moscow'
    role = 'salon'
    slug = 'unique_slug'
    image_type = 'portfolio'
    
    # Вызов метода, который нужно протестировать
    save_path = ImageOptimizer._create_save_path(city, role, slug, image_type)
    
    # Ожидаемый путь с использованием Path
    expected_path = MEDIA_DIR / city / role / slug / image_type
    
    # Проверка, что os.makedirs был вызван с правильным путем
    mock_makedirs.assert_called_once_with(expected_path, exist_ok=True)
    
    # Проверка, что возвращаемый путь соответствует ожидаемому
    assert save_path == expected_path
