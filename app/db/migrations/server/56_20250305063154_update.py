from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "newsphoto" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "file_name" VARCHAR(255)   DEFAULT 'default_name.jpg',
    "file_path" VARCHAR(1000) NOT NULL,
    "mime_type" VARCHAR(100),
    "size" INT NOT NULL,
    "width" INT,
    "height" INT,
    "is_main" BOOL NOT NULL  DEFAULT False,
    "sort_order" INT NOT NULL  DEFAULT 0,
    "version" VARCHAR(50) NOT NULL  DEFAULT 'pc',
    "description" TEXT
);
COMMENT ON TABLE "newsphoto" IS 'Модель фотографий новостей с описанием  ';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "newsphoto";"""
