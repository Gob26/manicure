from tempfile import NamedTemporaryFile
from PIL import Image
from app.use_case.utils.image import ImageOptimizer
from app.config.constants import MEDIA_DIR

from unittest.mock import patch
from tempfile import NamedTemporaryFile
from PIL import Image

@patch('os.makedirs')
@patch('PIL.Image.Image.save')
@patch('PIL.Image.open')
def test_image_optimizer(mock_open, mock_save, mock_makedirs):
    # Тестовые данные
    city = 'Moscow'
    role = 'salon'
    slug = 'unique_slug'
    image_type = 'portfolio'
    max_sizes = {'small': 300, 'medium': 600}
    
    # Создаём временный файл с изображением
    with NamedTemporaryFile(suffix='.jpg') as temp_image_file:
        # Генерируем изображение и сохраняем его во временный файл
        image = Image.new('RGB', (100, 100), color='blue')
        image.save(temp_image_file, format='JPEG')
        temp_image_file.seek(0)  # Возвращаем указатель в начало файла
    
        # Настраиваем мок для PIL.Image.open
        mock_open.return_value = image
    
        # Настраиваем мок для методов внутри тестируемого кода
        mock_save.reset_mock()  # Сброс предыдущих вызовов
    
        # 1. Тестирование _open_image
        opened_image = ImageOptimizer._open_image(temp_image_file.name)
        assert isinstance(opened_image, Image.Image)
        mock_open.assert_called_once()
    
        # 2. Тестирование _convert_to_rgb
        rgb_image = ImageOptimizer._convert_to_rgb(opened_image)
        assert rgb_image.mode == 'RGB'
    
        # 3. Тестирование _resize_image
        max_dimension = 300
        resized_image = ImageOptimizer._resize_image(rgb_image, max_dimension)
        resized_width, resized_height = resized_image.size
        assert resized_width <= max_dimension
        assert resized_height <= max_dimension
    
        # 4. Тестирование _create_save_path
        save_path = ImageOptimizer._create_save_path(city, role, slug, image_type)
        expected_path = MEDIA_DIR / city / role / slug / image_type
        mock_makedirs.assert_called_once_with(expected_path, exist_ok=True)
        assert save_path == expected_path
    
        # 5. Тестирование _save_image
        file_path = str(save_path / "test_image.webp")
        ImageOptimizer._save_image(resized_image, file_path, quality=90)
        mock_save.assert_called_once_with(file_path, format='WebP', quality=90, optimize=True)

