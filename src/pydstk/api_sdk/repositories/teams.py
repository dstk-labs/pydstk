from gql import gql
from pydstk.api_sdk.config import config
from pydstk.api_sdk.graphql import graphql_client
from pydstk.api_sdk import serializers
from pydstk.api_sdk.repositories.common import ListResources


class ParseTeamDictMixin(object):
    def _parse_object(self, model_dict, **kwargs):
        """
        :param dict model_dict:
        :rtype Team
        """
        model = serializers.Team().get_instance(model_dict)
        return model


class GetBaseTeamsApiUrlMixin(object):
    def _get_api_url(self, **_):
        return config.CONFIG_HOST


class ListTeams(GetBaseTeamsApiUrlMixin, ParseTeamDictMixin, ListResources):
    def _parse_objects(self, data, **kwargs):
        teams = []
        for team_dict in data:
            team = self._parse_object(team_dict)
            teams.append(team)

        return teams

    def list(self, api_key=None):
        client = graphql_client(api_key)
        query = gql(
            """
            query ListTeams($after: String) {
                team {
                    list(after: $after) {
                        pageInfo {
                            continuationToken
                            hasNextPage
                        }
                        edges {
                            node {
                                teamId
                                name
                                dateModified
                                dateCreated
                            }
                        }
                    }
                }
            }
            """
        )

        team_dicts = []
        after = None
        while True:
            result = client.execute(query, variable_values={"after": after})
            page = result["team"]["list"]
            team_dicts.extend(edge["node"] for edge in page["edges"] or [])

            if not page["pageInfo"]["hasNextPage"]:
                return self._parse_objects(team_dicts)

            after = page["pageInfo"]["continuationToken"]
