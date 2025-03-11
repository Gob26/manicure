from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi.exceptions import RequestValidationError
from fastapi_babel import BabelMiddleware, BabelConfigs
from fastapi_pagination import add_pagination
from tortoise import Tortoise, generate_config
from tortoise.contrib.fastapi import RegisterTortoise
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # <-- Импортируйте StaticFiles
from config import settings
from config.constants import APP_DIR, MEDIA_DIR
from core.exceptions.base import ApplicationException
from core.exceptions.handlers import application_exception_handler, internal_server_error_handler
from server.utils.exception_handler import validation_exception_handler
import os # <-- Импортируйте модуль os


def _init_router(_app: FastAPI) -> None:
    from api import router
    _app.include_router(router)


def _init_middleware(_app: FastAPI) -> None:
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )


def _init_internalization(_app: FastAPI) -> None:
    _app.add_middleware(
        BabelMiddleware, babel_configs=BabelConfigs(
            ROOT_DIR=APP_DIR.joinpath("any"),
            # we need this hack because of the way BabelConfigs is implemented, it takes parent dir
            BABEL_DEFAULT_LOCALE="en",
            BABEL_TRANSLATION_DIRECTORY="locales",
        )
    )

# Добавьте эту функцию для инициализации StaticFiles
def _init_static_files(_app: FastAPI) -> None:
    MEDIA_DIRECTORY = MEDIA_DIR  # <---- Используем константу MEDIA_DIR
    if not os.path.exists(MEDIA_DIRECTORY):
        os.makedirs(MEDIA_DIRECTORY, exist_ok=True)
    _app.mount("/media", StaticFiles(directory=MEDIA_DIRECTORY), name="media")


# Обработка глобальных ошибок
def _init_exception_handlers(_app: FastAPI) -> None:
    _app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )
    _app.add_exception_handler(
        ApplicationException,  # Обрабатываем все ошибки типа ApplicationException
        application_exception_handler,
    )
    _app.add_exception_handler(
        Exception,  # Обрабатываем все остальные непредвиденные ошибки
        internal_server_error_handler,
    )


def _init_pagination(_app: FastAPI) -> None:
    add_pagination(_app)


@asynccontextmanager
async def lifespan_test(_app: FastAPI) -> AsyncGenerator[None, None]:
    config = generate_config(
        db_url=settings.test_db_url,
        app_modules=settings.apps_for_tests,
        testing=True,
    )
    try:
        async with RegisterTortoise(
            app=_app,
            config=config,
            generate_schemas=True,
            add_exception_handlers=True,
            _create_db=True,
        ):
            yield
    except Exception as e:
        raise
    finally:
        await Tortoise._drop_databases()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        if getattr(_app.state, "testing", None):
            async with lifespan_test(_app) as _:
                _init_router(_app)
                _init_pagination(_app)
                yield
        else:
            async with RegisterTortoise(
                app=_app,
                config=settings.tortoise_config,
                generate_schemas=True,
                add_exception_handlers=True,
            ):
                _init_router(_app)
                _init_pagination(_app)
                yield
    except Exception as e:
        raise


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
    )
    _init_middleware(_app)
    _init_internalization(_app)
    # **Добавьте инициализацию StaticFiles здесь, после других middleware:**
    _init_static_files(_app)
    _init_exception_handlers(_app)
    return _app

app = create_app()