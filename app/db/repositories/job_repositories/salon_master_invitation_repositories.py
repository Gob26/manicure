
from typing import Any
from db.repositories.base_repositories.base_repositories import BaseRepository
from db.models.job.salon_master_invitation import SalonMasterInvitation


class InvitationRepository(BaseRepository):
    model: SalonMasterInvitation
    @classmethod
    async def create_invitation(cls, **kwargs: Any) -> SalonMasterInvitation:
        return await cls.create(**kwargs)