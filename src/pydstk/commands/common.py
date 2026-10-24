import abc

import six

from pydstk.cli_logger import CliLogger


def make_table(rows):
    widths = [max(len(str(cell)) for cell in column) for column in zip(*rows)]
    lines = [
        "  ".join(str(cell).ljust(width) for cell, width in zip(row, widths))
        for row in rows
    ]
    return "\n".join(line.rstrip() for line in lines)


def display(value):
    return "" if value is None else value


@six.add_metaclass(abc.ABCMeta)
class BaseCommand:
    def __init__(self, api_key, logger=CliLogger()):
        self.api_key = api_key
        self.client = self._get_client(api_key, logger)
        self.logger = logger

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def _get_client(self, api_key, logger):
        pass


@six.add_metaclass(abc.ABCMeta)
class ListCommandMixin(object):
    def execute(self, **kwargs):
        instances = self._get_instances(**kwargs)
        if not instances:
            self.logger.warning("No data found")
            return

        self.logger.log(make_table(self._get_table_data(instances)))

    @abc.abstractmethod
    def _get_instances(self, **kwargs):
        pass

    @abc.abstractmethod
    def _get_table_data(self, objects):
        pass


@six.add_metaclass(abc.ABCMeta)
class DetailCommandMixin(object):
    def execute(self, **kwargs):
        instance = self._get_instance(**kwargs)
        self.logger.log(make_table(self._get_table_data(instance)))

    @abc.abstractmethod
    def _get_instance(self, **kwargs):
        pass

    @abc.abstractmethod
    def _get_table_data(self, instance):
        """
        :return: list of (label, value) rows
        """
        pass
