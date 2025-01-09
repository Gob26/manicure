from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "categories" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "slug" VARCHAR(255) NOT NULL UNIQUE,
    "description" TEXT
);
CREATE TABLE IF NOT EXISTS "cities" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "district" VARCHAR(50) NOT NULL,
    "subject" VARCHAR(100) NOT NULL,
    "population" INT NOT NULL,
    "latitude" DOUBLE PRECISION NOT NULL,
    "longitude" DOUBLE PRECISION NOT NULL,
    "slug" VARCHAR(255) NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS "idx_cities_name_5891f2" ON "cities" ("name");
CREATE INDEX IF NOT EXISTS "idx_cities_populat_a438c1" ON "cities" ("population");
CREATE INDEX IF NOT EXISTS "idx_cities_latitud_095fa4" ON "cities" ("latitude");
CREATE INDEX IF NOT EXISTS "idx_cities_longitu_fa4a37" ON "cities" ("longitude");
CREATE INDEX IF NOT EXISTS "idx_cities_slug_5a3399" ON "cities" ("slug");
CREATE INDEX IF NOT EXISTS "idx_cities_latitud_acfeba" ON "cities" ("latitude", "longitude");
CREATE TABLE IF NOT EXISTS "city_descriptions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(255),
    "description" TEXT,
    "text" TEXT,
    "city_id" INT NOT NULL UNIQUE REFERENCES "cities" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "photos" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "file_name" VARCHAR(255) NOT NULL,
    "file_path" VARCHAR(1000) NOT NULL,
    "mime_type" VARCHAR(100) NOT NULL,
    "size" INT NOT NULL,
    "width" INT,
    "height" INT,
    "is_main" BOOL NOT NULL  DEFAULT False,
    "sort_order" INT NOT NULL  DEFAULT 0,
    "master_id" INT,
    "salon_id" INT,
    "service_id" INT,
    "entity_type" VARCHAR(14) NOT NULL,
    "caption" VARCHAR(1000),
    "is_active" BOOL NOT NULL  DEFAULT True
);
COMMENT ON COLUMN "photos"."entity_type" IS 'MASTER_AVATAR: master_avatar\nMASTER_WORK: master_work\nMASTER_POST: master_post\nSALON_INTERIOR: salon_interior\nSALON_POST: salon_post\nSALON_LOGO: salon_logo\nSERVICE_PHOTO: service_photo';
COMMENT ON TABLE "photos" IS 'Унифицированная модель фотографий, наследующая абстрактную модель';
CREATE TABLE IF NOT EXISTS "service_attribute_types" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "slug" VARCHAR(100) NOT NULL UNIQUE
);
COMMENT ON TABLE "service_attribute_types" IS 'Типы атрибутов (способ удаления кутикулы, материал покрытия и т.д.)';
CREATE TABLE IF NOT EXISTS "service_attribute_values" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "slug" VARCHAR(100) NOT NULL UNIQUE,
    "attribute_type_id" INT NOT NULL REFERENCES "service_attribute_types" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "service_attribute_values" IS 'Возможные значения атрибутов (аппаратный, классический, гель-лак и т.д.)';
CREATE TABLE IF NOT EXISTS "standard_services" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "title" VARCHAR(255),
    "description" TEXT,
    "content" TEXT,
    "slug" VARCHAR(255),
    "category_id" INT REFERENCES "categories" ("id") ON DELETE SET NULL,
    "default_photo_id" INT REFERENCES "photos" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "standard_services" IS 'Модель для стандартных услуг';
CREATE TABLE IF NOT EXISTS "template_attributes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_required" BOOL NOT NULL  DEFAULT False,
    "attribute_type_id" INT NOT NULL REFERENCES "service_attribute_types" ("id") ON DELETE CASCADE,
    "service_template_id" INT NOT NULL REFERENCES "standard_services" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_template_at_service_e97083" UNIQUE ("service_template_id", "attribute_type_id")
);
COMMENT ON TABLE "template_attributes" IS 'Связь шаблона услуги с возможными атрибутами';
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "role" VARCHAR(6) NOT NULL  DEFAULT 'client',
    "city_id" INT NOT NULL REFERENCES "cities" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "users"."role" IS 'client: client\nmaster: master\nsalon: salon\namin: admin';
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
    "name" VARCHAR(257) NOT NULL,
    "address" VARCHAR(255),
    "phone" VARCHAR(20),
    "telegram" VARCHAR(255),
    "whatsapp" VARCHAR(255),
    "website" VARCHAR(255),
    "vk" VARCHAR(255),
    "instagram" VARCHAR(255),
    "accepts_at_home" BOOL NOT NULL  DEFAULT False,
    "accepts_in_salon" BOOL NOT NULL  DEFAULT False,
    "accepts_offsite" BOOL NOT NULL  DEFAULT False,
    "avatar_id" INT REFERENCES "photos" ("id") ON DELETE SET NULL,
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
    "name" VARCHAR(255) NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "slug" VARCHAR(255) NOT NULL,
    "address" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "text" TEXT,
    "city_id" INT REFERENCES "cities" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL UNIQUE REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "custom_services" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "title" VARCHAR(255),
    "description" TEXT,
    "content" TEXT,
    "slug" VARCHAR(255),
    "base_price" DECIMAL(10,2) NOT NULL,
    "duration_minutes" INT NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "master_id" INT REFERENCES "master" ("id") ON DELETE CASCADE,
    "salon_id" INT REFERENCES "salon" ("id") ON DELETE CASCADE,
    "standard_service_id" INT NOT NULL REFERENCES "standard_services" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_custom_serv_master__48d4d5" UNIQUE ("master_id", "standard_service_id"),
    CONSTRAINT "uid_custom_serv_salon_i_c14773" UNIQUE ("salon_id", "standard_service_id")
);
COMMENT ON TABLE "custom_services" IS 'Модель пользовательской услуги (для мастеров и салонов)';
CREATE TABLE IF NOT EXISTS "custom_service_attributes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "additional_price" DECIMAL(10,2) NOT NULL  DEFAULT 0,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "attribute_value_id" INT NOT NULL REFERENCES "service_attribute_values" ("id") ON DELETE CASCADE,
    "custom_service_id" INT NOT NULL REFERENCES "custom_services" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_custom_serv_custom__de301c" UNIQUE ("custom_service_id", "attribute_value_id")
);
COMMENT ON TABLE "custom_service_attributes" IS 'Выбранные атрибуты услуги с ценами';
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
    "is_main" BOOL NOT NULL  DEFAULT False,
    "order" INT NOT NULL  DEFAULT 0,
    "custom_service_id" INT NOT NULL REFERENCES "custom_services" ("id") ON DELETE CASCADE,
    "photo_id" INT NOT NULL REFERENCES "photos" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "service_photos" IS 'Фотографии услуг';
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
COMMENT ON COLUMN "vacancies"."status" IS 'open: open\nclosed: closed';
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
COMMENT ON COLUMN "salon_master_invitations"."notification_status" IS 'sent: sent\nread: read\nunread: unread';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
