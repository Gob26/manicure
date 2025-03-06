from config.components.logging_config import logger
from db.models import AvatarPhotoSalon
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from db.repositories.photo_repositories.photo_repository import PhotoRepository # Импортируем PhotoRepository
from core.exceptions.service import ResourceNotFoundException, BusinessRuleException, ServiceException
from core.exceptions.validation import ValidationException
from core.exceptions.repository import EntityNotFoundException
from config.constants import MEDIA_URL # Импортируем MEDIA_URL
from db.schemas.salon_schemas.salon_schemas import SalonDetailsSchema # Импортируем SalonDetailsSchema


class SalonReadService:
    @staticmethod
    async def get_salon_by_slug(slug: str) -> SalonDetailsSchema: # Изменяем возвращаемый тип на SalonDetailsSchema
        try:
            logger.debug(f" Начало get_salon_by_slug(slug={slug})")

            if not slug or not isinstance(slug, str):
                logger.warning(f"⚠️ Недопустимый slug: {slug}")
                raise ValidationException(message="Недопустимый slug")

            # Получаем салон с предзагрузкой связанных аватаров
            salon = await SalonRepository.get_salon_by_slug_with_avatar(slug)
            if not salon:
                logger.error(f"❌ Салон '{slug}' не найден")
                raise ResourceNotFoundException(
                    resource_type="Салон",
                    identifier=slug,
                    error_code="SALON_NOT_FOUND"
                )

            logger.info(f"✅ Найден салон: {salon.slug} (ID={salon.id})")

            # Получаем аватарки салона
            avatar_photos = await PhotoRepository.get_entity_photos(
                model=AvatarPhotoSalon, entity_field='salon_id', entity_id=salon.id
            )

            avatar_urls = {} # Инициализируем словарь avatar_urls
            if avatar_photos: # Если есть аватарки
                avatar_photo = avatar_photos[0] # Берем первую аватарку (можно доработать, если нужно несколько)

                if avatar_photo.small:
                    avatar_urls['small'] = f"{MEDIA_URL}{avatar_photo.small}" # Формируем URL
                if avatar_photo.medium:
                    avatar_urls['medium'] = f"{MEDIA_URL}{avatar_photo.medium}"
                if avatar_photo.large:
                    avatar_urls['large'] = f"{MEDIA_URL}{avatar_photo.large}"
                if avatar_photo.original:
                    avatar_urls['original'] = f"{MEDIA_URL}{avatar_photo.original}"


            salon_data = { # Формируем словарь данных салона
                "id": salon.id, # Добавляем id салона
                "user_id": salon.user_id,
                "name": salon.name,
                "title": salon.title,
                "slug": salon.slug,
                "description": salon.description,
                "text": salon.text,
                "address": salon.address,
                "phone": salon.phone,
                "telegram": salon.telegram,
                "whatsapp": salon.whatsapp,
                "website": salon.website,
                "vk": salon.vk,
                "instagram": salon.instagram,
                "avatar_urls": avatar_urls # Добавляем avatar_urls
            }


            return SalonDetailsSchema(**salon_data) # Возвращаем SalonDetailsSchema

        except EntityNotFoundException as e:
            logger.error(f"❌ EntityNotFoundException: {e}")
            raise ResourceNotFoundException(
                resource_type="Салон",
                identifier=slug,
                error_code="SALON_NOT_FOUND"
            )
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f" Ошибка сервиса при получении салона по slug '{slug}': {e}", exc_info=True)
            raise ServiceException(
                message="Ошибка при получении данных салона",
                error_code="SERVICE_ERROR"
            )