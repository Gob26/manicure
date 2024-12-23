from pydantic import BaseModel, Field
from typing import Optional, List


# Схема для создания салона
class SalonCreateSchema(BaseModel):
    user_id: int = Field(..., title="ID пользователя", example=1)
    title: str = Field(..., max_length=255, title="Заголовок", example="Лучший салон красоты")
    description: Optional[str] = Field(None, title="Описание", example="Мы предоставляем высококачественные услуги красоты.")
    name: str = Field(..., max_length=255, title="Название", example="Салон Антуриум")
    address: str = Field(..., max_length=255, title="Адрес", example="ул. Большая Филёвская, 21к1")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Подробности о салоне.")
    slug: str = Field(..., max_length=255, title="Slug (уникальный идентификатор)", example="salon-anturium")


# Схема для обновления салона
class SalonUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255, title="Заголовок", example="Обновленный салон красоты")
    description: Optional[str] = Field(None, title="Описание", example="Измененное описание салона.")
    name: Optional[str] = Field(None, max_length=255, title="Название", example="Новый Антуриум")
    address: Optional[str] = Field(None, max_length=255, title="Адрес", example="ул. Новый Адрес, 10")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Обновленная информация о салоне.")
    slug: Optional[str] = Field(None, max_length=255, title="Slug", example="new-salon-anturium")


# Схема для отображения салона
class SalonOutSchema(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    name: str
    address: str
    text: Optional[str]
    slug: str

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
