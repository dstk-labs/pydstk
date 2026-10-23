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


def _require_team(ctx, param, value):
    if not value:
        raise click.UsageError(
            "No team selected. Run `pydstk teams use TEAM_ID` or pass --team."
        )
    return value


team_option = click.option(
    "--team",
    "team_id",
    default=lambda: config.TEAM_ID,
    show_default="team saved with `pydstk teams use`",
    callback=_require_team,
    help="Team ID",
)
