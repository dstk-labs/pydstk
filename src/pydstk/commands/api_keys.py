import abc

import six

from pydstk import api_sdk
from pydstk.cli_constants import CLI_CLIENT_NAME
from pydstk.commands.common import BaseCommand, ListCommandMixin, display


@six.add_metaclass(abc.ABCMeta)
class ApiKeysCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ApiKeysClient(
            api_key=api_key,
            logger=logger,
            client_name=CLI_CLIENT_NAME,
        )
        return client


class ListApiKeysCommand(ListCommandMixin, ApiKeysCommand):
    def _get_instances(self, **kwargs):
        return self.client.list()

    def _get_table_data(self, objects):
        data = [("ID", "Name", "Starts With", "Created Date")]

        for api_key in objects:
            data.append(
                (
                    api_key.api_key_id,
                    display(api_key.name),
                    display(api_key.start),
                    api_key.date_created,
                )
            )
        return data


class CreateApiKeyCommand(ApiKeysCommand):
    def execute(self, name):
        api_key = self.client.create(name)
        self.logger.log(
            "Created API key {} ({}).".format(api_key.name, api_key.api_key_id)
        )
        self.logger.log(api_key.key)
        self.logger.warning("Copy this key now. You won't be able to see it again.")


class ArchiveApiKeyCommand(ApiKeysCommand):
    def execute(self, api_key_id):
        api_key = self.client.archive(api_key_id)
        self.logger.log(
            "Disabled API key {} ({}).".format(api_key.name, api_key.api_key_id)
        )
