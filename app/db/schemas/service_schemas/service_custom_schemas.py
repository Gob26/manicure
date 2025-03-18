from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal


# Схема для вывода CustomService
class CustomServiceOut(BaseModel):
    id: int
    master_id: Optional[int] = Field(None, description="ID мастера, предоставляющего услугу")
    salon_id: Optional[int] = Field(None, description="ID салона, предоставляющего услугу")
    standard_service_id: int
    base_price: Decimal = Field(..., description="Базовая стоимость услуги")
    duration_minutes: int = Field(..., description="Длительность услуги в минутах")
    is_active: bool = Field(..., description="Активна ли услуга")
    description: Optional[str] = Field(None, description="Дополнительное описание услуги")

    class Config:
        from_attributes = True


# Схема для создания CustomService
class CustomServiceCreate(BaseModel):
    master_id: Optional[int] = Field(None, description="ID мастера, предоставляющего услугу")
    salon_id: Optional[int] = Field(None, description="ID салона, предоставляющего услугу")
    standard_service_id: int
    base_price: Decimal = Field(..., description="Базовая стоимость услуги")
    duration_minutes: int = Field(..., description="Длительность услуги в минутах")
    is_active: Optional[bool] = Field(True, description="Активна ли услуга")
    description: Optional[str] = Field(None, description="Дополнительное описание услуги")


# Схема для обновления CustomService
class CustomServiceUpdate(BaseModel):

    standard_service_id: Optional[int] = Field(None, description="ID базовой услуги")
    base_price: Optional[Decimal] = Field(None, description="Базовая стоимость услуги")
    duration_minutes: Optional[int] = Field(None, description="Длительность услуги в минутах")
    is_active: Optional[bool] = Field(None, description="Активна ли услуга")
    description: Optional[str] = Field(None, description="Дополнительное описание услуги")


# Схема для вывода CustomServiceAttribute
class CustomServiceAttributeOut(BaseModel):
    id: int
    custom_service_id: int
    attribute_value_id: int
    additional_price: Decimal = Field(..., description="Дополнительная стоимость за атрибут")
    is_active: bool = Field(..., description="Активен ли атрибут")

    class Config:
        from_attributes = True


# Схема для создания CustomServiceAttribute
class CustomServiceAttributeCreate(BaseModel):
    custom_service_id: int
    attribute_value_id: int
    additional_price: Optional[Decimal] = Field(0, description="Дополнительная стоимость за атрибут")
    is_active: Optional[bool] = Field(True, description="Активен ли атрибут")


# Схема для обновления CustomServiceAttribute
class CustomServiceAttributeUpdate(BaseModel):
    additional_price: Optional[Decimal] = Field(None, description="Дополнительная стоимость за атрибут")
    is_active: Optional[bool] = Field(None, description="Активен ли атрибут")
