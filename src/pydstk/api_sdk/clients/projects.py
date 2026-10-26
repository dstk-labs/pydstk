from pydstk.api_sdk import repositories
from pydstk.api_sdk.clients.base_client import BaseClient


class ProjectsClient(BaseClient):
    entity = "project"

    def list(self, team_id, include_archived=False, name=None):
        """Get list of projects in a team

        :param str team_id:
        :param bool include_archived:
        :param str name: only projects whose name contains this text
        :rtype: list[models.Project]
        """
        repository = self.build_repository(repositories.ListProjects)
        return repository.list(team_id, include_archived=include_archived, name=name)

    def get(self, project_id):
        """
        :param str project_id:
        :rtype: models.Project
        """
        repository = self.build_repository(repositories.GetProject)
        return repository.get(project_id)

    def create(self, team_id, name, description=""):
        """
        :param str team_id:
        :param str name:
        :param str description:
        :rtype: models.Project
        """
        repository = self.build_repository(repositories.CreateProject)
        return repository.create(team_id, name, description)

    def edit(self, project_id, name=None, description=None):
        """Change a project. Fields left as None keep their current value

        :param str project_id:
        :param str name:
        :param str description:
        :rtype: models.Project
        """
        current = self.get(project_id)
        repository = self.build_repository(repositories.EditProject)
        return repository.edit(
            project_id,
            current.name if name is None else name,
            current.description if description is None else description,
        )

    def archive(self, project_id):
        """Archive a project, or restore it if it is already archived

        :param str project_id:
        :rtype: models.Project
        """
        repository = self.build_repository(repositories.ArchiveProject)
        return repository.archive(project_id)
