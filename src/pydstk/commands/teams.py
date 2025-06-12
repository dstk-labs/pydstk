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
    def execute(self, **kwargs):
        return self._generate_data_table(**kwargs)

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
            created_date = team.created_date
            modified_date = team.modified_date
            data.append((handle, name, created_date, modified_date))
        return data

    def _generate_data_table(self, **kwargs):
        limit = kwargs.get("limit")
        offset = kwargs.get("offset")
        next_iteration = True

        while next_iteration:
            kwargs["offset"] = offset
            instances = self._get_instances(**kwargs)
            if instances:
                table_data = self._get_table_data(instances)
                table_str = self._make_list_table(table_data) + "\n"
            else:
                table_str = "No data found"

            if len(instances) < limit:
                next_iteration = False

            yield table_str, next_iteration
            offset += limit
