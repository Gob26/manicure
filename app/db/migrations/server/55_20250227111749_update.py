from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_master" ADD "version" VARCHAR(50) NOT NULL  DEFAULT 'pc';
        ALTER TABLE "avatar_photo_salon" ADD "version" VARCHAR(50) NOT NULL  DEFAULT 'pc';
        ALTER TABLE "custom_service_photo" ADD "version" VARCHAR(50) NOT NULL  DEFAULT 'pc';
        ALTER TABLE "standard_service_photo" ADD "version" VARCHAR(50) NOT NULL  DEFAULT 'pc';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_salon" DROP COLUMN "version";
        ALTER TABLE "avatar_photo_master" DROP COLUMN "version";
        ALTER TABLE "custom_service_photo" DROP COLUMN "version";
        ALTER TABLE "standard_service_photo" DROP COLUMN "version";"""
