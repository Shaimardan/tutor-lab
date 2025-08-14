import json
import logging.config
import os

from config import app_config

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def get_file_handler(name: str, log_format: str) -> logging.FileHandler:
    """Creates a file handler for logging.

    Args:
        name (str): Name of the log file.
        log_format (str): Format of the log messages.

    Returns:
        logging.FileHandler: Configured file handler.
    """
    file_path = os.path.join(LOG_DIR, f"{name}.log")
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    return file_handler


def get_stream_handler(log_format: str) -> logging.StreamHandler:
    """Creates a stream handler for logging.

    Args:
        log_format (str): Format of the log messages.

    Returns:
        logging.StreamHandler: Configured stream handler.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(log_format))
    return stream_handler


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Initializes and returns a logger with file and stream handlers.

    Args:
        name (str): Logger name.
        level (int): Logging level.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    with open("logging_config.json") as f:
        logging_config = json.load(f)

    logger.addHandler(get_file_handler(name, logging_config["formatters"]["detail"]["format"]))
    logger.addHandler(get_stream_handler(logging_config["formatters"]["detail"]["format"]))
    logger.propagate = False
    return logger


def remove_console_handlers(logging_config: dict) -> None:
    """Removes console handlers from the logging configuration. Removed on production mode.

    Args:
        logging_config (dict): Logging configuration dictionary.
    """
    handlers_to_remove = ["sqlalchemy_console"]

    for handler in handlers_to_remove:
        if handler in logging_config["handlers"]:
            del logging_config["handlers"][handler]

    for logger in logging_config["loggers"]:
        logging_config["loggers"][logger]["handlers"] = [
            handler
            for handler in logging_config["loggers"][logger]["handlers"]
            if handler not in handlers_to_remove
        ]


def logging_setting() -> None:
    """Configures logging settings based on the environment and logging configuration file."""
    with open("logging_config.json") as f:
        logging_config = json.load(f)
    if app_config.PRODUCTION:
        remove_console_handlers(logging_config)

    logging_config["handlers"]["file"]["filename"] = os.path.join(LOG_DIR, "base_log.log")
    logging_config["handlers"]["uvicorn_file"]["filename"] = os.path.join(LOG_DIR, "uvicorn.log")
    logging_config["handlers"]["sqlalchemy_file"]["filename"] = os.path.join(
        LOG_DIR, "sqlalchemy.log"
    )

    logging.config.dictConfig(logging_config)
