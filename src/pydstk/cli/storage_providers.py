import click

from pydstk.cli.cli import cli
from pydstk.cli.common import ClickGroup, api_key_option, team_option
from pydstk.commands import storage_providers

secret_access_key_option = click.option(
    "--secret-access-key",
    prompt=True,
    hide_input=True,
    help="Secret access key. Prompted for when left out",
)


@cli.group("storage", help="Manage storage providers", cls=ClickGroup)
def storage_group():
    pass


@storage_group.command("list", help="List storage providers in a team")
@team_option
@click.option("--bucket", help="Only show buckets whose name contains this text")
@click.option("--include-archived", is_flag=True, help="Include archived providers")
@api_key_option
def list_storage_providers(team_id, bucket, include_archived, api_key):
    command = storage_providers.ListStorageProvidersCommand(api_key=api_key)
    command.execute(team_id=team_id, bucket=bucket, include_archived=include_archived)


@storage_group.command("get", help="Show a storage provider")
@click.argument("provider_id")
@api_key_option
def get_storage_provider(provider_id, api_key):
    command = storage_providers.GetStorageProviderCommand(api_key=api_key)
    command.execute(provider_id=provider_id)


@storage_group.command("create", help="Connect an S3-compatible bucket")
@team_option
@click.option("--bucket", required=True, help="Bucket name")
@click.option(
    "--endpoint-url",
    required=True,
    help="S3-compatible endpoint, e.g. https://s3.us-east-1.amazonaws.com",
)
@click.option("--region", required=True, help="Bucket region, e.g. us-east-1")
@click.option("--access-key-id", required=True, help="Access key ID")
@secret_access_key_option
@api_key_option
def create_storage_provider(
    team_id, bucket, endpoint_url, region, access_key_id, secret_access_key, api_key
):
    command = storage_providers.CreateStorageProviderCommand(api_key=api_key)
    command.execute(
        team_id=team_id,
        bucket=bucket,
        endpoint_url=endpoint_url,
        region=region,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
    )


@storage_group.command("edit", help="Replace a storage provider's credentials")
@click.argument("provider_id")
@click.option("--access-key-id", required=True, help="New access key ID")
@secret_access_key_option
@api_key_option
def edit_storage_provider(provider_id, access_key_id, secret_access_key, api_key):
    command = storage_providers.EditStorageProviderCommand(api_key=api_key)
    command.execute(
        provider_id=provider_id,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
    )


@storage_group.command(
    "archive",
    help="Archive a storage provider, or restore it if it is already archived",
)
@click.argument("provider_id")
@api_key_option
def archive_storage_provider(provider_id, api_key):
    command = storage_providers.ArchiveStorageProviderCommand(api_key=api_key)
    command.execute(provider_id)
