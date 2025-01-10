from fastapi import APIRouter, Depends, HTTPException, status
from use_case.utils.jwt_handler import get_current_user
from use_case.service_service.standart_service import StandardServiceService
from db.schemas.service_schemas.service_standart_schemas import StandardServiceOut, StandardServiceCreate
from config.components.logging_config import logger
from use_case.utils.permissions import check_user_permission


service_standart_router = APIRouter()


@service_standart_router.post("/services/standart",
    response_model=StandardServiceOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создание стандартного сервиса",
    description="Создает новый стандартный сервис.",
)
async def create_service_standart_route(
    service_data: StandardServiceCreate,
    current_user: dict = Depends(get_current_user)
    ):
    logger.info(f"Текущий пользователь: {current_user}")

    check_user_permission(current_user, ["admin", "master"])
    try:
        service = await StandardServiceService.create_standart_service(
            current_user=current_user,
            **service_data.dict()
        )
        return service
    
    except ValueError as e:
        logger.warning(f"Ошибка бизнес-логики: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка при создании стандартного сервиса: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

@service_standart_router.get("/services/standart/{service_id}",
    response_model=StandardServiceOut,
    status_code=status.HTTP_200_OK,
    summary="Получение стандартного сервиса",
    description="Получает стандартный сервис по его ID.",
)
async def get_service_standart(
        service_id: int,
        current_user: dict = Depends(get_current_user)
        ):
    logger.info(f"Текущий пользователь: {current_user}")

    check_user_permission(current_user, ["admin", "master"]) 
    
    try:
        service = await StandardServiceService.get_standart_service(
            service_id=service_id,
            current_user=current_user
        )
        return service
    
    except ValueError as e:
        logger.warning(f"Ошибка бизнес-логики: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Ошибка при получении стандартного сервиса: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@service_standart_router.get("/services/standard", response_model=List[StandardServiceOut])
async def get_all_standard_services(service_service: ServiceService = Depends()):
    """Получение списка стандартных услуг"""
    return await service_service.get_all_services()


@service_standart_router.put("/services/standard/{service_id}", response_model=StandardServiceOut)
async def update_standard_service(service_id: int, service: StandardServiceCreate, service_service: ServiceService = Depends()):
    """Обновление стандартной услуги"""
    return await service_service.update_service(service_id, service)

@service_standart_router.delete("/services/standard/{service_id}")
async def delete_standard_service(service_id: int, service_service: ServiceService = Depends()):
    """Удаление стандартной услуги"""
    await service_service.delete_service(service_id)
    return {"message": "Service deleted successfully"}