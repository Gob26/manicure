from pydantic import BaseModel
from typing import Optional

class JobApplicationCreateSchema(BaseModel):
    vacancy_id: int
    message: Optional[str] = None

class JobApplicationResponseSchema(BaseModel):
    id: int
    vacancy_id: int
    master_id: int
    status: str
    message: Optional[str] = None

    class Config:
        from_attributes = True
