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


@service_categories_router.get(
    "/all",
    response_model=list[CategoryOut],
    status_code=status.HTTP_200_OK,
    summary="Получение всех категорий",
    description="Получает все категории услуг.",
)
async def get_all_service_categories():
    categories = await CategoryService.get_all_categories()
    return categories


@service_categories_router.get(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
    summary="Получение одной категории",
    description="Получает одну категорию услуг по её ID.",
)
async def get_service_category(category_id: int):
    category = await CategoryService.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )

    # Получаем связанные services и преобразуем их в список ID
    services = await category.services.all()
    category_data = {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description,
        "title": category.title,
        "content": category.content,
        "services": [service.id for service in services]  # Преобразуем в список ID
    }
    return category_data


@service_categories_router.put(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
    summary="Обновление категорий",
    description="Обновляет существующую категорию услуг.",
)
async def update_service_category(
    category_id: int,
    category_data: CategoryCreate,
    current_user: dict = Depends(get_current_user),
):
    check_user_permission(current_user, ["admin", "master"])

    # Получаем существующую категорию
    category = await CategoryService.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )

    # Обновляем категорию с помощью соответствующего метода CategoryService
    updated_category = await CategoryService.update_category(category_id, category_data.dict())

    # Получаем связанные services и преобразуем их в список ID
    services = await updated_category.services.all()
    category_out = CategoryOut(
        id=updated_category.id,
        name=updated_category.name,
        slug=updated_category.slug,
        description=updated_category.description,
        title=updated_category.title,
        content=updated_category.content,
        services=[service.id for service in services],  # Преобразуем в список ID
    )

    return category_out


#удаление категории 
@service_categories_router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление категорий",
    description="Удаляет существующую категорию услуг.",
)
async def delete_service_category(
    category_id: int, current_user: dict = Depends(get_current_user)
):
    check_user_permission(current_user, ["admin", "master"])

    # Получаем существующую категорию
    category = await CategoryService.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )

    # Удаляем категорию с помощью соответствующего метода CategoryService
    await CategoryService.delete_category(category_id)