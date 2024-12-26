from typing import Optional
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.photo_models import Photo

# Базовая схема для создания фотографий
PhotoCreateSchema = pydantic_model_creator(
    Photo,
    name="PhotoCreate",
    exclude=("id", "created_at", "updated_at")
)

# Схема для обновления фотографий
class PhotoUpdateSchema(BaseModel):
    is_main: Optional[bool] = None
    sort_order: Optional[int] = None
    caption: Optional[str] = None

# Схема для ответов
PhotoResponseSchema = pydantic_model_creator(
    Photo,
    name="PhotoResponse"
)

# Схема для списка фотографий
class PhotoListSchema(BaseModel):
    total: int
    items: list[PhotoResponseSchema]