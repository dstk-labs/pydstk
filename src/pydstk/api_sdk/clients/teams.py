from pydstk.api_sdk.clients.base_client import BaseClient
from pydstk.api_sdk import repositories


class TeamsClient(BaseClient):
    entity = "team"

    def list(self, **kwargs):
        """Get list of teams

        :returns: List of Team instances
        :rtype: list[models.Team]
        """
        repository = self.build_repository(repositories.ListTeams)
        teamss_list = repository.list()
        return teamss_list
