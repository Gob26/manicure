from db.models.job.salon_master_invitation import SalonMasterInvitation
from db.repositories.base_repositories.base_repositories import BaseRepository

class InvitationRepository(BaseRepository):
    model = SalonMasterInvitation

    @classmethod
    async def create_invitation(cls, **kwargs) -> SalonMasterInvitation:
        # Добавляем дефолтные значения для некоторых полей, если нужно
        return await cls.create(**kwargs, status="pending", notification_status="unread")
