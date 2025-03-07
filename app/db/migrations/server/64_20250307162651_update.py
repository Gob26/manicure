from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "master" DROP CONSTRAINT IF EXISTS "fk_master_avatar_p_219a57b4";
        ALTER TABLE "avatar_photo_master" ADD "salon_id" INT NOT NULL;
        ALTER TABLE "master" DROP COLUMN "avatar_id";
        ALTER TABLE "master" ALTER COLUMN "title" SET NOT NULL;
        ALTER TABLE "master" ALTER COLUMN "address" SET NOT NULL;
        ALTER TABLE "master" ALTER COLUMN "phone" SET NOT NULL;
        ALTER TABLE "avatar_photo_master" ADD CONSTRAINT "fk_avatar_p_master_8577db1c" FOREIGN KEY ("salon_id") REFERENCES "master" ("id") ON DELETE CASCADE;
        CREATE UNIQUE INDEX "uid_master_slug_19fbf8" ON "master" ("slug");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_master" DROP CONSTRAINT IF EXISTS "fk_avatar_p_master_8577db1c";
        DROP INDEX IF EXISTS "uid_master_slug_19fbf8";
        ALTER TABLE "master" ADD "avatar_id" INT;
        ALTER TABLE "master" ALTER COLUMN "title" DROP NOT NULL;
        ALTER TABLE "master" ALTER COLUMN "address" DROP NOT NULL;
        ALTER TABLE "master" ALTER COLUMN "phone" DROP NOT NULL;
        ALTER TABLE "avatar_photo_master" DROP COLUMN "salon_id";
        ALTER TABLE "master" ADD CONSTRAINT "fk_master_avatar_p_219a57b4" FOREIGN KEY ("avatar_id") REFERENCES "avatar_photo_master" ("id") ON DELETE SET NULL;"""
