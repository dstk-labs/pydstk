from gql import gql

from pydstk.api_sdk import serializers
from pydstk.api_sdk.exceptions import ResourceFetchingError
from pydstk.api_sdk.repositories.common import ListResources

TEAM_FIELDS = """
    teamId
    name
    description
    isArchived
    dateCreated
    dateModified
"""

LIST_TEAMS = gql(
    """
    query ListTeams($after: String, $teamId: String, $includeArchived: Boolean!) {
        team {
            list(after: $after, teamId: $teamId, includeArchived: $includeArchived) {
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
    % TEAM_FIELDS
)


class ListTeams(ListResources):
    SERIALIZER_CLS = serializers.Team

    def list(self, include_archived=False):
        team_dicts = self._fetch_all(
            LIST_TEAMS, ("team", "list"), {"includeArchived": include_archived}
        )
        return self._parse_objects(team_dicts)


class GetTeam(ListResources):
    SERIALIZER_CLS = serializers.Team

    def get(self, team_id):
        team_dicts = self._fetch_all(
            LIST_TEAMS,
            ("team", "list"),
            {"teamId": team_id, "includeArchived": True},
        )
        if not team_dicts:
            raise ResourceFetchingError(
                "Team {} doesn't exist or you aren't a member of it".format(team_id)
            )

        return self._parse_object(team_dicts[0])
