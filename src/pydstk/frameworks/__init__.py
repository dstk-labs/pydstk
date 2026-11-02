import platform

from pydstk.api_sdk.exceptions import UnsupportedModelError
from pydstk.frameworks.common import class_path, to_json_value
from pydstk.frameworks.lightgbm import LightGBMFramework
from pydstk.frameworks.pytorch import PyTorchFramework
from pydstk.frameworks.sklearn import SklearnFramework
from pydstk.frameworks.xgboost import XGBoostFramework

FRAMEWORKS = {
    framework.NAME: framework
    for framework in (
        SklearnFramework(),
        XGBoostFramework(),
        LightGBMFramework(),
        PyTorchFramework(),
    )
}


def detect(model):
    """Finds the model's framework from its class hierarchy, without importing any

    :rtype: Framework
    """
    for cls in type(model).__mro__:
        framework = FRAMEWORKS.get(cls.__module__.partition(".")[0])
        if framework is not None:
            return framework

    raise UnsupportedModelError(
        "pydstk can't save {} models yet. Supported frameworks: {}".format(
            class_path(type(model)), ", ".join(FRAMEWORKS)
        )
    )


def get(name):
    """
    :param str name: framework name recorded by `describe`
    :rtype: Framework
    """
    if name not in FRAMEWORKS:
        raise UnsupportedModelError("pydstk can't load {} models".format(name))
    return FRAMEWORKS[name]


def describe(framework, model, files):
    """
    :param Framework framework:
    :param model:
    :param list[str] files: what `framework.save` wrote
    :rtype: dict
    """
    return {
        "framework": framework.NAME,
        "framework_version": framework.version(),
        "model_class": class_path(type(model)),
        "python_version": platform.python_version(),
        "params": to_json_value(framework.params(model)),
        "files": files,
    }
