import marshmallow

from pydstk.api_sdk import models
from pydstk.api_sdk.serializers.base import BaseSchema, nested_field


class StorageProvider(BaseSchema):
    MODEL = models.StorageProvider

    provider_id = marshmallow.fields.Str(data_key="providerId", load_only=True)
    bucket = marshmallow.fields.Str()
    endpoint_url = marshmallow.fields.Str(data_key="endpointUrl", load_only=True)
    region = marshmallow.fields.Str(allow_none=True)
    access_key_id = marshmallow.fields.Str(data_key="accessKeyId", load_only=True)
    is_archived = marshmallow.fields.Bool(data_key="isArchived", allow_none=True)
    created_by = nested_field("createdBy", "realName")
    date_created = marshmallow.fields.Str(data_key="dateCreated", load_only=True)
    date_modified = marshmallow.fields.Str(data_key="dateModified", load_only=True)
