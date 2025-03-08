from fastapi import UploadFile
from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, Optional, List

# Исправленная схема для создания мастера
class MasterCreateSchema(BaseModel):
    city_id: Optional[int] = Field(None, title="ID города", example=1, description="Город, в котором находится мастер")
    user_id: int = Field(..., title="ID пользователя", example=1)
    title: str = Field(..., max_length=255, title="Заголовок", example="Опытный мастер маникюра")
    description: Optional[str] = Field(None, title="Описание мастера", example="Работаю в сфере маникюра более 5 лет.")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Специализируюсь на сложных дизайнах.")
    experience_years: int = Field(..., ge=0, title="Опыт работы в годах", example=5)
    specialty: str = Field(..., max_length=255, title="Специализация", example="Маникюр и педикюр")
    slug: str = Field(..., max_length=255, title="Slug (уникальный идентификатор)", example="opytnyj-master")
    name: str = Field(..., max_length=257, title="Имя мастера", example="Алина") # Исправлено max_length на 257
    address: str = Field(..., max_length=255, title="Адрес", example="ул. Ленина, 12") # Исправлено - поле стало обязательным
    phone: str = Field(..., max_length=20, title="Телефон", example="+7 900 123-45-67") # Исправлено - поле стало обязательным
    telegram: Optional[HttpUrl] = Field(None, title="Ссылка на Telegram", example="https://t.me/nailmaster")
    whatsapp: Optional[HttpUrl] = Field(None, title="Ссылка на WhatsApp", example="https://wa.me/79001234567")
    website: Optional[HttpUrl] = Field(None, title="Веб-сайт", example="https://alinanails.com")
    vk: Optional[HttpUrl] = Field(None, title="Ссылка на ВКонтакте", example="https://vk.com/nailmaster_alina")
    instagram: Optional[HttpUrl] = Field(None, title="Ссылка на Instagram", example="https://instagram.com/nailmaster_alina")
    accepts_at_home: bool = Field(False, title="Прием у себя")
    accepts_in_salon: bool = Field(False, title="Прием в салоне")
    accepts_offsite: bool = Field(False, title="Выезд к клиенту")
    avatar_file: Optional[UploadFile] = Field(None, description="Файл аватарки")

    class Config:
        from_attributes = True
        
# Исправленная схема для входящих данных на создание мастера (без изменений)
class MasterCreateInputSchema(BaseModel):
    title: str = Field(..., description="Название мастера")
    specialty: str = Field(..., description="Специализация мастера")
    experience_years: int = Field(..., ge=0, description="Опыт работы в годах") # Исправлено ранее - поле стало обязательным
    slug: Optional[str] = Field(None, description="Уникальный идентификатор")
    name: str = Field(..., description="Имя мастера")
    description: Optional[str] = Field(None, description="Описание мастера")
    text: Optional[str] = Field(None, description="Дополнительный текст")
    address: Optional[str] = Field(None, description="Адрес мастера")
    phone: Optional[str] = Field(None, description="Телефон мастера")
    telegram: Optional[HttpUrl] = Field(None, description="Telegram мастера")
    whatsapp: Optional[HttpUrl] = Field(None, description="WhatsApp мастера")
    website: Optional[HttpUrl] = Field(None, description="Веб-сайт мастера")
    vk: Optional[HttpUrl] = Field(None, description="ВКонтакте мастера")
    instagram: Optional[HttpUrl] = Field(None, description="Instagram мастера")
    accepts_at_home: bool = Field(False, description="Прием у себя")
    accepts_in_salon: bool = Field(False, description="Прием в салоне")
    accepts_offsite: bool = Field(False, description="Выезд к клиенту")
    avatar_file: Optional[UploadFile] = Field(None, description="Файл аватарки")

    class Config:
        from_attributes = True

# Схема для обновления мастера (без изменений)
class MasterUpdateSchema(BaseModel):
    city_id: Optional[int] = Field(None, title="ID города", example=1)
    title: Optional[str] = Field(None, max_length=255, title="Заголовок", example="Обновленный мастер маникюра")
    description: Optional[str] = Field(None, title="Описание мастера", example="Улучшенное описание.")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Больше информации.")
    experience_years: Optional[int] = Field(None, ge=0, title="Опыт работы в годах", example=7)
    specialty: Optional[str] = Field(None, max_length=255, title="Специализация", example="Наращивание ногтей")
    slug: Optional[str] = Field(None, max_length=255, title="Slug (уникальный идентификатор)", example="updated-master")
    name: Optional[str] = Field(None, max_length=257, title="Имя мастера", example="Алина")
    address: Optional[str] = Field(None, max_length=255, title="Адрес", example="ул. Ленина, 12")
    phone: Optional[str] = Field(None, max_length=20, title="Телефон", example="+7 900 123-45-67")
    telegram: Optional[HttpUrl] = Field(None, title="Ссылка на Telegram", example="https://t.me/nailmaster")
    whatsapp: Optional[HttpUrl] = Field(None, title="Ссылка на WhatsApp", example="https://wa.me/79001234567")
    website: Optional[HttpUrl] = Field(None, title="Веб-сайт", example="https://alinanails.com")
    vk: Optional[HttpUrl] = Field(None, title="Ссылка на ВКонтакте", example="https://vk.com/nailmaster_alina")
    instagram: Optional[HttpUrl] = Field(None, title="Ссылка на Instagram", example="https://instagram.com/nailmaster_alina")
    accepts_at_home: Optional[bool] = Field(None, title="Прием у себя")
    accepts_in_salon: Optional[bool] = Field(None, title="Прием в салоне")
    accepts_offsite: Optional[bool] = Field(None, title="Выезд к клиенту")
    avatar_file: Optional[UploadFile] = Field(None, description="Файл аватарки")

    class Config:
        from_attributes = True

