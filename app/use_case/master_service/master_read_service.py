from fastapi import HTTPException

from app.core.exceptions.repository import EntityNotFoundException
from app.core.exceptions.service import ResourceNotFoundException, ServiceException
from app.core.exceptions.validation import ValidationException
from app.db.models.photo_models.photo_avatar_model import AvatarPhotoMaster
from app.db.repositories.photo_repositories.photo_repository import PhotoRepository
from app.db.schemas.master_schemas.master_schemas import MasterDetailSchema
from db.models import City
from db.repositories.master_repositories.master_repositories import MasterRepository
from config.components.logging_config import logger


class MasterListService:
    @staticmethod
    async def get_masters_by_city(city_slug: str, limit: int = 10, offset: int = 0):
        """
        Получение всех мастеров города по slug
        """
        return await MasterRepository.get_masters_in_city(city_slug, limit, offset)
    

class MasterReadService:
    @staticmethod
    async def get_master(city_slug: str, master_slug: str) -> MasterDetailSchema:
        """
        Получение мастера по slug города и slug мастера.
        """
        try:
            logger.info(f"Запрос на получение мастера: Город - {city_slug}, Мастер - {master_slug}")

            if not city_slug or not isinstance(city_slug, str):
                logger.warning(f"⚠️ Недопустимый slug: {city_slug}")
                raise ValidationException(message="Недопустимый slug")

            # Получаем мастера с предзагрузкой связанных аватаров
            master = await MasterRepository._get_master_by_city_and_slug_with_avatar(city_slug, master_slug)
            if not master:
                logger.error(f"❌ Мастер '{master_slug}' в городе '{city_slug}' не найден")
                raise ResourceNotFoundException(
                    resource_type="Мастер",
                    identifier=master_slug,
                    error_code="MASTER_NOT_FOUND"
                )

            logger.info(f"✅ Найден мастер: {master.slug} (ID={master.id})")

            # Получаем аватарки мастера
            avatar_photos = await PhotoRepository._get_entity_photos(
                model=AvatarPhotoMaster, entity_field='master_id', entity_id=master.id
            )

            avatar_urls = {} # Инициализируем словарь avatar_urls
            if avatar_photos: # Если есть аватарки
                avatar_photo = avatar_photos[0] # Берем первую аватарку (можно доработать, если нужно несколько)

                if avatar_photo.small:
                    avatar_urls['small'] = f"{MEDIA_URL}{avatar_photo.small}"

                if avatar_photo.medium:
                    avatar_urls['medium'] = f"{MEDIA_URL}{avatar_photo.medium}"

                if avatar_photo.large:
                    avatar_urls['large'] = f"{MEDIA_URL}{avatar_photo.large}"

                if avatar_photo.original:
                    avatar_urls['original'] = f"{MEDIA_URL}{avatar_photo.original}"


            master_data = {
                "id": master.id,
                "user_id": master.user_id,
                "title": master.title,
                "description": master.description,
                "text": master.text,
                "experience_years": master.experience_years,
                "specialty": master.specialty,
                "slug": master.slug,
                "name": master.name,
                "address": master.address,
                "phone": master.phone,
                "telegram": master.telegram,
                "whatsapp": master.whatsapp,
                "website": master.website,
                "vk": master.vk,
                "instagram": master.instagram,
                "accepts_at_home": master.accepts_at_home,
                "accepts_in_salon": master.accepts_in_salon,
                "accepts_offsite": master.accepts_offsite,
                "avatar_urls": avatar_urls
            }

            return MasterDetailSchema(**master_data)
        
        except EntityNotFoundException as e:
            logger.error(f"❌ EntityNotFoundException: {e}")
            raise ResourceNotFoundException(
                resource_type="Салон",
                identifier=master_slug,
                error_code="SALON_NOT_FOUND"
            )
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f" Ошибка сервиса при получении мастера по slug '{master_slug}': {e}", exc_info=True)
            raise ServiceException(
                message="Ошибка при получении данных мастера",
                error_code="SERVICE_ERROR"
            )

