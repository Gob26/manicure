from pydantic import BaseModel
from typing import Optional


class StandardServiceBase(BaseModel):
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    category_id: Optional[int] = None
    default_photo_id: Optional[int] = None

    class Config:
        from_attributes = True

class StandardServiceCreate(StandardServiceBase):
    pass

class StandardServiceUpdate(StandardServiceBase):
    pass

class StandardServiceOut(StandardServiceBase):
    id: int
    category: Optional[str]  # Название категории услуги
    default_photo_url: Optional[str]  # URL фото услуги

    class Config:
        from_attributes = True


class ServiceAttributeTypeBase(BaseModel):
    name: str
    slug: str

    class Config:
        from_attributes = True

class ServiceAttributeTypeCreate(ServiceAttributeTypeBase):
    pass

class ServiceAttributeTypeUpdate(ServiceAttributeTypeBase):
    pass

class ServiceAttributeTypeOut(ServiceAttributeTypeBase):
    id: int

    class Config:
        from_attributes = True


class ServiceAttributeValueBase(BaseModel):
    name: str
    slug: str
    attribute_type_id: int

    class Config:
        from_attributes = True

class ServiceAttributeValueCreate(ServiceAttributeValueBase):
    pass

class ServiceAttributeValueUpdate(ServiceAttributeValueBase):
    pass

class ServiceAttributeValueOut(ServiceAttributeValueBase):
    id: int
    attribute_type_name: str  # Название типа атрибута

    class Config:
        from_attributes = True


class TemplateAttributeBase(BaseModel):
    service_template_id: int
    attribute_type_id: int
    is_required: bool

    class Config:
        from_attributes = True

class TemplateAttributeCreate(TemplateAttributeBase):
    pass

class TemplateAttributeUpdate(TemplateAttributeBase):
    pass

class TemplateAttributeOut(TemplateAttributeBase):
    id: int
    service_template_name: str  # Название шаблона услуги
    attribute_type_name: str  # Название типа атрибута

    class Config:
        from_attributes = True
