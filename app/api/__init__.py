from fastapi import APIRouter

from api.v1.auth.auth import auth_router




router = APIRouter()
router.include_router(auth_router, prefix="/api/examples")


__all__ = ["router"]
