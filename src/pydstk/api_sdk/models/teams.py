import attr


@attr.s
class Team(object):
    """
    Team class

    :param str teamId:
    :param str name:
    :param str dateCreated:
    :param str dateModified:
    """

    team_id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    date_created = attr.ib(type=str, default=None)
    date_modified = attr.ib(type=str, default=None)
