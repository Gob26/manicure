from typing import Optional
from tortoise.expressions import Q
from db.models.user.user import User
from db.models.location.city import City
from config.components.logging_config import logger


class UserRepository:
    @staticmethod
    async def get_city_by_name(name: str) -> Optional[City]:
        """
        Получение города по названию.
        """
        logger.debug(f"Поиск города: {name!r}")
        city = await City.get_or_none(Q(name__iexact=name))  # Поиск города по имени
        logger.debug(f"Результат поиска: {city!r}")
        return city  # Возвращаем найденный объект города
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Получение пользователя по имени."""
        return await User.get_or_none(username=username)
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Получение пользователя по email."""
        return await User.get_or_none(email=email)

    @staticmethod
    async def create_user(username: str, email: str, password: str, city_name: id, role: str) -> User:
        """Создание нового пользователя по имени, email и паролю и городу."""
        logger.debug(f"create_user: получено название города: {city_name!r}")
        city = await UserRepository.get_city_by_name(city_name)  # Используем название города для поиска
        logger.debug(f"create_user: найденный город: {city!r}")

        if not city:
            raise ValueError(f"Город {city_name} не найден")  # Добавляем проверку на отсутствие города

        user = await User.create(
            username=username,
            email=email,
            password=password,
            city=city,  # Используем ID найденного города
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
