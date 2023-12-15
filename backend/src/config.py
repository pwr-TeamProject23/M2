from os import environ
from os.path import abspath, basename, dirname, join
from zoneinfo import ZoneInfo

# CONFIG VARIABLES
BASE_DIR = dirname(dirname(abspath(__file__)))
SRC_DIR = dirname(abspath(__file__))
BASE_NAME = basename(BASE_DIR)

TZ_INFO = ZoneInfo("Europe/Warsaw")

API_RETRY_AFTER_THRESHOLD = 60
USER_SESSION_DURATION_DAYS = 30

# FASTAPI
ALLOWED_ORIGINS = ["http://localhost:5173", "https://envy.ii.pwr.edu.pl:12302"]

# SCOPUS
SCOPUS_API_KEY = environ.get("SCOPUS_API_KEY")
SCOPUS_LONG_PAGE_SIZE = 200
SCOPUS_SHORT_PAGE_SIZE = 25
SCOPUS_SEARCH_MAX_PAGES = 2
SCOPUS_SEARCH_MIN_PUBYEAR = 2010

# DBLP
DBLP_PAGE_SIZE = 100
DBLP_SEARCH_MAX_PAGES = 1

# SCHOLAR
SCHOLAR_SEARCH_MAX_PUBLICATIONS = 25
SCHOLAR_SEARCH_MAX_AUTHORS_PER_PUBLICATION = 1
SCHOLAR_SEARCH_YEAR_LOW = 2010

# LOGGING
LOGGING_FILE = join(environ.get("LOGGING_DIR", BASE_DIR), f"{BASE_NAME}.log")
LOGGING_LEVEL = environ.get("LOGGING_LEVEL", "DEBUG")
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
