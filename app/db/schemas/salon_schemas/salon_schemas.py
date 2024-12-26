from pydantic import BaseModel, Field
from typing import Optional, List

# Схема для создания салона
class SalonCreateSchema(BaseModel):
    user_id: int = Field(..., title="ID пользователя", example=1)
    name: str = Field(..., max_length=255, title="Название", example="Салон Антуриум")
    title: str = Field(..., max_length=255, title="Заголовок", example="Лучший салон красоты")
    slug: str = Field(..., max_length=255, title="Slug (уникальный идентификатор)", example="salon-anturium")
    
    # Поля местоположения
    city_id: Optional[int] = Field(None, title="ID города", example=1, description="Город, в котором находится мастер")
    address:  str = Field(..., max_length=255, title="Адрес", example="ул. Большая Филёвская, 21к1")
    
    # Опциональные поля с контентом
    description: Optional[str] = Field(None, title="Описание", example="Мы предоставляем высококачественные услуги красоты.")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Подробности о салоне.")

# Схема для создания салона без city и user_id
class SalonCreateInputSchema(BaseModel):
    name: str = Field(..., max_length=255, title="Название", example="Салон Антуриум")
    title: str = Field(..., max_length=255, title="Заголовок", example="Лучший салон красоты")
    slug: str = Field(..., max_length=255, title="Slug (уникальный идентификатор)", example="salon-anturium")
    
    # Поля местоположения
    address: str = Field(..., max_length=255, title="Адрес", example="ул. Большая Филёвская, 21к1")
    
    # Опциональные поля с контентом
    description: Optional[str] = Field(None, title="Описание", example="Мы предоставляем высококачественные услуги красоты.")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Подробности о салоне.")

# Схема для обновления салона
class SalonUpdateSchema(BaseModel):
    # Основная информация
    name: Optional[str] = Field(None, max_length=255, title="Название", example="Новый Антуриум")
    title: Optional[str] = Field(None, max_length=255, title="Заголовок", example="Обновленный салон красоты")
    slug: Optional[str] = Field(None, max_length=255, title="Slug", example="new-salon-anturium")
    
    # Поля местоположения
    city_id: Optional[int] = Field(None, title="ID города", example=1, description="Город, в котором находится мастер")
    address: Optional[str] = Field(None, max_length=255, title="Адрес", example="ул. Новый Адрес, 10")
    
    # Поля с контентом
    description: Optional[str] = Field(None, title="Описание", example="Измененное описание салона.")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Обновленная информация о салоне.")

# Схема для отображения салона
class SalonOutSchema(BaseModel):
    id: int
    user_id: int
    
    # Основная информация
    name: str
    title: str
    slug: str
    
    # Информация о местоположении
    city: int
    address: str
    
    # Контент
    description: Optional[str]
    text: Optional[str]

    class Config:
        orm_mode = True  # Поддержка работы с объектами Tortoise ORM

# Полная информация о салоне (включая связанные данные)
class SalonFullSchema(BaseModel):
    salon: SalonOutSchema
    services: Optional[List[dict]] = Field(None, title="Услуги", description="Список услуг, предоставляемых салоном")
    relations: Optional[List[dict]] = Field(None, title="Отношения с мастерами", description="Список мастеров, связанных с салоном")
    vacancies: Optional[List[dict]] = Field(None, title="Вакансии", description="Список вакансий салона")
    invitations: Optional[List[dict]] = Field(None, title="Приглашения", description="Список приглашений мастеров")

    class Config:
        orm_mode = True