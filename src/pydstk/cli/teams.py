import click

from pydstk.cli.cli import cli
from pydstk.cli.common import ClickGroup, api_key_option
from pydstk.commands.teams import ListTeamsCommand


@cli.group("teams", help="Manage teams", cls=ClickGroup)
def teams():
    pass


@teams.command("list", help="List your teams")
@api_key_option
def get_teams_list(api_key):
    command = ListTeamsCommand(api_key=api_key)

    res = command.execute()

    for team_str, next_iteration in res:
        click.echo(team_str)
        if next_iteration:
            click.confirm("Do you want to continue?", abort=True)
