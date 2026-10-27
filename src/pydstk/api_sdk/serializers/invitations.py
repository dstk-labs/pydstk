import marshmallow

from pydstk.api_sdk import models
from pydstk.api_sdk.serializers.base import BaseSchema, nested_field


class Invitation(BaseSchema):
    MODEL = models.Invitation

    invitation_id = marshmallow.fields.Str(data_key="id", load_only=True)
    email = marshmallow.fields.Str(allow_none=True)
    role = marshmallow.fields.Str(allow_none=True)
    status = marshmallow.fields.Str(allow_none=True)
    team = marshmallow.fields.Raw(data_key="teamId", load_only=True, allow_none=True)
    inviter = nested_field("inviter", "realName")
    expires_at = marshmallow.fields.Str(data_key="expiresAt", load_only=True)
    date_created = marshmallow.fields.Str(data_key="dateCreated", load_only=True)

    @marshmallow.post_load
    def flatten_team(self, data, **kwargs):
        team = data.pop("team", None) or {}
        data["team_id"] = team.get("teamId")
        data["team_name"] = team.get("name")
        return data
