import click
import getpass

from pydstk.cli_logger import CliLogger
from pydstk.cli.cli import cli
from pydstk.commands import login

logger = CliLogger()


@cli.command("apiKey", help="Save your api key")
@click.argument(
    "api_key",
    required=False,
)
def save_api_key(api_key):
    if not api_key:
        api_key = getpass.getpass("Enter your API Key: ")

    command = login.SetApiKeyCommand()
    api_key = api_key.strip()
    command.execute(api_key)


@cli.command("login", help="Log in through your browser")
def device_login():
    command = login.DeviceLoginCommand()
    command.execute()


@cli.command("logout", help="Log out and remove your saved login")
def logout():
    command = login.LogoutCommand()
    command.execute()
