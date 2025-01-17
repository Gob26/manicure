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
    class Meta:
        table = "avatar_photo_salon"