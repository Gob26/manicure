from db.models.photo_models.photo_standart_service_model import CustomServicePhoto
from db.repositories.base_repositories.base_repositories import BaseRepository


class PhotoCustomRepository(BaseRepository):
    model = CustomServicePhoto  # Добавьте определение модели

    @classmethod
    async def delete_by_custom_service_id(cls, custom_service_id: int):
        deleted_count = await cls.model.filter(custom_service_id=custom_service_id).delete()
        return deleted_count