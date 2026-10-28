import click

from pydstk.cli.cli import cli
from pydstk.cli.common import ClickGroup, api_key_option
from pydstk.commands import users


@cli.command("whoami", help="Show which account you're signed in as")
@api_key_option
def whoami(api_key):
    command = users.WhoAmICommand(api_key=api_key)
    command.execute()


@cli.command("reset-password", help="Email yourself a password reset link")
@click.argument("email")
def reset_password(email):
    command = users.RequestPasswordResetCommand(api_key=None)
    command.execute(email)


@cli.group("users", help="Find users", cls=ClickGroup)
def users_group():
    pass


@users_group.command("list", help="List users who share a team with you")
@click.option(
    "--name", "user_name", help="Only users whose user name contains this text"
)
@api_key_option
def list_users(user_name, api_key):
    command = users.ListUsersCommand(api_key=api_key)
    command.execute(user_name=user_name)
