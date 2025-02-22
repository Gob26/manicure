from typing import Optional

from db.models import Master
from db.repositories.master_repositories.master_repositories import MasterRepository
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger

class MasterService:
    @staticmethod
    async def create_master(
        current_user: dict,
        title: str,
        specialty: str,
        description: Optional[str] = None,
        text: Optional[str] = None,
        experience_years: Optional[int] = 0,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        telegram: Optional[str] = None,
        whatsapp: Optional[str] = None,
        website: Optional[str] = None,
        vk: Optional[str] = None,
        instagram: Optional[str] = None,
        accepts_at_home: Optional[bool] = False,
        accepts_in_salon: Optional[bool] = False,
        accepts_offsite: Optional[bool] = False,
    ) -> dict:
        """
        Создание мастера с использованием текущего пользователя.
        """
        logger.debug(f"create_master: старт создания мастера для пользователя ID {current_user['user_id']}")

        # Проверка на наличие мастера
        existing_master = await MasterRepository.get_master_by_user_id(current_user["user_id"])
        if existing_master:
            logger.error(f"Мастер уже существует для пользователя ID {current_user['user_id']}")
            raise ValueError(f"Мастер уже создан для пользователя с ID {current_user['user_id']}")

        # Генерация уникального слага
        if not slug:
            slug = await generate_unique_slug(Master, title)

        # Создаем мастера
        master = await MasterRepository.create_master(
            user_id=current_user["user_id"],
            city_id=current_user["city_id"],  # Город из токена
            title=title,
            specialty=specialty,
            description=description,
            text=text,
            experience_years=experience_years,
            slug=slug,
            name=name,
            address=address,
            phone=phone,
            telegram=telegram,
            whatsapp=whatsapp,
            website=website,
            vk=vk,
            instagram=instagram,
            accepts_at_home=accepts_at_home,
            accepts_in_salon=accepts_in_salon,
            accepts_offsite=accepts_offsite,
        )

        logger.info(f"create_master: мастер с ID {master.id} успешно создан")
        return {
            "user_id": current_user["user_id"],
            "city_id": current_user["city_id"],
            "title": master.title,
            "specialty": master.specialty,
            "description": master.description,
            "text": master.text,
            "experience_years": master.experience_years,
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
        }
