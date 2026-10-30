import copy

from pydstk.api_sdk import logger as sdk_logger
from pydstk.api_sdk.exceptions import DstkSdkError


class BaseClient(object):
    def __init__(
        self, api_key, client_name=None, logger=sdk_logger.MuteLogger(), team_id=None
    ):
        """
        Base class. All client classes inherit from it.

        :param str api_key: your API key
        :param str client_name:
        :param sdk_logger.Logger logger:
        :param str team_id: team to use when a method isn't given one
        """
        self.api_key = api_key
        self.client_name = client_name
        self.logger = logger
        self.team_id = team_id

    def resolve_team_id(self, team_id):
        """
        :param str team_id:
        :rtype: str
        """
        team_id = team_id or self.team_id
        if not team_id:
            raise DstkSdkError(
                "No team selected. Pass team_id, or save a default with "
                "`pydstk teams use TEAM_ID`."
            )
        return team_id

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
