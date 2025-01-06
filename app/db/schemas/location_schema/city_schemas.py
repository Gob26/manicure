from pydantic import BaseModel, Field
from typing import Optional

# Схема для создания города
class CityCreateSchema(BaseModel):
    name: str = Field(..., max_length=100, title="Название города", example="Москва")
    district: str = Field(..., max_length=50, title="Район", example="Центральный")
    subject: str = Field(..., max_length=100, title="Субъект РФ", example="Московская область")
    population: int = Field(..., ge=0, title="Население", example=12506468)
    latitude: float = Field(..., title="Широта", example=55.7558)
    longitude: float = Field(..., title="Долгота", example=37.6173)
    slug: str = Field(..., max_length=255, title="Слаг (уникальный идентификатор)", example="moskva")

# Схема для отображения города
class CityOutSchema(BaseModel):
    id: int
    name: str
    district: str
    subject: str
    population: int
    latitude: float
    longitude: float
    slug: str

    class Config:
        from_attributes = True

# Схема для создания описания города
class CityDescriptionCreateSchema(BaseModel):
    city_id: int = Field(..., title="ID города", example=1)
    title: Optional[str] = Field(None, max_length=255, title="Заголовок", example="Крупнейший город России")
    description: Optional[str] = Field(None, title="Описание", example="Москва — столица Российской Федерации.")
    text: Optional[str] = Field(None, title="Дополнительный текст", example="Историческая информация о городе.")

# Схема для отображения описания города
class CityDescriptionOutSchema(BaseModel):
    id: int
    city_id: int
    title: Optional[str]
    description: Optional[str]
    text: Optional[str]

    class Config:
        from_attributes = True

# Полная информация о городе с описанием
class FullCitySchema(BaseModel):
    city: CityOutSchema
    description: Optional[CityDescriptionOutSchema]

class CityLinkSchema(BaseModel):
    """Схема для отображения города со ссылкой"""
    id: int
    name: str = Field(..., description="Название города")
    slug: str = Field(..., description="Слаг для URL")
    url: str = Field(..., description="Ссылка на страницу города")
    count_masters: int = Field(default=0, description="Количество мастеров")
    count_salons: int = Field(default=0, description="Количество салонов")

    class Config:
        from_attributes = True