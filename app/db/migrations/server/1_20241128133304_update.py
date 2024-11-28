from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "city" RENAME TO "cities";
        ALTER TABLE "cities" ADD "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "cities" ADD "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "cities" RENAME TO "city";
        ALTER TABLE "cities" DROP COLUMN "updated_at";
        ALTER TABLE "cities" DROP COLUMN "created_at";"""
