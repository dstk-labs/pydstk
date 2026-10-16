import marshmallow

from pydstk.api_sdk.serializers.base import BaseSchema
from pydstk.api_sdk import models


class Team(BaseSchema):
    MODEL = models.Team

    team_id = marshmallow.fields.Str(data_key="teamId", load_only=True)
    name = marshmallow.fields.Str()
    date_created = marshmallow.fields.Str(data_key="dateCreated", load_only=True)
    date_modified = marshmallow.fields.Str(data_key="dateModified", load_only=True)
