from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "cities" ADD "title" VARCHAR(255);
        ALTER TABLE "cities" ADD "text" TEXT;
        ALTER TABLE "cities" ADD "description" TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "cities" DROP COLUMN "title";
        ALTER TABLE "cities" DROP COLUMN "text";
        ALTER TABLE "cities" DROP COLUMN "description";"""
