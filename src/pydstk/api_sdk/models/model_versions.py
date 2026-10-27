import attr


@attr.s
class ModelVersion(object):
    """
    ModelVersion class

    :param str model_version_id:
    :param int numeric_version:
    :param str description:
    :param bool is_archived:
    :param bool is_published:
    :param str s3_prefix:
    :param str model_id:
    :param str model_name:
    :param str created_by:
    :param str date_created:
    """

    model_version_id = attr.ib(type=str, default=None)
    numeric_version = attr.ib(type=int, default=None)
    description = attr.ib(type=str, default=None)
    is_archived = attr.ib(type=bool, default=None)
    is_published = attr.ib(type=bool, default=None)
    s3_prefix = attr.ib(type=str, default=None)
    model_id = attr.ib(type=str, default=None)
    model_name = attr.ib(type=str, default=None)
    created_by = attr.ib(type=str, default=None)
    date_created = attr.ib(type=str, default=None)


@attr.s
class ModelVersionFile(object):
    """
    A file stored under a model version

    :param str name:
    :param float size: bytes
    :param str last_modified:
    """

    name = attr.ib(type=str, default=None)
    size = attr.ib(type=float, default=None)
    last_modified = attr.ib(type=str, default=None)
