from pydantic import BaseModel
from typing import List, Optional


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    
    class Config:
        from_attributes = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    services: List[int]  # Список идентификаторов услуг в категории

    class Config:
        from_attributes = True
