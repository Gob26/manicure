from fastapi import APIRouter, HTTPException, status
from db.schemas.master_schemas.master_create_schema import MasterCreateSchema
from db.schemas.master_schemas.master_response_schema import MasterResponseSchema
from app.use_case.master.master_service import MasterService
from config.components.logging_config import logger

master_router = APIRouter()

@master_router.post(
    "/master",
    response_model=MasterResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание профиля мастера",
    description="""
    Создает новый профиль мастера с предоставленной информацией.
    
    Необходимые разрешения:
    - Аутентифицированный пользователь
    - Ограничение: 5 запросов в минуту
    """,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Профиль мастера успешно создан",
            "model": MasterResponseSchema
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Неверные входные данные"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Ошибка на сервере"
        },
    },
)
async def create_master_route(
    master_data: MasterCreateSchema
):
    """
    Основной метод для создания мастера.
    """
    try:
        logger.info(f"Пользователь с ID {master_data.user_id} пытается создать мастера {master_data.title}")
        
        # Передаем данные в сервис для создания мастера
        result = await MasterService.create_master(
            user_id=master_data.user_id,
            title=master_data.title,
            specialty=master_data.specialty,
            city_name=master_data.city_name,
            description=master_data.description,
            text=master_data.text,
            experience_years=master_data.experience_years,
            slug=master_data.slug,
        )
        return result
    except ValueError as e:
        logger.error(f"Ошибка при создании мастера: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка при создании мастера: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при создании мастера")
