from typing import List
from fastapi import APIRouter, Depends, UploadFile, HTTPException

from app.use_case.photo_service.photo_custom_service import CustomServicePhotoService
from app.use_case.utils.jwt_handler import get_current_user
from use_case.utils.permissions import check_user_permission

photo_custom_service_router = APIRouter()


@photo_custom_service_router.post("/custom-service/{custom_service_id}/upload/")
async def upload_photo_for_custom_service(
    custom_service_id: int, 
    images: List[UploadFile],
    current_user: dict = Depends(get_current_user),
):
    check_user_permission(current_user, ["admin", "master", "salon"])

    try:
        return await CustomServicePhotoService.upload_photo_for_custom_service(custom_service_id, images, current_user)
    
    except HTTPException as e:
        raise e  # Если выброшено HTTP-исключение, просто пробрасываем дальше
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки фото: {str(e)}")


@photo_custom_service_router.delete("/custom-service/{photo_id}/photo/")
async def delete_photo_for_custom_service(
    photo_id: int,
    current_user: dict = Depends(get_current_user),
):
    check_user_permission(current_user, ["admin", "master", "salon"])

    try:
        return await CustomServicePhotoService.delete_photo_for_custom_service(photo_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления фото: {str(e)}")