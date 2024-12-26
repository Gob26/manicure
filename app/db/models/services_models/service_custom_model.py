from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel

class CustomService(AbstractModel):
    name = fields.CharField(max_length=255, help_text="Название услуги")
    description = fields.TextField(null=True, help_text="Описание услуги")
    price = fields.DecimalField(max_digits=10, decimal_places=2, help_text="Цена услуги")
    duration = fields.IntField(help_text="Длительность в минутах")
    owner_type = fields.CharField(max_length=50, choices=[("master", "Мастер"), ("salon", "Салон")], help_text="Тип владельца")
    owner_id = fields.IntField(help_text="ID мастера или салона")

    class Meta:
        table = "custom_services"
        ordering = ["name"]

    # Ленивая загрузка Photo только при необходимости
    def get_photos(self):
        from app.db.models.photo_models.photo_model import Photo
        return Photo.filter(service_id=self.id)
