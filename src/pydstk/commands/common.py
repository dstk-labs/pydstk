import abc
import six
from pydstk.clilogger import CliLogger


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
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        instances = self._get_instances(**kwargs)
        self._log_objects_list(instances)

    @abc.abstractmethod
    def _get_instances(self, **kwargs):
        pass

    @abc.abstractmethod
    def _get_table_data(self, objects):
        pass

    def _log_objects_list(self, objects):
        if not objects:
            self.logger.warning("No data found")
            return

        table_data = self._get_table_data(objects)
        table_str = self._make_list_table(table_data)
        self._print_table_to_terminal(table_str)

    def _print_table_to_terminal(self, table_str):
        self.logger.log(table_str)

    @staticmethod
    def _make_list_table(table_data):
        widths = [max(len(str(cell)) for cell in column) for column in zip(*table_data)]
        rows = [
            "  ".join(str(cell).ljust(width) for cell, width in zip(row, widths))
            for row in table_data
        ]
        return "\n".join(row.rstrip() for row in rows)
