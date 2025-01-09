#photo_model.py
from tortoise import fields

from db.models.abstract.abstract_photo import AbstractPhoto, EntityType



class Photo(AbstractPhoto):
    """
    Унифицированная модель фотографий, наследующая абстрактную модель
    """
    # Entity identifiers
    master_id = fields.IntField(null=True)
    salon_id = fields.IntField(null=True)
    service_id = fields.IntField(null=True)
    
    # Photo metadata
    entity_type = fields.CharEnumField(EntityType) 
    caption = fields.CharField(max_length=1000, null=True) 
    is_active = fields.BooleanField(default=True)
    
    class Meta:
        table = "photos"
