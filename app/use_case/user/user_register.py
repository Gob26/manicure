from passlib.context import CryptContext
from fastapi import HTTPException, status
from db.repositories.location_repositories.city_repositories import CityRepository
from db.repositories.user_repositories.user_repositories import UserRepository
from config.components.logging_config import logger
from use_case.utils.email_services.send_jwt_email import send_confirmation_email
from use_case.utils.jwt_handler import create_confirmation_token

# Инициализируем контекст для работы с хешами паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def check_user_exists(username: str, email: str):
    """Проверяет, существует ли пользователь с таким username или email"""
    if await UserRepository.get_user_by_username(username):
        logger.warning(f"Пользователь с таким именем уже существует: {username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует",
        )

    if await UserRepository.get_user_by_email(email):
        logger.warning(f"Пользователь с таким email уже существует: {email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )


async def register_user(username: str, email: str, password: str, city_name: str, role: str):
    try:
        logger.info(f"Пользователь {username} пытается зарегистрироваться с городом {city_name}")

        # Проверяем, существует ли пользователь
        await check_user_exists(username, email)

        # Проверяем, существует ли город
        city = await CityRepository.get_city_by_name(city_name)
        if not city:
            logger.error(f"Город с названием {city_name} не найден")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Город с названием {city_name} не найден",
            )

        logger.info(f"Город {city_name} найден, ID: {city.id}")

        # Хешируем пароль и создаем пользователя
        hashed_password = hash_password(password)
        user = await UserRepository.create_user(
            username=username,
            email=email,
            password=hashed_password,
            city_name=city_name,
            role=role,
        )

        # Генерация токена подтверждения
        confirmation_token = create_confirmation_token(user.id, email)

        # Отправка письма с токеном
        await send_confirmation_email(email, confirmation_token)

        logger.info(f"Письмо с подтверждением отправлено на {email}")
        logger.info(f"Пользователь {username} успешно зарегистрирован.")

        return user

    except HTTPException:
        raise  # Если уже поднята HTTPException, просто пробрасываем дальше

    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя {username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при регистрации пользователя",
        )
