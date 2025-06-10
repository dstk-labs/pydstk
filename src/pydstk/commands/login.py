import importlib.metadata

from pydstk.cli_logger import CliLogger
from pydstk.login import set_apikey


class CommandBase(object):
    def __init__(self, api=None, logger_=CliLogger()):
        self.api = api
        self.logger = logger_


class SetApiKeyCommand(CommandBase):
    def execute(self, api_key):
        if not api_key:
            self.logger.error("API Key cannot be empty.")
            return

        set_apikey(api_key)


class ShowVersionCommand(CommandBase):
    def execute(self):
        __version__ = importlib.metadata.version("pydstk")
        self.logger.log(__version__)
