from tortoise import fields

from db.models.abstract.abstract_model import AbstractModel

# Модель вакансии
class Vacancy(AbstractModel):
    title = fields.CharField(max_length=255, null=False)
    position = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=True)
    salon = fields.ForeignKeyField('server.Salon', related_name='vacancies', on_delete=fields.CASCADE)
    status = fields.CharEnumField(enum_type=["open", "closed"], default="open")

    class Meta:
        table = "vacancies"