from pydantic import BaseModel
from typing import List, Optional

class ServiceAttributeTypeCreateSchema(BaseModel):
    name: str
    slug: str

class ServiceAttributeTypeResponseSchema(ServiceAttributeTypeCreateSchema):
    id: int

    class Config:
        from_attributes = True


class ServiceAttributeValueCreateSchema(BaseModel):
    attribute_type_id: int
    name: str
    slug: str

class ServiceAttributeValueResponseSchema(ServiceAttributeValueCreateSchema):
    id: int

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
