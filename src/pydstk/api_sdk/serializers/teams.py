import marshmallow

from pydstk.api_sdk.serializers.base import BaseSchema
from pydstk.api_sdk import models


class Team(BaseSchema):
    MODEL = models.Team

    team_id = marshmallow.fields.Str(data_key="teamId", load_only=True)
    name = marshmallow.fields.Str()
    description = marshmallow.fields.Str(allow_none=True)
    is_archived = marshmallow.fields.Bool(data_key="isArchived", allow_none=True)
    date_created = marshmallow.fields.Str(data_key="dateCreated", load_only=True)
    date_modified = marshmallow.fields.Str(data_key="dateModified", load_only=True)


class TeamMember(BaseSchema):
    MODEL = models.TeamMember

    member_id = marshmallow.fields.Str(data_key="memberId", load_only=True)
    role = marshmallow.fields.Str(allow_none=True)
    user = marshmallow.fields.Raw(load_only=True, allow_none=True)
    date_created = marshmallow.fields.Str(data_key="dateCreated", load_only=True)

    @marshmallow.post_load
    def flatten_user(self, data, **kwargs):
        user = data.pop("user", None) or {}
        data["user_id"] = user.get("userId")
        data["user_name"] = user.get("userName")
        data["real_name"] = user.get("realName")
        data["email"] = user.get("email")
        return data
