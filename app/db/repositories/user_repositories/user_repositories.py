from typing import Optional, List
from db.repositories.base_repositories.base_repositories import BaseRepository
from db.repositories.location_repositories.city_repositories import CityRepository
from db.models.user.user import User, UserRole
from config.components.logging_config import logger


class UserRepository(BaseRepository):
    model = User

    @classmethod
    async def get_user_by_username(cls, username: str) -> Optional[User]:
        """Получение пользователя по имени."""
        return await cls.get_or_none(username=username)

    @classmethod
    async def get_user_by_email(cls, email: str) -> Optional[User]:
        """Получение пользователя по email."""
        return await cls.get_or_none(email=email)

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> Optional[User]:
        """Получение пользователя по ID."""
        return await cls.get_by_id_with_related(user_id, "city")

    @classmethod
    async def update_user(cls, user_id: int, update_data: dict) -> Optional[User]:
        """Обновление пользователя по ID."""
        await User.filter(id=user_id).update(**update_data)
        return await User.get_or_none(id=user_id)

    @classmethod
    async def create_user(cls, username: str, email: str, password: str, city_name: str, role: str) -> User:
        """Создание нового пользователя с валидацией."""
        logger.debug(
            f"Получен запрос на создание пользователя: username={username}, city_name={city_name}, role={role}")

        # Валидация роли
        if role not in UserRole.__members__.values():
            raise ValueError(f"Недопустимая роль: {role}. Возможные роли: {', '.join(UserRole.__members__.keys())}")

        # Валидация города
        city = await CityRepository.get_city_by_name(city_name)
        if not city:
            raise ValueError(f"Город {city_name} не найден.")

        # Проверка уникальности
        if await cls.is_username_used(username) or await cls.is_email_used(email):
            raise ValueError(f"Пользователь с именем '{username}' или email '{email}' уже существует.")

        # Создание пользователя через базовый метод
        user = await cls.create(
            username=username,
            email=email,
            password=password,
            city=city,
            role=role
        )

        return user

    @classmethod
    async def get_users_by_city(cls, city_name: str, limit: int = 10, offset: int = 0) -> List[User]:
        """Получение пользователей по городу с пагинацией."""
        city = await CityRepository.get_city_by_name(city_name)
        if not city:
            raise ValueError(f"Город {city_name} не найден.")

        return await cls.filter(limit=limit, offset=offset, city=city)

    @classmethod
    async def get_users_by_role(cls, role: UserRole, limit: int = 10, offset: int = 0) -> List[User]:
        """Получение пользователей по роли."""
        if role not in UserRole.__members__.values():
            raise ValueError(f"Роль {role} недопустима. Возможные роли: {', '.join(UserRole.__members__.keys())}")

        return await cls.filter(limit=limit, offset=offset, role=role)

    @classmethod
    async def is_username_used(cls, username: str) -> bool:
        """Проверка, используется ли имя пользователя."""
        return await cls.exists(username=username)

    @classmethod
    async def is_email_used(cls, email: str) -> bool:
        """Проверка, используется ли email."""
        return await cls.exists(email=email)

   # @classmethod
    #async def get_all_users(cls, limit: int = 10, offset: int = 0) -> List[User]:
      #  """Получение всех пользователей с пагинацией."""
      #  return await cls.get_all(limit=limit, offset=offset, "city")

    # Наследуем остальные методы от BaseRepository:
    # - update (как update_user)
    # - delete (как delete_user)
    # - bulk_create (как bulk_create_users)