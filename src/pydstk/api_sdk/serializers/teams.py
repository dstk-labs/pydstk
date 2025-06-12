import marshmallow

from pydstk.api_sdk.serializers.base import BaseSchema
from pydstk.api_sdk import models


class Team(BaseSchema):
    MODEL = models.Team

    team_id = marshmallow.fields.Str(load_from="teamId", load_only=True)
    name = marshmallow.fields.Str()
    created_date = marshmallow.fields.Str(load_from="createdDate", load_only=True)
    modified_date = marshmallow.fields.Str(load_from="modifiedDate", load_only=True)
