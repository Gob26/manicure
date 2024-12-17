from tortoise import fields

from db.models.abstract.abstract_model import AbstractModel

# Модель заявки
class JobApplication(AbstractModel):
    vacancy = fields.ForeignKeyField('server.Vacancy', related_name='applications', on_delete=fields.CASCADE)
    master = fields.ForeignKeyField('server.Master', related_name='applications', on_delete=fields.CASCADE)
    status = fields.CharEnumField(enum_type=["pending", "accepted", "rejected"], default="pending")
    message = fields.TextField(null=True, help_text="Сообщение от мастера при отклике.")

    class Meta:
        table = "job_applications"