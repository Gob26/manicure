from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "standard_service_photo" DROP CONSTRAINT IF EXISTS "fk_standard_standard_dd0d6c13";
        ALTER TABLE "standard_service_photo" RENAME COLUMN "standard_services_id" TO "standard_service_id";
        ALTER TABLE "standard_service_photo" ADD CONSTRAINT "fk_standard_standard_a8b44263" FOREIGN KEY ("standard_service_id") REFERENCES "standard_services" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "standard_service_photo" DROP CONSTRAINT IF EXISTS "fk_standard_standard_a8b44263";
        ALTER TABLE "standard_service_photo" RENAME COLUMN "standard_service_id" TO "standard_services_id";
        ALTER TABLE "standard_service_photo" ADD CONSTRAINT "fk_standard_standard_dd0d6c13" FOREIGN KEY ("standard_services_id") REFERENCES "standard_services" ("id") ON DELETE CASCADE;"""
