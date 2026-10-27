import attr


@attr.s
class Invitation(object):
    """
    Invitation class

    :param str invitation_id:
    :param str email: address the invitation was sent to
    :param str role:
    :param str status: pending, accepted, rejected or canceled
    :param str team_id:
    :param str team_name:
    :param str inviter:
    :param str expires_at:
    :param str date_created:
    """

    invitation_id = attr.ib(type=str, default=None)
    email = attr.ib(type=str, default=None)
    role = attr.ib(type=str, default=None)
    status = attr.ib(type=str, default=None)
    team_id = attr.ib(type=str, default=None)
    team_name = attr.ib(type=str, default=None)
    inviter = attr.ib(type=str, default=None)
    expires_at = attr.ib(type=str, default=None)
    date_created = attr.ib(type=str, default=None)
