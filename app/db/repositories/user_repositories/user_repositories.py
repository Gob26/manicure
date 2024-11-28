from db.models.user.user import User


class UserRepository:
    @staticmethod
    async def get_user_by_username(username: str) -> User|None:
        return await User.get_or_none(username=username)
    

    @staticmethod
    async def create_user(username: str, email: str, password: str, city_id: str, role: str) -> User:
        return await User.create(
            username=username,
            email=email,
            password=password,
            city_id=city_id,
            role=role
        )


    @staticmethod
    async def update_user(user_id: int, **kwargs) -> int:
        return await User.filter(id=user_id).update(**kwargs)
    

    @staticmethod
    async def delete_user(user_id: int) -> int:
        return await User.filter(id=user_id).delete()

