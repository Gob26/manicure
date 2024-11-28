from fastapi import APIRouter

from api.v1.auth.user_router import user_router


router = APIRouter()

router.include_router(
    user_router,
    prefix="/api/v1/auth",
    tags=["auth"]
    )


__all__ = ["router"]
