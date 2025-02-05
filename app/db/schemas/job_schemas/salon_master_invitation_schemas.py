from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SalonMasterInvitationCreateSchema(BaseModel):
    master_id: int
    vacancy_id: Optional[int] = None  # может быть без привязки к вакансии
    message: Optional[str] = None
    expires_at: Optional[datetime] = None

class SalonMasterInvitationResponseSchema(BaseModel):
    id: int
    salon_id: int
    master_id: int
    vacancy_id: Optional[int]
    status: str
    message: Optional[str]
    expires_at: Optional[datetime]
    notification_status: str
    response_date: Optional[datetime]

    class Config:
        from_attributes = True
