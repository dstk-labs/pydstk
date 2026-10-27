import attr


@attr.s
class Team(object):
    """
    Team class

    :param str team_id:
    :param str name:
    :param str description:
    :param bool is_archived:
    :param str date_created:
    :param str date_modified:
    """

    team_id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    is_archived = attr.ib(type=bool, default=None)
    date_created = attr.ib(type=str, default=None)
    date_modified = attr.ib(type=str, default=None)


@attr.s
class TeamMember(object):
    """
    TeamMember class

    :param str member_id:
    :param str role:
    :param str user_id:
    :param str user_name:
    :param str real_name:
    :param str email:
    :param str date_created:
    """

    member_id = attr.ib(type=str, default=None)
    role = attr.ib(type=str, default=None)
    user_id = attr.ib(type=str, default=None)
    user_name = attr.ib(type=str, default=None)
    real_name = attr.ib(type=str, default=None)
    email = attr.ib(type=str, default=None)
    date_created = attr.ib(type=str, default=None)
