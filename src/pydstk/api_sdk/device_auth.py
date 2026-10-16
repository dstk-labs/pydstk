import time

import requests

from pydstk.api_sdk.config import config
from pydstk.api_sdk.exceptions import DeviceAuthorizationError

CLIENT_ID = "pydstk"
DEVICE_CODE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"
SLOW_DOWN_SECONDS = 5
REQUEST_TIMEOUT_SECONDS = 10

ERROR_MESSAGES = {
    "access_denied": "The login request was denied in the browser.",
    "expired_token": "The login code expired. Run `pydstk login` again.",
}

GET_USER_QUERY = "{ user { get { userName } } }"
LOGOUT_MUTATION = "mutation { auth { logout } }"


def request_device_code():
    response = requests.post(
        f"{config.AUTH_URL}/device/code",
        json={"client_id": CLIENT_ID},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def poll_for_session_token(device_code, interval, expires_in):
    deadline = time.monotonic() + expires_in

    while time.monotonic() < deadline:
        time.sleep(interval)
        response = requests.post(
            f"{config.AUTH_URL}/device/token",
            json={
                "client_id": CLIENT_ID,
                "device_code": device_code,
                "grant_type": DEVICE_CODE_GRANT_TYPE,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        body = response.json()

        if response.ok:
            return body["access_token"]

        error = body.get("error")
        if error == "authorization_pending":
            continue
        if error == "slow_down":
            interval += SLOW_DOWN_SECONDS
            continue

        raise DeviceAuthorizationError(
            ERROR_MESSAGES.get(error, body.get("error_description", error))
        )

    raise DeviceAuthorizationError(ERROR_MESSAGES["expired_token"])


def fetch_user_name(session_token):
    response = requests.post(
        config.API_HOST,
        json={"query": GET_USER_QUERY},
        headers={"Authorization": f"Bearer {session_token}"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()["data"]["user"]["get"]["userName"]


def sign_out(session_token):
    response = requests.post(
        config.API_HOST,
        json={"query": LOGOUT_MUTATION},
        headers={"Authorization": f"Bearer {session_token}"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
