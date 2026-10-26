import attr


@attr.s
class StorageProvider(object):
    """
    StorageProvider class

    :param str provider_id:
    :param str bucket:
    :param str endpoint_url:
    :param str region:
    :param str access_key_id:
    :param bool is_archived:
    :param str created_by:
    :param str date_created:
    :param str date_modified:
    """

    provider_id = attr.ib(type=str, default=None)
    bucket = attr.ib(type=str, default=None)
    endpoint_url = attr.ib(type=str, default=None)
    region = attr.ib(type=str, default=None)
    access_key_id = attr.ib(type=str, default=None)
    is_archived = attr.ib(type=bool, default=None)
    created_by = attr.ib(type=str, default=None)
    date_created = attr.ib(type=str, default=None)
    date_modified = attr.ib(type=str, default=None)
