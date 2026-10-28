from gql import Client
from gql.transport.requests import RequestsHTTPTransport

from pydstk.api_sdk.config import config
from pydstk.api_sdk.credentials import get_session_token


def auth_headers(api_key=None):
    if api_key is None:
        api_key = config.PYDSTK_API_KEY
    if api_key:
        return {"x-api-key": api_key}

    session_token = get_session_token()
    if session_token:
        return {"Authorization": f"Bearer {session_token}"}

    return {}


def graphql_client(api_key=None, anonymous=False):
    headers = {} if anonymous else auth_headers(api_key)
    transport = RequestsHTTPTransport(
        headers=headers, url=config.API_HOST, verify=True, retries=3
    )

    return Client(transport=transport)
