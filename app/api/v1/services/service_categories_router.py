from fastapi import APIRouter, Depends, HTTPException, status
from db.schemas.service_schemas.category_schemas import CategoryCreate
from use_case.utils.jwt_handler import get_current_user
from use_case.service_service.category_service import CategoryService
from db.schemas.service_schemas.category_schemas import CategoryCreate, CategoryOut
from use_case.utils.permissions import check_user_permission


service_categories_router = APIRouter()


@service_categories_router.post(
    "/",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создание категорий",
    description="Создает новые категории для услуг.",
)
async def create_service_categories(
    category_data: CategoryCreate,
    current_user: dict = Depends(get_current_user),
):
    check_user_permission(current_user, ["admin", "master"])

    # Создаем категорию и получаем связанные услуги
    category, services = await CategoryService.create_category(category_data.dict())

    # Формируем ответ, включив идентификаторы услуг
    category_out = CategoryOut(
        id=category.id,
        name=category.name,
        slug=category.slug,
        description=category.description,
        title=category.title,
        content=category.content,
        services=[service.id for service in services],  # Используем только идентификаторы услуг
    )

    return category_out



