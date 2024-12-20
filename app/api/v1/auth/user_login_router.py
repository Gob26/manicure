from fastapi import APIRouter, HTTPException, status
from db.schemas.user_schemas.user_login_schema import UserLoginSchema
from app.use_case.user.user_login import login
from config.components.logging_config import logger

login_router = APIRouter()

@login_router.post(
    "/login",
    response_model=UserLoginSchema,
    status_code=status.HTTP_200_OK,
    summary="Авторизация пользователя",
    description="""
    Выполняет авторизацию пользователя на основе предоставленных учетных данных (логин и пароль).

    После успешной авторизации возвращает данные пользователя, включая токены или другие необходимые параметры для работы с API.

    Необходимые разрешения:
    - Учетная запись пользователя должна быть активной
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Пользователь успешно авторизован",
            "model": UserLoginSchema,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Неверные учетные данные",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Ошибка на сервере",
        },
    },
)
async def login_route(credentials: UserLoginSchema):
    """
    Эндпоинт для авторизации пользователя.
    """
    try:
        logger.info(f"Попытка входа пользователя: {credentials.username}")
        user = await login(credentials.username, credentials.password)
        return user
    except HTTPException as e:
        logger.error(f"Ошибка при логине пользователя {credentials.username}: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Серверная ошибка при логине пользователя {credentials.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка сервера",
        )
