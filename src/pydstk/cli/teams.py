import click

from pydstk.cli.cli import cli
from pydstk.cli.common import ClickGroup, api_key_option, team_option
from pydstk.commands import teams as teams_commands


@cli.group("teams", help="Manage teams", cls=ClickGroup)
def teams():
    pass


@teams.command("list", help="List your teams")
@click.option("--include-archived", is_flag=True, help="Include archived teams")
@api_key_option
def get_teams_list(include_archived, api_key):
    command = teams_commands.ListTeamsCommand(api_key=api_key)
    command.execute(include_archived=include_archived)


@teams.command("use", help="Save a default team for other commands")
@click.argument("team_id")
@api_key_option
def use_team(team_id, api_key):
    command = teams_commands.UseTeamCommand(api_key=api_key)
    command.execute(team_id)


@teams.command("members", help="List a team's members")
@team_option
@api_key_option
def list_team_members(team_id, api_key):
    command = teams_commands.ListTeamMembersCommand(api_key=api_key)
    command.execute(team_id=team_id)


@teams.command("create", help="Create a team")
@click.option("--name", required=True, help="Team name")
@click.option("--description", default="", help="Team description")
@api_key_option
def create_team(name, description, api_key):
    command = teams_commands.CreateTeamCommand(api_key=api_key)
    command.execute(name=name, description=description)


@teams.command("edit", help="Change a team's name or description")
@click.argument("team_id")
@click.option("--name", help="New name")
@click.option("--description", help="New description")
@api_key_option
def edit_team(team_id, name, description, api_key):
    if name is None and description is None:
        raise click.UsageError("Pass --name or --description to change something.")

    command = teams_commands.EditTeamCommand(api_key=api_key)
    command.execute(team_id=team_id, name=name, description=description)


@teams.command(
    "archive", help="Archive a team, or restore it if it is already archived"
)
@click.argument("team_id")
@api_key_option
def archive_team(team_id, api_key):
    command = teams_commands.ArchiveTeamCommand(api_key=api_key)
    command.execute(team_id)
