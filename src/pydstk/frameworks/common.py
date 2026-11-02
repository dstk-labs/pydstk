import abc
import importlib
import math

import six


def class_path(cls):
    return "{}.{}".format(cls.__module__, cls.__qualname__)


def to_json_value(value):
    """Converts a parameter value into something JSON can hold"""
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    if isinstance(value, dict):
        return {str(key): to_json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [to_json_value(item) for item in value]
    if hasattr(value, "tolist") and not isinstance(value, type):
        return to_json_value(value.tolist())
    return repr(value)


@six.add_metaclass(abc.ABCMeta)
class Framework(object):
    NAME = None

    def version(self):
        return importlib.import_module(self.NAME).__version__

    @abc.abstractmethod
    def save(self, model, directory):
        """
        :param model:
        :param str directory: empty folder to write into
        :rtype: list[str]
        :returns: names of the written files, relative to directory
        """

    @abc.abstractmethod
    def params(self, model):
        """
        :param model:
        :rtype: dict
        """

    @abc.abstractmethod
    def load(self, directory, metadata):
        """
        :param str directory: folder holding the files `save` wrote
        :param dict metadata: what `describe` recorded for the model
        :returns: the model
        """
