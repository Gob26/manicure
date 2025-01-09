from pydantic import BaseModel
from typing import Optional

class CustomServiceBase(BaseModel):
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    master_id: Optional[int] = None
    salon_id: Optional[int] = None
    standard_service_id: int
    base_price: float
    duration_minutes: int
    is_active: bool
    additional_description: Optional[str] = None

    class Config:
        orm_mode = True

class CustomServiceCreate(CustomServiceBase):
    pass

class CustomServiceUpdate(CustomServiceBase):
    pass

class CustomServiceOut(CustomServiceBase):
    id: int
    master_name: Optional[str]  # Имя мастера (если связано)
    salon_name: Optional[str]  # Название салона (если связано)
    standard_service_name: str  # Название базовой услуги

    class Config:
        orm_mode = True


from pydantic import BaseModel

class CustomServiceAttributeBase(BaseModel):
    custom_service_id: int
    attribute_value_id: int
    additional_price: float
    is_active: bool

    class Config:
        orm_mode = True

class CustomServiceAttributeCreate(CustomServiceAttributeBase):
    pass

class CustomServiceAttributeUpdate(CustomServiceAttributeBase):
    pass

class CustomServiceAttributeOut(CustomServiceAttributeBase):
    id: int
    custom_service_name: str  # Название пользовательской услуги
    attribute_value_name: str  # Название атрибута

    class Config:
        orm_mode = True
