from pydstk.api_sdk.clients.base_client import BaseClient
from pydstk.api_sdk import repositories


class TeamsClient(BaseClient):
    entity = "team"

    def list(self, include_archived=False):
        """Get list of teams

        :param bool include_archived:
        :returns: List of Team instances
        :rtype: list[models.Team]
        """
        repository = self.build_repository(repositories.ListTeams)
        return repository.list(include_archived=include_archived)

    def get(self, team_id):
        """Get a team you are a member of

        :param str team_id:
        :rtype: models.Team
        """
        repository = self.build_repository(repositories.GetTeam)
        return repository.get(team_id)
