from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salon" ALTER COLUMN "phone" SET NOT NULL;
        ALTER TABLE "salon" ALTER COLUMN "slug" DROP NOT NULL;
        CREATE UNIQUE INDEX "uid_salon_slug_9d10e4" ON "salon" ("slug");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_salon_slug_9d10e4";
        ALTER TABLE "salon" ALTER COLUMN "phone" DROP NOT NULL;
        ALTER TABLE "salon" ALTER COLUMN "slug" SET NOT NULL;"""
