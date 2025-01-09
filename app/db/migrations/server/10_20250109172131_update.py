from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salon" ADD "whatsapp" VARCHAR(255);
        ALTER TABLE "salon" ADD "telegram" VARCHAR(255);
        ALTER TABLE "salon" ADD "website" VARCHAR(255);
        ALTER TABLE "salon" ADD "phone" VARCHAR(20);
        ALTER TABLE "salon" ADD "vk" VARCHAR(255);
        ALTER TABLE "salon" ADD "instagram" VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salon" DROP COLUMN "whatsapp";
        ALTER TABLE "salon" DROP COLUMN "telegram";
        ALTER TABLE "salon" DROP COLUMN "website";
        ALTER TABLE "salon" DROP COLUMN "phone";
        ALTER TABLE "salon" DROP COLUMN "vk";
        ALTER TABLE "salon" DROP COLUMN "instagram";"""
