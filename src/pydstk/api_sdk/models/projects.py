import attr


@attr.s
class Project(object):
    """
    Project class

    :param str project_id:
    :param str name:
    :param str description:
    :param bool is_archived:
    :param str created_by:
    :param str date_created:
    :param str date_modified:
    """

    project_id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    is_archived = attr.ib(type=bool, default=None)
    created_by = attr.ib(type=str, default=None)
    date_created = attr.ib(type=str, default=None)
    date_modified = attr.ib(type=str, default=None)
