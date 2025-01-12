from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from use_case.service_service.category_service import CategoryService
from use_case.utils.jwt_handler import get_current_user
from use_case.service_service.standart_service import StandardServiceService
from db.schemas.service_schemas.service_standart_schemas import (
    StandardServiceOut,
    StandardServiceCreate,
    StandardServiceUpdate
)
from config.components.logging_config import logger
from use_case.utils.permissions import check_user_permission

service_standart_router = APIRouter()


@service_standart_router.post(
    "/services/standart",
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

    # Проверяем, существует ли категория
    category = await CategoryService.get_category_by_id(service_data.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена."
        )

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


@service_standart_router.get(
    "/services/standart/{service_id}",
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


@service_standart_router.get(
    "/services/standart",
    response_model=List[StandardServiceOut],
    status_code=status.HTTP_200_OK,
    summary="Получение списка стандартных сервисов",
    description="Получает список всех стандартных сервисов.",
)
async def list_service_standart(
        current_user: dict = Depends(get_current_user),
        skip: int = 0,
        limit: int = 100
):
    logger.info(f"Текущий пользователь: {current_user}")

    try:
        services = await StandardServiceService.list_standart_services(
            current_user=current_user,
            skip=skip,
            limit=limit
        )
        return services
    except ValueError as e:
        logger.warning(f"Ошибка бизнес-логики: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка при получении списка стандартных сервисов: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@service_standart_router.put(
    "/services/standart/{service_id}",
    response_model=StandardServiceOut,
    status_code=status.HTTP_200_OK,
    summary="Обновление стандартного сервиса",
    description="Обновляет существующий стандартный сервис.",
)
async def update_service_standart(
        service_id: int,
        service_data: StandardServiceUpdate,
        current_user: dict = Depends(get_current_user)
):
    logger.info(f"Текущий пользователь: {current_user}")
    check_user_permission(current_user, ["admin", "master"])

    if service_data.category_id:
        category = await CategoryService.get_category_by_id(service_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена."
            )

    try:
        service = await StandardServiceService.update_standart_service(
            service_id=service_id,
            current_user=current_user,
            **service_data.dict(exclude_unset=True)
        )
        return service
    except ValueError as e:
        logger.warning(f"Ошибка бизнес-логики: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка при обновлении стандартного сервиса: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@service_standart_router.delete(
    "/services/standart/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление стандартного сервиса",
    description="Удаляет существующий стандартный сервис.",
)
async def delete_service_standart(
        service_id: int,
        current_user: dict = Depends(get_current_user)
):
    logger.info(f"Текущий пользователь: {current_user}")
    check_user_permission(current_user, ["admin"])

    try:
        await StandardServiceService.delete_standart_service(
            service_id=service_id,
            current_user=current_user
        )
    except ValueError as e:
        logger.warning(f"Ошибка бизнес-логики: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка при удалении стандартного сервиса: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")