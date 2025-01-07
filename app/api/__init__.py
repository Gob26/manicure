from fastapi import APIRouter

from app.api.v1.auth.user_register_router import user_router
from app.api.v1.auth.user_login_router import login_router
from app.api.v1.masters.masters_router import master_router
from app.api.v1.masters.masters_read_router import master_read_router
from app.api.v1.salons.salons import salon_router
from app.api.v1.cyties.city import city_router 


router = APIRouter()

router.include_router(
    user_router,
    prefix="/api/v1/auth",
    tags=["auth"]
    )

router.include_router(
    login_router,
    prefix="/api/v1/auth",
    tags=["login"]
    )
# Мастера
router.include_router(
    master_router,
    prefix="/api/v1/master",
    tags=["Мастера - создание"]
    )

router.include_router(
    master_read_router,
    prefix="/api/v1",
    tags=["Мастера - чтение"]
    )
# Салоны
router.include_router(
    salon_router,
    prefix="/api/v1/salon",
    tags=["salon"]
    )
#Города
router.include_router(
    city_router,
    prefix="/api/v1/cities",
    tags=["city"]
    )

__all__ = ["router"]
 