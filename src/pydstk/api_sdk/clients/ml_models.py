from pydstk.api_sdk import repositories
from pydstk.api_sdk.clients.base_client import BaseClient


class ModelsClient(BaseClient):
    entity = "model"

    def list(self, project_id=None, include_archived=False, name=None, team_id=None):
        """Get list of models in a team

        :param str project_id: only models in this project
        :param bool include_archived:
        :param str name: only models whose name contains this text
        :param str team_id: defaults to the client's team
        :rtype: list[models.Model]
        """
        repository = self.build_repository(repositories.ListModels)
        return repository.list(
            self.resolve_team_id(team_id),
            project_id=project_id,
            include_archived=include_archived,
            name=name,
        )

    def get(self, model_id):
        """
        :param str model_id:
        :rtype: models.Model
        """
        repository = self.build_repository(repositories.GetModel)
        return repository.get(model_id)

    def create(self, project_id, storage_provider_id, name, description=""):
        """
        :param str project_id:
        :param str storage_provider_id: where this model's versions are stored
        :param str name:
        :param str description:
        :rtype: models.Model
        """
        repository = self.build_repository(repositories.CreateModel)
        return repository.create(project_id, storage_provider_id, name, description)

    def edit(
        self,
        model_id,
        project_id=None,
        storage_provider_id=None,
        name=None,
        description=None,
    ):
        """Change a model. Fields left as None keep their current value

        :param str model_id:
        :param str project_id:
        :param str storage_provider_id:
        :param str name:
        :param str description:
        :rtype: models.Model
        """
        current = self.get(model_id)
        repository = self.build_repository(repositories.EditModel)
        return repository.edit(
            model_id,
            current.project_id if project_id is None else project_id,
            current.storage_provider_id
            if storage_provider_id is None
            else storage_provider_id,
            current.name if name is None else name,
            current.description if description is None else description,
        )

    def archive(self, model_id):
        """Archive a model, or restore it if it is already archived

        :param str model_id:
        :rtype: models.Model
        """
        repository = self.build_repository(repositories.ArchiveModel)
        return repository.archive(model_id)
