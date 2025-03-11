from fastapi import HTTPException, status
from db.repositories.user_repositories.user_repositories import UserRepository
from config.components.logging_config import logger
from use_case.utils.jwt_handler import decode_confirmation_token


async def confirm_user_email(token: str) -> str:
    """
    Подтверждает email пользователя на основе токена.
    """
    try:
        payload = decode_confirmation_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный токен")

        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

        if user.is_confirmed:
            return "Email уже подтвержден"

        # Обновляем статус пользователя
        await UserRepository.update_user(user_id, {"is_confirmed": True})
        logger.info(f"Email пользователя {user.email} успешно подтвержден.")

        return "Email успешно подтвержден"

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Ошибка подтверждения email: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")

