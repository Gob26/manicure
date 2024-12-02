from typing import Optional
from db.repositories.location_repositories.city_repositories import CityRepository
from db.models.user.user import User
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
    async def create_user(username: str, email: str, password: str, city_name: str, role: str) -> User:
        """Создание нового пользователя по имени, email и паролю и городу."""
        logger.debug(f"create_user: получено название города: {city_name!r}")

        # Используем CityRepository для поиска города
        city = await CityRepository.get_city_by_name(city_name)  # Вызываем метод get_city_by_name из CityRepository
        logger.debug(f"create_user: найденный город: {city!r}")

        if not city:
            raise ValueError(f"Город {city_name} не найден")  # Проверка на отсутствие города

        # Проверка, существует ли уже пользователь с таким именем
        existing_user = await UserRepository.get_user_by_username(username)
        if existing_user:
            raise ValueError(f"Пользователь с именем {username} уже существует")

        user = await User.create(
            username=username,
            email=email,
            password=password,
            city=city,  # Используем найденный город
            role=role
        )
        logger.info(f"Пользователь {username} успешно зарегистрирован в городе {city_name}")
        return user

    @staticmethod
    async def update_user(user_id: int, **kwargs) -> int:
        """Обновление данных пользователя по его ID."""
        return await User.filter(id=user_id).update(**kwargs)

    @staticmethod
    async def delete_user(user_id: int) -> int:
        """Удаление пользователя по ID."""
        return await User.filter(id=user_id).delete()
