from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_master" ALTER COLUMN "mime_type" DROP NOT NULL;
        ALTER TABLE "avatar_photo_salon" ALTER COLUMN "mime_type" DROP NOT NULL;
        ALTER TABLE "custom_service_photo" ALTER COLUMN "mime_type" DROP NOT NULL;
        ALTER TABLE "standard_service_photo" ALTER COLUMN "mime_type" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_salon" ALTER COLUMN "mime_type" SET NOT NULL;
        ALTER TABLE "avatar_photo_master" ALTER COLUMN "mime_type" SET NOT NULL;
        ALTER TABLE "custom_service_photo" ALTER COLUMN "mime_type" SET NOT NULL;
        ALTER TABLE "standard_service_photo" ALTER COLUMN "mime_type" SET NOT NULL;"""
