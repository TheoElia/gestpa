from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = [
    "127.0.0.1",
]

CORS_ORIGIN_ALLOW_ALL = True

DEBUG_TOOLBAR_CONFIG["SHOW_TOOLBAR_CALLBACK"] = lambda _: True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("RDS_DB_NAME"),
        "USER": os.getenv("RDS_USERNAME"),
        "PASSWORD": os.getenv("RDS_PASSWORD"),
        "HOST": os.getenv("RDS_HOSTNAME"),
        "PORT": os.getenv("RDS_PORT"),
        "CONN_MAX_AGE": 0,
    }
}

# Query Inspect
# Whether the Query Inspector should do anything (default: False)
QUERY_INSPECT_ENABLED = True
# Whether to log the stats via Django logging (default: True)
QUERY_INSPECT_LOG_STATS = True
# Whether to add stats headers (default: True)
QUERY_INSPECT_HEADER_STATS = True
# Whether to log duplicate queries (default: False)
QUERY_INSPECT_LOG_QUERIES = True
# Whether to log queries that are above an absolute limit (default: None - disabled)
QUERY_INSPECT_ABSOLUTE_LIMIT = 100  # in milliseconds
# Whether to log queries that are more than X
# standard deviations above the mean query time (default: None - disabled)
QUERY_INSPECT_STANDARD_DEVIATION_LIMIT = 2
# Whether to include tracebacks in the logs (default: False)
QUERY_INSPECT_LOG_TRACEBACKS = True
# Project root (a list of directories, see below - default empty)
QUERY_INSPECT_TRACEBACK_ROOTS = [str(BASE_DIR)]
