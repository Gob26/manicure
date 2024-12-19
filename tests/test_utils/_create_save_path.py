import pytest
from unittest.mock import patch
import os
from your_module import ImageOptimizer  # замените на фактический импорт

@patch('os.makedirs')
def test_create_save_path(mock_makedirs):
    city = 'Moscow'
    role = 'salon'
    slug = 'unique_slug'
    image_type = 'portfolio'
    save_path = ImageOptimizer._create_save_path(city, role, slug, image_type)
    
    expected_path = os.path.join('MEDIA_DIR', city, role, slug, image_type)
    mock_makedirs.assert_called_once_with(expected_path, exist_ok=True)
    assert save_path == expected_path
