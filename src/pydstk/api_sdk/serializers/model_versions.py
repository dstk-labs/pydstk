import marshmallow

from pydstk.api_sdk import models
from pydstk.api_sdk.serializers.base import BaseSchema, nested_field


class ModelVersion(BaseSchema):
    MODEL = models.ModelVersion

    model_version_id = marshmallow.fields.Str(data_key="modelVersionId", load_only=True)
    numeric_version = marshmallow.fields.Int(data_key="numericVersion", load_only=True)
    description = marshmallow.fields.Str(allow_none=True)
    is_archived = marshmallow.fields.Bool(data_key="isArchived", allow_none=True)
    is_published = marshmallow.fields.Bool(data_key="isFinalized", allow_none=True)
    s3_prefix = marshmallow.fields.Str(data_key="s3Prefix", load_only=True)
    model = marshmallow.fields.Raw(data_key="modelId", load_only=True, allow_none=True)
    created_by = nested_field("createdBy", "realName")
    date_created = marshmallow.fields.Str(data_key="dateCreated", load_only=True)

    @marshmallow.post_load
    def flatten_model(self, data, **kwargs):
        model = data.pop("model", None) or {}
        data["model_id"] = model.get("modelId")
        data["model_name"] = model.get("modelName")
        return data


class ModelVersionFile(BaseSchema):
    MODEL = models.ModelVersionFile

    name = marshmallow.fields.Str()
    size = marshmallow.fields.Float(allow_none=True)
    last_modified = marshmallow.fields.Str(
        data_key="lastModified", load_only=True, allow_none=True
    )
