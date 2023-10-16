from os import environ
from os.path import abspath, basename, dirname, join

# CONFIG VARIABLES
BASE_DIR = dirname(dirname(abspath(__file__)))
SRC_DIR = dirname(abspath(__file__))
BASE_NAME = basename(BASE_DIR)

# LOGGING
LOGGING_FILE = join(environ.get("LOGGING_DIR", BASE_DIR), f"{BASE_NAME}.log")
LOGGING_LEVEL = environ.get("LOGGING_LEVEL", "WARNING")
LOGGING_FILE_MAX_BYTES = 10485760
LOGGING_FILE_BACKUP_COUNT = 2
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "brief": {"format": "{levelname} {name}: {message}", "style": "{"},
        "verbose": {
            "format": "[{asctime}] {levelname:<8} {name}: {message}",
            "style": "{",
            "datefmt": "%m.%d.%Y %I:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": LOGGING_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "brief",
        },
        "file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": LOGGING_FILE,
            "maxBytes": LOGGING_FILE_MAX_BYTES,
            "backupCount": LOGGING_FILE_BACKUP_COUNT,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        }
    },
}
