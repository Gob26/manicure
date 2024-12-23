from pydantic import BaseModel, Field
from typing import Optional, List

# Схема для создания мастера
class MasterCreateSchema(BaseModel):
    city_id: Optional[int] = Field(None, title="ID города", example=1, description="Город, в котором находится мастер")
    user_id: int = Field(..., title="ID пользователя", example=1)
    title: str = Field(..., max_length=255, title="Заголовок", example="Опытный мастер маникюра")
    description: Optional[str] = Field(None, title="Описание мастера", example="Работаю в сфере маникюра более 5 лет.")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Специализируюсь на сложных дизайнах.")
    experience_years: int = Field(..., ge=0, title="Опыт работы в годах", example=5)
    specialty: str = Field(..., max_length=255, title="Специализация", example="Маникюр и педикюр")
    slug: str = Field(..., max_length=255, title="Slug (уникальный идентификатор)", example="opytnyj-master")


# Схема для обновления мастера
class MasterUpdateSchema(BaseModel):
    city_id: Optional[int] = Field(None, title="ID города", example=1)
    title: Optional[str] = Field(None, max_length=255, title="Заголовок", example="Обновленный мастер маникюра")
    description: Optional[str] = Field(None, title="Описание мастера", example="Улучшенное описание.")
    text: Optional[str] = Field(None, title="Дополнительная информация", example="Больше информации.")
    experience_years: Optional[int] = Field(None, ge=0, title="Опыт работы в годах", example=7)
    specialty: Optional[str] = Field(None, max_length=255, title="Специализация", example="Наращивание ногтей")
    slug: Optional[str] = Field(None, max_length=255, title="Slug (уникальный идентификатор)", example="updated-master")


# Схема для отображения мастера
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

    class Config:
        orm_mode = True  # Поддержка работы с объектами Tortoise ORM


# Полная информация о мастере (связи)
class MasterFullSchema(BaseModel):
    master: MasterOutSchema
    services: Optional[List[dict]] = Field(None, title="Услуги", description="Список услуг мастера")
    resumes: Optional[List[dict]] = Field(None, title="Резюме", description="Список резюме мастера")
    applications: Optional[List[dict]] = Field(None, title="Заявки", description="Список заявок мастера")
    relations: Optional[List[dict]] = Field(None, title="Отношения с салонами", description="Список отношений с салонами мастера")
