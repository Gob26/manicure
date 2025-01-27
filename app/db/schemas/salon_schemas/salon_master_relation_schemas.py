from datetime import date
from enum import Enum
from pydantic import BaseModel, Field

class StatusEnum(str, Enum):
    active = "active"
    pending = "pending"
    inactive = "inactive"

class RoleEnum(str, Enum):
    employee = "employee"
    freelancer = "freelancer"

class SalonMasterRelationCreate(BaseModel):
    salon_id: int = Field(..., description="ID салона")
    master_id: int = Field(..., description="ID мастера")
    status: StatusEnum = StatusEnum.pending
    role: RoleEnum = RoleEnum.employee
    start_date: date | None = None
    end_date: date | None = None
    notes: str | None = None

class SalonMasterRelationResponse(SalonMasterRelationCreate):
    id: int

    class Config:
        from_attributes = True