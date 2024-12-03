from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.salon_models.salon_master_relation import SalonMasterRelation


SalonMasterRelationInvitationSchema = pydantic_model_creator(SalonMasterRelation)