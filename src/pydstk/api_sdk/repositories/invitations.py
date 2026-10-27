from gql import gql

from pydstk.api_sdk import serializers
from pydstk.api_sdk.repositories.common import BaseRepository, ListResources

INVITATION_FIELDS = """
    id
    email
    role
    status
    teamId {
        teamId
        name
    }
    inviter {
        realName
    }
    expiresAt
    dateCreated
"""

LIST_INVITATIONS = gql(
    """
    query ListInvitations($after: String, $teamId: String, $status: String) {
        invitation {
            list(after: $after, teamId: $teamId, status: $status) {
                pageInfo {
                    continuationToken
                    hasNextPage
                }
                edges {
                    node {
                        %s
                    }
                }
            }
        }
    }
    """
    % INVITATION_FIELDS
)

GET_INVITATION = gql(
    """
    query GetInvitation($invitationId: String!) {
        invitation {
            get(invitationId: $invitationId) {
                %s
            }
        }
    }
    """
    % INVITATION_FIELDS
)

CREATE_INVITATION = gql(
    """
    mutation InviteTeamMember($data: InviteTeamMemberInput!) {
        invitation {
            create(data: $data) {
                %s
            }
        }
    }
    """
    % INVITATION_FIELDS
)

ACCEPT_INVITATION = gql(
    """
    mutation AcceptInvitation($invitationId: String!) {
        invitation {
            accept(invitationId: $invitationId) {
                %s
            }
        }
    }
    """
    % INVITATION_FIELDS
)

REJECT_INVITATION = gql(
    """
    mutation RejectInvitation($invitationId: String!) {
        invitation {
            reject(invitationId: $invitationId) {
                %s
            }
        }
    }
    """
    % INVITATION_FIELDS
)

CANCEL_INVITATION = gql(
    """
    mutation CancelInvitation($invitationId: String!, $teamId: String!) {
        invitation {
            cancel(invitationId: $invitationId, teamId: $teamId) {
                %s
            }
        }
    }
    """
    % INVITATION_FIELDS
)


class ListInvitations(ListResources):
    SERIALIZER_CLS = serializers.Invitation

    def list(self, team_id=None, status=None):
        invitation_dicts = self._fetch_all(
            LIST_INVITATIONS,
            ("invitation", "list"),
            {"teamId": team_id, "status": status},
        )
        return self._parse_objects(invitation_dicts)


class GetInvitation(BaseRepository):
    SERIALIZER_CLS = serializers.Invitation

    def get(self, invitation_id):
        result = self._execute(GET_INVITATION, {"invitationId": invitation_id})
        return self._parse_object(result["invitation"]["get"])


class CreateInvitation(BaseRepository):
    SERIALIZER_CLS = serializers.Invitation

    def create(self, team_id, user_id, role):
        data = {"teamId": team_id, "userId": user_id, "role": role}
        result = self._execute(CREATE_INVITATION, {"data": data})
        return self._parse_object(result["invitation"]["create"])


class AcceptInvitation(BaseRepository):
    SERIALIZER_CLS = serializers.Invitation

    def accept(self, invitation_id):
        result = self._execute(ACCEPT_INVITATION, {"invitationId": invitation_id})
        return self._parse_object(result["invitation"]["accept"])


class RejectInvitation(BaseRepository):
    SERIALIZER_CLS = serializers.Invitation

    def reject(self, invitation_id):
        result = self._execute(REJECT_INVITATION, {"invitationId": invitation_id})
        return self._parse_object(result["invitation"]["reject"])


class CancelInvitation(BaseRepository):
    SERIALIZER_CLS = serializers.Invitation

    def cancel(self, invitation_id, team_id):
        result = self._execute(
            CANCEL_INVITATION, {"invitationId": invitation_id, "teamId": team_id}
        )
        return self._parse_object(result["invitation"]["cancel"])
