from typing import Optional, List
from tortoise.exceptions import DoesNotExist
from db.repositories.location_repositories.city_repositories import CityRepository
from db.models.user.user import User, UserRole
from config.components.logging_config import logger


class UserRepository:
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Получение пользователя по имени."""
        return await User.get_or_none(username=username)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Получение пользователя по email."""
        return await User.get_or_none(email=email)

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        """Получение пользователя по ID."""
        return await User.get_or_none(id=user_id).prefetch_related("city")

    @staticmethod
    async def create_user(username: str, email: str, password: str, city_name: str, role: str) -> User:
        """Создание нового пользователя."""
        logger.debug(f"Получен запрос на создание пользователя: username={username}, city_name={city_name}, role={role}")

        # Проверка роли
        if role not in UserRole.__members__.values():
            raise ValueError(f"Недопустимая роль: {role}. Возможные роли: {', '.join(UserRole.__members__.keys())}")

        # Проверка города
        city = await CityRepository.get_city_by_name(city_name)
        if not city:
            raise ValueError(f"Город {city_name} не найден.")

        # Проверка уникальности пользователя
        if await UserRepository.get_user_by_username(username) or await UserRepository.get_user_by_email(email):
            raise ValueError(f"Пользователь с именем '{username}' или email '{email}' уже существует.")

        user = await User.create(
            username=username,
            email=email,
            password=password,
            city=city,
            role=role
        )
        logger.info(f"Пользователь {username} создан в городе {city.name} с ролью {role}.")
        return user

    @staticmethod
    async def update_user(user_id: int, **kwargs) -> int:
        """Обновление пользователя по ID."""
        updated_count = await User.filter(id=user_id).update(**kwargs)
        if updated_count:
            logger.info(f"Пользователь с ID {user_id} успешно обновлен: {kwargs}")
        else:
            logger.warning(f"Пользователь с ID {user_id} не найден.")
        return updated_count

    @staticmethod
    async def delete_user(user_id: int) -> int:
        """Удаление пользователя по ID."""
        deleted_count = await User.filter(id=user_id).delete()
        if deleted_count:
            logger.info(f"Пользователь с ID {user_id} успешно удален.")
        else:
            logger.warning(f"Пользователь с ID {user_id} не найден.")
        return deleted_count

    @staticmethod
    async def get_users_by_city(city_name: str, limit: int = 10, offset: int = 0) -> List[User]:
        """Получение пользователей по городу с пагинацией."""
        city = await CityRepository.get_city_by_name(city_name)
        if not city:
            raise ValueError(f"Город {city_name} не найден.")
        users = await User.filter(city=city).offset(offset).limit(limit).all()
        logger.info(f"Найдено {len(users)} пользователей в городе {city_name}.")
        return users

    @staticmethod
    async def get_users_by_role(role: UserRole, limit: int = 10, offset: int = 0) -> List[User]:
        """Получение пользователей по роли."""
        if role not in UserRole.__members__.values():
            raise ValueError(f"Роль {role} недопустима. Возможные роли: {', '.join(UserRole.__members__.keys())}")
        users = await User.filter(role=role).offset(offset).limit(limit).all()
        logger.info(f"Найдено {len(users)} пользователей с ролью {role}.")
        return users

    @staticmethod
    async def is_username_used(username: str) -> bool:
        """Проверка, используется ли имя пользователя."""
        exists = await User.filter(username=username).exists()
        logger.debug(f"Проверка имени пользователя '{username}': {exists}")
        return exists

    @staticmethod
    async def is_email_used(email: str) -> bool:
        """Проверка, используется ли email."""
        exists = await User.filter(email=email).exists()
        logger.debug(f"Проверка email '{email}': {exists}")
        return exists

    @staticmethod
    async def bulk_create_users(users_data: List[dict]) -> List[User]:
        """Массовое создание пользователей."""
        users = await User.bulk_create([User(**data) for data in users_data], batch_size=100)
        logger.info(f"Массовое создание пользователей завершено. Создано {len(users)} записей.")
        return users

    @staticmethod
    async def get_all_users(limit: int = 10, offset: int = 0) -> List[User]:
        """Получение всех пользователей с пагинацией."""
        users = await User.all().offset(offset).limit(limit).prefetch_related("city")
        logger.info(f"Найдено {len(users)} пользователей.")
        return users
