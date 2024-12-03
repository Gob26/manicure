from tortoise import fields

from db.models.abstract.abstract_model import AbstractModel

# Модель резюме
class Resume(AbstractModel):
    master = fields.ForeignKeyField('server.Master', related_name='resumes', on_delete=fields.CASCADE)
    title = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=True)
    experience_years = fields.IntField()

    class Meta:
        table = "resumes"