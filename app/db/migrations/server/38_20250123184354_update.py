from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_master" ALTER COLUMN "file_name" DROP NOT NULL;
        ALTER TABLE "avatar_photo_salon" ALTER COLUMN "file_name" DROP NOT NULL;
        ALTER TABLE "custom_service_photo" ALTER COLUMN "file_name" DROP NOT NULL;
        ALTER TABLE "standard_service_photo" ALTER COLUMN "file_name" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_salon" ALTER COLUMN "file_name" SET NOT NULL;
        ALTER TABLE "avatar_photo_master" ALTER COLUMN "file_name" SET NOT NULL;
        ALTER TABLE "custom_service_photo" ALTER COLUMN "file_name" SET NOT NULL;
        ALTER TABLE "standard_service_photo" ALTER COLUMN "file_name" SET NOT NULL;"""
