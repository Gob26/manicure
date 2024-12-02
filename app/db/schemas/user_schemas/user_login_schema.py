from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    username: str
    password: str


    class Config:
        orm_mode = True  # Чтобы Pydantic мог работать с ORM моделями (например, Tortoise ORM)

    