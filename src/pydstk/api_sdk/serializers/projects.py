import marshmallow

from pydstk.api_sdk import models
from pydstk.api_sdk.serializers.base import BaseSchema, nested_field


class Project(BaseSchema):
    MODEL = models.Project

    project_id = marshmallow.fields.Str(data_key="projectId", load_only=True)
    name = marshmallow.fields.Str()
    description = marshmallow.fields.Str(allow_none=True)
    is_archived = marshmallow.fields.Bool(data_key="isArchived", allow_none=True)
    created_by = nested_field("createdBy", "realName")
    date_created = marshmallow.fields.Str(data_key="dateCreated", load_only=True)
    date_modified = marshmallow.fields.Str(data_key="dateModified", load_only=True)
