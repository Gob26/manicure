import logging
import os
from pathlib import Path
from colorama import Fore, Style, init

from config.constants import APP_DIR

# Инициализация colorama для Windows
init()

# Создаём базовую директорию для логов
LOGS_DIR = APP_DIR / "config"/"components"/"logs"
LOGS_DIR.mkdir(exist_ok=True)

class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        if record.levelno in self.COLORS:
            color = self.COLORS[record.levelno]
            record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
            record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

def setup_logger(name: str = "my_app"):
    # Основной логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Проверяем, не были ли уже добавлены обработчики
    if logger.handlers:
        return logger

    # Форматтер для файловых логов
    file_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    console_handler.setLevel(logging.DEBUG)

    # Обработчик для info.log
    info_handler = logging.FileHandler(LOGS_DIR / "info.log")
    info_handler.setLevel(logging.DEBUG)
    info_handler.setFormatter(file_formatter)

    # Обработчик для error.log
    error_handler = logging.FileHandler(LOGS_DIR / "error.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(console_handler)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    return logger

# Создаём экземпляр логгера
logger = setup_logger()

# Если нужно проверить работу логгера, раскомментируйте:


logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")


