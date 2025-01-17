from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salon" DROP CONSTRAINT IF EXISTS "fk_salon_avatar_p_e4740811";
        ALTER TABLE "salon" DROP COLUMN "avatar_id";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salon" ADD "avatar_id" INT;
        ALTER TABLE "salon" ADD CONSTRAINT "fk_salon_avatar_p_e4740811" FOREIGN KEY ("avatar_id") REFERENCES "avatar_photo_salon" ("id") ON DELETE SET NULL;"""
