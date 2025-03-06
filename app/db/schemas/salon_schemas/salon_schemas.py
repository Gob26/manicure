from fastapi import UploadFile
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict

# Схема для создания салона (POST)
class SalonCreateSchema(BaseModel):
    user_id: int = Field(..., title="ID пользователя", example=1)
    name: str = Field(..., max_length=255, title="Название", example="Салон Антуриум")
    title: str = Field(..., max_length=255, title="Заголовок", example="Лучший салон красоты")
    slug: str = Field(..., max_length=255, title="Slug (уникальный идентификатор)", example="salon-anturium")
    city_id: Optional[int] = Field(None, title="ID города", example=1)
    address: str = Field(..., max_length=255, title="Адрес", example="ул. Большая Филёвская, 21к1")

    # Контактная информация (обязательное поле phone)
    phone: str = Field(..., max_length=20, title="Телефон", example="+79123456789")
    telegram: Optional[str] = Field(None, max_length=255, title="Telegram", example="https://t.me/example")
    whatsapp: Optional[str] = Field(None, max_length=255, title="WhatsApp", example="https://wa.me/123456789")
    website: Optional[str] = Field(None, max_length=255, title="Веб-сайт", example="https://example.com")
    vk: Optional[str] = Field(None, max_length=255, title="ВКонтакте", example="https://vk.com/example")
    instagram: Optional[str] = Field(None, max_length=255, title="Instagram", example="https://instagram.com/example")

    # Опциональные поля с контентом
    description: Optional[str] = Field(None, title="Описание",
                                       example="Мы предоставляем высококачественные услуги красоты.")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Подробности о салоне.")
    # Добавьте avatar_urls
    avatar_urls: Optional[Dict[str, str]] = Field(
        None,
        description="Ссылки на аватарки"
    )
    class Config:
        from_attributes = True


# Схема для создания салона через Form (POST)
class SalonCreateInputSchema(BaseModel):
    name: str = Field(..., description="Имя салона")
    title: str = Field(..., description="Тайтл салона")
    slug: Optional[str] = Field(None, description="Уникальный идентификатор")
    description: Optional[str] = Field(None, description="Описание салона")
    text: Optional[str] = Field(None, description="Дополнительный текст")
    address: str = Field(..., description="Адрес салона")
    phone: str = Field(..., description="Телефон салона")
    telegram: Optional[HttpUrl] = Field(None, description="Telegram салона")
    whatsapp: Optional[HttpUrl] = Field(None, description="WhatsApp салона")
    website: Optional[HttpUrl] = Field(None, description="Веб-сайт салона")
    vk: Optional[HttpUrl] = Field(None, description="ВКонтакте салона")
    instagram: Optional[HttpUrl] = Field(None, description="Instagram салона")
    avatar_file: Optional[UploadFile] = Field(None, description="Файл аватарки")

    class Config:
        from_attributes = True


# Схема для обновления салона (PUT)
class SalonUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, description="Имя салона")
    title: Optional[str] = Field(None, description="Тайтл салона")
    slug: Optional[str] = Field(None, description="Уникальный идентификатор")
    description: Optional[str] = Field(None, description="Описание салона")
    text: Optional[str] = Field(None, description="Дополнительный текст")
    address: Optional[str] = Field(None, description="Адрес салона")
    phone: Optional[str] = Field(None, description="Телефон салона")
    telegram: Optional[HttpUrl] = Field(None, description="Telegram салона")
    whatsapp: Optional[HttpUrl] = Field(None, description="WhatsApp салона")
    website: Optional[HttpUrl] = Field(None, description="Веб-сайт салона")
    vk: Optional[HttpUrl] = Field(None, description="ВКонтакте салона")
    instagram: Optional[HttpUrl] = Field(None, description="Instagram салона")
    avatar_file: Optional[UploadFile] = Field(None, description="Файл аватарки")

    class Config:
        from_attributes = True


# Схема для детальной информации с user_id
class SalonDetailsSchema(BaseModel):
    id: int
    user_id: int = Field(..., description="ID пользователя для чата и звонков")
    name: str = Field(..., description="Имя салона")
    title: str = Field(..., description="Тайтл салона")
    slug: Optional[str] = Field(None, description="Уникальный идентификатор")
    address: str = Field(..., description="Адрес салона")
    phone: str = Field(..., description="Телефон салона")
    telegram: Optional[HttpUrl] = Field(None, description="Telegram салона")
    whatsapp: Optional[HttpUrl] = Field(None, description="WhatsApp салона")
    website: Optional[HttpUrl] = Field(None, description="Веб-сайт салона")
    vk: Optional[HttpUrl] = Field(None, description="ВКонтакте салона")
    instagram: Optional[HttpUrl] = Field(None, description="Instagram салона")
    avatar_urls: Optional[Dict[str, str]] = Field(
        None,
        description="Словарь с ссылками на аватары для разных устройств"
    )
    description: Optional[str] = Field(None, description="Описание")
    text: Optional[str] = Field(None, description="Дополнительный текст")

    class Config:
        from_attributes = True


# Схема для отображения салона (GET)
class SalonOutSchema(BaseModel):
    id: int
    user_id: int
    name: str
    title: str
    slug: Optional[str]
    city_id: Optional[int]
    address: str
    phone: str  # Обязательное поле (null=False в модели)
    telegram: Optional[str]
    whatsapp: Optional[str]
    website: Optional[str]
    vk: Optional[str]
    instagram: Optional[str]
    description: Optional[str]
    text: Optional[str]
    # Добавьте avatar_urls
    avatar_urls: Optional[Dict[str, str]] = Field(
        None,
        description="Ссылки на аватарки"
    )

    class Config:
        from_attributes = True


# Полная информация о салоне
class SalonFullSchema(BaseModel):
    salon: SalonOutSchema
    services: Optional[List[dict]] = Field(None, title="Услуги")
    relations: Optional[List[dict]] = Field(None, title="Отношения с мастерами")
    vacancies: Optional[List[dict]] = Field(None, title="Вакансии")
    invitations: Optional[List[dict]] = Field(None, title="Приглашения мастеров")

    class Config:
        from_attributes = True


# Схема для списка салонов
class SalonListSchema(BaseModel):
    slug: str = Field(..., title="Slug (уникальный идентификатор салона)", example="opytnyj-master")
    name: str = Field(..., title="Название салона", example="Когти")
    address: Optional[str] = Field(None, title="Адрес", example="ул. Ленина, 13")
    phone: Optional[str] = Field(None, title="Телефон", example="+7 900 123-45-67")