from fastapi import APIRouter, Depends, HTTPException, status

from db.repositories.user_repositories.user_repositories import UserRepository
from use_case.utils.jwt_handler import get_current_user
from db.schemas.master_schemas.master_schemas import MasterCreateSchema
from use_case.master_service.master_service import MasterService
from config.components.logging_config import logger

master_router = APIRouter()

@master_router.post(
    "/master",
    response_model=dict,  # Можно указать схему ответа, если требуется
    status_code=status.HTTP_201_CREATED,
    summary="Создание профиля мастера",
    description="Создает новый профиль мастера.",
)
async def create_master_route(
    master_data: MasterCreateSchema,  # Данные для создания мастера
    current_user: dict = Depends(get_current_user),  # Получаем текущего пользователя
):
    """
    Роут для создания профиля мастера. Проверяет права пользователя, извлекает данные из токена и передает их в сервис.
    """
    logger.info(f"Текущий пользователь: {current_user}")  # Логирование текущего пользователя

    # Проверка прав доступа
    if current_user["role"] not in ["master", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для создания мастера"
        )

    # Создание мастера через сервис
    try:
        master = await MasterService.create_master(
            **master_data.dict(),  # Данные для создания мастера
            current_user=current_user  # Текущий пользователь
        )
        return {"message": "Мастер успешно создан", "master": master}
    except ValueError as ve:
        logger.warning(f"Ошибка бизнес-логики: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Системная ошибка при создании мастера: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при создании мастера")
