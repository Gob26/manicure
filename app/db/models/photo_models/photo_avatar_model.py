from db.models.abstract.abstract_photo import AbstractPhoto



class AvatarPhoto(AbstractPhoto):
    """
    Фотографии стандартных услуг
    """
    class Meta:
        table = "avatar_photo"