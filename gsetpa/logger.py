import logging
from dataclasses import dataclass

from django.conf import settings


@dataclass
class LevelLTEFilter:
    level: str

    def filter(self, log_record):
        return log_record.levelno <= logging.getLevelName(self.level)


def get_logger(name):
    return logging.getLogger(f"{settings.PROJECT_NAME}.{name}")


getLogger = get_logger
