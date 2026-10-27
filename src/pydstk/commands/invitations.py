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
class InvitationsCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.InvitationsClient(
            api_key=api_key,
            logger=logger,
            client_name=CLI_CLIENT_NAME,
        )
        return client


class ListInvitationsCommand(ListCommandMixin, InvitationsCommand):
    def _get_instances(self, **kwargs):
        return self.client.list(**kwargs)

    def _get_table_data(self, objects):
        data = [("ID", "Team", "Email", "Role", "Status", "Invited By", "Expires")]

        for invitation in objects:
            data.append(
                (
                    invitation.invitation_id,
                    display(invitation.team_name),
                    display(invitation.email),
                    display(invitation.role),
                    display(invitation.status),
                    display(invitation.inviter),
                    display(invitation.expires_at),
                )
            )
        return data


class GetInvitationCommand(DetailCommandMixin, InvitationsCommand):
    def _get_instance(self, **kwargs):
        return self.client.get(**kwargs)

    def _get_table_data(self, instance):
        return [
            ("ID", instance.invitation_id),
            ("Team", "{} ({})".format(instance.team_name, instance.team_id)),
            ("Email", display(instance.email)),
            ("Role", display(instance.role)),
            ("Status", display(instance.status)),
            ("Invited By", display(instance.inviter)),
            ("Expires", display(instance.expires_at)),
            ("Created Date", instance.date_created),
        ]


class CreateInvitationCommand(InvitationsCommand):
    def execute(self, **kwargs):
        invitation = self.client.create(**kwargs)
        self.logger.log(
            "Invited {} to {} as a {} ({}).".format(
                invitation.email,
                invitation.team_name,
                invitation.role,
                invitation.invitation_id,
            )
        )


class AcceptInvitationCommand(InvitationsCommand):
    def execute(self, invitation_id):
        invitation = self.client.accept(invitation_id)
        self.logger.log("You joined {}.".format(invitation.team_name))


class RejectInvitationCommand(InvitationsCommand):
    def execute(self, invitation_id):
        invitation = self.client.reject(invitation_id)
        self.logger.log("Declined the invitation to {}.".format(invitation.team_name))


class CancelInvitationCommand(InvitationsCommand):
    def execute(self, **kwargs):
        invitation = self.client.cancel(**kwargs)
        self.logger.log(
            "Canceled the invitation for {} ({}).".format(
                invitation.email, invitation.invitation_id
            )
        )
