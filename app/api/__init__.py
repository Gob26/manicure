from fastapi import APIRouter

from api.v1.job.vacancies_salons_router import vacancy_router
from api.v1.services.service_standart_router import service_standart_router
from api.v1.auth.user_register_router import user_router
from api.v1.auth.user_login_router import login_router
from api.v1.masters.masters_list_router import master_list_router
from api.v1.masters.masters_router import master_router
from api.v1.masters.masters_read_router import master_read_router
from api.v1.salons.salons_router import salon_router
from api.v1.cyties.city import city_router 
from api.v1.services.service_custom_router import service_custom_router
from api.v1.services.service_categories_router import service_categories_router
from api.v1.services.service_attribute_router import service_attribute_router
from app.api.v1.salons.salons_masters_relation_router import salon_master_relation_router


router = APIRouter()

router.include_router(
    user_router,
    prefix="/api/v1/auth",
    tags=["Регистрация"]
    )

router.include_router(
    login_router,
    prefix="/api/v1/auth",
    tags=["Логирование"]
    )

# Мастера
router.include_router(
    master_router,
    prefix="/api/v1/master",
    tags=["Мастер - создание, обновление и удаление"]
    )

router.include_router(
    master_read_router,
    prefix="/api/v1",
    tags=["Мастер - чтение"]
    )

router.include_router(
    master_list_router,
    prefix="/api/v1",
    tags=["Мастера - список"]
    )

# Салоны
router.include_router(
    salon_router,
    prefix="/api/v1/salon",
    tags=["Салон - создание, обновление и удаление"]
    )

# Вакансии и Связи
router.include_router(
    salon_master_relation_router,
    prefix="/api/v1/salon/relation",
    tags=["Связь мастера и салона"]
    )

router.include_router(
    vacancy_router,
    prefix="/api/v1/salon/vacancy",
    tags=["Вакансии салона"]
    )

# Услуги
router.include_router(
    service_custom_router,
    prefix="/api/v1/category/custom_service",
    tags=["Индивидуальные услуги"]
    )

router.include_router(
    service_standart_router,
    prefix="/api/v1/category",
    tags=["Услуги"]
    )

# Атрибуты
router.include_router(
    service_attribute_router,
    prefix="/api/v1/category/services/attribute_type",
    tags=["Атрибуты"]
    )

# Категории
router.include_router(
    service_categories_router,
    prefix="/api/v1/category",
    tags=["Категории"]
    )

# Города
router.include_router(
    city_router,
    prefix="/api/v1/cities",
    tags=["Город"]
    )

__all__ = ["router"]
 