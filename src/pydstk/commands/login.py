import importlib.metadata
import webbrowser

import requests
from keyring.errors import NoKeyringError

from pydstk.api_sdk import credentials, device_auth
from pydstk.api_sdk.config import config
from pydstk.cli_logger import CliLogger
from pydstk.exceptions import ApplicationError
from pydstk.login import set_apikey

USER_CODE_GROUP_LENGTH = 4


class CommandBase(object):
    def __init__(self, api=None, logger_=CliLogger()):
        self.api = api
        self.logger = logger_


class SetApiKeyCommand(CommandBase):
    def execute(self, api_key):
        if not api_key:
            self.logger.error("API Key cannot be empty.")
            return

        set_apikey(api_key)


class DeviceLoginCommand(CommandBase):
    def execute(self):
        device_code = device_auth.request_device_code()
        verification_url = device_code["verification_uri_complete"]

        self.logger.log(
            f"Your login code is {_format_user_code(device_code['user_code'])}"
        )
        self.logger.log(f"Opening {verification_url} to approve this device...")
        webbrowser.open(verification_url)

        session_token = device_auth.poll_for_session_token(
            device_code["device_code"],
            device_code["interval"],
            device_code["expires_in"],
        )
        self._save_session_token(session_token)

        user_name = device_auth.fetch_user_name(session_token)
        self.logger.log(f"Logged in as {user_name}.")

        if config.PYDSTK_API_KEY:
            self.logger.warning(
                "An API key is also configured and takes precedence over this login."
            )

    @staticmethod
    def _save_session_token(session_token):
        try:
            credentials.save_session_token(session_token)
        except NoKeyringError:
            raise ApplicationError(
                "No system keyring is available to store your login. "
                "Set PYDSTK_API_KEY to use an API key instead."
            )


class LogoutCommand(CommandBase):
    def execute(self):
        session_token = credentials.get_session_token()
        if not session_token:
            self.logger.log("You are not logged in.")
            return

        try:
            device_auth.sign_out(session_token)
        except requests.RequestException:
            self.logger.warning(
                "Could not reach DSTK to end the session. Removing the local login anyway."
            )

        credentials.delete_session_token()
        self.logger.log("Logged out.")


def _format_user_code(user_code):
    return f"{user_code[:USER_CODE_GROUP_LENGTH]}-{user_code[USER_CODE_GROUP_LENGTH:]}"


class ShowVersionCommand(CommandBase):
    def execute(self):
        __version__ = importlib.metadata.version("pydstk")
        self.logger.log(__version__)
