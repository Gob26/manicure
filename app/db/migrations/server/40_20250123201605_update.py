from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_master" ALTER COLUMN "file_name" SET DEFAULT 'default_name.jpg';
        ALTER TABLE "avatar_photo_salon" ALTER COLUMN "file_name" SET DEFAULT 'default_name.jpg';
        ALTER TABLE "custom_service_photo" ALTER COLUMN "file_name" SET DEFAULT 'default_name.jpg';
        ALTER TABLE "standard_service_photo" ALTER COLUMN "file_name" SET DEFAULT 'default_name.jpg';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_salon" ALTER COLUMN "file_name" DROP DEFAULT;
        ALTER TABLE "avatar_photo_master" ALTER COLUMN "file_name" DROP DEFAULT;
        ALTER TABLE "custom_service_photo" ALTER COLUMN "file_name" DROP DEFAULT;
        ALTER TABLE "standard_service_photo" ALTER COLUMN "file_name" DROP DEFAULT;"""
