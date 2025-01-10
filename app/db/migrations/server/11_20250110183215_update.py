from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_categories_name_c47ef4";
        DROP INDEX IF EXISTS "uid_categories_slug_3a37a8";
        ALTER TABLE "categories" ADD "title" VARCHAR(255);
        ALTER TABLE "categories" ADD "content" TEXT;
        ALTER TABLE "categories" ALTER COLUMN "slug" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "categories" DROP COLUMN "title";
        ALTER TABLE "categories" DROP COLUMN "content";
        ALTER TABLE "categories" ALTER COLUMN "slug" SET NOT NULL;
        CREATE UNIQUE INDEX "uid_categories_slug_3a37a8" ON "categories" ("slug");
        CREATE UNIQUE INDEX "uid_categories_name_c47ef4" ON "categories" ("name");"""
