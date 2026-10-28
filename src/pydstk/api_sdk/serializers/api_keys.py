import marshmallow

from pydstk.api_sdk import models
from pydstk.api_sdk.serializers.base import BaseSchema


class ApiKey(BaseSchema):
    MODEL = models.ApiKey

    api_key_id = marshmallow.fields.Str(data_key="apiKeyId", load_only=True)
    name = marshmallow.fields.Str(allow_none=True)
    start = marshmallow.fields.Str(allow_none=True)
    is_archived = marshmallow.fields.Bool(data_key="isArchived", allow_none=True)
    date_created = marshmallow.fields.Str(data_key="dateCreated", load_only=True)
