from fastapi import APIRouter, HTTPException, Query, status
from config.components.logging_config import logger
from use_case.user.user_email import confirm_user_email

email_router = APIRouter()

@email_router.get("/confirm-email", summary="Подтверждение почты")
async def confirm_email(token: str = Query(..., description="JWT токен подтверждения почты")):
    """
    Эндпоинт для подтверждения email.
    Пользователь переходит по ссылке с токеном, и его email подтверждается.
    """
    try:
        message = await confirm_user_email(token)
        return {"message": message}
    except HTTPException as e:
        raise e  # Пробрасываем HTTP исключения, чтобы сохранить статус
    except Exception as e:
        logger.error(f"Ошибка подтверждения email: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")