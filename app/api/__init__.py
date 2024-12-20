from fastapi import APIRouter

from app.api.v1.auth.user_register_router import user_router
from app.api.v1.auth.user_login_router import login_router
from app.api.v1.auth.

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

__all__ = ["router"]
