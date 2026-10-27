import click

from pydstk.cli.cli import cli
from pydstk.cli.common import ClickGroup, api_key_option, team_option
from pydstk.commands import ml_models


@cli.group("models", help="Manage models", cls=ClickGroup)
def models_group():
    pass


@models_group.command("list", help="List models in a team")
@team_option
@click.option("--project", "project_id", help="Only show models in this project")
@click.option("--name", help="Only show models whose name contains this text")
@click.option("--include-archived", is_flag=True, help="Include archived models")
@api_key_option
def list_models(team_id, project_id, name, include_archived, api_key):
    command = ml_models.ListModelsCommand(api_key=api_key)
    command.execute(
        team_id=team_id,
        project_id=project_id,
        name=name,
        include_archived=include_archived,
    )


@models_group.command("get", help="Show a model")
@click.argument("model_id")
@api_key_option
def get_model(model_id, api_key):
    command = ml_models.GetModelCommand(api_key=api_key)
    command.execute(model_id=model_id)


@models_group.command("create", help="Register a model")
@click.option("--project", "project_id", required=True, help="Project ID")
@click.option(
    "--storage",
    "storage_provider_id",
    required=True,
    help="Storage provider ID where the model's versions are stored",
)
@click.option("--name", required=True, help="Model name")
@click.option("--description", default="", help="Model description")
@api_key_option
def create_model(project_id, storage_provider_id, name, description, api_key):
    command = ml_models.CreateModelCommand(api_key=api_key)
    command.execute(
        project_id=project_id,
        storage_provider_id=storage_provider_id,
        name=name,
        description=description,
    )


@models_group.command("edit", help="Change a model")
@click.argument("model_id")
@click.option("--project", "project_id", help="Move the model to this project")
@click.option(
    "--storage", "storage_provider_id", help="Store new versions in this provider"
)
@click.option("--name", help="New name")
@click.option("--description", help="New description")
@api_key_option
def edit_model(model_id, project_id, storage_provider_id, name, description, api_key):
    if all(
        value is None for value in (project_id, storage_provider_id, name, description)
    ):
        raise click.UsageError(
            "Pass --project, --storage, --name or --description to change something."
        )

    command = ml_models.EditModelCommand(api_key=api_key)
    command.execute(
        model_id=model_id,
        project_id=project_id,
        storage_provider_id=storage_provider_id,
        name=name,
        description=description,
    )


@models_group.command(
    "archive", help="Archive a model, or restore it if it is already archived"
)
@click.argument("model_id")
@api_key_option
def archive_model(model_id, api_key):
    command = ml_models.ArchiveModelCommand(api_key=api_key)
    command.execute(model_id)
