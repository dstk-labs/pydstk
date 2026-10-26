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
class ProjectsCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ProjectsClient(
            api_key=api_key,
            logger=logger,
            client_name=CLI_CLIENT_NAME,
        )
        return client


class ListProjectsCommand(ListCommandMixin, ProjectsCommand):
    def _get_instances(self, **kwargs):
        return self.client.list(**kwargs)

    def _get_table_data(self, objects):
        data = [("ID", "Name", "Archived", "Created By", "Modified Date")]

        for project in objects:
            data.append(
                (
                    project.project_id,
                    project.name,
                    "yes" if project.is_archived else "",
                    display(project.created_by),
                    project.date_modified,
                )
            )
        return data


class GetProjectCommand(DetailCommandMixin, ProjectsCommand):
    def _get_instance(self, **kwargs):
        return self.client.get(**kwargs)

    def _get_table_data(self, instance):
        return [
            ("ID", instance.project_id),
            ("Name", instance.name),
            ("Description", display(instance.description)),
            ("Archived", "yes" if instance.is_archived else "no"),
            ("Created By", display(instance.created_by)),
            ("Created Date", instance.date_created),
            ("Modified Date", instance.date_modified),
        ]


class CreateProjectCommand(ProjectsCommand):
    def execute(self, **kwargs):
        project = self.client.create(**kwargs)
        self.logger.log(
            "Created project {} ({}).".format(project.name, project.project_id)
        )


class EditProjectCommand(ProjectsCommand):
    def execute(self, **kwargs):
        project = self.client.edit(**kwargs)
        self.logger.log(
            "Updated project {} ({}).".format(project.name, project.project_id)
        )


class ArchiveProjectCommand(ProjectsCommand):
    def execute(self, project_id):
        project = self.client.archive(project_id)
        action = "Archived" if project.is_archived else "Restored"
        self.logger.log(
            "{} project {} ({}).".format(action, project.name, project.project_id)
        )
