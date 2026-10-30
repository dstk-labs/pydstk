from pydstk.api_sdk import repositories
from pydstk.api_sdk.clients.base_client import BaseClient


class InvitationsClient(BaseClient):
    entity = "invitation"

    def list(self, team_id=None, status=None):
        """List invitations sent to you, or a team's invitations when team_id is set

        :param str team_id:
        :param str status: pending, accepted, rejected or canceled
        :rtype: list[models.Invitation]
        """
        repository = self.build_repository(repositories.ListInvitations)
        return repository.list(team_id=team_id, status=status)

    def get(self, invitation_id):
        """Get an invitation sent to you

        :param str invitation_id:
        :rtype: models.Invitation
        """
        repository = self.build_repository(repositories.GetInvitation)
        return repository.get(invitation_id)

    def create(self, user_id, role="member", team_id=None):
        """Invite a user to a team

        :param str user_id:
        :param str role: owner, member or viewer
        :param str team_id: defaults to the client's team
        :rtype: models.Invitation
        """
        repository = self.build_repository(repositories.CreateInvitation)
        return repository.create(self.resolve_team_id(team_id), user_id, role)

    def accept(self, invitation_id):
        """
        :param str invitation_id:
        :rtype: models.Invitation
        """
        repository = self.build_repository(repositories.AcceptInvitation)
        return repository.accept(invitation_id)

    def reject(self, invitation_id):
        """
        :param str invitation_id:
        :rtype: models.Invitation
        """
        repository = self.build_repository(repositories.RejectInvitation)
        return repository.reject(invitation_id)

    def cancel(self, invitation_id, team_id=None):
        """Cancel an invitation your team sent

        :param str invitation_id:
        :param str team_id: defaults to the client's team
        :rtype: models.Invitation
        """
        repository = self.build_repository(repositories.CancelInvitation)
        return repository.cancel(invitation_id, self.resolve_team_id(team_id))
