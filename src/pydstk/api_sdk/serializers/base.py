import marshmallow


class BaseSchema(marshmallow.Schema):
    MODEL = None

    @marshmallow.post_dump
    def remove_none_or_empty_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items() if value not in (None, {}, [])
        }

    def get_instance(self, obj_dict, many=False):
        if not self.MODEL:
            raise NotImplementedError

        if not many:
            return self._get_instance(obj_dict)

        instances = [self._get_instance(obj_d) for obj_d in obj_dict]
        return instances

    def _get_instance(self, obj_dict):
        data = self.load(obj_dict)
        if data is None:
            return None

        instance = self.MODEL(**data)
        self._get_nested(instance, obj_dict)
        return instance

    def _get_nested(self, instance, obj_dict):
        for field_name, field_type in self.fields.items():
            if not isinstance(field_type, marshmallow.fields.Nested):
                continue

            data_key = field_type.data_key or field_name
            field_dict = obj_dict.get(data_key, {})
            if field_dict is None:
                continue

            serializer = field_type.nested()
            field_data = serializer.get_instance(field_dict, many=field_type.many)

            if field_type.only:
                if isinstance(field_data, list):
                    field_data = [getattr(val, field_type.only) for val in field_data]
                else:
                    field_data = getattr(field_data, field_type.only)

            if field_data:
                setattr(instance, field_name, field_data)


def nested_field(data_key, key):
    """Loads one value out of a nested GraphQL object, e.g. createdBy.realName

    :param str data_key: field name in the GraphQL response
    :param str key: key inside the nested object
    """
    return marshmallow.fields.Function(
        deserialize=lambda value: value.get(key),
        data_key=data_key,
        allow_none=True,
        load_only=True,
    )
