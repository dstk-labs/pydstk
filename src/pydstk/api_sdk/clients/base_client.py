import copy

from pydstk.api_sdk import logger as sdk_logger


class BaseClient(object):
    def __init__(self, api_key, client_name=None, logger=sdk_logger.MuteLogger()):
        """
        Base class. All client classes inherit from it.

        :param str api_key: your API key
        :param str client_name:
        :param sdk_logger.Logger logger:
        """
        self.api_key = api_key
        self.client_name = client_name
        self.logger = logger

    def build_repository(self, repository_class, *args, **kwargs):
        """
        :param type[BaseRepository] repository_class:
        :rtype: BaseRepository
        """

        if self.client_name is not None and kwargs.get("client_name") is None:
            kwargs = copy.deepcopy(kwargs)
            kwargs["client_name"] = self.client_name

        repository = repository_class(
            *args, api_key=self.api_key, logger=self.logger, **kwargs
        )
        return repository
