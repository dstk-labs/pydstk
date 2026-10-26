from gql import gql

from pydstk.api_sdk import serializers
from pydstk.api_sdk.repositories.common import BaseRepository, ListResources

STORAGE_PROVIDER_FIELDS = """
    providerId
    bucket
    endpointUrl
    region
    accessKeyId
    isArchived
    createdBy {
        realName
    }
    dateCreated
    dateModified
"""

LIST_STORAGE_PROVIDERS = gql(
    """
    query ListStorageProviders(
        $after: String
        $teamId: String!
        $includeArchived: Boolean!
        $bucket: String
    ) {
        storageProvider {
            list(
                after: $after
                teamId: $teamId
                includeArchived: $includeArchived
                bucket: $bucket
            ) {
                pageInfo {
                    continuationToken
                    hasNextPage
                }
                edges {
                    node {
                        %s
                    }
                }
            }
        }
    }
    """
    % STORAGE_PROVIDER_FIELDS
)

GET_STORAGE_PROVIDER = gql(
    """
    query GetStorageProvider($storageProviderId: String!) {
        storageProvider {
            get(storageProviderId: $storageProviderId) {
                %s
            }
        }
    }
    """
    % STORAGE_PROVIDER_FIELDS
)

CREATE_STORAGE_PROVIDER = gql(
    """
    mutation CreateStorageProvider($data: StorageProviderInput!) {
        storageProvider {
            create(data: $data) {
                %s
            }
        }
    }
    """
    % STORAGE_PROVIDER_FIELDS
)

EDIT_STORAGE_PROVIDER = gql(
    """
    mutation EditStorageProvider($data: EditStorageProviderInput!) {
        storageProvider {
            edit(data: $data) {
                %s
            }
        }
    }
    """
    % STORAGE_PROVIDER_FIELDS
)

ARCHIVE_STORAGE_PROVIDER = gql(
    """
    mutation ArchiveStorageProvider($providerId: String!) {
        storageProvider {
            archive(providerId: $providerId) {
                %s
            }
        }
    }
    """
    % STORAGE_PROVIDER_FIELDS
)


class ListStorageProviders(ListResources):
    SERIALIZER_CLS = serializers.StorageProvider

    def list(self, team_id, include_archived=False, bucket=None):
        provider_dicts = self._fetch_all(
            LIST_STORAGE_PROVIDERS,
            ("storageProvider", "list"),
            {"teamId": team_id, "includeArchived": include_archived, "bucket": bucket},
        )
        return self._parse_objects(provider_dicts)


class GetStorageProvider(BaseRepository):
    SERIALIZER_CLS = serializers.StorageProvider

    def get(self, provider_id):
        result = self._execute(GET_STORAGE_PROVIDER, {"storageProviderId": provider_id})
        return self._parse_object(result["storageProvider"]["get"])


class CreateStorageProvider(BaseRepository):
    SERIALIZER_CLS = serializers.StorageProvider

    def create(
        self, team_id, bucket, endpoint_url, region, access_key_id, secret_access_key
    ):
        data = {
            "teamId": team_id,
            "bucket": bucket,
            "endpointUrl": endpoint_url,
            "region": region,
            "accessKeyId": access_key_id,
            "secretAccessKey": secret_access_key,
        }
        result = self._execute(CREATE_STORAGE_PROVIDER, {"data": data})
        return self._parse_object(result["storageProvider"]["create"])


class EditStorageProvider(BaseRepository):
    SERIALIZER_CLS = serializers.StorageProvider

    def edit(self, provider_id, access_key_id, secret_access_key):
        data = {
            "providerId": provider_id,
            "accessKeyId": access_key_id,
            "secretAccessKey": secret_access_key,
        }
        result = self._execute(EDIT_STORAGE_PROVIDER, {"data": data})
        return self._parse_object(result["storageProvider"]["edit"])


class ArchiveStorageProvider(BaseRepository):
    SERIALIZER_CLS = serializers.StorageProvider

    def archive(self, provider_id):
        result = self._execute(ARCHIVE_STORAGE_PROVIDER, {"providerId": provider_id})
        return self._parse_object(result["storageProvider"]["archive"])
