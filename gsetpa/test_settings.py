from .settings import *

#DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

SLACK_BOT_TOKEN = None
MIDDLEWARE = [x for x in MIDDLEWARE if x != "silk.middleware.SilkyMiddleware"]
DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
DATABASES["default"]["HOST"] = os.getenv("RDS_HOSTNAME")
