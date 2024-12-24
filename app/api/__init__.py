from fastapi import APIRouter

from app.api.v1.auth.user_register_router import user_router
from app.api.v1.auth.user_login_router import login_router
from app.api.v1.masters.masters_router import master_router
from app.api.v1.salons.salons import salon_router
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

router.include_router(
    master_router,
    prefix="/api/v1/auth",
    tags=["master"]
    )

router.include_router(
    salon_router,
    prefix="/api/v1/auth",
    tags=["salon"]
    )

__all__ = ["router"]
 