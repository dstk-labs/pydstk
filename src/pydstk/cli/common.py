import click
from click_didyoumean import DYMMixin
from click_help_colors import HelpColorsGroup

from pydstk.api_sdk.config import config


class ClickGroup(DYMMixin, HelpColorsGroup):
    pass


api_key_option = click.option(
    "--apiKey",
    "api_key",
    default=config.PYDSTK_API_KEY,
)
