from tortoise import fields

from db.models.abstract.abstract_model import AbstractModel

# Модель связи мастера и салонов
class SalonMasterRelation(AbstractModel):
    salon = fields.ForeignKeyField("server.Salon", on_delete=fields.CASCADE)
    master = fields.ForeignKeyField("server.Master", on_delete=fields.CASCADE)
    status = fields.CharEnumField(enum_type=["active", "pending", "inactive"], default="pending")
    role = fields.CharEnumField(enum_type=["employee", "freelancer"], default="employee")
    start_date = fields.DateField(null=True, help_text="Дата начала работы.")
    end_date = fields.DateField(null=True, help_text="Дата завершения работы.")
    notes = fields.TextField(null=True, help_text="Дополнительная информация.")

    class Meta:
        unique_together = ("salon", "master")  # Запретить дублирование связей
