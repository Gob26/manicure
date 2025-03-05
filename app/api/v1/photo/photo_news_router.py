from fastapi import APIRouter, File, UploadFile

from db.models.photo_models.photo_news_models import NewsPhoto
from app.use_case.photo_service.photo_base_servise import PhotoHandler


photo_news_router = APIRouter()

@photo_news_router.post("/upload")

async def upload_news_image(file: UploadFile = File(...)):
    news_images = await PhotoHandler.add_photos_to_service(
    images=[file],
    model=NewsPhoto,
    slug='test_news',
    city='test_city',
    role="salon",
    image_type="news_photo",

    )
    return {"message": "Изображение успешно загружено", "photo_ids": news_images}