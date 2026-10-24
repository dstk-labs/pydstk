import click

from pydstk.cli.cli import cli
from pydstk.cli.common import ClickGroup, api_key_option
from pydstk.commands.teams import ListTeamsCommand, UseTeamCommand


@cli.group("teams", help="Manage teams", cls=ClickGroup)
def teams():
    pass


@teams.command("list", help="List your teams")
@click.option("--include-archived", is_flag=True, help="Include archived teams")
@api_key_option
def get_teams_list(include_archived, api_key):
    command = ListTeamsCommand(api_key=api_key)
    command.execute(include_archived=include_archived)


@teams.command("use", help="Save a default team for other commands")
@click.argument("team_id")
@api_key_option
def use_team(team_id, api_key):
    command = UseTeamCommand(api_key=api_key)
    command.execute(team_id)
