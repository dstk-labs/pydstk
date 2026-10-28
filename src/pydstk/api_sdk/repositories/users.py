from gql import gql

from pydstk.api_sdk import serializers
from pydstk.api_sdk.repositories.common import BaseRepository, ListResources

USER_FIELDS = """
    userId
    userName
    realName
    email
    isEmailVerified
    isTwoFactorEnabled
    dateCreated
"""

GET_CURRENT_USER = gql(
    """
    query GetUser {
        user {
            get {
                %s
            }
        }
    }
    """
    % USER_FIELDS
)

LIST_USERS = gql(
    """
    query ListUsers($after: String, $userName: String) {
        user {
            list(after: $after, userName: $userName) {
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
    % USER_FIELDS
)

REQUEST_PASSWORD_RESET = gql(
    """
    mutation RequestPasswordReset($data: RequestPasswordResetInput!) {
        auth {
            requestPasswordReset(data: $data)
        }
    }
    """
)


class GetCurrentUser(BaseRepository):
    SERIALIZER_CLS = serializers.User

    def get(self):
        result = self._execute(GET_CURRENT_USER)
        return self._parse_object(result["user"]["get"])


class ListUsers(ListResources):
    SERIALIZER_CLS = serializers.User

    def list(self, user_name=None):
        user_dicts = self._fetch_all(
            LIST_USERS, ("user", "list"), {"userName": user_name}
        )
        return self._parse_objects(user_dicts)


class RequestPasswordReset(BaseRepository):
    def request(self, email):
        self._execute(
            REQUEST_PASSWORD_RESET, {"data": {"email": email}}, anonymous=True
        )
