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

    def list_members(self, team_id=None):
        """
        :param str team_id: defaults to the client's team
        :rtype: list[models.TeamMember]
        """
        repository = self.build_repository(repositories.ListTeamMembers)
        return repository.list(self.resolve_team_id(team_id))

    def create(self, name, description=""):
        """
        :param str name:
        :param str description:
        :rtype: models.Team
        """
        repository = self.build_repository(repositories.CreateTeam)
        return repository.create(name, description)

    def edit(self, team_id, name=None, description=None):
        """Change a team. Fields left as None keep their current value

        :param str team_id:
        :param str name:
        :param str description:
        :rtype: models.Team
        """
        current = self.get(team_id)
        repository = self.build_repository(repositories.EditTeam)
        return repository.edit(
            team_id,
            current.name if name is None else name,
            current.description if description is None else description,
        )

    def archive(self, team_id):
        """Archive a team, or restore it if it is already archived

        :param str team_id:
        :rtype: models.Team
        """
        repository = self.build_repository(repositories.ArchiveTeam)
        return repository.archive(team_id)
