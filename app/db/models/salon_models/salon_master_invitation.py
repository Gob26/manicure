from tortoise import fields
from enum import Enum
from db.models.abstract.abstract_model import AbstractModel

# Перечисления для статусов
class InvitationStatusEnum(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    cancelled = "cancelled"

class NotificationStatusEnum(str, Enum):
    sent = "sent"
    read = "read"
    unread = "unread"

# Модель приглашения мастера
class SalonMasterInvitation(AbstractModel):
    salon = fields.ForeignKeyField("server.Salon", related_name="invitations", on_delete=fields.CASCADE)
    master = fields.ForeignKeyField("server.Master", related_name="invitations", on_delete=fields.CASCADE)
    vacancy = fields.ForeignKeyField("server.Vacancy", related_name="invitations", null=True, on_delete=fields.SET_NULL)
    
    # Используем перечисления для статусов
    status = fields.CharEnumField(enum_type=InvitationStatusEnum, default=InvitationStatusEnum.pending)
    
    message = fields.TextField(null=True, help_text="Сообщение от салона к мастеру.")
    expires_at = fields.DatetimeField(null=True, help_text="Срок действия приглашения.")
    
    # Используем перечисление для статуса уведомления
    notification_status = fields.CharEnumField(enum_type=NotificationStatusEnum, default=NotificationStatusEnum.unread)
    
    response_date = fields.DatetimeField(null=True, help_text="Дата ответа мастера.")

    class Meta:
        table = "salon_master_invitations"
