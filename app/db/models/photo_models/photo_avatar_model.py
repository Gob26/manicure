from tortoise import fields

from db.models.abstract.abstract_photo import AbstractPhoto



class AvatarPhotoMaster(AbstractPhoto):
    """
    Фотографии стандартных услуг
    """
    class Meta:
        table = "avatar_photo_master"

class AvatarPhotoSalon(AbstractPhoto):
    """
    Фотографии стандартных услуг
    """
    salon = fields.ForeignKeyField("server.Salon", related_name="images", on_delete=fields.CASCADE)

    class Meta:
        table = "avatar_photo_salon"