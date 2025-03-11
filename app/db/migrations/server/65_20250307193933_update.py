from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_master" DROP CONSTRAINT IF EXISTS "fk_avatar_p_master_8577db1c";
        ALTER TABLE "avatar_photo_master" RENAME COLUMN "salon_id" TO "master_id";
        ALTER TABLE "avatar_photo_master" ADD CONSTRAINT "fk_avatar_p_master_ce6fd978" FOREIGN KEY ("master_id") REFERENCES "master" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_master" DROP CONSTRAINT IF EXISTS "fk_avatar_p_master_ce6fd978";
        ALTER TABLE "avatar_photo_master" RENAME COLUMN "master_id" TO "salon_id";
        ALTER TABLE "avatar_photo_master" ADD CONSTRAINT "fk_avatar_p_master_8577db1c" FOREIGN KEY ("salon_id") REFERENCES "master" ("id") ON DELETE CASCADE;"""
