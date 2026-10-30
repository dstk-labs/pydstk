from pydstk.api_sdk import clients
from pydstk.api_sdk.config import config


class Client(object):
    def __init__(self, api_key=None, team_id=None):
        """Entry point for using DSTK from Python

        :param str api_key: defaults to PYDSTK_API_KEY, the saved key, then the
            saved login
        :param str team_id: team for methods that need one and aren't given one.
            Defaults to PYDSTK_TEAM_ID, then the team saved with `pydstk teams use`
        """
        options = {"api_key": api_key, "team_id": team_id or config.TEAM_ID or None}

        self.teams = clients.TeamsClient(**options)
        self.projects = clients.ProjectsClient(**options)
        self.storage = clients.StorageProvidersClient(**options)
        self.models = clients.ModelsClient(**options)
        self.versions = clients.ModelVersionsClient(**options)
        self.invitations = clients.InvitationsClient(**options)
        self.users = clients.UsersClient(**options)
        self.api_keys = clients.ApiKeysClient(**options)
