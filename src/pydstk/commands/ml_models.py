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


def _version_label(version):
    return "" if version is None else "v{}".format(version)


@six.add_metaclass(abc.ABCMeta)
class ModelsCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ModelsClient(
            api_key=api_key,
            logger=logger,
            client_name=CLI_CLIENT_NAME,
        )
        return client


class ListModelsCommand(ListCommandMixin, ModelsCommand):
    def _get_instances(self, **kwargs):
        return self.client.list(**kwargs)

    def _get_table_data(self, objects):
        data = [("ID", "Name", "Project", "Latest", "Archived", "Modified Date")]

        for model in objects:
            data.append(
                (
                    model.model_id,
                    model.name,
                    display(model.project_name),
                    _version_label(model.current_version),
                    "yes" if model.is_archived else "",
                    model.date_modified,
                )
            )
        return data


class GetModelCommand(DetailCommandMixin, ModelsCommand):
    def _get_instance(self, **kwargs):
        return self.client.get(**kwargs)

    def _get_table_data(self, instance):
        return [
            ("ID", instance.model_id),
            ("Name", instance.name),
            ("Description", display(instance.description)),
            ("Project", "{} ({})".format(instance.project_name, instance.project_id)),
            (
                "Storage",
                "{} ({})".format(instance.bucket, instance.storage_provider_id),
            ),
            ("Latest Version", _version_label(instance.current_version) or "none"),
            ("Archived", "yes" if instance.is_archived else "no"),
            ("Created By", display(instance.created_by)),
            ("Created Date", instance.date_created),
            ("Modified Date", instance.date_modified),
        ]


class CreateModelCommand(ModelsCommand):
    def execute(self, **kwargs):
        model = self.client.create(**kwargs)
        self.logger.log("Created model {} ({}).".format(model.name, model.model_id))


class EditModelCommand(ModelsCommand):
    def execute(self, **kwargs):
        model = self.client.edit(**kwargs)
        self.logger.log("Updated model {} ({}).".format(model.name, model.model_id))


class ArchiveModelCommand(ModelsCommand):
    def execute(self, model_id):
        model = self.client.archive(model_id)
        action = "Archived" if model.is_archived else "Restored"
        self.logger.log("{} model {} ({}).".format(action, model.name, model.model_id))
