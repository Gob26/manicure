from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "salon_avatar_photo_salon";
        ALTER TABLE "avatar_photo_master" ADD "small" VARCHAR(255);
        ALTER TABLE "avatar_photo_master" ADD "medium" VARCHAR(255);
        ALTER TABLE "avatar_photo_master" ADD "large" VARCHAR(255);
        ALTER TABLE "avatar_photo_master" DROP COLUMN "version";
        ALTER TABLE "avatar_photo_salon" RENAME COLUMN "group_id" TO "small";
        ALTER TABLE "avatar_photo_salon" ADD "medium" VARCHAR(255);
        ALTER TABLE "avatar_photo_salon" ADD "salon_id" INT NOT NULL;
        ALTER TABLE "avatar_photo_salon" ADD "large" VARCHAR(255);
        ALTER TABLE "avatar_photo_salon" DROP COLUMN "version";
        ALTER TABLE "custom_service_photo" ADD "small" VARCHAR(255);
        ALTER TABLE "custom_service_photo" ADD "medium" VARCHAR(255);
        ALTER TABLE "custom_service_photo" ADD "large" VARCHAR(255);
        ALTER TABLE "custom_service_photo" DROP COLUMN "version";
        ALTER TABLE "photo_news" ADD "small" VARCHAR(255);
        ALTER TABLE "photo_news" ADD "medium" VARCHAR(255);
        ALTER TABLE "photo_news" ADD "large" VARCHAR(255);
        ALTER TABLE "photo_news" DROP COLUMN "version";
        ALTER TABLE "standard_service_photo" ADD "small" VARCHAR(255);
        ALTER TABLE "standard_service_photo" ADD "medium" VARCHAR(255);
        ALTER TABLE "standard_service_photo" ADD "large" VARCHAR(255);
        ALTER TABLE "standard_service_photo" DROP COLUMN "version";
        ALTER TABLE "avatar_photo_salon" ADD CONSTRAINT "fk_avatar_p_salon_be7c5035" FOREIGN KEY ("salon_id") REFERENCES "salon" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "avatar_photo_salon" DROP CONSTRAINT IF EXISTS "fk_avatar_p_salon_be7c5035";
        ALTER TABLE "photo_news" ADD "version" VARCHAR(50) NOT NULL  DEFAULT 'pc';
        ALTER TABLE "photo_news" DROP COLUMN "small";
        ALTER TABLE "photo_news" DROP COLUMN "medium";
        ALTER TABLE "photo_news" DROP COLUMN "large";
        ALTER TABLE "avatar_photo_salon" ADD "version" VARCHAR(50) NOT NULL  DEFAULT 'pc';
        ALTER TABLE "avatar_photo_salon" RENAME COLUMN "small" TO "group_id";
        ALTER TABLE "avatar_photo_salon" DROP COLUMN "medium";
        ALTER TABLE "avatar_photo_salon" DROP COLUMN "salon_id";
        ALTER TABLE "avatar_photo_salon" DROP COLUMN "large";
        ALTER TABLE "avatar_photo_master" ADD "version" VARCHAR(50) NOT NULL  DEFAULT 'pc';
        ALTER TABLE "avatar_photo_master" DROP COLUMN "small";
        ALTER TABLE "avatar_photo_master" DROP COLUMN "medium";
        ALTER TABLE "avatar_photo_master" DROP COLUMN "large";
        ALTER TABLE "custom_service_photo" ADD "version" VARCHAR(50) NOT NULL  DEFAULT 'pc';
        ALTER TABLE "custom_service_photo" DROP COLUMN "small";
        ALTER TABLE "custom_service_photo" DROP COLUMN "medium";
        ALTER TABLE "custom_service_photo" DROP COLUMN "large";
        ALTER TABLE "standard_service_photo" ADD "version" VARCHAR(50) NOT NULL  DEFAULT 'pc';
        ALTER TABLE "standard_service_photo" DROP COLUMN "small";
        ALTER TABLE "standard_service_photo" DROP COLUMN "medium";
        ALTER TABLE "standard_service_photo" DROP COLUMN "large";
        CREATE TABLE "salon_avatar_photo_salon" (
    "salon_id" INT NOT NULL REFERENCES "salon" ("id") ON DELETE CASCADE,
    "avatarphotosalon_id" INT NOT NULL REFERENCES "avatar_photo_salon" ("id") ON DELETE CASCADE
);"""
