from gql import gql

from pydstk.api_sdk import serializers
from pydstk.api_sdk.repositories.common import BaseRepository

API_KEY_FIELDS = """
    apiKeyId
    name
    start
    isArchived
    dateCreated
"""

LIST_API_KEYS = gql(
    """
    query ListApiKeys {
        apiKey {
            list {
                %s
            }
        }
    }
    """
    % API_KEY_FIELDS
)

CREATE_API_KEY = gql(
    """
    mutation CreateApiKey($name: String) {
        apiKey {
            create(name: $name) {
                key
                apiKey {
                    %s
                }
            }
        }
    }
    """
    % API_KEY_FIELDS
)

ARCHIVE_API_KEY = gql(
    """
    mutation ArchiveApiKey($apiKeyId: String!) {
        apiKey {
            archive(apiKeyId: $apiKeyId) {
                %s
            }
        }
    }
    """
    % API_KEY_FIELDS
)


class ListApiKeys(BaseRepository):
    SERIALIZER_CLS = serializers.ApiKey

    def list(self):
        result = self._execute(LIST_API_KEYS)
        return [
            self._parse_object(api_key_dict)
            for api_key_dict in result["apiKey"]["list"] or []
        ]


class CreateApiKey(BaseRepository):
    SERIALIZER_CLS = serializers.ApiKey

    def create(self, name=None):
        result = self._execute(CREATE_API_KEY, {"name": name})
        created = result["apiKey"]["create"]
        api_key = self._parse_object(created["apiKey"])
        api_key.key = created["key"]
        return api_key


class ArchiveApiKey(BaseRepository):
    SERIALIZER_CLS = serializers.ApiKey

    def archive(self, api_key_id):
        result = self._execute(ARCHIVE_API_KEY, {"apiKeyId": api_key_id})
        return self._parse_object(result["apiKey"]["archive"])
