from tortoise import fields

from db.models.abstract.abstract_model import AbstractModel

# Модель приглашения мастера
class SalonMasterInvitation(AbstractModel):
    salon = fields.ForeignKeyField("server.Salon", related_name="invitations", on_delete=fields.CASCADE)
    master = fields.ForeignKeyField("server.Master", related_name="invitations", on_delete=fields.CASCADE)
    vacancy = fields.ForeignKeyField("server.Vacancy", related_name="invitations", null=True, on_delete=fields.SET_NULL)
    status = fields.CharEnumField(enum_type=["pending", "accepted", "rejected", "cancelled"], default="pending")
    message = fields.TextField(null=True, help_text="Сообщение от салона к мастеру.")
    expires_at = fields.DatetimeField(null=True, help_text="Срок действия приглашения.")
    notification_status = fields.CharEnumField(enum_type=["sent", "read", "unread"], default="unread")
    response_date = fields.DatetimeField(null=True, help_text="Дата ответа мастера.")

    class Meta:
        table = "salon_master_invitations"
