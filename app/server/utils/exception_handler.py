import json
import os
from typing import Union, List, Dict, Any

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from pydantic_i18n import PydanticI18n, BabelLoader

from config.components.logging_config import logger
from config.constants import APP_DIR


class CustomBabelLoader(BabelLoader):  # FIXME move to separate file
    def __init__(self, translations_directory: str, domain: str = "messages"):
        try:
            from babel import Locale
            from babel.support import Translations
        except ImportError as e:  # pragma: no cover
            raise ImportError(
                "babel not installed, you cannot use this loader.\n"
                "To install, run: pip install babel"
            ) from e

        self.translations = {}

        for dir_name in [
            d
            for d in os.listdir(translations_directory)
            if os.path.isdir(os.path.join(translations_directory, d))
        ]:
            locale = Locale.parse(dir_name)
            self.translations[str(locale)] = Translations.load(
                translations_directory, [locale], domain=domain
            )


loader = CustomBabelLoader(os.path.join(APP_DIR, "locales"))
tr = PydanticI18n(loader, default_locale="en")


def make_errors_json_serializable(errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Делает ошибки JSON-сериализуемыми, преобразуя несериализуемые объекты,
    такие как ValueError, в строковые представления.
    """
    serializable_errors = []
    for error in errors:
        serializable_error = error.copy()
        if "ctx" in serializable_error and isinstance(serializable_error["ctx"], dict) and "error" in serializable_error["ctx"] and isinstance(serializable_error["ctx"]["error"], ValueError):
            serializable_error["ctx"]["error"] = str(serializable_error["ctx"]["error"]) # Преобразуем ValueError в строку
        serializable_errors.append(serializable_error)
    return serializable_errors


async def http_exception_handler(
    request: Request, exc: Union[HTTPException, StarletteHTTPException]
):
    logger.warning(f"HTTPException: status_code={exc.status_code}, detail={exc.detail}")
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.warning(f"Validation Error: {exc.errors()}")

    logger.debug(f"Содержимое exc.errors() перед переводом: {exc.errors()}")

    try:
        locale = request.state.babel.locale  # will work with BabelMiddleware
    except AttributeError:
        locale = "en"

    try:
        translated_errors = tr.translate(exc.errors(), locale)
    except ValueError as e: # Ловим ValueError, если tr.translate не может перевести
        logger.error(f"Ошибка перевода валидации: {e}", exc_info=True) # Логируем ошибку перевода
        translated_errors = exc.errors() # Возвращаем оригинальные ошибки, если перевод не удался

    translated_errors_serializable = make_errors_json_serializable(translated_errors) # Делаем ошибки сериализуемыми

    logger.debug(f"Тип translated_errors_serializable перед JSONResponse: {type(translated_errors_serializable)}")
    if isinstance(translated_errors_serializable, (list, dict)):
        logger.debug(f"Содержимое translated_errors_serializable перед JSONResponse: {translated_errors_serializable}")

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": translated_errors_serializable}, # Используем сериализуемые ошибки
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Непредвиденная ошибка: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500, content={"detail": "Внутренняя ошибка сервера"}
    )