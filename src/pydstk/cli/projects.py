import click

from pydstk.cli.cli import cli
from pydstk.cli.common import ClickGroup, api_key_option, team_option
from pydstk.commands import projects


@cli.group("projects", help="Manage projects", cls=ClickGroup)
def projects_group():
    pass


@projects_group.command("list", help="List projects in a team")
@team_option
@click.option("--name", help="Only show projects whose name contains this text")
@click.option("--include-archived", is_flag=True, help="Include archived projects")
@api_key_option
def list_projects(team_id, name, include_archived, api_key):
    command = projects.ListProjectsCommand(api_key=api_key)
    command.execute(team_id=team_id, name=name, include_archived=include_archived)


@projects_group.command("get", help="Show a project")
@click.argument("project_id")
@api_key_option
def get_project(project_id, api_key):
    command = projects.GetProjectCommand(api_key=api_key)
    command.execute(project_id=project_id)


@projects_group.command("create", help="Create a project")
@team_option
@click.option("--name", required=True, help="Project name")
@click.option("--description", default="", help="Project description")
@api_key_option
def create_project(team_id, name, description, api_key):
    command = projects.CreateProjectCommand(api_key=api_key)
    command.execute(team_id=team_id, name=name, description=description)


@projects_group.command("edit", help="Change a project's name or description")
@click.argument("project_id")
@click.option("--name", help="New name")
@click.option("--description", help="New description")
@api_key_option
def edit_project(project_id, name, description, api_key):
    if name is None and description is None:
        raise click.UsageError("Pass --name or --description to change something.")

    command = projects.EditProjectCommand(api_key=api_key)
    command.execute(project_id=project_id, name=name, description=description)


@projects_group.command(
    "archive", help="Archive a project, or restore it if it is already archived"
)
@click.argument("project_id")
@api_key_option
def archive_project(project_id, api_key):
    command = projects.ArchiveProjectCommand(api_key=api_key)
    command.execute(project_id)
