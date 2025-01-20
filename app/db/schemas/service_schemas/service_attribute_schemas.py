from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class ServiceAttributeTypeCreateSchema(BaseModel):
    name: str
    slug: str = Field(default="", description="Slug типа атрибута (может быть пустым)")

class ServiceAttributeTypeResponseSchema(ServiceAttributeTypeCreateSchema):
    id: int

    class Config:
        from_attributes = True

class ServiceAttributeTypeDictResponseSchema(BaseModel):
    data: Dict[str, str]


class ServiceAttributeValueCreateSchema(BaseModel):
    attribute_type_id: int = Field(..., description="Идентификатор типа атрибута")
    name: str = Field(..., min_length=1, max_length=100, description="Название значения атрибута")
    slug: str = Field(
        default="", 
        max_length=100, 
        description="Slug типа атрибута (уникальный идентификатор, может быть пустым)"
    )

class ServiceAttributeValueResponseSchema(ServiceAttributeValueCreateSchema):
    id: int = Field(..., description="Идентификатор значения атрибута")

    class Config:
        from_attributes = True


class TemplateAttributeCreateSchema(BaseModel):
    service_template_id: int
    attribute_type_id: int
    is_required: Optional[bool] = False

class TemplateAttributeResponseSchema(TemplateAttributeCreateSchema):
    id: int

    class Config:
        from_attributes = True
