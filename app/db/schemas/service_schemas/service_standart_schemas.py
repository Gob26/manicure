from pydantic import BaseModel, Field
from typing import Optional
from db.schemas.service_schemas.category_schemas import CategoryBase


class StandardServicePhotoSchema(BaseModel):
    file_name: str = Field(..., max_length=255)
    file_path: str = Field(..., max_length=1000)
    mime_type: str = Field(..., max_length=100)
    size: int = Field(..., ge=0, description="Размер файла должен быть неотрицательным.")
    width: Optional[int] = None
    height: Optional[int] = None
    is_main: bool = False
    sort_order: int = 0

    class Config:
        from_attributes = True


class StandardServiceBase(BaseModel):
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    category_id: Optional[int] = None
    default_photo_id: Optional[int] = None

    class Config:
        from_attributes = True


class StandardServiceCreate(StandardServiceBase):
    pass


class StandardServiceUpdate(StandardServiceBase):
    pass


class StandardServiceOut(StandardServiceBase):
    id: int
    category: Optional[CategoryBase]  # Более сложная структура для категории

    class Config:
        from_attributes = True