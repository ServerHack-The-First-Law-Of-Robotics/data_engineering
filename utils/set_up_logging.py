from logging import getLogger, basicConfig, FileHandler, StreamHandler
from sys import stderr
from os.path import isdir, join
from os import makedirs

from settings import LOGLEVEL

logger = getLogger(__name__)


def set_up_logging():
    logs_dir = "logs/"
    if not isdir(logs_dir):
        makedirs(logs_dir)
    handlers = [
        FileHandler(join(logs_dir, "log.txt")),
        StreamHandler(stderr)
    ]
    if LOGLEVEL in ("DEBUG", "INFO", "WARNING", "ERROR"):
        basicConfig(level=LOGLEVEL, handlers=handlers)
        getLogger().setLevel(LOGLEVEL)
        for handler in handlers:
            getLogger().addHandler(handler)
    else:
        logger.warning(f"Неподдерживаемый LOGLEVEL: {LOGLEVEL}")
