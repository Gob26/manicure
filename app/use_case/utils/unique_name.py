import os
import uuid
from typing import Coroutine

async def generate_unique_filename(original_filename: str) -> str:
    """
    Асинхронно генерирует уникальное имя файла, сохраняя оригинальное расширение.
    """
    ext = original_filename.split(".")[0]  # Получаем расширение файла
    unique_name = f"{uuid.uuid4()}-{ext}"  # Генерируем уникальное имя с тем же расширением
    return unique_name