import click

from pydstk.cli.cli import cli
from pydstk.cli.common import ClickGroup, api_key_option
from pydstk.commands import model_versions


@cli.group("versions", help="Manage model versions", cls=ClickGroup)
def versions_group():
    pass


@versions_group.command("list", help="List versions of a model")
@click.argument("model_id")
@click.option("--include-archived", is_flag=True, help="Include archived versions")
@api_key_option
def list_versions(model_id, include_archived, api_key):
    command = model_versions.ListModelVersionsCommand(api_key=api_key)
    command.execute(model_id=model_id, include_archived=include_archived)


@versions_group.command("get", help="Show a model version")
@click.argument("model_version_id")
@api_key_option
def get_version(model_version_id, api_key):
    command = model_versions.GetModelVersionCommand(api_key=api_key)
    command.execute(model_version_id=model_version_id)


@versions_group.command("create", help="Start a new version of a model")
@click.argument("model_id")
@click.option("--description", help="What changed in this version")
@api_key_option
def create_version(model_id, description, api_key):
    command = model_versions.CreateModelVersionCommand(api_key=api_key)
    command.execute(model_id=model_id, description=description)


@versions_group.command("edit", help="Change a version's description")
@click.argument("model_version_id")
@click.option("--description", required=True, help="New description")
@api_key_option
def edit_version(model_version_id, description, api_key):
    command = model_versions.EditModelVersionCommand(api_key=api_key)
    command.execute(model_version_id=model_version_id, description=description)


@versions_group.command(
    "upload", help="Upload files or folders to a version that isn't published yet"
)
@click.argument("model_version_id")
@click.argument(
    "paths", nargs=-1, required=True, type=click.Path(exists=True, readable=True)
)
@api_key_option
def upload_version(model_version_id, paths, api_key):
    command = model_versions.UploadModelVersionCommand(api_key=api_key)
    command.execute(model_version_id, list(paths))


@versions_group.command("files", help="List the files in a version")
@click.argument("model_version_id")
@click.option("--prefix", help="Only files whose name starts with this")
@api_key_option
def list_version_files(model_version_id, prefix, api_key):
    command = model_versions.ListModelVersionFilesCommand(api_key=api_key)
    command.execute(model_version_id=model_version_id, prefix=prefix)


@versions_group.command(
    "publish", help="Publish a version. Published versions can't take new files"
)
@click.argument("model_version_id")
@api_key_option
def publish_version(model_version_id, api_key):
    command = model_versions.PublishModelVersionCommand(api_key=api_key)
    command.execute(model_version_id)


@versions_group.command(
    "archive", help="Archive a version, or restore it if it is already archived"
)
@click.argument("model_version_id")
@api_key_option
def archive_version(model_version_id, api_key):
    command = model_versions.ArchiveModelVersionCommand(api_key=api_key)
    command.execute(model_version_id)
