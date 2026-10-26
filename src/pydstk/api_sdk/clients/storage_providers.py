from pydstk.api_sdk import repositories
from pydstk.api_sdk.clients.base_client import BaseClient


class StorageProvidersClient(BaseClient):
    entity = "storageProvider"

    def list(self, team_id, include_archived=False, bucket=None):
        """Get list of storage providers in a team

        :param str team_id:
        :param bool include_archived:
        :param str bucket: only providers whose bucket name contains this text
        :rtype: list[models.StorageProvider]
        """
        repository = self.build_repository(repositories.ListStorageProviders)
        return repository.list(
            team_id, include_archived=include_archived, bucket=bucket
        )

    def get(self, provider_id):
        """
        :param str provider_id:
        :rtype: models.StorageProvider
        """
        repository = self.build_repository(repositories.GetStorageProvider)
        return repository.get(provider_id)

    def create(
        self, team_id, bucket, endpoint_url, region, access_key_id, secret_access_key
    ):
        """Connect an S3-compatible bucket

        :param str team_id:
        :param str bucket:
        :param str endpoint_url:
        :param str region:
        :param str access_key_id:
        :param str secret_access_key:
        :rtype: models.StorageProvider
        """
        repository = self.build_repository(repositories.CreateStorageProvider)
        return repository.create(
            team_id, bucket, endpoint_url, region, access_key_id, secret_access_key
        )

    def edit(self, provider_id, access_key_id, secret_access_key):
        """Replace a storage provider's credentials

        :param str provider_id:
        :param str access_key_id:
        :param str secret_access_key:
        :rtype: models.StorageProvider
        """
        repository = self.build_repository(repositories.EditStorageProvider)
        return repository.edit(provider_id, access_key_id, secret_access_key)

    def archive(self, provider_id):
        """Archive a storage provider, or restore it if it is already archived

        :param str provider_id:
        :rtype: models.StorageProvider
        """
        repository = self.build_repository(repositories.ArchiveStorageProvider)
        return repository.archive(provider_id)
