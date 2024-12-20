from fastapi import APIRouter, HTTPException, status
from app.use_case.user.user_register import register_user
from config.components.logging_config import logger
from db.schemas.user_schemas.user_schemas import UserSchema

user_router = APIRouter()

@user_router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя",
    description="""
    Регистрация нового пользователя с указанием имени, электронной почты, пароля, города и роли.

    После успешной регистрации возвращает данные пользователя.

    Необходимые данные:
    - `username` (Имя пользователя, строка)
    - `email` (Электронная почта, строка)
    - `password` (Пароль, строка)
    - `city_name` (Город пользователя, строка)
    - `role` (Роль пользователя, строка, по умолчанию "client")
    """,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Пользователь успешно зарегистрирован",
            "model": UserSchema,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Ошибка валидации входных данных (например, пользователь уже существует)",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Ошибка на стороне сервера",
        },
    },
)
async def register(
    username: str,
    email: str,
    password: str,
    city_name: str,
    role: str = "client",
):
    """
    Эндпоинт для регистрации нового пользователя.
    """
    try:
        logger.info(f"Регистрация пользователя: {username}, город: {city_name}, роль: {role}")
        user = await register_user(username, email, password, city_name, role)
        logger.info(f"Пользователь {username} успешно зарегистрирован")
        return user
    except ValueError as e:
        logger.warning(f"Ошибка валидации данных при регистрации пользователя {username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Серверная ошибка при регистрации пользователя {username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при регистрации пользователя",
        )
