import attr


@attr.s
class Model(object):
    """
    Model class

    :param str model_id:
    :param str name:
    :param str description:
    :param bool is_archived:
    :param str project_id:
    :param str project_name:
    :param str storage_provider_id:
    :param str bucket:
    :param int current_version:
    :param str created_by:
    :param str date_created:
    :param str date_modified:
    """

    model_id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    is_archived = attr.ib(type=bool, default=None)
    project_id = attr.ib(type=str, default=None)
    project_name = attr.ib(type=str, default=None)
    storage_provider_id = attr.ib(type=str, default=None)
    bucket = attr.ib(type=str, default=None)
    current_version = attr.ib(type=int, default=None)
    created_by = attr.ib(type=str, default=None)
    date_created = attr.ib(type=str, default=None)
    date_modified = attr.ib(type=str, default=None)
