import json
import os

from pydstk.cli_logger import CliLogger
from pydstk.api_sdk.config import config


logger = CliLogger()


def apikey(pydstk_dir, config_path):
    pydstk_dir = os.path.expanduser("~/.pydstk") if pydstk_dir is None else pydstk_dir
    config_path = (
        os.path.join(pydstk_dir, "config.json") if config_path is None else config_path
    )

    if os.path.exists(config_path):
        config_data = json.load(open(config_path))
        if config_data and "apiKey" in config_data:
            return config_data["apiKey"]
    return ""


def set_apikey(apikey):
    pydstk_dir = os.path.expanduser("~/.pydstk")
    config_path = os.path.join(pydstk_dir, "config.json")
    if not os.path.exists(pydstk_dir):
        os.makedirs(pydstk_dir)
    config_data = {}

    # update config.PYDSTK_API_KEY
    config.PYDSTK_API_KEY = apikey

    # save api key
    config_data["apiKey"] = apikey
    with open(config_path, "w") as outfile:
        json.dump(config_data, outfile, indent=2, sort_keys=True)
        outfile.write("\n")

    logger.log(
        "Successfully added your API Key to {}. You're ready to go!".format(config_path)
    )

    return True
