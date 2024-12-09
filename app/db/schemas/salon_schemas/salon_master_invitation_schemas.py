from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.salon_models.salon_master_invitation import SalonMasterInvitation


# Создаем Pydantic-схему для приглашения мастера
SalonMasterInvitationCreateSchema = pydantic_model_creator(
    SalonMasterInvitation,
    exclude=("id", "created_at", "updated_at"),  # Исключаем поля, которые не нужны при создании
    name="SalonMasterInvitationCreateSchema"  # Имя схемы
)