from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "custom_services" DROP CONSTRAINT IF EXISTS "fk_custom_s_custom_s_b9628e84";
        ALTER TABLE "custom_services" DROP COLUMN "main_photo_id";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "custom_services" ADD "main_photo_id" INT;
        ALTER TABLE "custom_services" ADD CONSTRAINT "fk_custom_s_custom_s_b9628e84" FOREIGN KEY ("main_photo_id") REFERENCES "custom_service_photo" ("id") ON DELETE SET NULL;"""
