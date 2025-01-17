from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "master" ADD "avatar_id" INT;
        ALTER TABLE "master" ADD CONSTRAINT "fk_master_avatar_p_219a57b4" FOREIGN KEY ("avatar_id") REFERENCES "avatar_photo_master" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "master" DROP CONSTRAINT IF EXISTS "fk_master_avatar_p_219a57b4";
        ALTER TABLE "master" DROP COLUMN "avatar_id";"""
