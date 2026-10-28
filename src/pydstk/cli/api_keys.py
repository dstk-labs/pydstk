import click

from pydstk.cli.cli import cli
from pydstk.cli.common import ClickGroup, api_key_option
from pydstk.commands import api_keys


@cli.group("api-keys", help="Manage your API keys", cls=ClickGroup)
def api_keys_group():
    pass


@api_keys_group.command("list", help="List your API keys")
@api_key_option
def list_api_keys(api_key):
    command = api_keys.ListApiKeysCommand(api_key=api_key)
    command.execute()


@api_keys_group.command("create", help="Create an API key")
@click.option("--name", help="A name to recognize the key by")
@api_key_option
def create_api_key(name, api_key):
    command = api_keys.CreateApiKeyCommand(api_key=api_key)
    command.execute(name)


@api_keys_group.command("archive", help="Disable an API key. This can't be undone")
@click.argument("api_key_id")
@click.confirmation_option(prompt="Disable this API key? It stops working right away.")
@api_key_option
def archive_api_key(api_key_id, api_key):
    command = api_keys.ArchiveApiKeyCommand(api_key=api_key)
    command.execute(api_key_id)
