import marshmallow

from pydstk.api_sdk import models
from pydstk.api_sdk.serializers.base import BaseSchema, nested_field


class Model(BaseSchema):
    MODEL = models.Model

    model_id = marshmallow.fields.Str(data_key="modelId", load_only=True)
    name = marshmallow.fields.Str(data_key="modelName", load_only=True)
    description = marshmallow.fields.Str(allow_none=True)
    is_archived = marshmallow.fields.Bool(data_key="isArchived", allow_none=True)
    project = marshmallow.fields.Raw(load_only=True, allow_none=True)
    storage_provider = marshmallow.fields.Raw(
        data_key="storageProvider", load_only=True, allow_none=True
    )
    current_version = nested_field("currentModelVersion", "numericVersion")
    created_by = nested_field("createdBy", "realName")
    date_created = marshmallow.fields.Str(data_key="dateCreated", load_only=True)
    date_modified = marshmallow.fields.Str(data_key="dateModified", load_only=True)

    @marshmallow.post_load
    def flatten_relations(self, data, **kwargs):
        project = data.pop("project", None) or {}
        storage_provider = data.pop("storage_provider", None) or {}
        data["project_id"] = project.get("projectId")
        data["project_name"] = project.get("name")
        data["storage_provider_id"] = storage_provider.get("providerId")
        data["bucket"] = storage_provider.get("bucket")
        return data
