import os

from pydstk.frameworks.common import Framework

MODEL_FILE = "model.joblib"


class SklearnFramework(Framework):
    NAME = "sklearn"

    def save(self, model, directory):
        import joblib

        joblib.dump(model, os.path.join(directory, MODEL_FILE))
        return [MODEL_FILE]

    def params(self, model):
        return {
            name: _name_estimators(value)
            for name, value in model.get_params(deep=True).items()
        }

    def load(self, directory, metadata):
        import joblib

        return joblib.load(os.path.join(directory, MODEL_FILE))


def _name_estimators(value):
    """Swaps nested estimators for their class name, since their parameters are
    already listed under `<step>__<param>` keys
    """
    if hasattr(value, "get_params") and not isinstance(value, type):
        return type(value).__name__
    if isinstance(value, (list, tuple)):
        return [_name_estimators(item) for item in value]
    return value
