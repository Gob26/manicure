from fastapi import APIRouter, Depends, HTTPException, status

from db.repositories.user_repositories.user_repositories import UserRepository
from use_case.utils.jwt_handler import get_current_user
from db.schemas.master_schemas.master_schemas import MasterCreateSchema
from use_case.master_service.master_service import MasterService
from config.components.logging_config import logger

master_router = APIRouter()

@master_router.post(
    "/master",
    response_model=MasterCreateSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание профиля мастера",
    description="Создает новый профиль мастера.",
)
async def create_master_route(
    master_data: MasterCreateSchema,  # Данные для создания мастера
    current_user: dict = Depends(get_current_user)  # Получаем текущего пользователя
):
    logger.info(f"Текущий пользователь: {current_user}")  # Логирование пользователя
    try:
        # Проверка на роль
        if current_user["role"] not in ["master", "admin"]:
            raise HTTPException(
                status_code=403,
                detail="У вас нет прав для создания мастера"
            )

        # Извлекаем city_id из токена
        city_id = current_user.get("city_id")
        if not city_id:
            raise HTTPException(status_code=400, detail="Город не найден в токене")

        user_id = current_user.get("user_id")  # Извлекаем user_id из токена

        if not user_id:
            raise HTTPException(status_code=400, detail="ID пользователя не найден в токене")

        # Ищем пользователя по user_id
        user = await UserRepository.get_user_by_id(user_id)  # Проверяем наличие пользователя по ID
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Создание мастера с переданными данными
        master = await MasterService.create_master(
            user_id=user_id,  # ID пользователя
            city_id=city_id,  # Город (city_id) из токена
            **master_data.dict()  # Дополнительные данные для мастера
        )

        return {"message": "Мастер успешно создан", "master": master}

    except Exception as e:
        logger.error(f"Системная ошибка при создании мастера: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при создании мастера")