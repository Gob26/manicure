# utils/permissions.py
from fastapi import HTTPException, status


def check_user_permission(current_user: dict, allowed_roles: list):
    """
    Проверяет, есть ли у текущего пользователя права доступа.

    :param current_user: Данные текущего пользователя
    :param allowed_roles: Список ролей, которые могут выполнить действие
    :raises HTTPException: Если у пользователя нет нужных прав
    """
    if current_user["role"] not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для выполнения этого действия"
        )
