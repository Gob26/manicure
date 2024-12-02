from fastapi import APIRouter, HTTPException
from db.schemas.user_schemas.user_login_schema import UserLoginSchema
from app.use_case.user.user_login import login
from config.components.logging_config import logger

login_router = APIRouter()

@login_router.post("/login", response_model=UserLoginSchema)
async def login_route(credentials: UserLoginSchema):
    try:
        user = await login(credentials.username, credentials.password)
        return user
    except HTTPException as e:
        logger.error(f"Ошибка при логине: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Ошибка при логине: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")
