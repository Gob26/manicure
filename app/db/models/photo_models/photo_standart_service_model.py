from tortoise import fields
from db.models.abstract.abstract_photo import AbstractPhoto



class StandardServicePhoto(AbstractPhoto):
    """
    Фотографии стандартных услуг
    """
    class Meta:
        table = "standardservicephoto"