import os
import json


_DEFAULT_WEB_URL = "http://localhost:5173"
_DEFAULT_API_HOST = "http://localhost:4000/graphql"
_DEFAULT_AUTH_URL = "http://localhost:4000/api/auth"
_DEFAULT_CONFIG_DIR_PATH = os.path.expanduser("~/.dstk")
_DEFAULT_CONFIG_FILE_NAME = os.path.join(_DEFAULT_CONFIG_DIR_PATH, "config.json")
_DEFAULT_HELP_HEADERS_COLOR = "yellow"
_DEFAULT_HELP_OPTIONS_COLOR = "green"
_DEFAULT_USE_CONSOLE_COLORS = True


def read_config_file(config_path):
    if not os.path.exists(config_path):
        return {}

    with open(config_path) as config_file:
        return json.load(config_file) or {}


def get_help_colors_dict(use_colors, help_headers_color, help_options_color):
    if not use_colors:
        return {}

    d = {
        "help_headers_color": help_headers_color,
        "help_options_color": help_options_color,
    }
    return d


class config(object):
    DEBUG = os.environ.get("PYDSTK_CLI_DEBUG") in ("true", "1")

    WEB_URL = os.environ.get("PYDSTK_WEB_URL", _DEFAULT_WEB_URL)
    API_HOST = os.environ.get("PYDSTK_API_HOST", _DEFAULT_API_HOST)
    AUTH_URL = os.environ.get("PYDSTK_AUTH_URL", _DEFAULT_AUTH_URL)
    CONFIG_DIR_PATH = os.path.expanduser(
        os.environ.get("PYDSTK_CONFIG_PATH", _DEFAULT_CONFIG_DIR_PATH)
    )
    CONFIG_FILE_NAME = os.environ.get(
        "PYDSTK_CONFIG_FILE_NAME", _DEFAULT_CONFIG_FILE_NAME
    )
    PYDSTK_API_KEY = os.environ.get(
        "PYDSTK_API_KEY", read_config_file(CONFIG_FILE_NAME).get("apiKey", "")
    )
    TEAM_ID = os.environ.get(
        "PYDSTK_TEAM_ID", read_config_file(CONFIG_FILE_NAME).get("teamId", "")
    )

    HELP_HEADERS_COLOR = os.environ.get(
        "PYDSTK_HELP_HEADERS_COLOR", _DEFAULT_HELP_HEADERS_COLOR
    )
    HELP_OPTIONS_COLOR = os.environ.get(
        "PYDSTK_HELP_OPTIONS_COLOR", _DEFAULT_HELP_OPTIONS_COLOR
    )
    USE_CONSOLE_COLORS = os.environ.get(
        "PYDSTK_USE_CONSOLE_COLORS", _DEFAULT_USE_CONSOLE_COLORS
    ) in (True, "true", "1")
    HELP_COLORS_DICT = get_help_colors_dict(
        USE_CONSOLE_COLORS, HELP_HEADERS_COLOR, HELP_OPTIONS_COLOR
    )


def update_config_file(**values):
    os.makedirs(config.CONFIG_DIR_PATH, exist_ok=True)
    config_data = read_config_file(config.CONFIG_FILE_NAME)
    config_data.update(values)

    with open(config.CONFIG_FILE_NAME, "w") as config_file:
        json.dump(config_data, config_file, indent=2, sort_keys=True)
        config_file.write("\n")
