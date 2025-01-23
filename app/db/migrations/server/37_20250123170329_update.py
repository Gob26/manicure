from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "custom_services" DROP COLUMN "slug";
        ALTER TABLE "custom_services" DROP COLUMN "content";
        ALTER TABLE "custom_services" DROP COLUMN "name";
        ALTER TABLE "custom_services" DROP COLUMN "title";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "custom_services" ADD "slug" VARCHAR(255);
        ALTER TABLE "custom_services" ADD "content" TEXT;
        ALTER TABLE "custom_services" ADD "name" VARCHAR(255) NOT NULL;
        ALTER TABLE "custom_services" ADD "title" VARCHAR(255);"""
