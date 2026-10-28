import attr


@attr.s
class ApiKey(object):
    """
    ApiKey class

    :param str api_key_id:
    :param str name:
    :param str start: first characters of the key, to tell keys apart
    :param bool is_archived:
    :param str date_created:
    :param str key: the full key. Only set right after the key is created
    """

    api_key_id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    start = attr.ib(type=str, default=None)
    is_archived = attr.ib(type=bool, default=None)
    date_created = attr.ib(type=str, default=None)
    key = attr.ib(type=str, default=None)
