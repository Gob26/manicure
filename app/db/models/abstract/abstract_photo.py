from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel

# Абстрактная модель фотографий
class AbstractPhoto(AbstractModel):
    image_url = fields.CharField(max_length=255, help_text="URL изображения")
    alt = fields.CharField(max_length=255, null=True, help_text="Альтернативный текст для изображения (SEO и доступность)")
    description = fields.TextField(null=True, help_text="Описание изображения")

    class Meta:
        abstract = True
