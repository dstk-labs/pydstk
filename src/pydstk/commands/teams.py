import abc

import six

from pydstk import exceptions, api_sdk
from pydstk.api_sdk import sdk_exceptions
from pydstk.cli_constants import CLI_CLIENT_NAME
from pydstk.commands.common import ListCommandMixin, BaseCommand


@six.add_metaclass(abc.ABCMeta)
class TeamsCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.TeamsClient(
            api_key=api_key,
            logger=logger,
            client_name=CLI_CLIENT_NAME,
        )
        return client


class ListTeamsCommand(ListCommandMixin, TeamsCommand):
    def _get_instances(self, **kwargs):
        try:
            instances = self.client.list(**kwargs)
        except sdk_exceptions.PydstkSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    def _get_table_data(self, objects):
        data = [("ID", "Name", "Created Date", "Modified Date")]

        for team in objects:
            handle = team.team_id
            name = team.name
            created_date = team.date_created
            modified_date = team.date_modified
            data.append((handle, name, created_date, modified_date))
        return data
