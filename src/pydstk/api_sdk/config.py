import os
import json


_DEFAULT_WEB_URL = "http://localhost:5173"
_DEFAULT_API_HOST = "http://localhost:4000/graphql"
_DEFAULT_CONFIG_DIR_PATH = os.path.expanduser("~/.dstk")
_DEFAULT_CONFIG_FILE_NAME = os.path.join(_DEFAULT_CONFIG_DIR_PATH, "config.json")
_DEFAULT_HELP_HEADERS_COLOR = "yellow"
_DEFAULT_HELP_OPTIONS_COLOR = "green"
_DEFAULT_USE_CONSOLE_COLORS = True


# Copy-pasted from `login.py` to avoid a circular dependency
# Can probably be cleaned up later
def get_api_key(pydstk_dir, config_path):
    pydstk_dir = os.path.expanduser("~/.dstk") if pydstk_dir is None else pydstk_dir
    config_path = (
        os.path.join(pydstk_dir, "config.json") if config_path is None else config_path
    )

    if os.path.exists(config_path):
        config_data = json.load(open(config_path))
        if config_data and "apiKey" in config_data:
            return config_data["apiKey"]
    return ""


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
    CONFIG_DIR_PATH = os.path.expanduser(
        os.environ.get("PYDSTK_CONFIG_PATH", _DEFAULT_CONFIG_DIR_PATH)
    )
    CONFIG_FILE_NAME = os.environ.get(
        "PYDSTK_CONFIG_FILE_NAME", _DEFAULT_CONFIG_FILE_NAME
    )
    PYDSTK_API_KEY = os.environ.get(
        "PYDSTK_API_KEY", get_api_key(CONFIG_DIR_PATH, CONFIG_FILE_NAME)
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
