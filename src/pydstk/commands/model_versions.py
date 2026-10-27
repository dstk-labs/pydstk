import abc

import click
import six

from pydstk import api_sdk
from pydstk.cli_constants import CLI_CLIENT_NAME
from pydstk.commands.common import (
    BaseCommand,
    DetailCommandMixin,
    ListCommandMixin,
    display,
)

SIZE_UNITS = ("B", "KB", "MB", "GB", "TB")


def format_size(size):
    size = float(size or 0)
    if size < 1024:
        return "{:.0f} B".format(size)

    for unit in SIZE_UNITS[1:]:
        size /= 1024
        if size < 1024 or unit == SIZE_UNITS[-1]:
            return "{:.1f} {}".format(size, unit)


def _status(version):
    if version.is_archived:
        return "archived"
    return "published" if version.is_published else "draft"


@six.add_metaclass(abc.ABCMeta)
class ModelVersionsCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ModelVersionsClient(
            api_key=api_key,
            logger=logger,
            client_name=CLI_CLIENT_NAME,
        )
        return client


class ListModelVersionsCommand(ListCommandMixin, ModelVersionsCommand):
    def _get_instances(self, **kwargs):
        return self.client.list(**kwargs)

    def _get_table_data(self, objects):
        data = [
            ("ID", "Version", "Status", "Description", "Created By", "Created Date")
        ]

        for version in objects:
            data.append(
                (
                    version.model_version_id,
                    "v{}".format(version.numeric_version),
                    _status(version),
                    display(version.description),
                    display(version.created_by),
                    version.date_created,
                )
            )
        return data


class GetModelVersionCommand(DetailCommandMixin, ModelVersionsCommand):
    def _get_instance(self, **kwargs):
        return self.client.get(**kwargs)

    def _get_table_data(self, instance):
        return [
            ("ID", instance.model_version_id),
            ("Version", "v{}".format(instance.numeric_version)),
            ("Model", "{} ({})".format(instance.model_name, instance.model_id)),
            ("Status", _status(instance)),
            ("Description", display(instance.description)),
            ("Storage Prefix", instance.s3_prefix),
            ("Created By", display(instance.created_by)),
            ("Created Date", instance.date_created),
        ]


class ListModelVersionFilesCommand(ListCommandMixin, ModelVersionsCommand):
    def _get_instances(self, **kwargs):
        return self.client.list_files(**kwargs)

    def _get_table_data(self, objects):
        data = [("Name", "Size", "Last Modified")]

        for version_file in objects:
            data.append(
                (
                    version_file.name,
                    format_size(version_file.size),
                    display(version_file.last_modified),
                )
            )
        return data


class CreateModelVersionCommand(ModelVersionsCommand):
    def execute(self, **kwargs):
        version = self.client.create(**kwargs)
        self.logger.log(
            "Created v{} of {} ({}).".format(
                version.numeric_version, version.model_name, version.model_version_id
            )
        )


class EditModelVersionCommand(ModelVersionsCommand):
    def execute(self, **kwargs):
        version = self.client.edit(**kwargs)
        self.logger.log(
            "Updated v{} of {} ({}).".format(
                version.numeric_version, version.model_name, version.model_version_id
            )
        )


class PublishModelVersionCommand(ModelVersionsCommand):
    def execute(self, model_version_id):
        version = self.client.publish(model_version_id)
        self.logger.log(
            "Published v{} of {} ({}).".format(
                version.numeric_version, version.model_name, version.model_version_id
            )
        )


class ArchiveModelVersionCommand(ModelVersionsCommand):
    def execute(self, model_version_id):
        version = self.client.archive(model_version_id)
        action = "Archived" if version.is_archived else "Restored"
        self.logger.log(
            "{} v{} of {} ({}).".format(
                action,
                version.numeric_version,
                version.model_name,
                version.model_version_id,
            )
        )


class UploadModelVersionCommand(ModelVersionsCommand):
    def execute(self, model_version_id, paths):
        total_size = self.client.upload_size(paths)

        with click.progressbar(
            length=total_size, label="Uploading", show_percent=True
        ) as bar:
            keys = self.client.upload(
                model_version_id,
                paths,
                on_file=lambda filename, size: setattr(bar, "label", filename),
                on_progress=bar.update,
            )

        self.logger.log(
            "Uploaded {} {} ({}) to {}.".format(
                len(keys),
                "file" if len(keys) == 1 else "files",
                format_size(total_size),
                model_version_id,
            )
        )
