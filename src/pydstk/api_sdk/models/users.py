import attr


@attr.s
class User(object):
    """
    User class

    :param str user_id:
    :param str user_name:
    :param str real_name:
    :param str email:
    :param bool is_email_verified:
    :param bool is_two_factor_enabled:
    :param str date_created:
    """

    user_id = attr.ib(type=str, default=None)
    user_name = attr.ib(type=str, default=None)
    real_name = attr.ib(type=str, default=None)
    email = attr.ib(type=str, default=None)
    is_email_verified = attr.ib(type=bool, default=None)
    is_two_factor_enabled = attr.ib(type=bool, default=None)
    date_created = attr.ib(type=str, default=None)
