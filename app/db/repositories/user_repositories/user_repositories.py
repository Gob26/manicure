from typing import Optional
from db.models.user.user import User

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
    async def create_user(username: str, email: str, password: str, city_id: int, role: str) -> User:
        """Создание нового пользователя."""
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
