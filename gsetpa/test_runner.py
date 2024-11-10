import dataclasses
import os

from django.conf import settings
from django.test.runner import DiscoverRunner


@dataclasses.dataclass
class MockResponse:
    json_data: dict
    status_code: int

    def json(self):
        return self.json_data


class FastTestRunner(DiscoverRunner):
    def setup_test_environment(self):
        super().setup_test_environment()
        settings.MIDDLEWARE = [
            x for x in settings.MIDDLEWARE if x != "silk.middleware.SilkyMiddleware"
        ]
        settings.DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"
        settings.PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
        settings.DATABASES["default"]["HOST"] = os.getenv("RDS_HOSTNAME")
