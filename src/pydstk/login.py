from pydstk.cli_logger import CliLogger
from pydstk.api_sdk.config import config, update_config_file


logger = CliLogger()


def set_apikey(apikey):
    config.PYDSTK_API_KEY = apikey
    update_config_file(apiKey=apikey)

    logger.log(
        "Successfully added your API Key to {}. You're ready to go!".format(
            config.CONFIG_FILE_NAME
        )
    )

    return True
