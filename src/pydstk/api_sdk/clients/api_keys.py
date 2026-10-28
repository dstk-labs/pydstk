from pydstk.api_sdk import repositories
from pydstk.api_sdk.clients.base_client import BaseClient


class ApiKeysClient(BaseClient):
    entity = "apiKey"

    def list(self):
        """
        :rtype: list[models.ApiKey]
        """
        repository = self.build_repository(repositories.ListApiKeys)
        return repository.list()

    def create(self, name=None):
        """Create an API key. Its `key` is only returned this once

        :param str name:
        :rtype: models.ApiKey
        """
        repository = self.build_repository(repositories.CreateApiKey)
        return repository.create(name)

    def archive(self, api_key_id):
        """Disable an API key. This can't be undone

        :param str api_key_id:
        :rtype: models.ApiKey
        """
        repository = self.build_repository(repositories.ArchiveApiKey)
        return repository.archive(api_key_id)
