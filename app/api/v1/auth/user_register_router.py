from fastapi import APIRouter, HTTPException
from app.use_case.user.user_register import register_user
from config.components.logging_config import logger
from db.schemas.user_schemas.user_schemas import UserSchema

user_router = APIRouter()  # Переименование объекта

@user_router.post("/register", response_model=UserSchema)
async def register(username: str, email: str, password: str, city_name: str, role: str = "client"):
    try:
        logger.info(f"Пользователь {username} пытается зарегистрироваться")
        user = await register_user(username, email, password, city_name, role)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при регистрации пользователя")
