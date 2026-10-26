import abc

import six

from pydstk import api_sdk
from pydstk.cli_constants import CLI_CLIENT_NAME
from pydstk.commands.common import (
    BaseCommand,
    DetailCommandMixin,
    ListCommandMixin,
    display,
)


@six.add_metaclass(abc.ABCMeta)
class StorageProvidersCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.StorageProvidersClient(
            api_key=api_key,
            logger=logger,
            client_name=CLI_CLIENT_NAME,
        )
        return client


class ListStorageProvidersCommand(ListCommandMixin, StorageProvidersCommand):
    def _get_instances(self, **kwargs):
        return self.client.list(**kwargs)

    def _get_table_data(self, objects):
        data = [("ID", "Bucket", "Region", "Endpoint", "Archived")]

        for provider in objects:
            data.append(
                (
                    provider.provider_id,
                    provider.bucket,
                    display(provider.region),
                    provider.endpoint_url,
                    "yes" if provider.is_archived else "",
                )
            )
        return data


class GetStorageProviderCommand(DetailCommandMixin, StorageProvidersCommand):
    def _get_instance(self, **kwargs):
        return self.client.get(**kwargs)

    def _get_table_data(self, instance):
        return [
            ("ID", instance.provider_id),
            ("Bucket", instance.bucket),
            ("Endpoint", instance.endpoint_url),
            ("Region", display(instance.region)),
            ("Access Key ID", instance.access_key_id),
            ("Archived", "yes" if instance.is_archived else "no"),
            ("Created By", display(instance.created_by)),
            ("Created Date", instance.date_created),
            ("Modified Date", instance.date_modified),
        ]


class CreateStorageProviderCommand(StorageProvidersCommand):
    def execute(self, **kwargs):
        provider = self.client.create(**kwargs)
        self.logger.log(
            "Added storage provider {} ({}).".format(
                provider.bucket, provider.provider_id
            )
        )


class EditStorageProviderCommand(StorageProvidersCommand):
    def execute(self, **kwargs):
        provider = self.client.edit(**kwargs)
        self.logger.log(
            "Updated credentials for {} ({}).".format(
                provider.bucket, provider.provider_id
            )
        )


class ArchiveStorageProviderCommand(StorageProvidersCommand):
    def execute(self, provider_id):
        provider = self.client.archive(provider_id)
        action = "Archived" if provider.is_archived else "Restored"
        self.logger.log(
            "{} storage provider {} ({}).".format(
                action, provider.bucket, provider.provider_id
            )
        )
