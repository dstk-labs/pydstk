import keyring
from keyring.errors import KeyringError, PasswordDeleteError

from pydstk.api_sdk.config import config

KEYRING_SERVICE = "dstk"


def get_session_token():
    try:
        return keyring.get_password(KEYRING_SERVICE, config.AUTH_URL)
    except KeyringError:
        return None


def save_session_token(token):
    keyring.set_password(KEYRING_SERVICE, config.AUTH_URL, token)


def delete_session_token():
    try:
        keyring.delete_password(KEYRING_SERVICE, config.AUTH_URL)
    except PasswordDeleteError:
        pass
