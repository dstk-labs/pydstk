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
        for team_dict in data["listTeams"]:
            team = self._parse_object(team_dict)
            teams.append(team)

        return teams

    def list(self, api_key=None):
        client = graphql_client(api_key)
        query = gql(
            """
            query ListTeams {
                listTeams {
                    teamId
                    name
                    dateModified
                    dateCreated
                }
            }
            """
        )
        resp = client.execute(query)["data"]
        return self._parse_objects(resp)
