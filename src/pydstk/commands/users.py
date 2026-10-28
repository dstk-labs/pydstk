import abc

import six

from pydstk import api_sdk
from pydstk.cli_constants import CLI_CLIENT_NAME
from pydstk.commands.common import (
    BaseCommand,
    DetailCommandMixin,
    ListCommandMixin,
    display,
)


@six.add_metaclass(abc.ABCMeta)
class UsersCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.UsersClient(
            api_key=api_key,
            logger=logger,
            client_name=CLI_CLIENT_NAME,
        )
        return client


class WhoAmICommand(DetailCommandMixin, UsersCommand):
    def _get_instance(self, **kwargs):
        return self.client.get_current()

    def _get_table_data(self, instance):
        return [
            ("ID", instance.user_id),
            ("User Name", instance.user_name),
            ("Name", display(instance.real_name)),
            ("Email", display(instance.email)),
            ("Email Verified", "yes" if instance.is_email_verified else "no"),
            ("Two-Factor", "on" if instance.is_two_factor_enabled else "off"),
        ]


class ListUsersCommand(ListCommandMixin, UsersCommand):
    def _get_instances(self, **kwargs):
        return self.client.list(**kwargs)

    def _get_table_data(self, objects):
        data = [("ID", "User Name", "Name", "Email")]

        for user in objects:
            data.append(
                (
                    user.user_id,
                    user.user_name,
                    display(user.real_name),
                    display(user.email),
                )
            )
        return data


class RequestPasswordResetCommand(UsersCommand):
    def execute(self, email):
        self.client.request_password_reset(email)
        self.logger.log(
            "If {} has a DSTK account, a reset link is on its way.".format(email)
        )
