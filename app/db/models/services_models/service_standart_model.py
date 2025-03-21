#service_standart_model.py
from tortoise import fields
from db.models.abstract.abstract_model import AbstractModel
from db.models.abstract.abstract_service import AbstractService
import typing
if typing.TYPE_CHECKING:
    from db.models import StandardServicePhoto

class StandardService(AbstractService):
    """
    Модель для стандартных услуг
    """
    category = fields.ForeignKeyField(
        'server.Category',
        related_name='services',
        null=True,
        on_delete=fields.SET_NULL,
        help_text="Категория услуги (например, маникюр, педикюр)."
    )
    
    images: fields.ReverseRelation["StandardServicePhoto"]

    class Meta:
        table = "standard_services"
        ordering = ["name"]


#Атрбуты услуг
class ServiceAttributeType(AbstractModel):
    """Типы атрибутов (способ удаления кутикулы, материал покрытия и т.д.)"""
    name = fields.CharField(max_length=100, help_text="Название типа атрибута.")
    slug = fields.CharField(max_length=100, unique=True, help_text="Уникальный идентификатор типа.")

    class Meta:
        table = "service_attribute_types"


class ServiceAttributeValue(AbstractModel):
    """Возможные значения атрибутов (аппаратный, классический, гель-лак и т.д.)"""
    attribute_type = fields.ForeignKeyField(
        'server.ServiceAttributeType',
        related_name='values',
        on_delete=fields.CASCADE,
        help_text="Тип атрибута, к которому относится значение."
    )
    name = fields.CharField(max_length=100, help_text="Название значения атрибута.")
    slug = fields.CharField(max_length=100, unique=True, help_text="Уникальный идентификатор значения.")

    class Meta:
        table = "service_attribute_values"


class TemplateAttribute(AbstractModel):
    """Связь шаблона услуги с возможными атрибутами"""
    service_template = fields.ForeignKeyField(
        'server.StandardService',
        related_name='possible_attributes',
        on_delete=fields.CASCADE,
        help_text="Шаблон услуги, связанный с атрибутами."
    )
    attribute_type = fields.ForeignKeyField(
        'server.ServiceAttributeType',
        on_delete=fields.CASCADE,
        help_text="Тип атрибута."
    )
    is_required = fields.BooleanField(default=False, help_text="Является ли атрибут обязательным.")

    class Meta:
        table = "template_attributes"
        unique_together = ("service_template", "attribute_type")
