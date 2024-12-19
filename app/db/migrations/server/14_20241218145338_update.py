from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "categories" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "slug" VARCHAR(255) NOT NULL UNIQUE,
    "description" TEXT
);
        CREATE TABLE IF NOT EXISTS "custom_services" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "slug" VARCHAR(255),
    "description" TEXT,
    "duration" INT,
    "price" DECIMAL(10,2),
    "is_active" BOOL NOT NULL  DEFAULT True,
    "standard_service_id" INT REFERENCES "standard_services" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "job_applications" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(8) NOT NULL  DEFAULT 'pending',
    "message" TEXT,
    "master_id" INT NOT NULL REFERENCES "master" ("id") ON DELETE CASCADE,
    "vacancy_id" INT NOT NULL REFERENCES "vacancies" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "job_applications"."status" IS 'pending: pending\naccepted: accepted\nrejected: rejected';
        CREATE TABLE IF NOT EXISTS "master" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "text" TEXT,
    "experience_years" INT NOT NULL,
    "specialty" VARCHAR(255) NOT NULL,
    "slug" VARCHAR(255) NOT NULL,
    "city_id" INT REFERENCES "cities" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL UNIQUE REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "resumes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "experience_years" INT NOT NULL,
    "master_id" INT NOT NULL REFERENCES "master" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "salon" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "name" VARCHAR(255) NOT NULL,
    "address" VARCHAR(255) NOT NULL,
    "text" TEXT,
    "slug" VARCHAR(255) NOT NULL,
    "user_id" INT NOT NULL UNIQUE REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "salon_master_invitations" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(9) NOT NULL  DEFAULT 'pending',
    "message" TEXT,
    "expires_at" TIMESTAMPTZ,
    "notification_status" VARCHAR(6) NOT NULL  DEFAULT 'unread',
    "response_date" TIMESTAMPTZ,
    "master_id" INT NOT NULL REFERENCES "master" ("id") ON DELETE CASCADE,
    "salon_id" INT NOT NULL REFERENCES "salon" ("id") ON DELETE CASCADE,
    "vacancy_id" INT REFERENCES "vacancies" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "salon_master_invitations"."status" IS 'pending: pending\naccepted: accepted\nrejected: rejected\ncancelled: cancelled';
COMMENT ON COLUMN "salon_master_invitations"."notification_status" IS 'sent: sent\nread: read\nunread: unread';
        CREATE TABLE IF NOT EXISTS "salonmasterrelation" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(8) NOT NULL  DEFAULT 'pending',
    "role" VARCHAR(10) NOT NULL  DEFAULT 'employee',
    "start_date" DATE,
    "end_date" DATE,
    "notes" TEXT,
    "master_id" INT NOT NULL REFERENCES "master" ("id") ON DELETE CASCADE,
    "salon_id" INT NOT NULL REFERENCES "salon" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_salonmaster_salon_i_a86277" UNIQUE ("salon_id", "master_id")
);
COMMENT ON COLUMN "salonmasterrelation"."status" IS 'active: active\npending: pending\ninactive: inactive';
COMMENT ON COLUMN "salonmasterrelation"."role" IS 'employee: employee\nfreelancer: freelancer';
        CREATE TABLE IF NOT EXISTS "service_photos" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "image_url" VARCHAR(255) NOT NULL,
    "alt" VARCHAR(255),
    "description" TEXT,
    "service_id" INT NOT NULL REFERENCES "custom_services" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "standard_services" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "slug" VARCHAR(255),
    "description" TEXT,
    "duration" INT,
    "price" DECIMAL(10,2),
    "is_active" BOOL NOT NULL  DEFAULT True,
    "category_id" INT REFERENCES "categories" ("id") ON DELETE SET NULL
);
        CREATE TABLE IF NOT EXISTS "vacancies" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(255) NOT NULL,
    "position" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "status" VARCHAR(6) NOT NULL  DEFAULT 'open',
    "salon_id" INT NOT NULL REFERENCES "salon" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "vacancies"."status" IS 'open: open\nclosed: closed';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "resumes";
        DROP TABLE IF EXISTS "custom_services";
        DROP TABLE IF EXISTS "categories";
        DROP TABLE IF EXISTS "standard_services";
        DROP TABLE IF EXISTS "job_applications";
        DROP TABLE IF EXISTS "master";
        DROP TABLE IF EXISTS "service_photos";
        DROP TABLE IF EXISTS "salon_master_invitations";
        DROP TABLE IF EXISTS "salonmasterrelation";
        DROP TABLE IF EXISTS "vacancies";
        DROP TABLE IF EXISTS "salon";"""
