from pydantic import BaseModel, Field
from typing import Optional, List


class Service_Standart_Create_Schema(BaseModel):
    title: str = Field(..., max_length=255, title="Название услуги")
    description: Optional[str] = Field(None, title="Описание услуги")
    price: int = Field(..., title="Цена услуги")
    duration: int = Field(..., title="Продолжительность услуги (в минутах)")
    salon_id: int = Field(..., title="ID салона")

    class Config:
        from_attributes = True