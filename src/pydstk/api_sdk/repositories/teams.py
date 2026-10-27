from gql import gql

from pydstk.api_sdk import serializers
from pydstk.api_sdk.exceptions import ResourceFetchingError
from pydstk.api_sdk.repositories.common import BaseRepository, ListResources

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


LIST_TEAM_MEMBERS = gql(
    """
    query ListTeamMembers($teamId: String!) {
        team {
            listMembers(teamId: $teamId) {
                memberId
                role
                dateCreated
                user {
                    userId
                    userName
                    realName
                    email
                }
            }
        }
    }
    """
)

CREATE_TEAM = gql(
    """
    mutation CreateTeam($data: TeamInput!) {
        team {
            create(data: $data) {
                %s
            }
        }
    }
    """
    % TEAM_FIELDS
)

EDIT_TEAM = gql(
    """
    mutation EditTeam($data: EditTeamInput!) {
        team {
            edit(data: $data) {
                %s
            }
        }
    }
    """
    % TEAM_FIELDS
)

ARCHIVE_TEAM = gql(
    """
    mutation ArchiveTeam($teamId: String!) {
        team {
            archive(teamId: $teamId) {
                %s
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


class ListTeamMembers(BaseRepository):
    SERIALIZER_CLS = serializers.TeamMember

    def list(self, team_id):
        result = self._execute(LIST_TEAM_MEMBERS, {"teamId": team_id})
        return [
            self._parse_object(member_dict)
            for member_dict in result["team"]["listMembers"] or []
        ]


class CreateTeam(BaseRepository):
    SERIALIZER_CLS = serializers.Team

    def create(self, name, description):
        data = {"name": name, "description": description}
        result = self._execute(CREATE_TEAM, {"data": data})
        return self._parse_object(result["team"]["create"])


class EditTeam(BaseRepository):
    SERIALIZER_CLS = serializers.Team

    def edit(self, team_id, name, description):
        data = {"teamId": team_id, "name": name, "description": description}
        result = self._execute(EDIT_TEAM, {"data": data})
        return self._parse_object(result["team"]["edit"])


class ArchiveTeam(BaseRepository):
    SERIALIZER_CLS = serializers.Team

    def archive(self, team_id):
        result = self._execute(ARCHIVE_TEAM, {"teamId": team_id})
        return self._parse_object(result["team"]["archive"])
