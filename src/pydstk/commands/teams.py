import abc

import six

from pydstk import api_sdk
from pydstk.api_sdk.config import config, update_config_file
from pydstk.cli_constants import CLI_CLIENT_NAME
from pydstk.commands.common import BaseCommand, ListCommandMixin, display


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
        return self.client.list(**kwargs)

    def _get_table_data(self, objects):
        data = [("ID", "Name", "Archived", "Created Date", "Modified Date")]

        for team in objects:
            marker = " (current)" if team.team_id == config.TEAM_ID else ""
            data.append(
                (
                    team.team_id,
                    display(team.name) + marker,
                    "yes" if team.is_archived else "",
                    team.date_created,
                    team.date_modified,
                )
            )
        return data


class UseTeamCommand(TeamsCommand):
    def execute(self, team_id):
        team = self.client.get(team_id)
        config.TEAM_ID = team.team_id
        update_config_file(teamId=team.team_id)
        self.logger.log("Now using team {} ({}).".format(team.name, team.team_id))


class ListTeamMembersCommand(ListCommandMixin, TeamsCommand):
    def _get_instances(self, **kwargs):
        return self.client.list_members(**kwargs)

    def _get_table_data(self, objects):
        data = [("User ID", "User Name", "Name", "Email", "Role")]

        for member in objects:
            data.append(
                (
                    member.user_id,
                    display(member.user_name),
                    display(member.real_name),
                    display(member.email),
                    display(member.role),
                )
            )
        return data


class CreateTeamCommand(TeamsCommand):
    def execute(self, **kwargs):
        team = self.client.create(**kwargs)
        self.logger.log("Created team {} ({}).".format(team.name, team.team_id))


class EditTeamCommand(TeamsCommand):
    def execute(self, **kwargs):
        team = self.client.edit(**kwargs)
        self.logger.log("Updated team {} ({}).".format(team.name, team.team_id))


class ArchiveTeamCommand(TeamsCommand):
    def execute(self, team_id):
        team = self.client.archive(team_id)
        action = "Archived" if team.is_archived else "Restored"
        self.logger.log("{} team {} ({}).".format(action, team.name, team.team_id))
