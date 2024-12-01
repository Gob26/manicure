from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    city_name: str
    role: Optional[str] = "client"

    class Config:
        from_attributes = True