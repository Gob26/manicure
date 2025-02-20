from fastapi import APIRouter, HTTPException, status, Form
from use_case.user.user_login import login
from config.components.logging_config import logger
from config.envs.development import Settings

settings = Settings()
login_router = APIRouter()

@login_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Авторизация пользователя",
    description="Данный endpoint предназначен для аутентификации пользователя на основе логина и пароля. Данные передаются в формате form-data.",
    responses={
        status.HTTP_200_OK: {
            "description": "Пользователь успешно авторизован",
            "content": {"application/json": {"example": {"access_token": "JWT токен", "token_type": "bearer", "username": "Имя пользователя", "user_id": "ID пользователя", "role": "Роль", "city": "Город"}}},
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Неверные учетные данные"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Ошибка на сервере"},
    },
)
async def login_route(
        username: str = Form(...),
        password: str = Form(...)):
    try:
        logger.info(f"Попытка входа пользователя: {username}")

        # Выполняем проверку логина
        user_data = await login(username, password)

        if not user_data:
            logger.warning(f"Не найден пользователь с логином: {username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверные учетные данные"
            )

        logger.info(f"Пользователь {username} успешно авторизован")

        return {
            "access_token": user_data["access_token"],
            "token_type": user_data["token_type"],
            "username": user_data["username"],
            "user_id": user_data["user_id"],  # user_id будет возвращён из функции login
            "role": user_data["role"],
            "city": user_data["city"],  # Город пользователя
            "is_confirmed": user_data["is_confirmed"],  # Добавляем в проверку подтверждения
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        }

    except HTTPException as e:
        logger.error(f"Ошибка при логине пользователя {username}: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Серверная ошибка при логине пользователя {username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка сервера"
        )