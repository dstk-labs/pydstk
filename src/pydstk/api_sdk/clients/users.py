from pydstk.api_sdk import repositories
from pydstk.api_sdk.clients.base_client import BaseClient


class UsersClient(BaseClient):
    entity = "user"

    def get_current(self):
        """The user these credentials belong to

        :rtype: models.User
        """
        repository = self.build_repository(repositories.GetCurrentUser)
        return repository.get()

    def list(self, user_name=None):
        """List users who share a team with you

        :param str user_name: only users whose user name contains this text
        :rtype: list[models.User]
        """
        repository = self.build_repository(repositories.ListUsers)
        return repository.list(user_name=user_name)

    def request_password_reset(self, email):
        """Email a password reset link. Sent without credentials

        :param str email:
        """
        repository = self.build_repository(repositories.RequestPasswordReset)
        repository.request(email)
