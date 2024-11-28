from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "client"

    class Config:
        orm_mode = True
