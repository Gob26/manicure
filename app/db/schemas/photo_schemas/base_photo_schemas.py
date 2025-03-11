from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StandardServicePhotoSchema(BaseModel):
    id: int
    file_name: str = Field(..., max_length=255)  # Имя файла фотографии
    file_path: str = Field(..., max_length=1000)  # Путь к файлу фотографии
    mime_type: str = Field(..., max_length=100)  # MIME тип фотографии
    size: int  # Размер фотографии в байтах
    width: Optional[int] = None  # Ширина фотографии (опционально)
    height: Optional[int] = None  # Высота фотографии (опционально)
    is_main: bool = False  # Флаг основной фотографии
    sort_order: int = 0  # Порядок сортировки фотографий

    class Config:
        orm_mode = True  # Включаем работу с объектами ORM