class MasterDetailSchema(BaseModel):
    id: int
    user_id: int = Field(..., title="ID пользователя", example=1)
    title: str = Field(..., max_length=255, title="Заголовок", example="Опытный мастер маникюра")
    description: Optional[str] = Field(None, title="Описание мастера", example="Работаю в сфере маникюра более 5 лет.")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Специализируюсь на сложных дизайнах.")
    experience_years: int = Field(..., ge=0, title="Опыт работы в годах", example=5)
    specialty: str = Field(..., max_length=255, title="Специализация", example="Маникюр и педикюр")
    slug: str = Field(..., max_length=255, title="Slug (уникальный идентификатор)", example="opytnyj-master")
    name: str = Field(..., max_length=257, title="Имя мастера", example="Алина") # Исправлено max_length на 257
    address: str = Field(..., max_length=255, title="Адрес", example="ул. Ленина, 12") # Исправлено - поле стало обязательным
    phone: str = Field(..., max_length=20, title="Телефон", example="+7 900 123-45-67") # Исправлено - поле стало обязательным
    telegram: Optional[HttpUrl] = Field(None, title="Ссылка на Telegram", example="https://t.me/nailmaster")
    whatsapp: Optional[HttpUrl] = Field(None, title="Ссылка на WhatsApp", example="https://wa.me/79001234567")
    website: Optional[HttpUrl] = Field(None, title="Веб-сайт", example="https://alinanails.com")
    vk: Optional[HttpUrl] = Field(None, title="Ссылка на ВКонтакте", example="https://vk.com/nailmaster_alina")
    instagram: Optional[HttpUrl] = Field(None, title="Ссылка на Instagram", example="https://instagram.com/nailmaster_alina")
    accepts_at_home: bool = Field(False, title="Прием у себя")
    accepts_in_salon: bool = Field(False, title="Прием в салоне")
    accepts_offsite: bool = Field(False, title="Выезд к клиенту")
    avatar_urls: Optional[Dict[str, str]] = Field(
        None,
        description="Ссылки на аватарки"
    )
    class Config:
        from_attributes = True


# Схема для отображения списка мастеров (без изменений)
class MasterListSchema(BaseModel):
    slug: str = Field(..., title="Slug (уникальный идентификатор мастера)", example="opytnyj-master")
    name: str = Field(..., title="Имя мастера", example="Алина")
    address: Optional[str] = Field(None, title="Адрес", example="ул. Ленина, 12")
    phone: Optional[str] = Field(None, title="Телефон", example="+7 900 123-45-67")
    specialty: str = Field(..., title="Специализация мастера", example="Маникюр и педикюр")
    experience_years: int = Field(..., ge=0, title="Опыт работы в годах", example=5)
    accepts_at_home: bool = Field(False, title="Прием у себя")
    accepts_in_salon: bool = Field(False, title="Прием в салоне")
    accepts_offsite: bool = Field(False, title="Выезд к клиенту")

    class Config:
        from_attributes = True  # Поддержка работы с объектами Tortoise ORM


# Пример схемы для ответа с списком мастеров (без изменений)
class MasterListResponseSchema(BaseModel):
    masters: List[MasterListSchema] = Field(..., title="Список мастеров в городе")

    class Config:
        from_attributes = True  # Поддержка работы с объектами Tortoise ORM


# Исправленная схема для отображения мастера
class MasterOutSchema(BaseModel):
    id: int
    city_id: Optional[int]
    user_id: int
    title: str
    description: Optional[str]
    text: Optional[str]
    experience_years: int
    specialty: str
    slug: str
    name: str
    address: str = Field(..., title="Адрес") # Исправлено - поле стало обязательным
    phone: str = Field(..., title="Телефон") # Исправлено - поле стало обязательным
    telegram: Optional[str]
    whatsapp: Optional[str]
    website: Optional[str]
    vk: Optional[str]
    instagram: Optional[str]
    accepts_at_home: bool
    accepts_in_salon: bool
    accepts_offsite: bool

    class Config:
        from_attributes = True  # Поддержка работы с объектами Tortoise ORM

# Полная информация о мастере (связи) (без изменений)
class MasterFullSchema(BaseModel):
    master: MasterOutSchema
    services: Optional[List[dict]] = Field(None, title="Услуги", description="Список услуг мастера")
    resumes: Optional[List[dict]] = Field(None, title="Резюме", description="Список резюме мастера")
    applications: Optional[List[dict]] = Field(None, title="Заявки", description="Список заявок мастера")
    relations: Optional[List[dict]] = Field(None, title="Отношения с салонами", description="Список отношений с салонами мастера")