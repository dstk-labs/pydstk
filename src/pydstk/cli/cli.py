import click
import requests
from pydstk.cli import common
from pydstk.api_sdk.config import config
from pydstk.exceptions import ApplicationError
from pydstk.api_sdk.exceptions import DstkSdkError
from pydstk.cli_logger import CliLogger
from pydstk.commands import login


class GradientGroup(common.ClickGroup):
    def main(self, *args, **kwargs):
        try:
            super(GradientGroup, self).main(*args, **kwargs)
        except requests.exceptions.RequestException:
            msg = "🥺👉👈"
            CliLogger().error(msg)
        except (ApplicationError, DstkSdkError) as e:
            if config.DEBUG:
                raise

            CliLogger().error(e)


@click.group(cls=GradientGroup, **config.HELP_COLORS_DICT)
def cli():
    pass


@cli.command("version", help="Show the version and exit")
def get_version():
    command = login.ShowVersionCommand()
    command.execute()


if __name__ == "__main__":
    cli()
