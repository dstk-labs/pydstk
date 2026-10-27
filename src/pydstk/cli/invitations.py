import click

from pydstk.cli.cli import cli
from pydstk.cli.common import ClickGroup, api_key_option, team_option
from pydstk.commands import invitations

STATUSES = ("pending", "accepted", "rejected", "canceled")
ROLES = ("owner", "member", "viewer")


@cli.group("invitations", help="Manage team invitations", cls=ClickGroup)
def invitations_group():
    pass


@invitations_group.command(
    "list", help="List invitations sent to you, or a team's with --team"
)
@click.option("--team", "team_id", help="List the invitations this team sent")
@click.option("--status", type=click.Choice(STATUSES), help="Only this status")
@api_key_option
def list_invitations(team_id, status, api_key):
    command = invitations.ListInvitationsCommand(api_key=api_key)
    command.execute(team_id=team_id, status=status)


@invitations_group.command("get", help="Show an invitation sent to you")
@click.argument("invitation_id")
@api_key_option
def get_invitation(invitation_id, api_key):
    command = invitations.GetInvitationCommand(api_key=api_key)
    command.execute(invitation_id=invitation_id)


@invitations_group.command("create", help="Invite a user to a team")
@team_option
@click.option("--user", "user_id", required=True, help="User ID to invite")
@click.option("--role", type=click.Choice(ROLES), default="member", show_default=True)
@api_key_option
def create_invitation(team_id, user_id, role, api_key):
    command = invitations.CreateInvitationCommand(api_key=api_key)
    command.execute(team_id=team_id, user_id=user_id, role=role)


@invitations_group.command("accept", help="Accept an invitation and join the team")
@click.argument("invitation_id")
@api_key_option
def accept_invitation(invitation_id, api_key):
    command = invitations.AcceptInvitationCommand(api_key=api_key)
    command.execute(invitation_id)


@invitations_group.command("reject", help="Decline an invitation")
@click.argument("invitation_id")
@api_key_option
def reject_invitation(invitation_id, api_key):
    command = invitations.RejectInvitationCommand(api_key=api_key)
    command.execute(invitation_id)


@invitations_group.command("cancel", help="Cancel an invitation your team sent")
@click.argument("invitation_id")
@team_option
@api_key_option
def cancel_invitation(invitation_id, team_id, api_key):
    command = invitations.CancelInvitationCommand(api_key=api_key)
    command.execute(invitation_id=invitation_id, team_id=team_id)
