from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.salon_models.salon_master_invitation import SalonMasterInvitation


SalonMasterInvitationSchema = pydantic_model_creator(SalonMasterInvitation)