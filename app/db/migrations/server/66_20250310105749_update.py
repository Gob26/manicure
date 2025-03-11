from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "standard_services" DROP CONSTRAINT IF EXISTS "fk_standard_standard_e1408f97";
        ALTER TABLE "standard_services" DROP COLUMN "default_photo_id";
        ALTER TABLE "standard_service_photo" ADD "photo_standard_service_id" INT NOT NULL;
        ALTER TABLE "standard_service_photo" ADD CONSTRAINT "fk_standard_standard_38b224e7" FOREIGN KEY ("photo_standard_service_id") REFERENCES "standard_services" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "standard_service_photo" DROP CONSTRAINT IF EXISTS "fk_standard_standard_38b224e7";
        ALTER TABLE "standard_services" ADD "default_photo_id" INT  UNIQUE;
        ALTER TABLE "standard_service_photo" DROP COLUMN "photo_standard_service_id";
        ALTER TABLE "standard_services" ADD CONSTRAINT "fk_standard_standard_e1408f97" FOREIGN KEY ("default_photo_id") REFERENCES "standard_service_photo" ("id") ON DELETE SET NULL;"""
