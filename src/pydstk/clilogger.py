from click import secho

from pydstk.api_sdk.config import config
from pydstk.api_sdk.logger import Logger


class CliLogger(Logger):
    def _log(self, message, color=None, err=False):
        message = str(message)
        color = color if config.USE_CONSOLE_COLORS else None
        secho(message, fg=color, err=err)

    def log(self, message, color=None, err=False):
        self._log(message, color=color, err=err)

    def error(self, message, *args, **kwargs):
        color = "red" if config.USE_CONSOLE_COLORS else None
        self._log(message, color=color, err=True)

    def warning(self, message, *args, **kwargs):
        color = "yellow" if config.USE_CONSOLE_COLORS else None
        self._log(message, color=color)

    def debug(self, message, *args, **kwargs):
        if config.DEBUG:
            self._log("DEBUG: {}".format(message))
