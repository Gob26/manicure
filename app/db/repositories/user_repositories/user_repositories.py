from typing import Optional
from tortoise.expressions import Q
from db.models.user.user import User
from db.models.location.city import City


class UserRepository:
    @staticmethod
    async def get_city_by_name(name: str ) -> Optional[City]:
        """
        Получение города по названию.
        """
        return await City.get_or_none(Q(name__iexact=name))
    
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
        """Создание нового пользователя  по имени, email и паролю и городу."""
        city = await UserRepository.get_city_by_name(city_name)
        if not city:
            raise ValueError(f"Город {city_name} не найден")
        return await User.create(
            username=username,
            email=email,
            password=password,
            city_id=city_id,
            role=role
        )

    @staticmethod
    async def update_user(user_id: int, **kwargs) -> int:
        """Обновление данных пользователя по его ID."""
        return await User.filter(id=user_id).update(**kwargs)

    @staticmethod
    async def delete_user(user_id: int) -> int:
        """Удаление пользователя по ID."""
        return await User.filter(id=user_id).delete()
