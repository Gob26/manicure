from pydantic import BaseModel
from typing import Optional


class VacancyCreateSchema(BaseModel):
    title: str
    position: str
    description: Optional[str] = None

class VacancyResponseSchema(VacancyCreateSchema):
    id: int
    status: str

    class Config:
        from_attributes = True
