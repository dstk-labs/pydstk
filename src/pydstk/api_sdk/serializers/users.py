import marshmallow

from pydstk.api_sdk import models
from pydstk.api_sdk.serializers.base import BaseSchema


class User(BaseSchema):
    MODEL = models.User

    user_id = marshmallow.fields.Str(data_key="userId", load_only=True)
    user_name = marshmallow.fields.Str(data_key="userName", load_only=True)
    real_name = marshmallow.fields.Str(
        data_key="realName", load_only=True, allow_none=True
    )
    email = marshmallow.fields.Str(allow_none=True)
    is_email_verified = marshmallow.fields.Bool(
        data_key="isEmailVerified", load_only=True, allow_none=True
    )
    is_two_factor_enabled = marshmallow.fields.Bool(
        data_key="isTwoFactorEnabled", load_only=True, allow_none=True
    )
    date_created = marshmallow.fields.Str(
        data_key="dateCreated", load_only=True, allow_none=True
    )
