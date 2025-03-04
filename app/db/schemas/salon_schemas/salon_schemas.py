from fastapi import UploadFile
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict


# Базовая схема для контактной информации
class ContactInfoSchema(BaseModel):
    phone: Optional[str] = Field(None, max_length=20, title="Телефон", example="+79123456789")
    telegram: Optional[str] = Field(None, max_length=255, title="Telegram", example="https://t.me/example")
    whatsapp: Optional[str] = Field(None, max_length=255, title="WhatsApp", example="https://wa.me/123456789")
    website: Optional[str] = Field(None, max_length=255, title="Веб-сайт", example="https://example.com")
    vk: Optional[str] = Field(None, max_length=255, title="ВКонтакте", example="https://vk.com/example")
    instagram: Optional[str] = Field(None, max_length=255, title="Instagram", example="https://instagram.com/example")


# Схема для респонс
class SalonCreateSchema(BaseModel):
    user_id: int = Field(..., title="ID пользователя", example=1)
    name: str = Field(..., max_length=255, title="Название", example="Салон Антуриум")
    title: str = Field(..., max_length=255, title="Заголовок", example="Лучший салон красоты")
    slug: str = Field(..., max_length=255, title="Slug (уникальный идентификатор)", example="salon-anturium")
    city_id: Optional[int] = Field(None, title="ID города", example=1)
    address: str = Field(..., max_length=255, title="Адрес", example="ул. Большая Филёвская, 21к1")

    # Контактная информация
    contact_info: ContactInfoSchema = Field(default_factory=ContactInfoSchema)

    # Опциональные поля с контентом
    description: Optional[str] = Field(None, title="Описание",
                                       example="Мы предоставляем высококачественные услуги красоты.")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Подробности о салоне.")


# Схема для создания салона без city и user_id
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


# Схема для обновления салона
class SalonUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255, title="Название")
    title: Optional[str] = Field(None, max_length=255, title="Заголовок")
    slug: Optional[str] = Field(None, max_length=255, title="Slug")
    city_id: Optional[int] = Field(None, title="ID города")
    address: Optional[str] = Field(None, max_length=255, title="Адрес")

    # Контактная информация
    contact_info: Optional[ContactInfoSchema] = Field(None)

    # Опциональные поля с контентом
    description: Optional[str] = Field(None, title="Описание")
    text: Optional[str] = Field(None, title="Дополнительная информация")

# Схема для отображения салона с  user_id(для чата)
class SalonDetailsSchema(BaseModel):
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
    avatar_urls: Optional[Dict[str,str]] = Field(None,
        discription="Словарь с ссылками на аватари под каждое устройство (ключи: pc, phone, tablet)"
    )
    user_id: int = Field(..., description="ID пользователя для чата и звонков")

    class Config:
        from_attributes = True

# Схема для отображения салона
class SalonOutSchema(BaseModel):
    id: int
    user_id: int
    name: str
    title: str
    slug: str
    city_id: Optional[int]
    address: str

    # Контактная информация
    contact_info: ContactInfoSchema

    # Опциональные поля с контентом
    description: Optional[str]
    text: Optional[str]

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


# Схема для отображения списка мастеров
class SalonListSchema(BaseModel):
    slug: str = Field(..., title="Slug (уникальный идентификатор салона)", example="opytnyj-master")
    name: str = Field(..., title="Название салона", example="Когти")
    address: Optional[str] = Field(None, title="Адрес", example="ул. Ленина, 13")
    phone: Optional[str] = Field(None, title="Телефон", example="+7 900 123-45-67")


