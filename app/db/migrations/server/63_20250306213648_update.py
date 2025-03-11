from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_master" ADD "original" TEXT;
        ALTER TABLE "avatar_photo_salon" ADD "original" TEXT;
        ALTER TABLE "custom_service_photo" ADD "original" TEXT;
        ALTER TABLE "photo_news" ADD "original" TEXT;
        ALTER TABLE "standard_service_photo" ADD "original" TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "photo_news" DROP COLUMN "original";
        ALTER TABLE "avatar_photo_salon" DROP COLUMN "original";
        ALTER TABLE "avatar_photo_master" DROP COLUMN "original";
        ALTER TABLE "custom_service_photo" DROP COLUMN "original";
        ALTER TABLE "standard_service_photo" DROP COLUMN "original";"""
